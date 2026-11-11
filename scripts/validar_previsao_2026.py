"""
Validação extra da página Previsão com dados reais de 2026 (fora da base).

GDIC - Grupo 1 - Power BI Clima.
NÃO altera data/clima_latam.csv nem data/clima_latam_ampliado.csv: a base oficial continua
indo até dez/2025. Este script só baixa 2026 à parte e compara com o que a página Previsão diz.

Uso (na raiz do repositório):
  python scripts/validar_previsao_2026.py             -> baixa 2026 (o que faltar) e gera o relatório
  python scripts/validar_previsao_2026.py --so-cache  -> gera o relatório só com o que já foi baixado

Saídas:
  data/extra/real_2026.csv          2026 mensal das 39 cidades (mesmo formato da base: ";" e ",")
  data/extra/cache_2026/*.json      respostas da API (para não baixar de novo)
  docs/validacao_2026.md            relatório: previsão x real, cenário El Niño x real

Fonte: Open-Meteo Historical Weather API (ERA5), mesma da base. O ERA5 sai com ~5 dias de atraso,
então o script usa só meses completos.
"""
import ast
import csv
import datetime as dt
import json
import os
import statistics as st
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQ_BASE = os.path.join(RAIZ, "data", "clima_latam_ampliado.csv")
PASTA_EXTRA = os.path.join(RAIZ, "data", "extra")
PASTA_CACHE = os.path.join(PASTA_EXTRA, "cache_2026")
ARQ_REAL = os.path.join(PASTA_EXTRA, "real_2026.csv")
ARQ_RELATORIO = os.path.join(RAIZ, "docs", "validacao_2026.md")

SO_CACHE = "--so-cache" in sys.argv
for i, a in enumerate(sys.argv):            # opção para testes: --cache <pasta>
    if a == "--cache" and i + 1 < len(sys.argv):
        PASTA_CACHE = sys.argv[i + 1]

LIMIAR_DIA_CHUVA_MM = 1.0
PAUSA_ENTRE_CIDADES_S = 3
ESPERAS_429_S = [65, 120, 300]
VARIAVEIS = "temperature_2m_mean,temperature_2m_max,temperature_2m_min,precipitation_sum"

# Mesmas regiões da coluna calculada `regiao` do Power BI
REGIOES = {
    "México": ["Cidade do México", "Monterrey"],
    "América Central e Caribe": ["Cidade da Guatemala", "San Salvador", "Tegucigalpa", "Manágua", "San José",
                                 "Cidade do Panamá", "Havana", "Santo Domingo", "Porto Príncipe"],
    "Norte da América do Sul": ["Bogotá", "Medellín", "Cartagena", "Caracas"],
    "Amazônia": ["Manaus", "Belém"],
    "Nordeste do Brasil": ["Fortaleza", "Recife", "Salvador", "Petrolina"],
    "Centro-Sudeste do Brasil": ["Brasília", "Cuiabá", "São Paulo", "Rio de Janeiro"],
    "Costa do Pacífico": ["Guayaquil", "Piura", "Lima"],
    "Andes tropicais": ["Quito", "La Paz"],
    "Sul do Brasil e Bacia do Prata": ["Porto Alegre", "Curitiba", "Asunción", "Buenos Aires", "Montevidéu"],
    "Chile e Argentina andina": ["Santiago", "Antofagasta", "Mendoza", "Ushuaia"],
}
REGIAO_DA = {c: r for r, cs in REGIOES.items() for c in cs}
MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]


# ---------------------------------------------------------------- coordenadas
def ler_lista(arquivo, nome):
    """Lê a lista de cidades (cidade, país, lat, lon) de um dos scripts da base, sem executá-lo."""
    arvore = ast.parse(open(os.path.join(RAIZ, "scripts", arquivo), encoding="utf-8").read())
    for no in arvore.body:
        if isinstance(no, ast.Assign) and any(getattr(t, "id", None) == nome for t in no.targets):
            return ast.literal_eval(no.value)
    return []


def coordenadas():
    cidades = {}
    for arq, nome in (("baixar.py", "CIDADES"), ("ampliar_clima_latam.py", "NOVAS_CIDADES")):
        for cidade, pais, lat, lon in ler_lista(arq, nome):
            cidades.setdefault(cidade, (pais, lat, lon))
    return cidades


# ---------------------------------------------------------------- base (só leitura)
def num(s):
    return float(s.replace(",", "."))


def ler_base():
    with open(ARQ_BASE, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f, delimiter=";"))


