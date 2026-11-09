# GDIC – Grupo 1 – Power BI Clima

Projeto de Business Intelligence da disciplina **Gestão de Dados, Informação e Conhecimento (GDIC)**, CIn-UFPE.
Dashboard em **Power BI** sobre o clima da América Latina: aquecimento por cidade, efeitos do El Niño e da La Niña na chuva e na temperatura, e previsões.

**Integrantes:** _(preencher)_
**Apresentação:** 16 ou 19/11/2026
**Status:** base de dados validada (v1.1.0) · dashboard em construção (`powerbi/GDIC_Grupo1_Clima.pbip`)

## Perguntas que o dashboard responde
1. As cidades da América Latina estão esquentando? Quanto, por década?
2. Como o El Niño e a La Niña mudam a chuva e a temperatura em cada região?
3. Eventos extremos recentes (enchentes do RS em 2024, chuvas de Recife em 2022, seca da Amazônia em 2023) aparecem nos dados?
4. O que esperar para os próximos meses (previsão)?

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
powerbi/
  GDIC_Grupo1_Clima.pbip      dashboard (Power BI Project) ← abrir este
  GDIC_Grupo1_Clima.Report/   páginas e visuais
  GDIC_Grupo1_Clima.SemanticModel/  tabelas, colunas calculadas e medidas (.tmdl)
CHANGELOG.md                  histórico de versões
```

## Como abrir o dashboard no Power BI

Requer **Power BI Desktop atualizado (Windows)**. O arquivo a abrir é **`powerbi/GDIC_Grupo1_Clima.pbip`**.

1. **Baixar o repositório inteiro:** no VS Code, *Ctrl+Shift+P → Git: Clone* e colar o endereço do repositório; ou, no GitHub, *Code → Download ZIP* e extrair a pasta.
2. **Abrir:** dois cliques em `powerbi/GDIC_Grupo1_Clima.pbip` (ou *Arquivo → Abrir* no Power BI). As pastas `.Report` e `.SemanticModel` precisam estar ao lado do `.pbip`.
3. **Apontar para o CSV no seu computador:** *Transformar dados* → consulta **clima_cidades** → engrenagem da etapa **Fonte** → *Procurar…* → `data/clima_latam_ampliado.csv` do seu clone → *OK* → *Fechar e Aplicar*.
4. **Carregar os dados:** o cache não é versionado, então na primeira abertura os gráficos podem vir vazios. Clique em *Página Inicial → Atualizar*.

| Problema | Solução |
|---|---|
| Windows não abre `.pbip` | Atualizar o Power BI Desktop ou usar *Arquivo → Abrir* |
| "Não foi possível encontrar o arquivo" | Passo 3 |
| Gráficos vazios | Passo 4 |

As colunas calculadas (`temp_normal`, `anomalia_temp`, `chuva_normal`, `Local`) e as medidas já estão no projeto. Use sempre medidas relativas ao normal de cada cidade (anomalia em °C e chuva em % do normal). Onde ficam as fórmulas: [powerbi/README.md](powerbi/README.md).

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
