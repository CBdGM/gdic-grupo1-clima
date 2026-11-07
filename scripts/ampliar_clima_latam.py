"""
Amplia o clima_latam.csv com novas cidades, usando a API historica do Open-Meteo (ERA5).

GDIC - Grupo 1 - Power BI Clima. Gera a v1.1.0 (clima_latam_ampliado.csv) a partir da v1.0.0.

Como usar (na raiz do repositorio):
  python scripts/ampliar_clima_latam.py              -> baixa o que faltar e gera o CSV
  python scripts/ampliar_clima_latam.py --so-cache   -> gera o CSV so com o cache (sem internet)
Entrada: data/clima_latam.csv | Saida: data/clima_latam_ampliado.csv | Cache: data/cache_openmeteo/

Versao 2: salva cada cidade baixada na pasta "cache_openmeteo". Se a API bloquear por
limite (erro 429) ou o script for interrompido, e so rodar de novo: as cidades ja baixadas
nao sao baixadas outra vez.

A API gratuita tem limite por minuto, por hora (~10 cidades de 46 anos) e por dia.
Por isso o script espera entre uma cidade e outra e, se for bloqueado, espera mais.
"""
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict

# Caminhos relativos ao repositorio: o script fica em scripts/ e os dados em data/
PASTA_DADOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
ARQ_ORIGINAL = os.path.join(PASTA_DADOS, "clima_latam.csv")            # v1.0.0 (entrada)
ARQ_SAIDA = os.path.join(PASTA_DADOS, "clima_latam_ampliado.csv")      # v1.1.0 (saida)
PASTA_CACHE = os.path.join(PASTA_DADOS, "cache_openmeteo")
INICIO, FIM = "1980-01-01", "2025-12-31"
LIMIAR_DIA_CHUVA_MM = 1.0       # padrao da OMM para "dia de chuva"
ESPERA_ENTRE_CIDADES_S = 75     # respeita o limite por minuto
ESPERAS_429_S = [70, 120, 300, 600, 900, 900, 900, 900]  # ate ~1h30 no total

# cidade, pais (como no CSV original), latitude, longitude
NOVAS_CIDADES = [
    ("Recife", "Brasil", -8.05, -34.88),
    ("Salvador", "Brasil", -12.97, -38.50),
    ("Belém", "Brasil", -1.46, -48.49),
    ("Rio de Janeiro", "Brasil", -22.91, -43.17),
    ("Curitiba", "Brasil", -25.43, -49.27),
    ("Cuiabá", "Brasil", -15.60, -56.10),
    ("San José", "Costa Rica", 9.93, -84.08),
    ("San Salvador", "El Salvador", 13.69, -89.22),
    ("Porto Príncipe", "Haiti", 18.54, -72.34),
    ("Medellín", "Colômbia", 6.24, -75.58),
    # Planejadas para a v1.2.0 (nao baixadas na v1.1.0 por limite diario da API).
    # Para inclui-las, tire o "#" do inicio das linhas e rode o script de novo.
    # ("Cusco", "Peru", -13.53, -71.97),
    # ("Córdoba", "Argentina", -31.42, -64.18),
    # ("Santa Cruz de la Sierra", "Bolívia", -17.78, -63.18),
    # ("Iquitos", "Peru", -3.75, -73.25),
]

COLUNAS = ["cidade", "pais", "data", "ano", "mes", "temp_media", "temp_max_media",
           "temp_min_media", "temp_max_absoluta", "precip_total_mm", "dias_chuva",
           "oni", "fase", "intensidade", "evento_enso"]


def num_br(x, casas=3):
    return f"{x:.{casas}f}".replace(".", ",")


def arquivo_cache(cidade):
    nome = "".join(ch if ch.isalnum() else "_" for ch in cidade)
    return os.path.join(PASTA_CACHE, f"{nome}.json")


def ler_original():
    with open(ARQ_ORIGINAL, encoding="utf-8-sig", newline="") as f:
        linhas = list(csv.DictReader(f, delimiter=";"))
    enso = {}
    for r in linhas:
        enso.setdefault(r["data"], (r["oni"], r["fase"], r["intensidade"], r["evento_enso"]))
    return linhas, enso