# ---------------------------------------------------------------- download 2026
def periodo_2026():
    """De 01/01/2026 até o fim do último mês completo disponível no ERA5 (~5 dias de atraso)."""
    limite = dt.date.today() - dt.timedelta(days=6)
    fim = limite.replace(day=1) - dt.timedelta(days=1)
    if fim.year < 2026:
        sys.exit("Ainda não há nenhum mês completo de 2026 no ERA5.")
    return dt.date(2026, 1, 1), min(fim, dt.date(2026, 12, 31))


def baixar(cidade, lat, lon, inicio, fim):
    os.makedirs(PASTA_CACHE, exist_ok=True)
    arq = os.path.join(PASTA_CACHE, f"{cidade}.json")
    if os.path.exists(arq):
        dados = json.load(open(arq, encoding="utf-8"))
        completo = dados.get("variaveis") == VARIAVEIS
        if (dados.get("fim") == fim.isoformat() and completo) or (SO_CACHE and "daily" in dados):
            return dados["daily"], False
    if SO_CACHE:
        return None, False
    url = ("https://archive-api.open-meteo.com/v1/archive"
           f"?latitude={lat}&longitude={lon}&start_date={inicio}&end_date={fim}"
           f"&daily={VARIAVEIS}&timezone=auto")
    for espera in ESPERAS_429_S + [None]:
        try:
            with urllib.request.urlopen(url, timeout=120) as resp:
                daily = json.loads(resp.read().decode("utf-8"))["daily"]
            json.dump({"fim": fim.isoformat(), "variaveis": VARIAVEIS, "daily": daily}, open(arq, "w", encoding="utf-8"))
            return daily, True
        except Exception as e:
            if espera is None:
                print(f"   {cidade}: falhou ({e})")
                return None, True
            limite = isinstance(e, urllib.error.HTTPError) and e.code == 429
            print(f"   {'limite da API' if limite else f'erro: {e}'}; esperando {espera} s...")
            time.sleep(espera)


def mensal(daily):
    meses = defaultdict(lambda: {"t": [], "tx": [], "tn": [], "p": []})
    vazio = [None] * len(daily["time"])
    for d, t, tx, tn, p in zip(daily["time"], daily["temperature_2m_mean"], daily.get("temperature_2m_max", vazio),
                               daily.get("temperature_2m_min", vazio), daily["precipitation_sum"]):
        for chave, v in (("t", t), ("tx", tx), ("tn", tn), ("p", p)):
            if v is not None:
                meses[d[:7]][chave].append(v)
    saida = {}
    for ym, m in meses.items():
        if not (m["t"] and m["p"]):
            continue
        saida[ym] = {"temp_media": st.mean(m["t"]), "precip_total_mm": sum(m["p"]),
                     "dias_chuva": sum(1 for v in m["p"] if v >= LIMIAR_DIA_CHUVA_MM),
                     "temp_max_media": st.mean(m["tx"]) if m["tx"] else None,
                     "temp_min_media": st.mean(m["tn"]) if m["tn"] else None,
                     "temp_max_absoluta": max(m["tx"]) if m["tx"] else None}
    return saida


# ---------------------------------------------------------------- análise
def fmt(x, casas=2, sinal=True):
    s = f"{x:+.{casas}f}" if sinal else f"{x:.{casas}f}"
    return s.replace(".", ",").replace("-", "−")


def dec(x, casas=3):
    return "" if x is None else f"{x:.{casas}f}".replace(".", ",")


def pct(x):
    return fmt(x * 100, 0) + "%"


