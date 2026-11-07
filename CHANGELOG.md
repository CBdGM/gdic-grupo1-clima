# Changelog – Clima LatAm

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [Planejado] – v1.2.0
- Incluir Cusco, Córdoba, Santa Cruz de la Sierra e Iquitos (linhas comentadas em `scripts/ampliar_clima_latam.py`).

## [1.1.0] – 2026-11-07
Arquivo: `data/clima_latam_ampliado.csv` · 39 cidades · 20 países · 21.528 linhas
SHA-256: `b66050830f4f4777b61ea777fd585dac02b10bf03f8f11d3141367ef5cecab26`

### Adicionado
- 10 cidades via Open-Meteo Historical Weather API (ERA5): Recife, Salvador, Belém, Rio de Janeiro, Curitiba, Cuiabá, San José, San Salvador, Porto Príncipe, Medellín.
- 3 países novos: Costa Rica, El Salvador e Haiti.
- San José já estava prevista no `baixar.py` da v1.0.0, mas não tinha sido baixada (limite da API). Foi incluída com as mesmas coordenadas.
- Script `scripts/ampliar_clima_latam.py` e cache das cidades novas em `data/cache_openmeteo/`.

### Método
- Mesmo método da v1.0.0: médias mensais das variáveis diárias e dia de chuva = precipitação ≥ 1 mm.
- Colunas de El Niño (`oni`, `fase`, `intensidade`, `evento_enso`) copiadas da v1.0.0 por mês, porque são iguais para todas as cidades.
- Dados baixados em 2026-11-07.

### Validação
- As 16.008 linhas da v1.0.0 estão idênticas na v1.1.0.
- 39 × 552 meses completos, sem vazios, sem duplicados; ONI e fase batem em 100% dos meses.
- Normais 1991–2020 comparadas com INMET, IDEAM, MARN e outros serviços; eventos reais conferidos (Recife mai/2022 +245%, crise hídrica de Curitiba 2020, secas do Pantanal 2020 e 2024). Ver `docs/validacao.md`.

### Limitações conhecidas
- Chuva absoluta subestimada em cidades costeiras (Recife −56%, Belém −38%, Salvador −34%) e superestimada em cidades de vale ou serra (San José +53%, Rio +50%).
- Temperatura mais fria em Medellín (−2,9 °C) e San José (−2,3 °C).
- Dias de chuva acima dos registrados nas estações (garoa no ERA5).

## [1.0.0] – 2026-11-07
Arquivo: `data/clima_latam.csv` · 29 cidades · 17 países · 16.008 linhas
SHA-256: `4d70d6a519e8cca1aaac6cf200418b734aaf475964da43d1801238630ad257c3`

### Adicionado
- Base original criada por uma integrante do grupo com `scripts/baixar.py`.
- Clima: Open-Meteo Historical Weather API (ERA5), 1980-01 a 2025-12, agregado por mês.
- El Niño / La Niña: ONI da NOAA CPC, com fase pelo critério oficial (5 trimestres móveis seguidos com ONI ≥ +0,5 ou ≤ −0,5) e intensidade pelo pico do evento.

### Observações
- O script lista 30 cidades, mas San José (Costa Rica) não foi baixada nesta versão.
- Validação: chuva e temperatura absolutas com vieses do ERA5 em algumas cidades (Lima, Quito, Guayaquil, Cidade do México); ONI conferido com a tabela da NOAA.
