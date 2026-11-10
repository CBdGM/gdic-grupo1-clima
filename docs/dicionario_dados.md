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

## Colunas criadas no Power BI (não estão no CSV)

Ficam na tabela `clima_cidades` (`powerbi/GDIC_Grupo1_Clima.SemanticModel/definition/tables/clima_cidades.tmdl`). São 13: 11 colunas calculadas em DAX e 2 criadas no Power Query.

"Normal" é sempre a média **da mesma cidade e do mesmo mês** no período de referência **1991–2020**. "Anomalia" é o valor do mês menos o normal: positiva = acima do normal, negativa = abaixo.

### Normais (referência 1991–2020)
| Coluna | Unidade | Fórmula (resumo) | Para que serve |
|---|---|---|---|
| `temp_normal` | °C | Média de `temp_media` da mesma cidade e mês em 1991–2020 | Base da anomalia de temperatura |
| `temp_max_normal` | °C | Média de `temp_max_media` da mesma cidade e mês em 1991–2020 | Base da anomalia das máximas |
| `temp_min_normal` | °C | Média de `temp_min_media` da mesma cidade e mês em 1991–2020 | Base da anomalia das mínimas |
| `chuva_normal` | mm | Média de `precip_total_mm` da mesma cidade e mês em 1991–2020 | Denominador de `Chuva vs Normal (%)` |

### Anomalias e amplitude
| Coluna | Unidade | Fórmula | Para que serve |
|---|---|---|---|
| `anomalia_temp` | °C | `temp_media − temp_normal` | Quanto o mês ficou mais quente ou mais frio que o normal |
| `anomalia_max` | °C | `temp_max_media − temp_max_normal` | Desvio das máximas (página Calor extremo) |
| `anomalia_min` | °C | `temp_min_media − temp_min_normal` | Desvio das mínimas (página Calor extremo) |
| `amplitude_termica` | °C | `temp_max_media − temp_min_media` | Diferença média entre máxima e mínima do mês |

Não existe coluna de anomalia de chuva: a comparação com o normal é feita pela medida `Chuva vs Normal (%)`.

### Colunas de apoio
| Coluna | Tipo | Fórmula | Para que serve |
|---|---|---|---|
| `Local` | texto (categoria *Local*) | `cidade & ", " & pais` | Localização no visual de mapa |
| `decada` | inteiro | `INT(ano / 10) * 10` (ex.: 1980, 1990) | Agrupar por década |
| `nome_mes` | texto | `FORMAT(data, "MMM")`, ordenada por `mes` | Nome curto do mês no eixo, em ordem de calendário |
| `ordem_fase` | inteiro, **oculta** | Power Query: La Niña = 1, Neutro = 2, El Niño = 3 | Ordena a coluna `fase` |
| `ordem_intensidade` | inteiro, **oculta** | Power Query: Fraco = 1, Moderado = 2, Forte = 3, Muito forte = 4, demais = 0 | Ordena a coluna `intensidade` |

### Região (`regiao`)

| Coluna | Tipo | Fórmula | Para que serve |
|---|---|---|---|
| `regiao` | texto | Coluna calculada em DAX: `SWITCH` sobre `cidade` (tabela abaixo); cidade fora da lista recebe "Sem região" | Agrupar as 39 cidades em 10 regiões para comparar o efeito do El Niño e da La Niña |

| Região | Cidades |
|---|---|
| México | Cidade do México, Monterrey |
| América Central e Caribe | Cidade da Guatemala, San Salvador, Tegucigalpa, Manágua, San José, Cidade do Panamá, Havana, Santo Domingo, Porto Príncipe |
| Norte da América do Sul | Bogotá, Medellín, Cartagena, Caracas |
| Amazônia | Manaus, Belém |
| Nordeste do Brasil | Fortaleza, Recife, Salvador, Petrolina |
| Centro-Sudeste do Brasil | Brasília, Cuiabá, São Paulo, Rio de Janeiro |
| Costa do Pacífico | Guayaquil, Piura, Lima |
| Andes tropicais | Quito, La Paz |
| Sul do Brasil e Bacia do Prata | Porto Alegre, Curitiba, Asunción, Buenos Aires, Montevidéu |
| Chile e Argentina andina | Santiago, Antofagasta, Mendoza, Ushuaia |

Fórmula:

```dax
regiao =
SWITCH (
    TRUE (),
    clima_cidades[cidade] IN { "Cidade do México", "Monterrey" }, "México",
    clima_cidades[cidade] IN { "Cidade da Guatemala", "San Salvador", "Tegucigalpa", "Manágua", "San José", "Cidade do Panamá", "Havana", "Santo Domingo", "Porto Príncipe" }, "América Central e Caribe",
    clima_cidades[cidade] IN { "Bogotá", "Medellín", "Cartagena", "Caracas" }, "Norte da América do Sul",
    clima_cidades[cidade] IN { "Manaus", "Belém" }, "Amazônia",
    clima_cidades[cidade] IN { "Fortaleza", "Recife", "Salvador", "Petrolina" }, "Nordeste do Brasil",
    clima_cidades[cidade] IN { "Brasília", "Cuiabá", "São Paulo", "Rio de Janeiro" }, "Centro-Sudeste do Brasil",
    clima_cidades[cidade] IN { "Guayaquil", "Piura", "Lima" }, "Costa do Pacífico",
    clima_cidades[cidade] IN { "Quito", "La Paz" }, "Andes tropicais",
    clima_cidades[cidade] IN { "Porto Alegre", "Curitiba", "Asunción", "Buenos Aires", "Montevidéu" }, "Sul do Brasil e Bacia do Prata",
    clima_cidades[cidade] IN { "Santiago", "Antofagasta", "Mendoza", "Ushuaia" }, "Chile e Argentina andina",
    "Sem região"
)
```

