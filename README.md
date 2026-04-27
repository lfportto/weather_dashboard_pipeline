# Dashboard Global de Clima 100% Automatizado

📄 [English version](README_English.md)

## Descrição do Projeto
Este projeto consiste na construção de um pipeline completo de dados meteorológicos, desde a ingestão automatizada até a visualização final em um dashboard interativo no Power BI. Os dados são coletados a partir de APIs REST externas, armazenados em um banco de dados na nuvem e atualizados automaticamente ao longo do dia. O dashboard permite explorar condições climáticas atuais, históricas e previsões futuras para múltiplas cidades ao redor do mundo, fornecendo dados quase em tempo real (com atraso de no máximo poucas horas). Além da parte técnica, o projeto também explora uma identidade visual diferenciada, inspirada na estética Frutiger Aero, trazendo uma experiência visual nostálgica, leve e agradável.

## 🎯 Objetivo
Este é um projeto pessoal desenvolvido com foco no aprimoramento de habilidades em análise de dados, incluindo:
- Construir um pipeline de dados completo (end-to-end)
- Integrar múltiplas fontes de dados meteorológicos
- Automatizar a ingestão e atualização dos dados
- Desenvolver um dashboard interativo e intuitivo
- Aplicar boas práticas de modelagem e visualização de dados
- Explorar UX/UI aplicada a dashboards

## Tecnologias Utilizadas
- Python
- Principais bibliotecas: meteostat, numpy, psycopg2, dotenv, requests
- Git & GitHub
- PostgreSQL (Neon - Cloud)
- OpenWeather API
- Meteostat API
- Prefect Cloud
- Power BI

## Arquitetura do Projeto
A figura abaixo mostra como foi estruturada a arquitetura por trás desse projeto:  

