# Como trabalhar em equipe no dashboard

Cada integrante tem uma cópia do repositório (clone), trabalha **só na própria página** e sincroniza pelo GitHub. No formato `.pbip` cada página é uma pasta separada, então o Git junta o trabalho de todos sem conflito, desde que as regras abaixo sejam seguidas.

## Configuração (uma vez)
1. Conta no GitHub e aceitar o convite de colaborador.
2. Instalar Git, VS Code e Power BI Desktop atualizado (Windows).
3. Clonar em **`C:\gdic-grupo1-clima`** (*Ctrl+Shift+P → Git: Clone*).
4. Configurar a identidade no terminal:
   ```
   git config --global user.name "Seu Nome"
   git config --global user.email "email-da-sua-conta-github"
   ```
5. Abrir `powerbi\GDIC_Grupo1_Clima.pbip` → *Página Inicial → Atualizar*.

## Páginas e responsáveis

| # | Página | Pergunta | Responsável |
|---|---|---|---|
| 1 | Visão Geral | O que tem na base? | _(preencher)_ |
| 2 | Aquecimento | As cidades estão esquentando? Quanto por década? | _(preencher)_ |
| 3 | Calor extremo | Máximas e mínimas mudam igual? Há mais calor extremo? | _(preencher)_ |
| 4 | El Niño e La Niña | Como mudam a chuva e a temperatura por região? | _(preencher)_ |
| 5 | Eventos extremos | Os eventos recentes aparecem nos dados? | _(preencher)_ |
| 6 | Previsão | O que esperar? | _(preencher)_ |
| 7 | Ficha da cidade | Como é o clima de cada cidade em detalhe? (drill-through) | _(preencher)_ |

A página oculta **Rascunho (análise inicial)** guarda os primeiros visuais de teste, para consulta. Pode ser apagada no final.

## Fluxo de cada sessão
1. **Power BI fechado** → VS Code → **Sincronizar** (pull).
2. Abrir o `.pbip` → *Atualizar*, se pedir.
3. Trabalhar **só na sua página**.
4. **Salvar e fechar** o Power BI.
5. VS Code → conferir os arquivos alterados → mensagem (ex.: `feat(aquecimento): ranking das cidades`) → **Confirmar** → **Sincronizar**.

O Power BI não percebe mudanças feitas por fora enquanto está aberto: se você fizer pull com ele aberto e depois salvar, sobrescreve o trabalho dos colegas.

## Regras
| Regra | Por quê |
|---|---|
| Cada um mexe só na própria página | Cada página é uma pasta própria (`…Report/definition/pages/<id>/`) |
| Medida ou coluna nova: avisar no grupo, fazer pull, criar e já enviar | Todas as medidas ficam em um arquivo só (`Medidas.tmdl`); duas pessoas criando ao mesmo tempo gera conflito |
| Não renomear nem apagar medidas, colunas ou páginas dos outros | Quebra os visuais de outra pessoa |
| Não alterar a fonte de dados (caminho do CSV) | O caminho `C:\gdic-grupo1-clima\...` é o mesmo para todos |
| Tema, navegação e filtros padrão: só a pessoa da página 7 | Ficam em arquivos compartilhados (`report.json`) |
| Nunca editar os CSVs à mão | A base é versionada por script (ver CHANGELOG) |
| Nunca usar force push | Apaga o trabalho de quem enviou antes |

**Confira a lista de arquivos alterados antes de confirmar.** Devem aparecer quase só arquivos da sua página. Se aparecer `Medidas.tmdl`, `pages.json` ou `report.json` sem você ter mexido neles, pergunte no grupo antes de enviar.

## Padrão visual
- Vermelho = quente / El Niño; azul = frio / La Niña; cinza = neutro.
- Página 1280 × 720; título no canto superior esquerdo; filtros no canto superior direito.
- Use as medidas da tabela **Medidas** (pastas Base, Temperatura, Chuva, El Niño e La Niña, Tendência e previsão) em vez de criar versões parecidas.

## Se der conflito
- Arquivo da sua página: aceite a sua versão (*Aceitar alteração atual*).
- `Medidas.tmdl`, `pages.json`, `report.json`: não resolva sozinho, chame o integrador (geralmente *Aceitar ambas*).
- Plano B: guarde uma cópia da pasta da sua página, clone de novo e cole a página de volta.

## Sem Git ou sem Power BI
- Mac ou sem Power BI: relatório, slides e revisão.
- Sem Git: monte a página num `.pbix` próprio e mande ao integrador, que copia para o projeto.

## Entrega
O integrador faz pull, abre, atualiza, testa todas as páginas, salva uma cópia `.pbix` para o Classroom e cria a tag `v1.0-entrega`.
