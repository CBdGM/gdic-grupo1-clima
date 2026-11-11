# Previsão do Power BI × real de 2026

Previsão: página **Previsão**, gráfico "Previsão 2026–2027" (recurso Previsão do Power BI, treinado com 2016–2025, sem filtro = média das 39 cidades), valores lidos na dica de ferramenta em 10/11/2026.
Real: `data/extra/real_2026.csv`, gerado por `scripts/validar_previsao_2026.py` (Open-Meteo/ERA5). A base oficial não foi alterada.

| Mês | Previsto (°C) | Faixa 95% (°C) | Real (°C) | Real − previsto | Dentro da faixa? |
|---|---|---|---|---|---|
| jan/2026 | 22,59 | 22,08–23,10 | 22,35 | −0,24 | sim |
| fev/2026 | 22,87 | 22,30–23,44 | 22,51 | −0,36 | sim |
| mar/2026 | 22,71 | 22,09–23,33 | 22,56 | −0,15 | sim |
| abr/2026 | 22,10 | 21,43–22,77 | 22,02 | −0,08 | sim |
| mai/2026 | 21,20 | 20,48–21,92 | 21,22 | +0,02 | sim |
| jun/2026 | 20,14 | 19,38–20,90 | 20,41 | +0,27 | sim |
| jul/2026 | 20,05 | 19,25–20,86 | 20,93 | **+0,88** | **não (acima)** |
| ago/2026 | 20,57 | 19,73–21,41 | 21,64 | **+1,07** | **não (acima)** |
| set/2026 | 21,23 | 20,35–22,11 | 21,85 | +0,62 | sim |
| out/2026 | 21,54 | 20,62–22,45 | 21,93 | +0,39 | sim |

- Jan–mai (antes do El Niño): real em média **0,16 °C abaixo** do previsto. A previsão acertou.
- Jun–out (El Niño em curso): real em média **0,65 °C acima** do previsto; jul e ago acima da faixa de 95%.
- Jul–set/2026 tiveram anomalia média de +1,4 a +1,7 °C, acima do maior valor mensal da base (+1,28 °C, set/2023, também El Niño).
- Maiores anomalias em jul–set: Guayaquil (+4,4 °C), Lima (+4,1 °C) e Piura (+4,0 °C), o padrão clássico do El Niño na costa do Pacífico.
- Leitura: a previsão estatística não sabe do El Niño; o desvio aparece justamente nos meses de El Niño e é maior onde o El Niño mais atua. É evidência coerente com o efeito do El Niño (um único ano; o aquecimento de fundo também contribui).

Gráfico: `docs/img/validacao_2026.png`.

## Lima e Recife

Mesmo método, com o filtro de Cidade da página Previsão (valores lidos em 10/11/2026).

| Mês | Lima previsto (faixa) | Lima real | Recife previsto (faixa) | Recife real |
|---|---|---|---|---|
| jan | 21,73 (20,52–22,94) | 22,21 | 26,84 (26,24–27,45) | 27,23 |
| fev | 23,01 (21,35–24,68) | 23,49 | 26,98 (26,30–27,66) | 27,30 |
| mar | 22,46 (20,52–24,39) | 22,92 | 26,87 (26,13–27,62) | 27,56 |
| abr | 20,79 (18,75–22,82) | 21,73 | 26,61 (25,81–27,41) | 26,28 |
| mai | 18,60 (16,58–20,61) | **20,95** | 25,88 (25,05–26,71) | 25,73 |
| jun | 17,04 (15,03–19,04) | **20,74** | 25,01 (24,16–25,86) | 25,51 |
| jul | 16,21 (14,15–18,26) | **20,82** | 24,44 (23,56–25,31) | **25,35** |
| ago | 15,85 (13,71–17,99) | **20,36** | 24,51 (23,59–25,43) | 25,40 |
| set | 16,11 (13,81–18,41) | **21,01** | 25,05 (24,06–26,03) | **26,16** |
| out | 16,74 (14,22–19,25) | **22,89** | 25,95 (24,90–27,01) | **27,34** |

Em negrito: acima do limite superior da faixa de 95%.

