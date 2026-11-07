# Dicionário de dados – Clima LatAm

Arquivos: `data/clima_latam.csv` (v1.0.0) e `data/clima_latam_ampliado.csv` (v1.1.0).
Formato: CSV com separador `;`, decimal `,`, codificação UTF-8 com BOM. Uma linha por **cidade × mês**.

| Coluna | Tipo | Unidade | Descrição | Exemplo |
|---|---|---|---|---|
| `cidade` | texto | – | Nome da cidade (em português) | Porto Alegre |
| `pais` | texto | – | País (em português) | Brasil |
| `data` | data | AAAA-MM-DD | Primeiro dia do mês | 2024-05-01 |
| `ano` | inteiro | – | Ano | 2024 |
| `mes` | inteiro | 1–12 | Mês | 5 |
| `temp_media` | decimal | °C | Média mensal da temperatura média diária (2 m) | 18,402 |
| `temp_max_media` | decimal | °C | Média mensal das máximas diárias | 22,915 |
| `temp_min_media` | decimal | °C | Média mensal das mínimas diárias | 15,031 |
| `temp_max_absoluta` | decimal | °C | Maior máxima diária do mês | 29,100 |
| `precip_total_mm` | decimal | mm | Chuva total do mês | 356,100 |
| `dias_chuva` | inteiro | dias | Dias com chuva ≥ 1 mm | 18 |
| `oni` | decimal | °C | Oceanic Niño Index (anomalia da temperatura do Pacífico, trimestre móvel centrado no mês). Igual para todas as cidades | 0,400 |
| `fase` | texto | – | El Niño / La Niña / Neutro (critério NOAA: 5 trimestres seguidos ≥ +0,5 ou ≤ −0,5) | Neutro |
| `intensidade` | texto | – | Fraco / Moderado / Forte / Muito forte, pelo pico do evento (0,5 / 1,0 / 1,5 / 2,0) | Forte |
| `evento_enso` | texto | – | Nome do evento | El Niño 2023–24 |

## Chave
`cidade` + `data` é única (sem duplicados).

## Cuidados de uso
- **ONI:** repetido em todas as cidades do mesmo mês. Agregue com **média**, nunca com soma.
- **Chuva e dias de chuva:** use valores relativos ao normal da própria cidade (ex.: % vs. média 1991–2020), não compare valores absolutos entre cidades.
- **Fase por mês:** a maioria dos anos mistura fases. Para análises anuais, use o ONI médio.

## Colunas calculadas no Power BI (não estão no CSV)
| Coluna | Fórmula (resumo) |
|---|---|
| `temp_normal` | Média de `temp_media` da mesma cidade e mês em 1991–2020 |
| `anomalia_temp` | `temp_media − temp_normal` |
| `chuva_normal` | Média de `precip_total_mm` da mesma cidade e mês em 1991–2020 |
| `Local` | `cidade & ", " & pais` (para o mapa) |
