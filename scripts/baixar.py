import re
import time
import unicodedata
from io import StringIO
from pathlib import Path

import numpy as np
import pandas as pd
import requests

# ----------------------------------------------------------------------------
# Configuração
# ----------------------------------------------------------------------------
INICIO = "1980-01-01"
FIM = "2025-12-31"
PASTA_SAIDA = Path("dados_clima")
PASTA_CACHE = PASTA_SAIDA / "cache"
FORMATO_BR = True   # True: separador ";" e decimal "," (Power BI em português)
PAUSA_ENTRE_CIDADES = 2   # segundos

URL_OPENMETEO = "https://archive-api.open-meteo.com/v1/archive"
URL_ONI = "https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt"

# (cidade, país, lat, lon)
CIDADES = [
    # Pacífico e Andes
    ("Piura", "Peru", -5.19, -80.63),
    ("Guayaquil", "Equador", -2.19, -79.89),
    ("Quito", "Equador", -0.18, -78.47),
    ("Lima", "Peru", -12.05, -77.04),
    ("Antofagasta", "Chile", -23.65, -70.40),
    ("Santiago", "Chile", -33.45, -70.67),
    ("La Paz", "Bolívia", -16.50, -68.15),
    ("Bogotá", "Colômbia", 4.71, -74.07),
    # Norte da América do Sul
    ("Cartagena", "Colômbia", 10.39, -75.51),
    ("Caracas", "Venezuela", 10.49, -66.88),
    # Brasil
    ("Manaus", "Brasil", -3.12, -60.02),
    ("Fortaleza", "Brasil", -3.73, -38.52),
    ("Petrolina", "Brasil", -9.39, -40.50),
    ("Brasília", "Brasil", -15.79, -47.88),
    ("São Paulo", "Brasil", -23.55, -46.63),
    ("Porto Alegre", "Brasil", -30.03, -51.23),
    # Cone Sul
    ("Asunción", "Paraguai", -25.26, -57.58),
    ("Montevidéu", "Uruguai", -34.90, -56.16),
    ("Buenos Aires", "Argentina", -34.60, -58.38),
    ("Mendoza", "Argentina", -32.89, -68.83),
    ("Ushuaia", "Argentina", -54.80, -68.30),
    # América Central
    ("Cidade da Guatemala", "Guatemala", 14.63, -90.51),
    ("Tegucigalpa", "Honduras", 14.07, -87.19),
    ("Manágua", "Nicarágua", 12.11, -86.24),
    ("San José", "Costa Rica", 9.93, -84.08),
    ("Cidade do Panamá", "Panamá", 8.98, -79.52),
    # México e Caribe
    ("Cidade do México", "México", 19.43, -99.13),
    ("Monterrey", "México", 25.69, -100.32),
    ("Havana", "Cuba", 23.11, -82.37),
    ("Santo Domingo", "Rep. Dominicana", 18.49, -69.93),
]

COLUNAS_CIDADES = ["cidade", "pais", "lat", "lon"]

VARIAVEIS_DIARIAS = {
    "temperature_2m_mean": "temp_media",
    "temperature_2m_max": "temp_max",
    "temperature_2m_min": "temp_min",
    "precipitation_sum": "precip_mm",
}


# ----------------------------------------------------------------------------
# Open-Meteo
# ----------------------------------------------------------------------------
def slug(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "_", texto.lower()).strip("_")


