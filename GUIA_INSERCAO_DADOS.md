# 📥 Guia de Inserção de Dados no PostgreSQL

Este guia explica como inserir os dados da planilha Excel no banco PostgreSQL.

---

## 📋 **Formato Recomendado: XLSX** ✅

**Recomendamos usar XLSX** porque:
- ✅ Um único arquivo com todas as abas
- ✅ Mantém a estrutura organizada
- ✅ Fácil de processar com Python/pandas
- ✅ Não precisa converter nada

**CSV também funciona**, mas:
- ⚠️ Precisa de um arquivo CSV para cada aba/tabela
- ⚠️ Mais trabalhoso de gerenciar
- ⚠️ Pode perder formatação de datas

---

## 🚀 **Como Usar o Script de Inserção**

### **Passo 1: Configurar Credenciais**

Edite o arquivo `config_banco.py` com suas credenciais do PostgreSQL:

```python
CONFIG_BANCO = {
    'host': 'localhost',
    'port': 5432,
    'database': 'centros_inovacao',
    'user': 'postgres',
    'password': 'sua_senha_aqui'  # ⚠️ COLOQUE SUA SENHA
}
```

**Como obter as credenciais no pgAdmin4:**
1. Clique com botão direito no servidor PostgreSQL
2. Selecione "Properties" (Propriedades)
3. Vá na aba "Connection" (Conexão)
4. Copie as informações

### **Passo 2: Preparar a Planilha**

Certifique-se de que sua planilha Excel:
- ✅ Tem todas as abas necessárias
- ✅ Está salva como `.xlsx`
- ✅ Não tem duplicatas (use o script `remover_atores_duplicados_mesmo_centro.py` se necessário)
- ✅ Está no mesmo diretório do script

**Prioridade de arquivos (o script procura nesta ordem):**
1. `*FINAL.xlsx` (planilha final - maior prioridade)
2. `*SEM_DUPLICATAS.xlsx`
3. `*CORRIGIDO.xlsx`
4. `*COM_FKs_CORRETAS*.xlsx`

### **Passo 3: Executar o Script**

```bash
python inserir_dados_banco.py
```

O script irá:
1. ✅ Procurar o arquivo Excel automaticamente
2. ✅ Conectar ao banco PostgreSQL
3. ✅ Ler todas as abas
4. ✅ Mapear colunas automaticamente (case-insensitive)
5. ✅ Inserir dados na ordem correta (respeitando FKs)
6. ✅ Mostrar progresso e estatísticas

---

## 📊 **Ordem de Inserção**

O script insere os dados nesta ordem (respeitando dependências):

1. `estado` (sem dependências)
2. `cidade` (depende de estado)
3. `bairro` (depende de cidade)
4. `tipo_logradouro` (sem dependências)
5. `endereco` (depende de tipo_logradouro e bairro)
6. `telefone` (sem dependências)
7. `contato` (depende de telefone)
8. `contato_telefone` (N-N, depende de contato e telefone)
9. `centros_inovacao` (depende de contato)
10. `endereco_centro` (N-N, depende de endereco e centros_inovacao)
11. `ator` (depende de centros_inovacao)
12. `programa` (depende de ator)

---

## 🔍 **Mapeamento de Abas**

O script mapeia automaticamente as abas do Excel para as tabelas do banco:

| Aba Excel | Tabela Banco |
|-----------|--------------|
| ESTADO | estado |
| CIDADE | cidade |
| BAIRRO | bairro |
| TIPO_LOGRADOURO | tipo_logradouro |
| ENDERECO | endereco |
| TELEFONE | telefone |
| CONTATO | contato |
| CONTATO_TELEFONE | contato_telefone |
| CENTROS_INOVACAO | centros_inovacao |
| ENDERECO_CENTRO | endereco_centro |
| ATOR | ator |
| PROGRAMA | programa |

**Nota:** O mapeamento é case-insensitive (não diferencia maiúsculas/minúsculas).

---

## 🛠️ **Tratamento Automático**

O script trata automaticamente:

- ✅ **Nomes de colunas**: Mapeia variações (ex: `Id_Ator`, `id_ator`, `Id_Ator(PK)`)
- ✅ **Datas**: Converte vários formatos para DATE do PostgreSQL
- ✅ **Valores nulos**: Trata `NaN`, `None`, strings vazias
- ✅ **Tipos de dados**: Converte conforme tipo da coluna no banco
- ✅ **Duplicatas**: Usa `ON CONFLICT DO NOTHING` (não insere duplicatas)

---

## ⚠️ **Tratamento de Erros**

Se houver erro:

1. **Erro de conexão**: Verifique `config_banco.py`
2. **Erro de coluna não encontrada**: Verifique se os nomes das colunas na planilha correspondem ao esperado
3. **Erro de Foreign Key**: Verifique se os dados estão na ordem correta e se as FKs existem
4. **Erro de tipo de dado**: O script tenta converter automaticamente, mas alguns valores podem precisar de ajuste manual

---

## 📈 **Exemplo de Saída**

```
====================================================================================================
INSERÇÃO DE DADOS NO POSTGRESQL
====================================================================================================

📂 Procurando arquivo Excel...
✅ Arquivo encontrado: projeto_aplicado_SEM_DUPLICATAS.xlsx

📖 Lendo arquivo Excel...
✅ 12 abas encontradas: ESTADO, CIDADE, BAIRRO, ...

🔌 Conectando ao PostgreSQL...
✅ Conectado ao banco: centros_inovacao@localhost

====================================================================================================
INICIANDO INSERÇÃO DE DADOS
====================================================================================================

📊 estado (aba: ESTADO)
   Registros na planilha: 27
   ✅ 27 registros inseridos

📊 cidade (aba: CIDADE)
   Registros na planilha: 150
   ✅ 150 registros inseridos

...

====================================================================================================
RESUMO DA INSERÇÃO
====================================================================================================
✅ Tabelas processadas: 12
   estado, cidade, bairro, tipo_logradouro, endereco, telefone, contato, contato_telefone, centros_inovacao, endereco_centro, ator, programa
📊 Total de registros inseridos: 1.234

✅ Conexão fechada
```

---

## 💡 **Dicas**

1. **Faça backup do banco** antes de inserir dados
2. **Teste com poucos dados** primeiro (crie uma planilha de teste)
3. **Verifique os logs** se houver erros
4. **Use transações**: O script usa transações, então se houver erro, nada é inserido

---

## 🔄 **Se Preferir CSV**

Se você realmente quiser usar CSV:

1. Exporte cada aba do Excel como CSV separado
2. Nomeie os arquivos: `estado.csv`, `cidade.csv`, etc.
3. Modifique o script para ler CSV em vez de XLSX (substitua `pd.read_excel` por `pd.read_csv`)

Mas **recomendamos XLSX** porque é mais simples! 😊

