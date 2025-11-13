#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SCRIPT DE INSERÇÃO DE DADOS NO POSTGRESQL
Lê arquivo XLSX e insere todos os dados no banco PostgreSQL
Respeita a ordem de dependências (Foreign Keys)
"""

try:
    import pandas as pd
except ImportError as e:
    print("❌ Erro: pandas não está instalado!")
    print("   Execute: pip install pandas openpyxl")
    sys.exit(1)

try:
    import psycopg2
    from psycopg2 import sql
    from psycopg2.extras import execute_values
except ImportError as e:
    print("❌ Erro: psycopg2 não está instalado!")
    print("   Execute: pip install psycopg2-binary")
    sys.exit(1)

from pathlib import Path
from datetime import datetime
import sys
import os

# ============================================
# CONFIGURAÇÕES DE CONEXÃO
# ============================================
try:
    # Carregar config_banco.py de forma mais segura com encoding explícito
    import importlib.util
    import importlib.machinery
    
    config_path = os.path.join(os.path.dirname(__file__), 'config_banco.py')
    if os.path.exists(config_path):
        # Carregar com encoding UTF-8 explícito
        loader = importlib.machinery.SourceFileLoader("config_banco", config_path)
        spec = importlib.util.spec_from_loader("config_banco", loader)
        config_module = importlib.util.module_from_spec(spec)
        loader.exec_module(config_module)
        CONFIG_BANCO = config_module.CONFIG_BANCO
        print("✅ Configurações carregadas de config_banco.py")
    else:
        raise ImportError("config_banco.py não encontrado")
except (ImportError, AttributeError):
    # Se config_banco.py não existir, usar valores padrão
    print("⚠️  config_banco.py não encontrado, usando valores padrão")
    CONFIG_BANCO = {
        'host': 'localhost',
        'port': 5432,
        'database': 'centros_inovacao',
        'user': 'postgres',
        'password': ''  # ⚠️ CONFIGURE SUA SENHA AQUI ou crie config_banco.py
    }
except Exception as e:
    print(f"⚠️  Erro ao carregar config_banco.py: {e}")
    print("   Usando valores padrão...")
    # Usar valores padrão mesmo com erro
    CONFIG_BANCO = {
        'host': 'localhost',
        'port': 5432,
        'database': 'centros_inovacao',
        'user': 'postgres',
        'password': ''
    }

# ============================================
# MAPEAMENTO: ABA EXCEL → TABELA BANCO
# ============================================
MAPEAMENTO_ABAS = {
    'ESTADO': 'estado',
    'CIDADE': 'cidade',
    'BAIRRO': 'bairro',
    'TIPO_LOGRADOURO': 'tipo_logradouro',
    'ENDERECO': 'endereco',
    'TELEFONE': 'telefone',
    'CONTATO': 'contato',
    'CONTATO_TELEFONE': 'contato_telefone',
    'CENTROS_INOVACAO': 'centros_inovacao',
    'CENTROS_INOVACAO': 'centros_inovacao',  # Pode ter variação no nome
    'ENDERECO_CENTRO': 'endereco_centro',
    'ATOR': 'ator',
    'PROGRAMA': 'programa'
}

# Ordem de inserção (respeitando dependências de FK)
ORDEM_INSERCAO = [
    'estado',
    'cidade',
    'bairro',
    'tipo_logradouro',
    'endereco',
    'telefone',
    'contato',
    'contato_telefone',
    'centros_inovacao',
    'endereco_centro',
    'ator',
    'programa'
]

# ============================================
# FUNÇÕES AUXILIARES
# ============================================

def normalizar_nome_coluna(nome):
    """Normaliza nome de coluna para comparação (remove acentos, espaços, etc)"""
    import unicodedata
    import re
    
    nome = str(nome).strip()
    
    # Remover parênteses e conteúdo dentro (FK), (PK), etc
    nome = re.sub(r'\([^)]*\)', '', nome)
    
    # Converter para minúsculas
    nome = nome.lower()
    
    # Remover acentos
    nome = unicodedata.normalize('NFD', nome)
    nome = ''.join(char for char in nome if unicodedata.category(char) != 'Mn')
    
    # Substituir espaços, hífens, pontos por underscore
    nome = re.sub(r'[\s\-\.]+', '_', nome)
    
    # Remover FK, PK se estiver no início ou fim
    nome = re.sub(r'^fk_|_fk$|^pk_|_pk$', '', nome)
    nome = nome.replace('fk', '').replace('pk', '')
    
    # Remover underscores duplicados
    nome = re.sub(r'_+', '_', nome)
    
    # Remover underscores no início e fim
    nome = nome.strip('_')
    
    return nome

def encontrar_coluna(col_esperada, colunas_planilha):
    """Encontra coluna na planilha com variações de nome"""
    col_esperada_norm = normalizar_nome_coluna(col_esperada)
    
    # Primeiro: tentar match exato normalizado (mais confiável)
    matches_exatos = []
    for col in colunas_planilha:
        col_norm = normalizar_nome_coluna(col)
        if col_norm == col_esperada_norm:
            matches_exatos.append(col)
    
    if matches_exatos:
        # Se houver múltiplos matches exatos, preferir o mais curto (mais específico)
        return min(matches_exatos, key=len)
    
    # Segundo: tentar match por palavras principais (ignorar palavras comuns)
    palavras_comuns = {'id', 'fk', 'pk', 'de', 'da', 'do', 'em', 'no', 'na'}
    palavras_esperadas = set(p for p in col_esperada_norm.split('_') if p and p not in palavras_comuns)
    
    melhor_match = None
    melhor_score = 0
    
    for col in colunas_planilha:
        col_norm = normalizar_nome_coluna(col)
        palavras_col = set(p for p in col_norm.split('_') if p and p not in palavras_comuns)
        
        # Calcular score de similaridade
        palavras_iguais = palavras_esperadas.intersection(palavras_col)
        if palavras_iguais:
            score = len(palavras_iguais) / max(len(palavras_esperadas), len(palavras_col))
            # Bonus se todas as palavras esperadas estão presentes
            if palavras_esperadas.issubset(palavras_col):
                score += 0.5
            # Penalizar se a coluna é muito mais longa (pode ser uma coluna diferente)
            if len(col_norm) > len(col_esperada_norm) + 5:
                score *= 0.7
            if score > melhor_score:
                melhor_score = score
                melhor_match = col
    
    # Se encontrou um match bom (score > 0.7), retornar
    if melhor_match and melhor_score > 0.7:
        return melhor_match
    
    # Terceiro: tentar match parcial (contém) - mas com cuidado para não pegar colunas muito diferentes
    matches_parciais = []
    for col in colunas_planilha:
        col_norm = normalizar_nome_coluna(col)
        # Verificar se uma contém a outra
        if col_esperada_norm in col_norm:
            # Se a coluna da planilha contém a esperada, verificar se não é muito maior
            if len(col_norm) <= len(col_esperada_norm) + 8:  # Tolerância maior para "contém"
                matches_parciais.append((col, len(col_norm)))
        elif col_norm in col_esperada_norm:
            # Se a esperada contém a da planilha, preferir
            matches_parciais.append((col, len(col_norm)))
    
    if matches_parciais:
        # Preferir o match mais curto (mais específico)
        return min(matches_parciais, key=lambda x: x[1])[0]
    
    return None

def mapear_colunas_planilha_para_banco(df, colunas_banco, mostrar_debug=False):
    """Mapeia colunas da planilha para colunas do banco"""
    mapeamento = {}
    colunas_planilha = list(df.columns)
    
    # Criar dicionário de colunas normalizadas (sem espaços no final) para busca rápida
    colunas_planilha_normalizadas = {col.strip(): col for col in colunas_planilha}
    
    # Mapeamentos manuais para casos especiais
    mapeamentos_especiais = {
        'email': ['E-mail', 'E-mail ', 'email', 'Email', 'EMAIL', 'e-mail', 'E-Mail'],
        'codigo_area': ['Código_Area', 'Codigo_Area', 'codigo_area', 'Código Area', 'Codigo Area', 'Código_Área'],
        'id_tipo_logradouro': ['Id_Tipo_de_Logradouro', 'Id_Tipo_Logradouro', 'id_tipo_logradouro', 'Id_Tipo_de_Logradouro(FK)', 'Id_Tipo_Logradouro(FK)'],
        'id_endereco': ['Id_Endereço', 'Id_Endereco', 'id_endereco', 'Id_Endereço(FK)', 'Id_Endereco(FK)'],
        'ano_fundacao': ['Ano_Fundação', 'Ano_Fundacao', 'ano_fundacao', 'Ano Fundação', 'Ano_Fundacao'],
        'nome': ['Nome', 'Nome ', 'nome', 'NOME'],  # Tratar espaço no final
    }
    
    if mostrar_debug:
        print(f"   🔍 Colunas na planilha: {', '.join(colunas_planilha[:10])}{'...' if len(colunas_planilha) > 10 else ''}")
        print(f"   🔍 Colunas esperadas no banco: {', '.join(colunas_banco[:10])}{'...' if len(colunas_banco) > 10 else ''}")
    
    for col_banco in colunas_banco:
        col_planilha = None
        
        # Primeiro: tentar mapeamento especial
        if col_banco in mapeamentos_especiais:
            for variacao in mapeamentos_especiais[col_banco]:
                # Tentar match exato
                if variacao in colunas_planilha:
                    col_planilha = variacao
                    break
                # Tentar match sem espaços no final
                variacao_stripped = variacao.strip()
                if variacao_stripped in colunas_planilha_normalizadas:
                    col_planilha = colunas_planilha_normalizadas[variacao_stripped]
                    break
        
        # Segundo: tentar encontrar automaticamente (com normalização)
        if not col_planilha:
            col_planilha = encontrar_coluna(col_banco, colunas_planilha)
        
        # Terceiro: tentar match exato normalizado (sem espaços)
        if not col_planilha:
            col_banco_norm = normalizar_nome_coluna(col_banco)
            for col in colunas_planilha:
                if normalizar_nome_coluna(col) == col_banco_norm:
                    col_planilha = col
                    break
        
        if col_planilha:
            mapeamento[col_banco] = col_planilha
            if mostrar_debug:
                print(f"   ✅ '{col_banco}' → '{col_planilha}'")
        else:
            print(f"   ⚠️  Coluna '{col_banco}' não encontrada na planilha")
            if mostrar_debug:
                # Sugerir colunas similares
                col_banco_norm = normalizar_nome_coluna(col_banco)
                similares = [col for col in colunas_planilha 
                            if col_banco_norm[:3] in normalizar_nome_coluna(col) 
                            or normalizar_nome_coluna(col)[:3] in col_banco_norm]
                if similares:
                    print(f"      Sugestões: {', '.join(similares[:3])}")
    
    return mapeamento

def converter_data(valor):
    """Converte valor para data (DATE)"""
    if pd.isna(valor) or valor is None or valor == '':
        return None
    
    # Se já é datetime
    if isinstance(valor, (datetime, pd.Timestamp)):
        return valor.date() if hasattr(valor, 'date') else valor
    
    # Se é string, tentar parsear
    if isinstance(valor, str):
        try:
            # Tentar vários formatos
            for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d', '%d-%m-%Y']:
                try:
                    return datetime.strptime(valor, fmt).date()
                except:
                    continue
            # Se falhar, tentar parse automático do pandas
            return pd.to_datetime(valor).date()
        except:
            return None
    
    return None

def limpar_valor(valor, tipo='VARCHAR'):
    """Limpa e converte valor conforme tipo do banco"""
    if pd.isna(valor) or valor is None:
        return None
    
    # Converter para string e limpar
    valor_str = str(valor).strip()
    
    if valor_str == '' or valor_str.lower() in ['nan', 'none', 'null']:
        return None
    
    # Tratamento por tipo
    if 'DATE' in tipo.upper():
        return converter_data(valor)
    elif 'INTEGER' in tipo.upper() or 'INT' in tipo.upper():
        try:
            return int(float(valor_str))
        except:
            return None
    elif 'CHAR' in tipo.upper() and 'VARCHAR' not in tipo.upper():
        # CHAR fixo - remover espaços extras
        return valor_str[:int(tipo.split('(')[1].split(')')[0])] if '(' in tipo else valor_str
    else:
        return valor_str

def obter_colunas_tabela(conn, nome_tabela):
    """Obtém lista de colunas de uma tabela com informações de NOT NULL"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT column_name, data_type, character_maximum_length, is_nullable
            FROM information_schema.columns
            WHERE table_name = %s
            ORDER BY ordinal_position
        """, (nome_tabela,))
        
        colunas = []
        for row in cursor.fetchall():
            col_name = row[0]
            data_type = row[1]
            max_length = row[2]
            is_nullable = row[3]  # 'YES' ou 'NO'
            
            tipo_completo = data_type
            if max_length:
                tipo_completo = f"{data_type}({max_length})"
            
            colunas.append({
                'nome': col_name,
                'tipo': tipo_completo,
                'not_null': (is_nullable == 'NO')  # True se NOT NULL
            })
        
        cursor.close()
        return colunas
    except Exception as e:
        print(f"   ❌ Erro ao obter colunas: {e}")
        return []

def obter_pk_tabela(conn, nome_tabela):
    """Obtém o nome da coluna PK de uma tabela"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.attname
            FROM pg_index i
            JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)
            WHERE i.indrelid = %s::regclass
            AND i.indisprimary
        """, (nome_tabela,))
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else None
    except:
        return None

def inserir_dados_tabela(conn, nome_tabela, df, mapeamento_colunas):
    """Insere dados de um DataFrame na tabela"""
    try:
        # Obter colunas do banco
        colunas_banco = obter_colunas_tabela(conn, nome_tabela)
        nomes_colunas_banco = [c['nome'] for c in colunas_banco]
        tipos_colunas = {c['nome']: c['tipo'] for c in colunas_banco}
        
        # Obter PK para verificar duplicatas
        pk_coluna = obter_pk_tabela(conn, nome_tabela)
        
        # Filtrar apenas colunas que existem no banco e foram mapeadas
        colunas_para_inserir = []
        colunas_not_null = []  # Colunas que são realmente NOT NULL no banco
        
        for col_info in colunas_banco:
            col_banco = col_info['nome']
            if col_banco in mapeamento_colunas:
                colunas_para_inserir.append(col_banco)
                # Verificar se é NOT NULL no banco (não assumir, verificar de verdade)
                if col_info.get('not_null', False):
                    colunas_not_null.append(col_banco)
        
        if not colunas_para_inserir:
            print(f"   ⚠️  Nenhuma coluna mapeada para inserir")
            return 0
        
        # Verificar se PK está mapeada
        if pk_coluna and pk_coluna not in mapeamento_colunas:
            print(f"   ⚠️  Coluna PK '{pk_coluna}' não encontrada na planilha!")
            return 0
        
        # Preparar dados
        dados_para_inserir = []
        registros_ignorados = 0
        
        for idx, row in df.iterrows():
            valores = []
            valores_dict = {}
            tem_null_obrigatorio = False
            
            for col_banco in colunas_para_inserir:
                col_planilha = mapeamento_colunas[col_banco]
                # Garantir que a coluna existe no DataFrame (pode ter espaços)
                if col_planilha in row:
                    valor = row[col_planilha]
                elif col_planilha.strip() in df.columns:
                    # Tentar com strip se a coluna tiver espaços
                    col_planilha_stripped = col_planilha.strip()
                    mapeamento_colunas[col_banco] = col_planilha_stripped  # Atualizar mapeamento
                    valor = row[col_planilha_stripped] if col_planilha_stripped in row else None
                else:
                    valor = None
                tipo = tipos_colunas[col_banco]
                valor_limpo = limpar_valor(valor, tipo)
                
                # Verificar se campo obrigatório está NULL
                if col_banco in colunas_not_null and valor_limpo is None:
                    tem_null_obrigatorio = True
                
                valores.append(valor_limpo)
                valores_dict[col_banco] = valor_limpo
            
            # Ignorar registros com NULL em campos obrigatórios
            if tem_null_obrigatorio:
                registros_ignorados += 1
                # Mostrar detalhes apenas dos primeiros 3 registros ignorados
                if registros_ignorados <= 3:
                    campos_null = [col for col in colunas_not_null 
                                  if col in valores_dict and valores_dict[col] is None]
                    if campos_null:
                        print(f"      ⚠️  Linha {idx+1} ignorada: campos obrigatórios NULL: {', '.join(campos_null[:3])}")
                continue
            
            dados_para_inserir.append(tuple(valores))
        
        if registros_ignorados > 0:
            print(f"   ⚠️  {registros_ignorados} registros ignorados (campos obrigatórios NULL)")
        
        if not dados_para_inserir:
            print(f"   ⚠️  Nenhum registro válido para inserir")
            return 0
        
        # Inserir usando execute_values (mais eficiente)
        cursor = conn.cursor()
        
        # Construir query INSERT com ON CONFLICT para evitar duplicatas
        colunas_str = ', '.join([f'"{col}"' for col in colunas_para_inserir])
        
        # Se tem PK, usar ON CONFLICT na PK
        if pk_coluna and pk_coluna in colunas_para_inserir:
            query = f"""
                INSERT INTO {nome_tabela} ({colunas_str})
                VALUES %s
                ON CONFLICT ({pk_coluna}) DO NOTHING
            """
        else:
            query = f"""
                INSERT INTO {nome_tabela} ({colunas_str})
                VALUES %s
                ON CONFLICT DO NOTHING
            """
        
        execute_values(
            cursor,
            query,
            dados_para_inserir,
            template=None,
            page_size=1000
        )
        
        linhas_inseridas = cursor.rowcount
        conn.commit()
        cursor.close()
        
        return linhas_inseridas
        
    except psycopg2.IntegrityError as e:
        conn.rollback()
        # Erro de integridade (FK, unique, etc)
        error_msg = str(e)
        print(f"   ❌ Erro de integridade: {error_msg[:150]}")
        # Tentar inserir linha por linha para identificar o problema
        print(f"   🔍 Tentando inserir individualmente para identificar o problema...")
        return inserir_individualmente(conn, nome_tabela, df, mapeamento_colunas, colunas_banco, pk_coluna)
    except Exception as e:
        conn.rollback()
        print(f"   ❌ Erro ao inserir dados: {e}")
        import traceback
        traceback.print_exc()
        raise

def inserir_individualmente(conn, nome_tabela, df, mapeamento_colunas, colunas_banco, pk_coluna=None):
    """Insere dados linha por linha para identificar problemas"""
    tipos_colunas = {c['nome']: c['tipo'] for c in colunas_banco}
    nomes_colunas_banco = [c['nome'] for c in colunas_banco]
    colunas_para_inserir = [col for col in nomes_colunas_banco if col in mapeamento_colunas]
    
    linhas_inseridas = 0
    linhas_erro = 0
    linhas_duplicadas = 0
    
    colunas_str = ', '.join([f'"{col}"' for col in colunas_para_inserir])
    
    # Construir ON CONFLICT
    if pk_coluna and pk_coluna in colunas_para_inserir:
        conflict_clause = f"ON CONFLICT ({pk_coluna}) DO NOTHING"
    else:
        conflict_clause = "ON CONFLICT DO NOTHING"
    
    for idx, row in df.iterrows():
        # Criar novo cursor para cada tentativa (evita problemas de transação)
        cursor = conn.cursor()
        try:
            valores = []
            for col_banco in colunas_para_inserir:
                col_planilha = mapeamento_colunas[col_banco]
                # Garantir que a coluna existe no DataFrame (pode ter espaços)
                if col_planilha in row:
                    valor = row[col_planilha]
                elif col_planilha.strip() in df.columns:
                    # Tentar com strip se a coluna tiver espaços
                    col_planilha_stripped = col_planilha.strip()
                    mapeamento_colunas[col_banco] = col_planilha_stripped  # Atualizar mapeamento
                    valor = row[col_planilha_stripped] if col_planilha_stripped in row else None
                else:
                    valor = None
                tipo = tipos_colunas[col_banco]
                valor_limpo = limpar_valor(valor, tipo)
                valores.append(valor_limpo)
            
            placeholders = ', '.join(['%s'] * len(valores))
            query = f"""
                INSERT INTO {nome_tabela} ({colunas_str})
                VALUES ({placeholders})
                {conflict_clause}
            """
            
            cursor.execute(query, valores)
            conn.commit()  # Commit após cada inserção bem-sucedida
            
            if cursor.rowcount > 0:
                linhas_inseridas += 1
            else:
                linhas_duplicadas += 1
            cursor.close()
            
        except psycopg2.IntegrityError as e:
            conn.rollback()  # Rollback em caso de erro
            cursor.close()
            linhas_erro += 1
            error_msg = str(e)
            if linhas_erro <= 5:  # Mostrar apenas os 5 primeiros erros
                print(f"      ⚠️  Linha {idx+1}: {error_msg[:120]}")
            continue
        except Exception as e:
            conn.rollback()  # Rollback em caso de erro
            cursor.close()
            linhas_erro += 1
            if linhas_erro <= 5:
                print(f"      ⚠️  Linha {idx+1}: {str(e)[:120]}")
            continue
    
    if linhas_duplicadas > 0:
        print(f"   ℹ️  {linhas_duplicadas} registros já existiam (duplicatas ignoradas)")
    if linhas_erro > 0:
        print(f"   ⚠️  {linhas_erro} registros com erro (FKs inválidas ou outros problemas)")
    
    return linhas_inseridas

# ============================================
# FUNÇÃO PRINCIPAL
# ============================================

def analisar_planilha_detalhadamente(arquivo_excel):
    """Analisa a planilha em detalhes para entender estrutura"""
    print("=" * 100)
    print("ANÁLISE DETALHADA DA PLANILHA")
    print("=" * 100)
    print()
    
    try:
        abas_excel = pd.read_excel(arquivo_excel, sheet_name=None, engine='openpyxl')
        
        for sheet_name in abas_excel.keys():
            df = abas_excel[sheet_name]
            print(f"\n{'='*100}")
            print(f"ABA: {sheet_name}")
            print(f"{'='*100}")
            print(f"📏 Dimensões: {len(df)} linhas × {len(df.columns)} colunas")
            print(f"\n📝 COLUNAS EXATAS ({len(df.columns)}):")
            for i, col in enumerate(df.columns, 1):
                # Contar valores não nulos
                na_count = df[col].isna().sum()
                not_na = len(df) - na_count
                pct = (not_na / len(df) * 100) if len(df) > 0 else 0
                print(f"   {i:2d}. {repr(col):60s} | Não-nulos: {not_na:4d}/{len(df)} ({pct:5.1f}%)")
            
            print(f"\n📊 PRIMEIRAS 3 LINHAS (valores reais):")
            for idx in range(min(3, len(df))):
                print(f"\n   Linha {idx+1}:")
                for col in df.columns:
                    valor = df.iloc[idx][col]
                    if pd.isna(valor):
                        print(f"      {col:50s} → NULL")
                    else:
                        valor_str = str(valor)[:50]
                        print(f"      {col:50s} → {valor_str}")
            
            print(f"\n🔍 TIPOS DE DADOS:")
            for col in df.columns:
                dtype = df[col].dtype
                print(f"   {col:50s} → {str(dtype):20s}")
        
        print("\n" + "=" * 100)
        return abas_excel
        
    except Exception as e:
        print(f"❌ Erro ao analisar planilha: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    # Garantir que estamos no diretório correto
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    
    print("=" * 100)
    print("INSERÇÃO DE DADOS NO POSTGRESQL")
    print("=" * 100)
    print(f"📁 Diretório de trabalho: {script_dir}")
    print()
    
    # 1. Encontrar arquivo Excel
    print("📂 Procurando arquivo Excel...")
    arquivo_excel = None
    
    # Prioridade: FINAL > SEM_DUPLICATAS > CORRIGIDO > COM_FKs_CORRETAS
    for f in Path('.').glob('*.xlsx'):
        nome_upper = f.name.upper()
        if 'FINAL' in nome_upper:
            arquivo_excel = str(f)
            break
        elif 'SEM_DUPLICATAS' in nome_upper and arquivo_excel is None:
            arquivo_excel = str(f)
        elif 'CORRIGIDO' in nome_upper and arquivo_excel is None:
            arquivo_excel = str(f)
        elif 'COM_FKs_CORRETAS' in nome_upper and arquivo_excel is None:
            arquivo_excel = str(f)
    
    if not arquivo_excel:
        print("❌ Arquivo Excel não encontrado!")
        print("   Procurando por: *FINAL.xlsx, *SEM_DUPLICATAS.xlsx, *CORRIGIDO.xlsx ou *COM_FKs_CORRETAS*.xlsx")
        return
    
    print(f"✅ Arquivo encontrado: {arquivo_excel}")
    print()
    
    # 2. ANALISAR PLANILHA PRIMEIRO
    print("🔍 Analisando estrutura da planilha...")
    abas_excel = analisar_planilha_detalhadamente(arquivo_excel)
    
    if abas_excel is None:
        print("❌ Erro ao ler arquivo Excel")
        return
    
    print(f"\n✅ {len(abas_excel)} abas carregadas: {', '.join(abas_excel.keys())}")
    print()
    
    # 3. Conectar ao banco
    print("🔌 Conectando ao PostgreSQL...")
    print(f"   Host: {CONFIG_BANCO['host']}")
    print(f"   Port: {CONFIG_BANCO['port']}")
    print(f"   Database: {CONFIG_BANCO['database']}")
    print(f"   User: {CONFIG_BANCO['user']}")
    print(f"   Password: {'*' * len(str(CONFIG_BANCO['password'])) if CONFIG_BANCO['password'] else '(vazia)'}")
    print()
    
    try:
        # Converter todos os valores para strings seguras (ASCII quando possível)
        def garantir_string_segura(valor):
            """Converte valor para string segura para conexão"""
            if valor is None:
                return ''
            if isinstance(valor, (int, float)):
                return str(valor)
            if isinstance(valor, bytes):
                try:
                    return valor.decode('utf-8', errors='replace')
                except:
                    return valor.decode('latin-1', errors='replace')
            if isinstance(valor, str):
                # Tentar garantir que é UTF-8 válido
                try:
                    # Testar se pode codificar em UTF-8
                    valor.encode('utf-8')
                    return valor
                except UnicodeEncodeError:
                    # Se não conseguir, usar replace para substituir caracteres problemáticos
                    return valor.encode('utf-8', errors='replace').decode('utf-8', errors='replace')
            return str(valor)
        
        # Preparar parâmetros de conexão
        host = garantir_string_segura(CONFIG_BANCO['host'])
        database = garantir_string_segura(CONFIG_BANCO['database'])
        user = garantir_string_segura(CONFIG_BANCO['user'])
        password = garantir_string_segura(CONFIG_BANCO['password'])
        port = int(CONFIG_BANCO['port'])
        
        # Conectar usando parâmetros nomeados (mais seguro que DSN string)
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            client_encoding='UTF8'
        )
        print(f"✅ Conectado ao banco: {database}@{host}")
        print()
    except psycopg2.OperationalError as e:
        print(f"❌ Erro de conexão com o banco:")
        print(f"   {e}")
        print()
        print("💡 Possíveis causas:")
        print("   1. Servidor PostgreSQL não está rodando")
        print("   2. Credenciais incorretas em config_banco.py")
        print("   3. Banco de dados 'centros_inovacao' não existe")
        print("   4. Firewall bloqueando a conexão")
        print()
        print("🔧 Soluções:")
        print("   • Verifique se o PostgreSQL está rodando (serviço Windows)")
        print("   • Confirme as credenciais no pgAdmin4")
        print("   • Crie o banco se não existir: CREATE DATABASE centros_inovacao;")
        return
    except Exception as e:
        print(f"❌ Erro inesperado ao conectar: {e}")
        print(f"   Tipo do erro: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return
    
    # 4. Inserir dados na ordem correta
    print("=" * 100)
    print("INICIANDO INSERÇÃO DE DADOS")
    print("=" * 100)
    print()
    
    total_inserido = 0
    tabelas_processadas = []
    tabelas_erro = []
    
    try:
        for tabela_banco in ORDEM_INSERCAO:
            # Encontrar aba correspondente
            aba_encontrada = None
            for aba_excel, tab_banco in MAPEAMENTO_ABAS.items():
                if tab_banco == tabela_banco:
                    # Tentar encontrar a aba (case-insensitive)
                    for aba_real in abas_excel.keys():
                        if aba_real.upper() == aba_excel.upper():
                            aba_encontrada = aba_real
                            break
                    if aba_encontrada:
                        break
            
            if not aba_encontrada:
                print(f"⏭️  {tabela_banco}: Aba não encontrada no Excel (pulando)")
                continue
            
            df = abas_excel[aba_encontrada].copy()
            
            if df.empty:
                print(f"⏭️  {tabela_banco}: Aba vazia (pulando)")
                continue
            
            print(f"📊 {tabela_banco} (aba: {aba_encontrada})")
            print(f"   Registros na planilha: {len(df)}")
            
            # Mapear colunas
            colunas_banco = [c['nome'] for c in obter_colunas_tabela(conn, tabela_banco)]
            
            # Mostrar debug apenas se houver erro anterior ou se for tabela problemática
            tabelas_problematicas = ['endereco', 'contato', 'contato_telefone', 'centros_inovacao', 
                                    'endereco_centro', 'ator', 'programa']
            mostrar_debug = tabela_banco in tabelas_problematicas or tabela_banco in tabelas_erro
            
            mapeamento = mapear_colunas_planilha_para_banco(df, colunas_banco, mostrar_debug=mostrar_debug)
            
            if not mapeamento:
                print(f"   ⚠️  Nenhuma coluna mapeada (pulando)")
                print(f"   💡 Colunas disponíveis na planilha: {', '.join(list(df.columns)[:15])}")
                continue
            
            # Inserir dados
            try:
                linhas_inseridas = inserir_dados_tabela(conn, tabela_banco, df, mapeamento)
                print(f"   ✅ {linhas_inseridas} registros inseridos")
                total_inserido += linhas_inseridas
                tabelas_processadas.append(tabela_banco)
            except Exception as e:
                print(f"   ❌ Erro: {e}")
                tabelas_erro.append(tabela_banco)
            
            print()
        
        # Resumo final
        print("=" * 100)
        print("RESUMO DA INSERÇÃO")
        print("=" * 100)
        print(f"✅ Tabelas processadas: {len(tabelas_processadas)}")
        print(f"   {', '.join(tabelas_processadas)}")
        if tabelas_erro:
            print(f"❌ Tabelas com erro: {len(tabelas_erro)}")
            print(f"   {', '.join(tabelas_erro)}")
        print(f"📊 Total de registros inseridos: {total_inserido}")
        print()
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        conn.rollback()
    finally:
        conn.close()
        print("✅ Conexão fechada")

if __name__ == "__main__":
    # Verificar se senha foi configurada
    if not CONFIG_BANCO['password']:
        print("⚠️  ATENÇÃO: Configure a senha do banco na linha 20 do script!")
        print("   CONFIG_BANCO['password'] = 'sua_senha_aqui'")
        print()
        resposta = input("Deseja continuar mesmo assim? (s/n): ").lower().strip()
        if resposta not in ['s', 'sim', 'y', 'yes']:
            sys.exit(0)
    
    main()