def baixar_cidade(nome: str, lat: float, lon: float, tentativas: int = 6) -> pd.DataFrame:
    """Baixa a série diária de uma cidade (com cache e nova tentativa em caso de limite)."""
    cache = PASTA_CACHE / f"{slug(nome)}.csv"
    if cache.exists():
        return pd.read_csv(cache, parse_dates=["data"])

    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": INICIO,
        "end_date": FIM,
        "daily": ",".join(VARIAVEIS_DIARIAS),
        "timezone": "auto",
    }
    espera = 30
    for tentativa in range(1, tentativas + 1):
        try:
            r = requests.get(URL_OPENMETEO, params=params, timeout=180)
        except requests.RequestException as erro:
            print(f"   erro de conexão ({erro}); nova tentativa em {espera}s")
            time.sleep(espera)
            espera = min(espera * 2, 600)
            continue

        if r.status_code == 429:
            print(f"   limite da API atingido; esperando {espera}s (tentativa {tentativa}/{tentativas})")
            time.sleep(espera)
            espera = min(espera * 2, 600)
            continue

        r.raise_for_status()
        diario = r.json()["daily"]
        df = pd.DataFrame(diario).rename(columns={"time": "data", **VARIAVEIS_DIARIAS})
        df["data"] = pd.to_datetime(df["data"])
        df.to_csv(cache, index=False)
        return df

    raise RuntimeError(f"não foi possível baixar {nome} (limite da API?)")


def agregar_mensal(diario: pd.DataFrame) -> pd.DataFrame:
    """Transforma a série diária em mensal."""
    d = diario.copy()
    d["dia_chuva"] = (d["precip_mm"] >= 1.0).astype(int)   # dia com chuva >= 1 mm
    mensal = (
        d.groupby(pd.Grouper(key="data", freq="MS"))
        .agg(
            temp_media=("temp_media", "mean"),
            temp_max_media=("temp_max", "mean"),
            temp_min_media=("temp_min", "mean"),
            temp_max_absoluta=("temp_max", "max"),
            precip_total_mm=("precip_mm", "sum"),
            dias_chuva=("dia_chuva", "sum"),
        )
        .reset_index()
    )
    mensal["ano"] = mensal["data"].dt.year
    mensal["mes"] = mensal["data"].dt.month
    return mensal


# ----------------------------------------------------------------------------
# ONI (NOAA)
# ----------------------------------------------------------------------------
TRIMESTRE_PARA_MES = {  # mês central de cada trimestre móvel
    "DJF": 1, "JFM": 2, "FMA": 3, "MAM": 4, "AMJ": 5, "MJJ": 6,
    "JJA": 7, "JAS": 8, "ASO": 9, "SON": 10, "OND": 11, "NDJ": 12,
}


def processar_oni(texto: str) -> pd.DataFrame:
    """
    Lê o oni.ascii.txt da NOAA e classifica cada mês.

    Critério oficial da NOAA: El Niño (La Niña) quando o ONI fica >= +0,5
    (<= -0,5) por pelo menos 5 trimestres móveis seguidos. Meses no fim da
    série, num episódio ainda em andamento com menos de 5 meses, ficam Neutro.
    """
    oni = pd.read_csv(StringIO(texto), sep=r"\s+")
    oni["mes"] = oni["SEAS"].map(TRIMESTRE_PARA_MES)
    oni = oni.rename(columns={"YR": "ano", "ANOM": "oni"})[["ano", "mes", "oni"]]
    oni = oni.dropna().sort_values(["ano", "mes"]).reset_index(drop=True)
    oni["data"] = pd.to_datetime(dict(year=oni["ano"], month=oni["mes"], day=1))

    oni["fase"] = "Neutro"
    oni["intensidade"] = "Neutro"
    oni["evento_enso"] = "Neutro"

    for nome, cond in (("El Niño", oni["oni"] >= 0.5), ("La Niña", oni["oni"] <= -0.5)):
        grupo = (cond != cond.shift()).cumsum()
        tamanho = cond.groupby(grupo).transform("size")
        evento = cond & (tamanho >= 5)
        if not evento.any():
            continue

        pico = oni["oni"].abs().groupby(grupo).transform("max")
        intensidade = pd.cut(
            pico, bins=[0.5, 1.0, 1.5, 2.0, np.inf], right=False,
            labels=["Fraco", "Moderado", "Forte", "Muito forte"],
        ).astype(str)
        ano_ini = oni["ano"].groupby(grupo).transform("min")
        ano_fim = oni["ano"].groupby(grupo).transform("max")
        rotulo = [
            f"{nome} {a}" if a == b else f"{nome} {a}–{str(b)[-2:]}"
            for a, b in zip(ano_ini, ano_fim)
        ]

        oni.loc[evento, "fase"] = nome
        oni.loc[evento, "intensidade"] = intensidade[evento]
        oni.loc[evento, "evento_enso"] = pd.Series(rotulo, index=oni.index)[evento]

    return oni[["data", "ano", "mes", "oni", "fase", "intensidade", "evento_enso"]]