- **Lima:** jan–mai +0,94 °C vs. previsto; jun–out **+4,77 °C**, fora da faixa de mai a out. O inverno de Lima (normalmente ~16 °C) praticamente não aconteceu: é o efeito clássico do El Niño costeiro.
- **Recife:** jan–mai +0,18 °C; jun–out **+0,96 °C**, fora da faixa em jul, set e out. Cuidado na leitura: nos El Niños fortes da base, Recife ficou só +0,04 °C acima do normal, então o calor de 2026 em Recife provavelmente tem outras causas além do El Niño (por exemplo, o Atlântico tropical quente). Recife mostra que a previsão errou para cima, mas não serve como prova do efeito do El Niño.

Gráficos: `docs/img/validacao_2026_lima.png` e `docs/img/validacao_2026_recife.png`.

## Temperatura máxima (botão Máxima da página Previsão)

Mesmo método: previsão do Power BI lida na tela em 10/11/2026; real em `data/extra/real_2026.csv` (`temp_max_media`).

| Mês | Geral previsto (faixa) | Geral real | Lima previsto (faixa) | Lima real | Recife previsto (faixa) | Recife real |
|---|---|---|---|---|---|---|
| jan | 27,48 (26,90–28,07) | 27,13 | 24,00 (22,77–25,22) | 24,36 | 29,63 (28,80–30,46) | 30,00 |
| fev | 27,87 (27,21–28,52) | 27,32 | 25,29 (23,61–26,97) | 25,70 | 29,52 (28,60–30,45) | 30,16 |
| mar | 27,70 (26,98–28,42) | 27,42 | 24,76 (22,81–26,71) | 25,27 | 29,52 (28,51–30,54) | 30,53 |
| abr | 26,92 (26,14–27,69) | 26,74 | 23,03 (20,97–25,09) | 24,03 | 29,24 (28,16–30,33) | 28,89 |
| mai | 25,71 (24,88–26,54) | 25,83 | 20,85 (18,78–22,92) | **23,52** | 28,07 (26,95–29,19) | 28,18 |
| jun | 24,58 (23,70–25,46) | 24,78 | 19,36 (17,27–21,45) | **23,20** | 27,12 (25,97–28,26) | 27,70 |
| jul | 24,80 (23,87–25,72) | 25,59 | 18,65 (16,48–20,81) | **23,13** | 26,58 (25,40–27,76) | **27,77** |
| ago | 25,54 (24,57–26,51) | 26,45 | 18,27 (16,01–20,53) | **22,97** | 26,68 (25,44–27,92) | 27,76 |
| set | 26,18 (25,17–27,20) | 26,61 | 18,63 (16,19–21,07) | **23,48** | 27,26 (25,94–28,59) | 28,51 |
| out | 26,27 (25,21–27,33) | 26,31 | 19,27 (16,62–21,92) | **25,25** | 28,33 (26,90–29,77) | **29,94** |

Em negrito: acima do limite superior da faixa de 95%.

| | Jan–mai (real − previsto) | Jun–out (real − previsto) |
|---|---|---|
| Geral | −0,25 °C | +0,47 °C (nenhum mês fora da faixa) |
| Lima | +0,99 °C | **+4,77 °C** (mai a out fora da faixa) |
| Recife | +0,36 °C | +1,14 °C (jul e out fora da faixa) |

- Na média das 39 cidades, o desvio da máxima em relação à previsão foi menor que o da média diária (+0,47 °C contra +0,65 °C) e ficou dentro da faixa. Isso não significa que a máxima esquentou menos: em relação ao normal 1991–2020, jun–out/2026 teve máxima +1,53 °C, média +1,25 °C e mínima +1,07 °C. A diferença vem da própria previsão: para jun–out, a previsão da máxima já estava cerca de 1,0 °C acima do normal (a da média, cerca de 0,6 °C), porque as máximas de 2016–2025 já vinham mais altas em relação ao normal; além disso, a faixa da máxima é mais larga.
- Em Lima o sinal é igual ao da média: a máxima de inverno ficou ~4,8 °C acima do previsto.

Gráficos: `docs/img/validacao_2026_max_geral.png`, `docs/img/validacao_2026_max_lima.png`, `docs/img/validacao_2026_max_recife.png`.
