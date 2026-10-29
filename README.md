# dba-instagram

Artes dos posts do Instagram @dbalternativa (Distribuidora Alternativa), uma pasta por semana.
As imagens são publicadas pelo Metricool a partir dos links públicos deste repositório.

## Padrão visual
- Base preta (#0D0D0D) e amarelo da fachada (#FFC400); vermelho do logo (#D8261C) só para preço.
- Logo `_assets/logo.png` sempre no topo à esquerda; foto real da loja em `_assets/`.
- Modelos: `chamada` (tipográfico), `foto` (foto da loja no topo), `oferta` (produto + preço).
- Gerar: `python3 _template/render.py <pasta> <pasta>/semana.json`

## Calendário de datas
`calendario.json` lista feriados (nacionais e do DF), datas comerciais e locais (ex.: aniversário de Ceilândia) com o que fazer em cada uma.
Toda segunda a tarefa semanal verifica os próximos 14 dias e cria flyers extras. Preencha "horario" quando a loja abrir em horário diferente num feriado.
