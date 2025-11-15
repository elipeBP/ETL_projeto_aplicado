#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para gerar dicionário de dados completo baseado nas respostas do questionário
"""
import json
import os
from datetime import datetime

def carregar_respostas():
    """Carrega as respostas do questionário"""
    arquivo = "respostas_dicionario_dados.json"
    if not os.path.exists(arquivo):
        print(f"❌ Arquivo {arquivo} não encontrado!")
        print("💡 Execute primeiro: python coletar_dicionario_dados.py")
        return None
    
    with open(arquivo, 'r', encoding='utf-8') as f:
        return json.load(f)

def gerar_dicionario(respostas):
    """Gera o dicionário de dados completo"""
    
    # Ler estrutura do banco
    estrutura_banco = {
        "estado": {
            "id_estado": "Chave primária da tabela estado",
            "nome": "Nome completo do estado",
            "sigla": "Sigla do estado (ex: SC, SP, RJ)"
        },
        "cidade": {
            "id_cidade": "Chave primária da tabela cidade",
            "nome": "Nome da cidade",
            "id_estado": "Chave estrangeira para estado"
        },
        "bairro": {
            "id_bairro": "Chave primária da tabela bairro",
            "nome": "Nome do bairro",
            "id_cidade": "Chave estrangeira para cidade"
        },
        "tipo_logradouro": {
            "id_tipo_de_logradouro": "Chave primária da tabela tipo_logradouro",
            "nome": "Nome do tipo de logradouro (Rua, Avenida, etc.)"
        },
        "endereco": {
            "id_endereco": "Chave primária da tabela endereco",
            "nome_logradouro": "Nome do logradouro",
            "numero": "Número do endereço",
            "id_tipo_logradouro": "Chave estrangeira para tipo de logradouro",
            "id_bairro": "Chave estrangeira para bairro"
        },
        "telefone": {
            "id_telefone": "Chave primária da tabela telefone",
            "codigo_area": "Código de área (ex: 47, 48)",
            "numero": "Número do telefone"
        },
        "contato": {
            "id_contato": "Chave primária da tabela contato",
            "email": "Email de contato",
            "id_telefone": "Chave estrangeira para telefone"
        },
        "contato_telefone": {
            "id_contato_telefone": "Chave primária da tabela contato_telefone",
            "id_contato": "Chave estrangeira para contato",
            "id_telefone": "Chave estrangeira para telefone"
        },
        "centros_inovacao": {
            "id_centro": "Chave primária da tabela centros_inovacao",
            "nome": "Nome do centro de inovação",
            "ano_fundacao": "Ano de fundação do centro",
            "id_contato": "Chave estrangeira para contato"
        },
        "endereco_centro": {
            "id_endereco_centro": "Chave primária da tabela endereco_centro",
            "id_endereco": "Chave estrangeira para endereço",
            "id_centro": "Chave estrangeira para centro de inovação"
        },
        "ator": {
            "id_ator": "Chave primária da tabela ator",
            "nome": "Nome do ator",
            "tipo_ator": "Tipo do ator",
            "participa_programa": "Se participa de programas (Sim/Não)",
            "tamanho_ator": "Tamanho do ator",
            "cnpj": "CNPJ do ator",
            "id_centro": "Chave estrangeira para centro de inovação"
        },
        "programa": {
            "id_programa": "Chave primária da tabela programa",
            "nome": "Nome do programa",
            "ano_inicio": "Ano de início do programa",
            "descricao": "Descrição detalhada do programa",
            "id_ator": "Chave estrangeira para ator"
        }
    }
    
    # Construir dicionário de dados
    dicionario = []
    dicionario.append("=" * 80)
    dicionario.append("DICIONÁRIO DE DADOS")
    dicionario.append("Sistema de Gestão de Centros de Inovação")
    dicionario.append("=" * 80)
    dicionario.append("")
    dicionario.append(f"Data de criação: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    dicionario.append("")
    dicionario.append("=" * 80)
    dicionario.append("1. INTRODUÇÃO")
    dicionario.append("=" * 80)
    dicionario.append("")
    dicionario.append("Este dicionário de dados descreve todas as tabelas, colunas e")
    dicionario.append("conceitos do sistema de gestão de centros de inovação.")
    dicionario.append("")
    
    if respostas.get("secao1_conceitos_gerais", {}).get("centro_inovacao"):
        dicionario.append("DEFINIÇÃO DE CENTRO DE INOVAÇÃO:")
        dicionario.append(respostas["secao1_conceitos_gerais"]["centro_inovacao"])
        dicionario.append("")
    
    if respostas.get("secao1_conceitos_gerais", {}).get("objetivo_sistema"):
        dicionario.append("OBJETIVO DO SISTEMA:")
        dicionario.append(respostas["secao1_conceitos_gerais"]["objetivo_sistema"])
        dicionario.append("")
    
    dicionario.append("=" * 80)
    dicionario.append("2. GLOSSÁRIO DE TERMOS")
    dicionario.append("=" * 80)
    dicionario.append("")
    
    # Glossário
    termos = []
    
    if respostas.get("secao2_atores", {}).get("definicao_ator"):
        termos.append(("ATOR", respostas["secao2_atores"]["definicao_ator"]))
    
    if respostas.get("secao2_atores", {}).get("empresa_incubada"):
        termos.append(("EMPRESA INCUBADA", respostas["secao2_atores"]["empresa_incubada"]))
    
    if respostas.get("secao3_programas", {}).get("definicao_programa"):
        termos.append(("PROGRAMA", respostas["secao3_programas"]["definicao_programa"]))
    
    if respostas.get("secao4_centros", {}).get("ano_fundacao"):
        termos.append(("ANO DE FUNDAÇÃO", respostas["secao4_centros"]["ano_fundacao"]))
    
    for termo, definicao in termos:
        dicionario.append(f"{termo}:")
        dicionario.append(f"  {definicao}")
        dicionario.append("")
    
    # Tipos de atores
    if respostas.get("secao2_atores", {}).get("tipos_ator"):
        dicionario.append("TIPOS DE ATORES:")
        for tipo in respostas["secao2_atores"]["tipos_ator"]:
            dicionario.append(f"  - {tipo.get('item', '')}: {tipo.get('definicao', '')}")
        dicionario.append("")
    
    # Tamanhos de atores
    if respostas.get("secao2_atores", {}).get("tamanho_ator"):
        dicionario.append("TAMANHOS DE ATORES:")
        for tamanho in respostas["secao2_atores"]["tamanho_ator"]:
            dicionario.append(f"  - {tamanho.get('item', '')}: {tamanho.get('definicao', '')}")
        dicionario.append("")
    
    # Tipos de programas
    if respostas.get("secao3_programas", {}).get("tipos_programa"):
        dicionario.append("TIPOS DE PROGRAMAS:")
        for programa in respostas["secao3_programas"]["tipos_programa"]:
            dicionario.append(f"  - {programa.get('item', '')}: {programa.get('definicao', '')}")
        dicionario.append("")
    
    dicionario.append("=" * 80)
    dicionario.append("3. ESTRUTURA DAS TABELAS")
    dicionario.append("=" * 80)
    dicionario.append("")
    
    # Gerar descrição de cada tabela
    for tabela, colunas in estrutura_banco.items():
        dicionario.append("-" * 80)
        dicionario.append(f"TABELA: {tabela.upper()}")
        dicionario.append("-" * 80)
        dicionario.append("")
        
        # Descrição da tabela
        descricoes_tabelas = {
            "estado": "Armazena informações sobre os estados brasileiros e Distrito Federal.",
            "cidade": "Armazena informações sobre as cidades, vinculadas aos estados.",
            "bairro": "Armazena informações sobre os bairros, vinculados às cidades.",
            "tipo_logradouro": "Armazena os tipos de logradouro (Rua, Avenida, Rodovia, etc.).",
            "endereco": "Armazena endereços completos com logradouro, número e localização.",
            "telefone": "Armazena números de telefone com código de área.",
            "contato": "Armazena informações de contato (email e telefone).",
            "contato_telefone": "Tabela de relacionamento N-N entre contato e telefone.",
            "centros_inovacao": "Armazena informações sobre os centros de inovação.",
            "endereco_centro": "Tabela de relacionamento N-N entre centro e endereço.",
            "ator": "Armazena informações sobre os atores que participam dos centros.",
            "programa": "Armazena informações sobre os programas oferecidos pelos atores."
        }
        
        dicionario.append(f"Descrição: {descricoes_tabelas.get(tabela, '')}")
        dicionario.append("")
        dicionario.append("COLUNAS:")
        dicionario.append("")
        
        for coluna, descricao_base in colunas.items():
            dicionario.append(f"  • {coluna}")
            dicionario.append(f"    Tipo: Ver estrutura SQL")
            dicionario.append(f"    Descrição: {descricao_base}")
            
            # Adicionar informações específicas baseadas nas respostas
            if tabela == "ator" and coluna == "tipo_ator":
                if respostas.get("secao2_atores", {}).get("tipos_ator"):
                    dicionario.append(f"    Valores possíveis:")
                    for tipo in respostas["secao2_atores"]["tipos_ator"]:
                        dicionario.append(f"      - {tipo.get('item', '')}")
            
            if tabela == "ator" and coluna == "tamanho_ator":
                if respostas.get("secao2_atores", {}).get("tamanho_ator"):
                    dicionario.append(f"    Valores possíveis:")
                    for tamanho in respostas["secao2_atores"]["tamanho_ator"]:
                        dicionario.append(f"      - {tamanho.get('item', '')}")
                    if respostas.get("secao2_atores", {}).get("criterio_tamanho"):
                        dicionario.append(f"    Critério: {respostas['secao2_atores']['criterio_tamanho']}")
            
            if tabela == "ator" and coluna == "participa_programa":
                if respostas.get("secao2_atores", {}).get("participa_programa"):
                    dicionario.append(f"    {respostas['secao2_atores']['participa_programa']}")
            
            if tabela == "ator" and coluna == "cnpj":
                if respostas.get("secao7_regras_negocio", {}).get("regras_cnpj"):
                    dicionario.append(f"    Regras: {respostas['secao7_regras_negocio']['regras_cnpj']}")
            
            if tabela == "centros_inovacao" and coluna == "ano_fundacao":
                if respostas.get("secao4_centros", {}).get("ano_fundacao"):
                    dicionario.append(f"    Observação: {respostas['secao4_centros']['ano_fundacao']}")
            
            if tabela == "programa" and coluna == "ano_inicio":
                if respostas.get("secao3_programas", {}).get("ano_inicio"):
                    dicionario.append(f"    Observação: {respostas['secao3_programas']['ano_inicio']}")
            
            dicionario.append("")
        
        dicionario.append("")
    
    # Regras de negócio
    dicionario.append("=" * 80)
    dicionario.append("4. REGRAS DE NEGÓCIO")
    dicionario.append("=" * 80)
    dicionario.append("")
    
    if respostas.get("secao7_regras_negocio", {}).get("exclusao_centro"):
        dicionario.append("EXCLUSÃO DE CENTRO:")
        dicionario.append(respostas["secao7_regras_negocio"]["exclusao_centro"])
        dicionario.append("")
    
    if respostas.get("secao2_atores", {}).get("ator_multiplos_centros"):
        dicionario.append("MÚLTIPLOS CENTROS:")
        dicionario.append("Um ator pode estar associado a mais de um centro de inovação.")
        if respostas.get("secao2_atores", {}).get("explicacao_multiplos_centros"):
            dicionario.append(respostas["secao2_atores"]["explicacao_multiplos_centros"])
        dicionario.append("")
    
    if respostas.get("secao4_centros", {}).get("multiplos_enderecos"):
        dicionario.append("MÚLTIPLOS ENDEREÇOS:")
        dicionario.append("Um centro pode ter mais de um endereço.")
        if respostas.get("secao4_centros", {}).get("quando_multiplos_enderecos"):
            dicionario.append(respostas["secao4_centros"]["quando_multiplos_enderecos"])
        dicionario.append("")
    
    # Relacionamentos
    dicionario.append("=" * 80)
    dicionario.append("5. RELACIONAMENTOS ENTRE TABELAS")
    dicionario.append("=" * 80)
    dicionario.append("")
    dicionario.append("Estado → Cidade (1:N)")
    dicionario.append("Cidade → Bairro (1:N)")
    dicionario.append("Bairro → Endereço (1:N)")
    dicionario.append("Tipo Logradouro → Endereço (1:N)")
    dicionario.append("Telefone → Contato (1:N)")
    dicionario.append("Contato → Centro de Inovação (1:N)")
    dicionario.append("Centro → Ator (1:N)")
    dicionario.append("Ator → Programa (1:N)")
    dicionario.append("Centro ↔ Endereço (N:N via endereco_centro)")
    dicionario.append("Contato ↔ Telefone (N:N via contato_telefone)")
    dicionario.append("")
    
    return "\n".join(dicionario)

def main():
    print("=" * 70)
    print("GERADOR DE DICIONÁRIO DE DADOS")
    print("=" * 70)
    print()
    
    respostas = carregar_respostas()
    if not respostas:
        return
    
    print("📝 Gerando dicionário de dados...")
    dicionario = gerar_dicionario(respostas)
    
    # Salvar dicionário
    arquivo_saida = "DICIONARIO_DADOS.txt"
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        f.write(dicionario)
    
    print(f"✅ Dicionário de dados gerado com sucesso!")
    print(f"📄 Arquivo salvo em: {arquivo_saida}")
    print()
    print("=" * 70)

if __name__ == "__main__":
    main()