def main():
    inicio, fim = periodo_2026()
    cidades = coordenadas()
    base = ler_base()
    nomes = sorted({r["cidade"] for r in base})
    faltando = [c for c in nomes if c not in cidades]
    if faltando:
        sys.exit(f"Sem coordenadas para: {faltando}")

    print(f"Período 2026: {inicio} a {fim} · {len(nomes)} cidades")
    real = {}
    for i, c in enumerate(nomes, 1):
        pais, lat, lon = cidades[c]
        daily, baixou = baixar(c, lat, lon, inicio, fim)
        print(f"[{i:2}/{len(nomes)}] {c}: {'baixado' if baixou and daily else 'cache' if daily else 'sem dados'}")
        if daily:
            real[c] = mensal(daily)
        if baixou and i < len(nomes):
            time.sleep(PAUSA_ENTRE_CIDADES_S)
    if len(real) < len(nomes):
        print(f"Atenção: só {len(real)} de {len(nomes)} cidades com dados. Rode de novo para completar.")

    # Normais 1991–2020 e média 2016–2025 por cidade × mês (da base, só leitura)
    norm_t, norm_p, rec_t = defaultdict(list), defaultdict(list), defaultdict(list)
    norm_tx, rec_tx = defaultdict(list), defaultdict(list)
    forte_t, forte_p = defaultdict(list), defaultdict(list)
    for r in base:
        k, ano = (r["cidade"], int(r["mes"])), int(r["ano"])
        if 1991 <= ano <= 2020:
            norm_t[k].append(num(r["temp_media"]))
            norm_p[k].append(num(r["precip_total_mm"]))
            norm_tx[k].append(num(r["temp_max_media"]))
        if 2016 <= ano <= 2025:
            rec_t[k].append(num(r["temp_media"]))
            rec_tx[k].append(num(r["temp_max_media"]))
    norm_t = {k: st.mean(v) for k, v in norm_t.items()}
    norm_p = {k: st.mean(v) for k, v in norm_p.items()}
    rec_t = {k: st.mean(v) for k, v in rec_t.items()}
    norm_tx = {k: st.mean(v) for k, v in norm_tx.items()}
    rec_tx = {k: st.mean(v) for k, v in rec_tx.items()}
    for r in base:   # cenário: El Niños fortes da base (mesmo filtro da página)
        if r["fase"] == "El Niño" and r["intensidade"] in ("Forte", "Muito forte"):
            k = (r["cidade"], int(r["mes"]))
            forte_t[REGIAO_DA[r["cidade"]]].append(num(r["temp_media"]) - norm_t[k])
            forte_p[REGIAO_DA[r["cidade"]]].append((num(r["precip_total_mm"]), norm_p[k]))

    # CSV extra com o real de 2026
    os.makedirs(PASTA_EXTRA, exist_ok=True)
    with open(ARQ_REAL, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["cidade", "pais", "regiao", "data", "ano", "mes", "temp_media", "temp_normal",
                    "anomalia_temp", "temp_max_media", "temp_max_normal", "anomalia_max", "temp_min_media",
                    "temp_max_absoluta", "precip_total_mm", "chuva_normal", "dias_chuva"])
        for c in sorted(real):
            for ym, v in sorted(real[c].items()):
                m = int(ym[5:])
                k = (c, m)
                w.writerow([c, cidades[c][0], REGIAO_DA[c], f"{ym}-01", ym[:4], m,
                            f"{v['temp_media']:.3f}".replace(".", ","), f"{norm_t[k]:.3f}".replace(".", ","),
                            f"{v['temp_media'] - norm_t[k]:.3f}".replace(".", ","),
                            dec(v["temp_max_media"]), dec(norm_tx[k]),
                            dec(v["temp_max_media"] - norm_tx[k] if v["temp_max_media"] is not None else None),
                            dec(v["temp_min_media"]), dec(v["temp_max_absoluta"]),
                            f"{v['precip_total_mm']:.1f}".replace(".", ","), f"{norm_p[k]:.1f}".replace(".", ","),
                            v["dias_chuva"]])

    meses = sorted({ym for c in real for ym in real[c]})
    cs = sorted(real)

    # 1) Temperatura média das cidades, mês a mês
    linhas, err_norm, err_rec = [], [], []
    for ym in meses:
        m = int(ym[5:])
        ok = [c for c in cs if ym in real[c]]
        r_ = st.mean(real[c][ym]["temp_media"] for c in ok)
        n_ = st.mean(norm_t[(c, m)] for c in ok)
        e_ = st.mean(rec_t[(c, m)] for c in ok)
        err_norm.append(abs(r_ - n_))
        err_rec.append(abs(r_ - e_))
        linhas.append(f"| {MESES[m - 1]}/2026 | {fmt(r_, 2, False)} | {fmt(e_, 2, False)} | {fmt(n_, 2, False)} | {fmt(r_ - n_)} |")

    # 1b) Temperatura máxima média
    linhas_tx = []
    for ym in meses:
        m = int(ym[5:])
        ok = [c for c in cs if ym in real[c] and real[c][ym]["temp_max_media"] is not None]
        if not ok:
            continue
        r_ = st.mean(real[c][ym]["temp_max_media"] for c in ok)
        n_ = st.mean(norm_tx[(c, m)] for c in ok)
        e_ = st.mean(rec_tx[(c, m)] for c in ok)
        linhas_tx.append(f"| {MESES[m - 1]}/2026 | {fmt(r_, 2, False)} | {fmt(e_, 2, False)} | {fmt(n_, 2, False)} | {fmt(r_ - n_)} |")
    secao_tx = ("\n## 1b. Temperatura máxima média das cidades: real 2026 × referências\n\n"
                "| Mês | Real 2026 (°C) | Média 2016–2025 (°C) | Normal 1991–2020 (°C) | Anomalia 2026 |\n|---|---|---|---|---|\n"
                + "\n".join(linhas_tx) + "\n") if linhas_tx else ""

    # 2) Por região: anomalia de temperatura e chuva vs normal nos meses de 2026
    meses_en = [ym for ym in meses if int(ym[5:]) >= 6]   # El Niño em curso a partir do meio do ano
    reg_linhas = []
    for g in REGIOES:
        cg = [c for c in REGIOES[g] if c in real]
        if not cg:
            continue
        an = [real[c][ym]["temp_media"] - norm_t[(c, int(ym[5:]))] for c in cg for ym in meses if ym in real[c]]
        pr = sum(real[c][ym]["precip_total_mm"] for c in cg for ym in meses_en if ym in real[c])
        pn = sum(norm_p[(c, int(ym[5:]))] for c in cg for ym in meses_en if ym in real[c])
        cen_p = sum(p for p, _ in forte_p[g]) / sum(n for _, n in forte_p[g]) - 1
        cen_t = st.mean(forte_t[g])
        mesmo = "sim" if pn and (pr / pn - 1) * cen_p > 0 else "não"
        reg_linhas.append(f"| {g} | {fmt(st.mean(an))} | {fmt(cen_t)} | {pct(pr / pn - 1) if pn else '–'} | {pct(cen_p)} | {mesmo} |")

    p_ini = f"{MESES[int(meses_en[0][5:]) - 1]}–{MESES[int(meses_en[-1][5:]) - 1]}/2026" if meses_en else "–"
    texto = f"""# Validação com dados reais de 2026

Gerado por `scripts/validar_previsao_2026.py` em {dt.date.today():%d/%m/%Y}.
Dados de 2026: Open-Meteo (ERA5), {MESES[int(meses[0][5:]) - 1]} a {MESES[int(meses[-1][5:]) - 1]}/2026, {len(cs)} cidades.
**A base oficial não foi alterada** (continua até dez/2025). O real de 2026 fica à parte em `data/extra/real_2026.csv`.

## 1. Temperatura média das cidades: real 2026 × referências

| Mês | Real 2026 (°C) | Média 2016–2025 (°C) | Normal 1991–2020 (°C) | Anomalia 2026 |
|---|---|---|---|---|
{chr(10).join(linhas)}

Erro médio absoluto: média 2016–2025 = **{fmt(st.mean(err_rec), 2, False)} °C** · normal 1991–2020 = **{fmt(st.mean(err_norm), 2, False)} °C**.
Para comparar com a previsão do Power BI: abra a página Previsão sem filtro e passe o mouse na linha preta
de 2026 (gráfico "Previsão 2026–27", botão Média); compare mês a mês com a coluna "Real 2026".
Para a máxima, use o botão Máxima do mesmo gráfico e a seção 1b.
{secao_tx}
## 2. Cenário El Niño 2026–27 × o que aconteceu até agora

Anomalia de temperatura: média dos meses de 2026. Chuva: {p_ini}, quando o El Niño já estava em curso.
"Cenário" = média dos El Niños fortes da base (o mesmo gráfico da página).

| Região | Anomalia 2026 | Cenário (anomalia) | Chuva {p_ini} | Cenário (chuva) | Mesmo sinal na chuva? |
|---|---|---|---|---|---|
{chr(10).join(reg_linhas)}

## Cuidados
- O pico do El Niño é esperado para nov/2026–jan/2027; os meses analisados são o início do evento.
- Na Costa do Pacífico (Lima, Piura) jun–out é estação seca, com normais de poucos mm: a % fica instável. O efeito do El Niño ali aparece em dez–abr.
- Chuva absoluta do ERA5 tem viés em várias cidades; por isso a comparação é sempre relativa ao normal da própria cidade.
- Este arquivo é gerado pelo script; para atualizar, rode o script de novo.
"""
    os.makedirs(os.path.dirname(ARQ_RELATORIO), exist_ok=True)
    open(ARQ_RELATORIO, "w", encoding="utf-8").write(texto)
    print(f"\nOK: {ARQ_REAL}\nOK: {ARQ_RELATORIO}")


if __name__ == "__main__":
    main()