def baixar_oni() -> pd.DataFrame:
    r = requests.get(URL_ONI, timeout=60)
    r.raise_for_status()
    return processar_oni(r.text)


# ----------------------------------------------------------------------------
# Saída
# ----------------------------------------------------------------------------
def salvar(df: pd.DataFrame, nome: str) -> None:
    caminho = PASTA_SAIDA / nome
    df = df.copy()
    if "data" in df.columns:
        df["data"] = df["data"].dt.strftime("%Y-%m-%d")
    if FORMATO_BR:
        df.to_csv(caminho, index=False, sep=";", decimal=",", encoding="utf-8-sig", float_format="%.3f")
    else:
        df.to_csv(caminho, index=False, encoding="utf-8", float_format="%.3f")
    print(f"   -> {caminho} ({len(df):,} linhas)")


def main() -> None:
    PASTA_CACHE.mkdir(parents=True, exist_ok=True)
    dim_cidades = pd.DataFrame(CIDADES, columns=COLUNAS_CIDADES)

    print(f"Baixando {len(dim_cidades)} cidades da Open-Meteo ({INICIO} a {FIM})...")
    mensais, faltando = [], []
    for i, linha in enumerate(dim_cidades.itertuples(), start=1):
        print(f"[{i:02d}/{len(dim_cidades)}] {linha.cidade} ({linha.pais})")
        ja_em_cache = (PASTA_CACHE / f"{slug(linha.cidade)}.csv").exists()
        try:
            diario = baixar_cidade(linha.cidade, linha.lat, linha.lon)
        except Exception as erro:
            print(f"   FALHOU: {erro}")
            faltando.append(linha.cidade)
            continue
        m = agregar_mensal(diario)
        m.insert(0, "cidade", linha.cidade)
        mensais.append(m)
        if not ja_em_cache:
            time.sleep(PAUSA_ENTRE_CIDADES)

    if not mensais:
        raise SystemExit("Nenhuma cidade baixada. Verifique a conexão e tente de novo.")

    fato = pd.concat(mensais, ignore_index=True)

    print("Baixando ONI da NOAA...")
    oni = baixar_oni()

    completo = (
        fato.merge(dim_cidades,
                   on="cidade", how="left")
        .merge(oni[["data", "oni", "fase", "intensidade", "evento_enso"]], on="data", how="left")
    )

    colunas_finais = [
        "cidade", "pais",
        "data", "ano", "mes",
        "temp_media", "temp_max_media", "temp_min_media", "temp_max_absoluta",
        "precip_total_mm", "dias_chuva",
        "oni", "fase", "intensidade", "evento_enso",
    ]
    completo = completo[colunas_finais].sort_values(["cidade", "data"])

    print("Salvando arquivo...")
    salvar(completo, "clima_latam.csv")

    if faltando:
        print(f"\nATENÇÃO: faltaram {len(faltando)} cidades: {', '.join(faltando)}")
        print("Provavelmente o limite diário da API. Rode o script de novo mais tarde;")
        print("as cidades já baixadas estão em cache e não serão baixadas de novo.")
    else:
        print("\nPronto! Todas as cidades baixadas.")


if __name__ == "__main__":
    main()