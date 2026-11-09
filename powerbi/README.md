# Power BI – GDIC_Grupo1_Clima

Dashboard salvo como **Power BI Project (.pbip)**: em vez de um arquivo binário, o projeto é uma pasta de arquivos de texto, e o Git mostra exatamente o que mudou em cada commit.

| Item | O que contém |
|---|---|
| `GDIC_Grupo1_Clima.pbip` | Arquivo que se abre no Power BI Desktop |
| `GDIC_Grupo1_Clima.Report/` | Páginas e visuais (`definition/pages/…/visual.json`) |
| `GDIC_Grupo1_Clima.SemanticModel/` | Modelo de dados: consulta, colunas calculadas e medidas |

## Onde estão as fórmulas
- **Colunas calculadas**: `GDIC_Grupo1_Clima.SemanticModel/definition/tables/clima_cidades.tmdl`
  - normal e anomalia: `temp_normal`, `anomalia_temp`, `chuva_normal`, `temp_max_normal`, `temp_min_normal`, `anomalia_max`, `anomalia_min`
  - apoio: `Local` (mapa), `decada`, `nome_mes` (ordenado por `mes`), `amplitude_termica`, `ordem_fase` e `ordem_intensidade` (ocultas, ordenam `fase` e `intensidade`)
- **Medidas**: `GDIC_Grupo1_Clima.SemanticModel/definition/tables/Medidas.tmdl`, organizadas em pastas:
  - **Base:** Nº Cidades, Nº Países, Nº Registros, Período
  - **Temperatura:** Temp Média, Temp Normal, Anomalia Temp, Anomalia Máx, Anomalia Mín, Amplitude Térmica, Máxima Absoluta
  - **Chuva:** Chuva Mensal Média, Chuva Anual Média, Chuva Normal, Chuva vs Normal (%)
  - **El Niño e La Niña:** ONI Médio, % Meses El Niño, % Meses La Niña
  - **Tendência e previsão:** Tendência (°C por década), Anomalia Projetada 2030 (regressão linear com `LINESTX`)
- **Páginas**: `GDIC_Grupo1_Clima.Report/definition/pages/` (uma pasta por página; a ordem fica em `pages.json`)

## Como trabalhar
1. Para abrir pela primeira vez, siga o [README principal](../README.md#como-abrir-o-dashboard-no-power-bi). Para o trabalho em equipe, siga o [COLABORACAO.md](../COLABORACAO.md).
2. Abra sempre o `.pbip` **deste repositório** (não cópias em Downloads). A consulta `clima_cidades` lê `C:\gdic-grupo1-clima\data\clima_latam_ampliado.csv`: clone o repositório nesse caminho e não altere a fonte.
3. Depois de salvar no Power BI, faça o commit pelo VS Code descrevendo o que mudou (ex.: `feat: página Visão Geral`).
4. O cache local (`.pbi/cache.abf`) e as configurações locais (`.pbi/localSettings.json`) são ignorados pelo `.gitignore`.

## Entrega no Classroom
Gere uma cópia `.pbix` (*Arquivo → Salvar como → .pbix*) com o mesmo nome. O `.pbix` não precisa ser versionado.