def baixar_diario(lat, lon):
    url = ("https://archive-api.open-meteo.com/v1/archive"
           f"?latitude={lat}&longitude={lon}&start_date={INICIO}&end_date={FIM}"
           "&daily=temperature_2m_mean,temperature_2m_max,temperature_2m_min,precipitation_sum"
           "&timezone=auto")
    for espera in ESPERAS_429_S + [None]:
        try:
            with urllib.request.urlopen(url, timeout=180) as resp:
                return json.loads(resp.read().decode("utf-8"))["daily"]
        except Exception as e:
            if espera is None:
                break
            limite = isinstance(e, urllib.error.HTTPError) and e.code == 429
            motivo = "limite da API" if limite else f"erro: {e}"
            print(f"   {motivo}; esperando {espera // 60} min {espera % 60} s e tentando de novo...")
            time.sleep(espera)
    return None


def agregar_mensal(diario):
    meses = defaultdict(lambda: {"tm": [], "tx": [], "tn": [], "p": []})
    for d, tm, tx, tn, p in zip(diario["time"], diario["temperature_2m_mean"],
                                diario["temperature_2m_max"], diario["temperature_2m_min"],
                                diario["precipitation_sum"]):
        m = meses[d[:7]]
        if tm is not None: m["tm"].append(tm)
        if tx is not None: m["tx"].append(tx)
        if tn is not None: m["tn"].append(tn)
        if p is not None: m["p"].append(p)
    saida = {}
    for ym, m in meses.items():
        if not (m["tm"] and m["tx"] and m["tn"] and m["p"]):
            continue
        saida[ym] = {
            "temp_media": sum(m["tm"]) / len(m["tm"]),
            "temp_max_media": sum(m["tx"]) / len(m["tx"]),
            "temp_min_media": sum(m["tn"]) / len(m["tn"]),
            "temp_max_absoluta": max(m["tx"]),
            "precip_total_mm": sum(m["p"]),
            "dias_chuva": sum(1 for v in m["p"] if v >= LIMIAR_DIA_CHUVA_MM),
        }
    return saida


SO_CACHE = "--so-cache" in sys.argv  # gera o CSV so com o que ja foi baixado, sem acessar a API


def obter_mensal(cidade, lat, lon):
    """Usa o cache se a cidade ja foi baixada; senao baixa e salva no cache."""
    caminho = arquivo_cache(cidade)
    if os.path.exists(caminho):
        with open(caminho, encoding="utf-8") as f:
            return json.load(f), False
    if SO_CACHE:
        return None, False
    diario = baixar_diario(lat, lon)
    if diario is None:
        return None, True
    mensal = agregar_mensal(diario)
    os.makedirs(PASTA_CACHE, exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(mensal, f)
    return mensal, True


def main():
    linhas, enso = ler_original()
    existentes = {r["cidade"] for r in linhas}
    novas, faltando = [], []
    for cidade, pais, lat, lon in NOVAS_CIDADES:
        if cidade in existentes:
            print(f"- {cidade}: ja existe no original, pulando")
            continue
        print(f"- {cidade} ({pais})...")
        mensal, baixou = obter_mensal(cidade, lat, lon)
        if mensal is None:
            print("   ainda nao baixada (fica para a proxima rodada).")
            faltando.append(cidade)
            continue
        print(f"   {len(mensal)} meses" + ("" if baixou else " (do cache)"))
        for ym in sorted(mensal):
            data = f"{ym}-01"
            if data not in enso:
                continue
            v = mensal[ym]
            oni, fase, intens, evento = enso[data]
            novas.append({
                "cidade": cidade, "pais": pais, "data": data,
                "ano": ym[:4], "mes": str(int(ym[5:7])),
                "temp_media": num_br(v["temp_media"]),
                "temp_max_media": num_br(v["temp_max_media"]),
                "temp_min_media": num_br(v["temp_min_media"]),
                "temp_max_absoluta": num_br(v["temp_max_absoluta"]),
                "precip_total_mm": num_br(v["precip_total_mm"]),
                "dias_chuva": str(v["dias_chuva"]),
                "oni": oni, "fase": fase, "intensidade": intens, "evento_enso": evento,
            })
        if baixou:
            time.sleep(ESPERA_ENTRE_CIDADES_S)

    with open(ARQ_SAIDA, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUNAS, delimiter=";")
        w.writeheader()
        w.writerows(linhas)
        w.writerows(novas)
    print(f"\nArquivo salvo: {ARQ_SAIDA} com {len(linhas) + len(novas)} linhas ({len(novas)} novas).")
    if faltando:
        print("Ficaram faltando: " + ", ".join(faltando))
        print("Rode o script de novo mais tarde (ex.: daqui a 1 hora): ele so baixa o que falta.")
    else:
        print("Todas as cidades foram incluidas.")


if __name__ == "__main__":
    main()
