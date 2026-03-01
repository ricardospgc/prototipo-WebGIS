# Análise Espacial dos Equipamentos Esportivos de Belo Horizonte

Este projeto realiza o processamento e a visualização geoespacial dos equipamentos esportivos públicos da cidade de Belo Horizonte, Minas Gerais. O objetivo foi converter dados brutos da prefeitura e IBGE em um mapa interativo e otimizado para navegação.

## Desafios Técnicos Resolvidos

- **Sistemas de Coordenadas (CRS):** Os dados originais da PBH/BHGEO utilizam o sistema **SIRGAS 2000 / UTM zone 23S (EPSG:31983)**, que mede distâncias em metros. Para a visualização no Folium (web), os dados foram reprojetados para **WGS84 (EPSG:4326)**, que utiliza graus decimais (Latitude/Longitude).
- **Performance (Clusterização):** Para evitar lentidão no browser ao renderizar centenas de marcadores, foi utilizada a técnica de **Marker Clustering**, agrupando pontos próximos dinamicamente.

## Estrutura do Projeto

```text
Prototipo_WebGIS/
├── data/               # Bases de dados
├── maps/               # Saída dos mapas gerados em .html
├──notebooks/           # Notebooks python de estudo das bibliotecas e testes
├── src/                # Módulos de lógica do sistema
│   ├── processamento.py # Limpeza, conversão UTM e cálculo de Lat/Lon
│   └── visualizacao.py  # Estilização, clusters e macros de interface
├── main.py             # Entry Point da aplicação
└── requirements.txt    # Dependências
```

## Como Executar

1. **Prepare o ambiente virtual:**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

```


2. **Instale as dependências:**
```bash
pip install -r requirements.txt

```


3. **Execute o processamento e geração do mapa:**
```bash
python main.py

```


## Fontes de Dados

* **Prefeitura de Belo Horizonte (PBH):** Localização espacial dos equipamentos públicos da prefeitura de Belo Horizonte destinados à prática de esportes como por exemplo as academias a céu aberto, quadras, campos de futebol. Versão de Janeiro de 2026.
https://dados.pbh.gov.br/dataset/equipamento-esportivo1/resource/ce13db76-97d9-418e-b0aa-d44b4d698222

* **IBGE:** Malha municipal do estado de Minas Gerais.
https://www.ibge.gov.br/geociencias/organizacao-do-territorio/malhas-territoriais/15774-malhas.html
---

*Projeto desenvolvido como parte de um estudo prático de Geoprocessamento com Python.*