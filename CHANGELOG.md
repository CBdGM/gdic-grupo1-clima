# Changelog – Clima LatAm

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e [Versionamento Semântico](https://semver.org/lang/pt-BR/).

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
