# Validação com dados reais de 2026

Gerado por `scripts/validar_previsao_2026.py` em 10/11/2026.
Dados de 2026: Open-Meteo (ERA5), jan a out/2026, 39 cidades.
**A base oficial não foi alterada** (continua até dez/2025). O real de 2026 fica à parte em `data/extra/real_2026.csv`.

## 1. Temperatura média das cidades: real 2026 × referências

| Mês | Real 2026 (°C) | Média 2016–2025 (°C) | Normal 1991–2020 (°C) | Anomalia 2026 |
|---|---|---|---|---|
| jan/2026 | 22,35 | 22,31 | 22,10 | +0,25 |
| fev/2026 | 22,51 | 22,57 | 22,32 | +0,20 |
| mar/2026 | 22,56 | 22,47 | 22,23 | +0,33 |
| abr/2026 | 22,02 | 21,84 | 21,67 | +0,35 |
| mai/2026 | 21,22 | 20,85 | 20,61 | +0,61 |
| jun/2026 | 20,41 | 19,87 | 19,74 | +0,67 |
| jul/2026 | 20,93 | 19,73 | 19,41 | +1,53 |
| ago/2026 | 21,64 | 20,23 | 19,95 | +1,69 |
| set/2026 | 21,85 | 20,91 | 20,45 | +1,40 |
| out/2026 | 21,93 | 21,26 | 20,97 | +0,96 |

Erro médio absoluto: média 2016–2025 = **0,55 °C** · normal 1991–2020 = **0,80 °C**.
Para comparar com a previsão do Power BI: abra a página Previsão sem filtro e passe o mouse na linha preta
de 2026 (gráfico "Previsão 2026–27", botão Média); compare mês a mês com a coluna "Real 2026".
Para a máxima, use o botão Máxima do mesmo gráfico e a seção 1b.

## 1b. Temperatura máxima média das cidades: real 2026 × referências

| Mês | Real 2026 (°C) | Média 2016–2025 (°C) | Normal 1991–2020 (°C) | Anomalia 2026 |
|---|---|---|---|---|
| jan/2026 | 27,13 | 26,95 | 26,47 | +0,67 |
| fev/2026 | 27,32 | 27,34 | 26,80 | +0,52 |
| mar/2026 | 27,42 | 27,23 | 26,72 | +0,70 |
| abr/2026 | 26,74 | 26,44 | 26,02 | +0,72 |
| mai/2026 | 25,83 | 25,17 | 24,70 | +1,13 |
| jun/2026 | 24,78 | 24,09 | 23,82 | +0,96 |
| jul/2026 | 25,59 | 24,25 | 23,68 | +1,91 |
| ago/2026 | 26,45 | 24,95 | 24,46 | +1,99 |
| set/2026 | 26,61 | 25,62 | 24,87 | +1,74 |
| out/2026 | 26,31 | 25,80 | 25,26 | +1,05 |

## 2. Cenário El Niño 2026–27 × o que aconteceu até agora

Anomalia de temperatura: média dos meses de 2026. Chuva: jun–out/2026, quando o El Niño já estava em curso.
"Cenário" = média dos El Niños fortes da base (o mesmo gráfico da página).

| Região | Anomalia 2026 | Cenário (anomalia) | Chuva jun–out/2026 | Cenário (chuva) | Mesmo sinal na chuva? |
|---|---|---|---|---|---|
| México | +1,33 | −0,17 | +49% | +0% | sim |
| América Central e Caribe | +0,51 | +0,37 | −28% | −10% | sim |
| Norte da América do Sul | +0,57 | +0,52 | −24% | −17% | sim |
| Amazônia | +0,96 | +0,54 | +10% | −23% | não |
| Nordeste do Brasil | +0,85 | +0,14 | +22% | −10% | não |
| Centro-Sudeste do Brasil | +0,60 | +0,41 | +74% | +3% | sim |
| Costa do Pacífico | +2,64 | +1,11 | +58% | +77% | sim |
| Andes tropicais | +1,02 | +0,47 | −20% | −1% | sim |
| Sul do Brasil e Bacia do Prata | +0,03 | +0,21 | +9% | +17% | sim |
| Chile e Argentina andina | +0,94 | −0,02 | +29% | +22% | sim |

## Cuidados
- O pico do El Niño é esperado para nov/2026–jan/2027; os meses analisados são o início do evento.
- Na Costa do Pacífico (Lima, Piura) jun–out é estação seca, com normais de poucos mm: a % fica instável. O efeito do El Niño ali aparece em dez–abr.
- Chuva absoluta do ERA5 tem viés em várias cidades; por isso a comparação é sempre relativa ao normal da própria cidade.
- Este arquivo é gerado pelo script; para atualizar, rode o script de novo.