Cuidados:
- A classificação é uma escolha do grupo (geografia + comportamento parecido no El Niño), não uma divisão oficial.
- **Ao acrescentar cidades à base** (ex.: v1.2.0), inclua-as na fórmula; senão aparecem como "Sem região".
- Regiões com poucas cidades (México, Amazônia e Andes tropicais têm 2) representam só essas cidades, não a região inteira.
- Em `Chuva vs Normal (%)` por região, as cidades mais chuvosas pesam mais (a medida soma os mm antes de dividir).

## Medidas (tabela `Medidas`)

Ficam em `powerbi/GDIC_Grupo1_Clima.SemanticModel/definition/tables/Medidas.tmdl`. São 21. A coluna **Pasta** é a pasta de exibição no painel *Dados* do Power BI; "–" indica medida ainda sem pasta (aparece solta na raiz da tabela).

### Base
| Medida | Pasta | Fórmula (resumo) | O que mostra |
|---|---|---|---|
| `Nº Cidades` | Base | Contagem distinta de `cidade` | Cidades no filtro atual |
| `Nº Países` | Base | Contagem distinta de `pais` | Países no filtro atual |
| `Nº Registros` | Base | Contagem de linhas | Linhas (cidade × mês) no filtro atual |
| `Período` | Base | `MIN(ano) & " – " & MAX(ano)` | Texto com o intervalo de anos, ex.: "1980 – 2025" |

### Temperatura
| Medida | Pasta | Fórmula (resumo) | O que mostra |
|---|---|---|---|
| `Temp Média (°C)` | – | Média de `temp_media` | Temperatura média |
| `Temp Normal (°C)` | Temperatura | Média de `temp_normal` | Temperatura normal (1991–2020) |
| `Anomalia Temp (°C)` | – | Média de `anomalia_temp` | Desvio médio da temperatura em relação ao normal |
| `Anomalia Máx (°C)` | Temperatura | Média de `anomalia_max` | Desvio médio das máximas |
| `Anomalia Mín (°C)` | Temperatura | Média de `anomalia_min` | Desvio médio das mínimas |
| `Amplitude Térmica (°C)` | Temperatura | Média de `amplitude_termica` | Diferença média entre máxima e mínima |
| `Máxima Absoluta (°C)` | Temperatura | Máximo de `temp_max_absoluta` | Maior temperatura registrada no filtro atual |

### Chuva
| Medida | Pasta | Fórmula (resumo) | O que mostra |
|---|---|---|---|
| `Chuva Mensal Média (mm)` | – | Média de `precip_total_mm` | Chuva média por mês |
| `Chuva Anual Média (mm)` | Chuva | Soma de `precip_total_mm` por cidade e ano, depois média | Chuva média por ano |
| `Chuva Normal (mm)` | Chuva | Média de `chuva_normal` | Chuva mensal normal (1991–2020) |
| `Chuva vs Normal (%)` | – | `SUM(precip_total_mm) / SUM(chuva_normal) − 1` | Quanto choveu a mais ou a menos que o normal dos mesmos meses e cidades |
| `Chuva vs Neutro (%)` | – | `Chuva Mensal Média ÷ Chuva Mensal Média dos meses neutros − 1` | Chuva do filtro atual comparada com a dos meses neutros |

### El Niño e La Niña
| Medida | Pasta | Fórmula (resumo) | O que mostra |
|---|---|---|---|
| `ONI Médio` | – | Média de `oni` | Índice médio do Pacífico (positivo = El Niño, negativo = La Niña) |
| `% Meses El Niño` | El Niño e La Niña | Meses distintos com `fase = "El Niño"` ÷ meses distintos | Parcela do período em El Niño |
| `% Meses La Niña` | El Niño e La Niña | Meses distintos com `fase = "La Niña"` ÷ meses distintos | Parcela do período em La Niña |

### Tendência e previsão
| Medida | Pasta | Fórmula (resumo) | O que mostra |
|---|---|---|---|
| `Tendência (°C por década)` | Tendência e previsão | Inclinação da regressão linear (`LINESTX`) de `Anomalia Temp` por ano × 10 | Ritmo de aquecimento |
| `Anomalia Projetada 2030 (°C)` | Tendência e previsão | Mesma reta, calculada para o ano 2030 | Anomalia esperada em 2030 se a tendência continuar |

### Cuidados com as medidas
- **`Chuva vs Normal (%)` × `Chuva vs Neutro (%)`:** prefira `Chuva vs Normal (%)` para comparar fases. Ela compara cada mês com o normal do mesmo mês e da mesma cidade, então não é afetada pela época do ano. `Chuva vs Neutro (%)` compara médias de chuva em mm e mistura estações: El Niño e La Niña se concentram em certos meses do ano, e a diferença pode refletir só a estação chuvosa.
- **`Chuva vs Neutro (%)`** ignora o filtro de `fase` no denominador. Com `fase` no eixo, a barra "Neutro" é sempre 0%.
- **Medidas de chuva em mm** (`Chuva Mensal Média`, `Chuva Anual Média`, `Chuva Normal`) não servem para comparar cidades entre si (viés do ERA5, ver `docs/validacao.md`).
- **`Chuva Anual Média (mm)`** só faz sentido com anos completos: com filtro de mês ou de fase, soma apenas os meses filtrados.
- **Tendência e projeção** precisam de vários anos no filtro. Com poucos anos o resultado não é confiável.
