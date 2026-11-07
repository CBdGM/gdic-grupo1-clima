# Validação – Clima LatAm

Validação feita em 2026-11-07, comparando as normais 1991–2020 da base com as normais climatológicas das estações oficiais (tabelas das páginas das cidades na Wikipedia, que citam INMET, SENAMHI, IDEAM, SMN, DMC, MARN, WMO) e conferindo eventos extremos conhecidos.

**Conclusão:** confiável para tendências, anomalias, El Niño e eventos extremos; não confiável para valores absolutos de chuva em várias cidades (viés da reanálise ERA5, que representa uma área de ~25 km × 25 km).

## 1. Estrutura
| Verificação | v1.0.0 | v1.1.0 |
|---|---|---|
| Linhas / cidades / países | 16.008 / 29 / 17 | 21.528 / 39 / 20 |
| Meses por cidade (1980-01 a 2025-12) | 552 | 552 |
| Valores vazios / duplicados | 0 / 0 | 0 / 0 |
| Máx ≥ mín, média entre as duas | OK | OK |
| Linhas da v1.0.0 preservadas | – | 16.008 idênticas |

## 2. Normais 1991–2020: base × estação
| Cidade | Temp. média base / estação (°C) | Chuva anual base / estação (mm) | Avaliação |
|---|---|---|---|
| Porto Alegre | 19,6 / 19,9 | 1.542 / 1.498 | Muito bom |
| Porto Príncipe | 27,2 / 27,2 | 1.454 / 1.295 | Muito bom |
| Brasília | 21,8 / 21,4 | 1.375 / 1.479 | Bom |
| Bogotá | 14,1 / 13,9 | 935 / 877 | Bom |
| Cuiabá | 26,2 / 26,4 | 1.380 / 1.516 | Bom |
| Curitiba | 17,4 / 17,8 | 1.544 / 1.631 | Bom |
| San Salvador | 23,8 / 24,0 | 1.542 / 1.781 | Bom |
| La Paz (El Alto) | 8,2 / 7,9 | 715 / 603 | Razoável |
| Buenos Aires | 17,2 / 18,1 | 1.070 / 1.258 | Chuva −15% |
| São Paulo | 19,6 / 20,2 | 1.289 / 1.658 | Chuva −22% |
| Manaus | 26,4 / 27,4 | 2.694 / 2.362 | Temp −1 °C, chuva +14% |
| Salvador | 25,0 / 25,6 | 1.205 / 1.833 | Chuva −34% |
| Fortaleza | 26,6 / 27,0 | 1.007 / 1.584 | Chuva −36% |
| Belém | 26,6 / 26,8 | 2.052 / 3.308 | Chuva −38% |
| Recife | 25,9 / 26,0 | 938 / 2.156 | Chuva −56% |
| Rio de Janeiro* | 23,7 / 25,3 | 1.601 / 1.069 | Chuva +50% |
| Santiago | 15,3 / 16,0 | 488 / 286 | Chuva +70% |
| Guayaquil | 24,3 / 26,4 | 2.142 / 1.186 | Chuva +80% |
| San José | 20,3 / 22,6 | 3.021 / 1.971 | Temp −2,3 °C, chuva +53% |
| Cidade do México | 15,7 / 18,1 | 1.006 / 847 | Temp −2,4 °C |
| Medellín | 20,2 / 23,1 | 2.795 / 2.238 | Temp −2,9 °C |
| Quito | 11,8 / 14,1 | 2.876 / 1.100 | Chuva 2,6× |
| Lima | 19,0 / 19,6–20,5 | 85 / 6–10 | Chuva 8–13× |

\* Estação do Rio com normal 1981–2010.
Padrão: cidades costeiras com chuva subestimada; cidades em vale ou serra mais frias e com chuva superestimada; máximas médias abaixo das estações.

## 3. El Niño (ONI) × tabela da NOAA
| Evento | Pico na base | Pico na tabela | Classificação |
|---|---|---|---|
| El Niño 1982–83 | 2,14 | 2,23 | Muito forte |
| El Niño 1997–98 | 2,37 | 2,40 | Muito forte |
| El Niño 2015–16 | 2,59 | 2,75 | Muito forte |
| El Niño 2023–24 | 1,99 | 2,06 | Forte |
| La Niña 1988–89 | −1,85 | −1,85 | Forte |
| 2024–25 | −0,46 | −0,45 | Neutro |

Diferenças pequenas por versão do índice. Fim de 2025 (ONI ≈ −0,6) corretamente neutro: ainda sem 5 trimestres seguidos.

## 4. Eventos reais capturados
| Evento | Na base |
|---|---|
| Seca de São Paulo (jan/2014) | −63% de chuva |
| Seca da Amazônia (ago–out/2023) | Manaus −75% |
| El Niño 1998 em Piura | jan–mar com 622, 423 e 729 mm (normais 37, 65 e 112) |
| Seca do Nordeste (2012) | Fortaleza −64% em abril |
| Enchentes do RS (set/2023, mai/2024) | Porto Alegre +188% e +230%, os meses mais chuvosos da série |
| Chuvas de Recife (mai/2022) | +245% (437 mm) |
| Chuvas do Rio (abr/2010) | +81% |
| La Niña 2010–11 na Colômbia | Medellín +83% em nov/2010 |
| Crise hídrica do Paraná (2020) | Curitiba −56% a −63% |
| Secas do Pantanal (2020 e 2024) | Cuiabá com 0–2 mm em ago–set |
| Calor extremo em Monterrey (mai/2024) | 44,4 °C, maior máxima da base |

## 5. Aquecimento (anomalia média vs. 1991–2020)
| Década | 29 cidades originais | 10 cidades novas |
|---|---|---|
| 1980 | −0,29 °C | −0,33 °C |
| 2000 | −0,08 °C | −0,05 °C |
| 2020 | +0,31 °C | +0,21 °C |
Tendência das 29 originais: +0,15 °C por década.
