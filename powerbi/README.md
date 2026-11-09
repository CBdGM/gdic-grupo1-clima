# Power BI – GDIC_Grupo1_Clima

Dashboard salvo como **Power BI Project (.pbip)**: em vez de um arquivo binário, o projeto é uma pasta de arquivos de texto, e o Git mostra exatamente o que mudou em cada commit.

| Item | O que contém |
|---|---|
| `GDIC_Grupo1_Clima.pbip` | Arquivo que se abre no Power BI Desktop |
| `GDIC_Grupo1_Clima.Report/` | Páginas e visuais (`definition/pages/…/visual.json`) |
| `GDIC_Grupo1_Clima.SemanticModel/` | Modelo de dados: consulta, colunas calculadas e medidas |

## Onde estão as fórmulas
- **Colunas calculadas** (`Local`, `temp_normal`, `anomalia_temp`, `chuva_normal`): `GDIC_Grupo1_Clima.SemanticModel/definition/tables/clima_cidades.tmdl`
- **Medidas** (`Anomalia Temp (°C)`, `Chuva vs Normal (%)`, `Temp Média (°C)`, `ONI Médio` …): `GDIC_Grupo1_Clima.SemanticModel/definition/tables/Medidas.tmdl`

## Como trabalhar
1. Para abrir pela primeira vez (clonar, abrir, apontar o CSV e atualizar), siga o passo a passo do [README principal](../README.md#como-abrir-o-dashboard-no-power-bi).
2. Abra sempre o `.pbip` **deste repositório** (não cópias em Downloads). A consulta `clima_cidades` guarda o caminho completo do CSV de quem salvou por último; em outro computador, reaponte a etapa **Fonte** para `data/clima_latam_ampliado.csv`.
3. Depois de salvar no Power BI, faça o commit pelo VS Code descrevendo o que mudou (ex.: `feat: página Visão Geral`).
4. O cache local (`.pbi/cache.abf`) e as configurações locais (`.pbi/localSettings.json`) são ignorados pelo `.gitignore`.

## Entrega no Classroom
Gere uma cópia `.pbix` (*Arquivo → Salvar como → .pbix*) com o mesmo nome. O `.pbix` não precisa ser versionado.
