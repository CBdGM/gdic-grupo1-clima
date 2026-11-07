# GDIC – Grupo 1 – Power BI Clima

Projeto de Business Intelligence da disciplina **Gestão de Dados, Informação e Conhecimento (GDIC)**, CIn-UFPE.
Dashboard em **Power BI** sobre o clima da América Latina: aquecimento por cidade, efeitos do El Niño e da La Niña na chuva e na temperatura, e previsões.

**Integrantes:** _(preencher)_
**Apresentação:** 16 ou 19/11/2026

---

## Dataset: Clima LatAm

Série mensal de temperatura e chuva de cidades latino-americanas, de jan/1980 a dez/2025, com a classificação de cada mês em El Niño, La Niña ou neutro.

| Versão | Arquivo | Cidades | Países | Linhas | Data |
|---|---|---|---|---|---|
| **v1.1.0** (atual) | `data/clima_latam_ampliado.csv` | 39 | 20 | 21.528 | 2026-11-07 |
| v1.0.0 | `data/clima_latam.csv` | 29 | 17 | 16.008 | 2026-11-07 |

A v1.1.0 contém a v1.0.0 inteira, sem alterações, mais 10 cidades. O histórico completo está no [CHANGELOG](CHANGELOG.md).

### Fontes
- **Clima:** [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api), baseada na reanálise **ERA5** (ECMWF / Copernicus).
- **El Niño / La Niña:** **Oceanic Niño Index (ONI)**, NOAA Climate Prediction Center.

### Como citar
> Os dados climáticos mensais de 39 cidades latino-americanas (1980–2025) foram obtidos da Open-Meteo Historical Weather API, baseada na reanálise ERA5 (ECMWF/Copernicus), e cruzados com o Oceanic Niño Index (ONI) da NOAA.

- Zippenfenig, P. (2023). *Open-Meteo.com Weather API*. Zenodo. https://doi.org/10.5281/zenodo.7970649
- Hersbach, H. et al. (2020). The ERA5 global reanalysis. *Q. J. R. Meteorol. Soc.*, 146, 1999–2049. https://doi.org/10.1002/qj.3803
- NOAA CPC. *Oceanic Niño Index (ONI)*. https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.php

### Limitação principal
O ERA5 representa a média de uma área de cerca de 25 km × 25 km, não um ponto. **Tendências, anomalias e eventos extremos são confiáveis**, mas valores absolutos de chuva podem divergir muito das estações (ex.: Recife −56%, Lima 8× maior). Use sempre medidas relativas ao normal de cada cidade. Detalhes em [docs/validacao.md](docs/validacao.md).

---

## Estrutura

```
data/
  clima_latam.csv             v1.0.0 – base original (29 cidades)
  clima_latam_ampliado.csv    v1.1.0 – base atual (39 cidades) ← usar no Power BI
  cache_openmeteo/            dados mensais de cada cidade nova (gerados pelo script)
scripts/
  baixar.py                   gera a v1.0.0 (Open-Meteo + ONI da NOAA)
  ampliar_clima_latam.py      gera a v1.1.0 a partir da v1.0.0
docs/
  dicionario_dados.md         o que é cada coluna
  validacao.md                comparação com estações oficiais e eventos reais
powerbi/                      arquivos do dashboard
CHANGELOG.md                  histórico de versões
```

## Como reproduzir

Requer Python 3. Na raiz do repositório:

```bash
# v1.0.0 (precisa de: pip install pandas numpy requests). Gera dados_clima/clima_latam.csv
python scripts/baixar.py

# v1.1.0 (só biblioteca padrão). Lê data/clima_latam.csv e gera data/clima_latam_ampliado.csv
python scripts/ampliar_clima_latam.py
python scripts/ampliar_clima_latam.py --so-cache   # sem internet, usando só o cache
```

A API gratuita do Open-Meteo limita cerca de 10 cidades (46 anos) por hora e tem limite diário. Os scripts guardam cada cidade em cache e retomam de onde pararam.

## Regras de versionamento

- **Nunca editar um CSV à mão.** Toda mudança passa por script e é registrada no CHANGELOG.
- Arquivos de versões anteriores não são sobrescritos.
- Numeração **MAIOR.MENOR.CORREÇÃO**:
  - **CORREÇÃO** (1.1.**1**): corrige erro sem mudar a estrutura;
  - **MENOR** (1.**2**.0): acrescenta cidades ou anos, mesmas colunas;
  - **MAIOR** (**2**.0.0): muda colunas (renomear, remover, mudar unidade) e pode quebrar o Power BI.
- Cada versão vira um commit e uma tag `vX.Y.Z`.
