# Projeto Aplicado - Centros de Inovação

Sistema ETL (Extract, Transform, Load) desenvolvido em Python para migração automática de dados de planilhas Excel para banco de dados PostgreSQL.

## 📝 Sobre o Projeto

Este projeto implementa um processo completo de ETL que:
- **Extrai** dados de múltiplas abas de arquivos Excel (.xlsx)
- **Transforma** e normaliza dados com mapeamento inteligente de colunas
- **Carrega** dados no PostgreSQL respeitando dependências e integridade referencial

### ✨ Características Principais

- ✅ Mapeamento automático de colunas (case-insensitive, acento-insensitive)
- ✅ Conversão automática de tipos de dados
- ✅ Tratamento de Foreign Keys e dependências
- ✅ Validação de constraints e integridade referencial
- ✅ Tratamento robusto de erros e duplicatas
- ✅ Logging detalhado do processo
- ✅ Idempotente (pode ser executado múltiplas vezes sem duplicar dados)

### 🛠️ Tecnologias

- **Python 3.7+**
- **PostgreSQL**
- **pandas** - Manipulação de dados
- **psycopg2** - Conexão com PostgreSQL
- **openpyxl** - Leitura de arquivos Excel

## 📁 Estrutura do Projeto

### Arquivos Essenciais

- **`projeto_aplicado_final.xlsx`** - Planilha final com todos os dados prontos para inserção
- **`inserir_dados_banco.py`** - Script principal para inserção de dados no PostgreSQL
- **`config_banco.py`** - Configurações de conexão com o banco (edite com suas credenciais)
- **`SCRIPT_SQL_COMPLETO.sql`** - Script SQL completo para criar a estrutura do banco
- **`requirements.txt`** - Dependências Python do projeto
- **`GUIA_INSERCAO_DADOS.md`** - Guia completo de como inserir os dados

## 🚀 Como Usar

### 1. Configurar o Banco de Dados

1. Execute o script `SCRIPT_SQL_COMPLETO.sql` no pgAdmin4 para criar a estrutura do banco
2. Copie `config_banco.py.example` para `config_banco.py` e edite com suas credenciais do PostgreSQL
   ```bash
   cp config_banco.py.example config_banco.py
   # Ou no Windows:
   copy config_banco.py.example config_banco.py
   ```

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3. Inserir Dados

```bash
python inserir_dados_banco.py
```

O script irá:
- Procurar automaticamente por `projeto_aplicado_final.xlsx`
- Conectar ao PostgreSQL
- Inserir todos os dados na ordem correta (respeitando Foreign Keys)
- Mostrar progresso detalhado

## 📋 Requisitos

- Python 3.7+
- PostgreSQL (pgAdmin4)
- Bibliotecas: pandas, psycopg2-binary, openpyxl

## 📖 Documentação

- **`DOCUMENTACAO_PROCESSO_ETL.txt`** - 📚 **Documentação técnica completa** do processo ETL (Planilha → Transformação → Banco)
- **`GUIA_INSERCAO_DADOS.md`** - Guia prático de como inserir os dados
- **`QUERIES_UTEIS.sql`** - Queries SQL prontas para análise dos dados

