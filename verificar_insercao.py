"""
Script para verificar se os dados foram inseridos corretamente no banco
"""
import psycopg2
import sys
import os
import importlib.util
import importlib.machinery

# Carregar configurações
try:
    config_path = os.path.join(os.path.dirname(__file__), 'config_banco.py')
    if os.path.exists(config_path):
        loader = importlib.machinery.SourceFileLoader("config_banco", config_path)
        spec = importlib.util.spec_from_loader("config_banco", loader)
        config_module = importlib.util.module_from_spec(spec)
        loader.exec_module(config_module)
        CONFIG_BANCO = config_module.CONFIG_BANCO
    else:
        print("❌ config_banco.py não encontrado!")
        sys.exit(1)
except Exception as e:
    print(f"❌ Erro ao carregar config: {e}")
    sys.exit(1)

# Tabelas esperadas
TABELAS = [
    'estado', 'cidade', 'bairro', 'tipo_logradouro', 'endereco',
    'telefone', 'contato', 'contato_telefone', 'centros_inovacao',
    'endereco_centro', 'ator', 'programa'
]

print("=" * 80)
print("VERIFICAÇÃO DE INSERÇÃO DE DADOS")
print("=" * 80)
print()

try:
    # Conectar ao banco
    conn = psycopg2.connect(
        host=CONFIG_BANCO['host'],
        port=CONFIG_BANCO['port'],
        database=CONFIG_BANCO['database'],
        user=CONFIG_BANCO['user'],
        password=CONFIG_BANCO['password']
    )
    
    cursor = conn.cursor()
    
    total_registros = 0
    tabelas_com_dados = []
    tabelas_vazias = []
    
    print("📊 Verificando registros em cada tabela:\n")
    
    for tabela in TABELAS:
        try:
            cursor.execute(f'SELECT COUNT(*) FROM {tabela}')
            count = cursor.fetchone()[0]
            total_registros += count
            
            if count > 0:
                tabelas_com_dados.append((tabela, count))
                print(f"   ✅ {tabela:25s} → {count:5d} registros")
            else:
                tabelas_vazias.append(tabela)
                print(f"   ⚠️  {tabela:25s} → {count:5d} registros (VAZIA)")
        except Exception as e:
            print(f"   ❌ {tabela:25s} → ERRO: {e}")
    
    print()
    print("=" * 80)
    print("RESUMO")
    print("=" * 80)
    print(f"📊 Total de registros no banco: {total_registros:,}")
    print(f"✅ Tabelas com dados: {len(tabelas_com_dados)}/{len(TABELAS)}")
    
    if tabelas_vazias:
        print(f"⚠️  Tabelas vazias: {', '.join(tabelas_vazias)}")
    
    print()
    
    if total_registros > 0:
        print("🎉 SUCESSO! Dados foram inseridos no banco!")
    else:
        print("⚠️  ATENÇÃO: Nenhum dado encontrado no banco.")
        print("   Execute o script inserir_dados_banco.py primeiro.")
    
    cursor.close()
    conn.close()
    
except psycopg2.Error as e:
    print(f"❌ Erro ao conectar ao banco: {e}")
    sys.exit(1)

