# 🦆 Pipeline Local: NYC TLC Trip Data
### Python → DuckDB → Parquet → Power BI

> Prova de conceito de um pipeline de dados local usando dados reais de táxi de Nova York.  
> O objetivo é demonstrar que processar dados **fora do Power BI** é mais eficiente, escalável e fácil de manter.

---

## 🏗️ Arquitetura

```
Fonte (NYC TLC)
      ↓ download via Python (requests)
  BRONZE → dado bruto, sem alteração
      ↓ DuckDB (SQL)
  SILVER → dado limpo, enriquecido com zonas
      ↓ DuckDB (SQL)
  GOLD   → dado agregado, pronto para o BI
      ↓ Parquet
  Power BI → só lê, não processa
```

---

## 📁 Estrutura do Projeto

```
eta_duckdb/
├── dados/
│   ├── bronze/    ← arquivos originais baixados da NYC TLC
│   ├── silver/    ← dados limpos e enriquecidos
│   └── gold/      ← tabelas agregadas para o Power BI
├── db/
│   └── lakehouse.duckdb  ← banco DuckDB local
├── scripts/
│   ├── 01-baixar.py      ← download dos arquivos
│   ├── 02-explorar.py    ← exploração e diagnóstico
│   ├── 03-silver.py      ← limpeza e enriquecimento
│   └── 04-gold.py        ← agregações para o BI
└── requirements.txt
```

---

## 📊 Fonte de Dados

**NYC Taxi & Limousine Commission (TLC) Trip Records**  
https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

- Yellow Taxi Trip Records — Janeiro 2024
- ~3 milhões de viagens reais
- Já disponibilizado em formato Parquet pela NYC

---

## 🔄 O Pipeline

### Bronze — Dado bruto
Download direto da fonte sem nenhuma alteração. Preserva o dado original para auditoria.

### Silver — Dado limpo
- JOIN com tabela de zonas (embarque e desembarque)
- Remoção de registros inválidos (valores negativos, distância zero, datas fora do período)
- Colunas calculadas: duração da viagem em minutos
- Filtro de período: apenas Janeiro/2024

### Gold — Dado agregado
Duas tabelas prontas para consumo no Power BI:

| Tabela | Descrição |
|---|---|
| `viagens_por_bairro.parquet` | Total de viagens, receita e ticket médio por zona |
| `viagens_por_hora.parquet` | Volume e ticket médio por hora do dia |

---

## 📦 Resultado

| Camada | Tamanho |
|---|---|
| Bronze (raw) | ~50 MB |
| Silver (limpo) | ~61 MB |
| Gold (agregado) | **~10 KB** |

> O Power BI carrega **10 KB** em vez de 50 MB — sem nenhuma transformação dentro da ferramenta.

---

## 🚀 Como rodar

### 1. Instalar dependências

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Baixar os dados

```bash
python3 scripts/01-baixar.py
```

### 3. Explorar os dados

```bash
python3 scripts/02-explorar.py
```

### 4. Gerar camada Silver

```bash
python3 scripts/03-silver.py
```

### 5. Gerar camada Gold

```bash
python3 scripts/04-gold.py
```

---

## 🛠️ Tecnologias

| Ferramenta | Uso |
|---|---|
| Python 3.10+ | Orquestração e download |
| DuckDB | Processamento SQL local |
| Parquet | Formato de armazenamento colunar |
| Power BI | Consumo e visualização |

---

## 💡 Por que esse approach?

| | Power Query (atual) | Pipeline externo (proposta) |
|---|---|---|
| Onde fica a lógica | Dentro do Power BI | Em SQL versionado no Git |
| Performance | Reprocessa tudo ao abrir | Lê arquivo já processado |
| Manutenção | Difícil de auditar | SQL legível e documentado |
| Escalabilidade | Limitada pela memória do PBI | DuckDB processa bilhões de linhas |
| Custo | — | Zero — DuckDB é open source |