![Pipeline](https://github.com/user-attachments/assets/622c01e0-2752-4dff-b708-0cd436411eeb)

## Pipeline de Dados (ETL)
### 🔹 Extração
- Coleta de dados históricos utilizando a API do Meteostat
- Coleta de dados atuais (near real-time) via OpenWeather API
- Coleta de dados de previsão para os próximos 5 dias
- Execução de múltiplas requisições para diferentes cidades globais

### 🔹 Transformação
- Tratamento de valores nulos
- Padronização de unidades e formatos
- Conversão de timestamps para UTC
- Enriquecimento dos dados com atributos adicionais (ex: weather_main, description, icon)

### 🔹 Carregamento
- Inserção dos dados em tabelas no PostgreSQL (Neon)
- Estruturação em múltiplas tabelas:
  - Dados históricos
  - Dados atuais
  - Dados de previsão
- Controle de integridade e consistência dos dados
- Atualizações contínuas via automação

## 🛢 Estratégia de Ingestão de Dados
- **Dados históricos ([historical_ingestion.py](historical_ingestion.py))**  
Dados de 10 cidades de diferentes países ao redor do mundo, coletados com granularidade diária.

- **Dados atuais ([current_ingestion.py](current_ingestion.py))**
  - Execução automática 4x ao dia
  - 00h, 06h, 12h, 18h
  - Atualização incremental do banco
 
- **Dados de previsão ([forecast_ingestion.py](forecast_ingestion.py))**
  - Execução automática 1x ao dia, às 00h
  - Atualização incremental do banco
 
## Acesse o Dashboard
🔗 [Clique aqui para acessar o dashboard no Power BI](https://app.powerbi.com/view?r=eyJrIjoiMTM4NTYzYjMtZWIxMS00ZjYxLTkyMTItNmJlNjBkN2Y1NzZhIiwidCI6ImNmNzJlMmJkLTdhMmItNDc4My1iZGViLTM5ZDU3YjA3Zjc2ZiIsImMiOjR9)

## Dashboard Interativo
O dashboard foi desenvolvido no Power BI com foco em clareza, interatividade e experiência do usuário. Na barra lateral, ele conta com alguns filtros, sendo eles: `Cidade` (filtro principal, seleção única), `Data/hora` e `Condição do tempo`. No topo, abaixo do título, conta com alguns indicadores de performance, todos eles com tooltips explicativos para melhor compreensão por parte do usuário, além de ícones dinâmicos. Ainda no topo, no canto direito há um seletor único que permite `alternância de unidade de temperatura`, possibilitando a visualização do dashboard em graus Celsius ou Fahrenheit.

![Dashboard](https://github.com/user-attachments/assets/622848f5-9ede-4b43-863f-942777f2af85)

Na seção principal do dashboard, há um espaço com `seleção de abas` (criadas com a função Bookmark), em que as 4 abas têm os respectivos gráficos:
- `Gráfico de linha:` Temperatura ([unidade]) em [cidade] nos últimos [periodo] dias
- `Gráfico de linha:` Previsão da Temperatura ([unidade]) em [cidade] nos próximos 5 dias
- `Gráfico de barras:` Variação Mensal de Temperatura (Mínimo x Máximo) em [cidade]
- `Gráfico de barras:` Temperatura ([unidade]) Dia x Noite em [cidade]

**Observação:** As palavras dentro de `[]` representam placeholders cujo valor varia de acordo com os filtros selecionados pelo usuário no dashboard.

Abaixo dessa seção, há um gráfico de rosca intitulado "`Distribuição da Condição Climática em [cidade] (Top 5)`". Ao lado desse gráfico, há uma seção com um medidor de umidade do ar (dada em %) e um medidor de pressão atmosférica (dada em hPa), cada um com cards objetivos que fornecem algum insight sobre o valor:
- `Umidade do ar:` seco, confortável, úmido, muito úmido
- `Pressão atmosférica:` instável, estável

Por fim, ao lado direito da seção principal, há uma `seção de comparação entre cidade`, onde há um toggle interativo (criado via bookmarks) que fica desativado por padrão, mas que ao ser ativado, revela um filtro de cidade e uma tabela comparativa com atributos (como temperatura, sensação térmica, umidade etc.) entre a cidade selecionada no dashboard e a cidade selecionada no filtro específico dessa seção.

## Estética Escolhida: Frutiger Aero
A identidade visual deste dashboard foi fortemente inspirada na estética [Frutiger Aero](https://www.bing.com/images/search?q=frutiger+aero&form=HDRSC3&first=1), um estilo de design popular entre meados dos anos 2000 e início dos anos 2010. Essa estética ficou marcada pelo uso de elementos como gradientes suaves, transparências, superfícies brilhantes, cores vibrantes (especialmente tons de azul e verde) e ícones que remetem à natureza e tecnologia — como céu, água, folhas e luz.

Muito associada a interfaces de sistemas como o Windows Vista e o Windows 7, a Frutiger Aero transmitia uma sensação de futuro otimista, limpeza e integração entre tecnologia e meio ambiente.

Esse conceito se encaixa perfeitamente com a proposta deste projeto, que envolve dados climáticos e ambientais. A combinação de cores, elementos visuais e efeitos busca não apenas apresentar informações, mas também criar uma experiência mais imersiva, agradável e até mesmo nostálgica para o usuário, conectando dados meteorológicos com uma estética que reforça essa relação com a natureza e o ambiente.

## Paleta de Cores
![Paleta](https://github.com/user-attachments/assets/c947069c-e3eb-4aa9-8858-3e3910e77035)

## Automação (Prefect Cloud)
A fim de manter os dados sempre atualizados, foi criada uma orquestração com Prefect Cloud, para a execução automática dos scripts de ingestão de dados. Os jobs criados foram:
- current_ingestion
- forecast_ingestion  
### Benefícios:
- Execução automática na nuvem
- Independência do ambiente local
- Agendamento com cron jobs
- Monitoramento de execução (logs e status)
- Escalabilidade do pipeline

## 🚀 Possíveis Melhorias Futuras
- Integração com mais cidades ou regiões
- Inclusão de dados históricos com maior granularidade (horária)
- Implementação de alertas climáticos
- Criação de API própria para servir os dados
- Adição de mapas interativos

## Aprendizados
- Construção de pipelines de dados end-to-end
- Integração de múltiplas APIs
- Modelagem de dados para análise
- Aplicação de UX/UI em visualização de dados
- Boas práticas de automação e versionamento

## Licença
Este projeto está licenciado sob a [Licença MIT](LICENSE).

## Tags
`#Dados` `#AnaliseDeDados` `#EngenhariaDeDados` `#PowerBI` `#Python` `#ETL` `#Dashboard` `#VisualizaçãoDeDados` `#Prefect` `#API` `#PostgreSQL` `#ProjetoDeDados` `#Clima` `#Portfolio` `#Data` `#DataAnalytics` `#DataEngineering` `#DataVisualization` `#DataProject` `#Weather`
