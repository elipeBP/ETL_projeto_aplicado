#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script interativo para coletar informações e gerar dicionário de dados
"""
import json
from datetime import datetime

def coletar_resposta(pergunta, obrigatoria=False):
    """Coleta uma resposta do usuário"""
    while True:
        resposta = input(f"\n{pergunta}\n> ").strip()
        if resposta or not obrigatoria:
            return resposta
        print("⚠️  Esta pergunta é obrigatória. Por favor, responda.")

def coletar_multiplas_respostas(pergunta_base, quantidade=3):
    """Coleta múltiplas respostas para uma pergunta"""
    respostas = []
    print(f"\n{pergunta_base}")
    print("(Deixe em branco para parar)")
    
    for i in range(1, quantidade + 1):
        item = input(f"  Item {i}: ").strip()
        if not item:
            break
        definicao = input(f"    Definição: ").strip()
        respostas.append({
            "item": item,
            "definicao": definicao
        })
    
    return respostas

def coletar_sim_nao(pergunta):
    """Coleta resposta Sim/Não"""
    while True:
        resposta = input(f"\n{pergunta} [S/N]\n> ").strip().upper()
        if resposta in ['S', 'SIM', 'Y', 'YES']:
            return True
        elif resposta in ['N', 'NAO', 'NÃO', 'NO']:
            return False
        print("⚠️  Por favor, responda S (Sim) ou N (Não)")

def main():
    print("=" * 70)
    print("QUESTIONÁRIO PARA CRIAÇÃO DO DICIONÁRIO DE DADOS")
    print("Sistema de Gestão de Centros de Inovação")
    print("=" * 70)
    print("\nEste questionário coletará informações para criar um dicionário")
    print("de dados completo e profissional.")
    print("\n💡 Dica: Você pode deixar em branco se não souber a resposta.")
    print("=" * 70)
    
    dados = {
        "data_coleta": datetime.now().isoformat(),
        "secao1_conceitos_gerais": {},
        "secao2_atores": {},
        "secao3_programas": {},
        "secao4_centros": {},
        "secao5_enderecos": {},
        "secao6_contatos": {},
        "secao7_regras_negocio": {},
        "secao8_terminologia": {},
        "secao9_contexto": {},
        "secao10_adicionais": {}
    }
    
    # SEÇÃO 1: CONCEITOS GERAIS
    print("\n" + "=" * 70)
    print("SEÇÃO 1: CONCEITOS GERAIS DO SISTEMA")
    print("=" * 70)
    
    dados["secao1_conceitos_gerais"]["centro_inovacao"] = coletar_resposta(
        "1.1. O que é um CENTRO DE INOVAÇÃO?"
    )
    
    dados["secao1_conceitos_gerais"]["objetivo_sistema"] = coletar_resposta(
        "1.2. Qual é o objetivo principal deste sistema?"
    )
    
    dados["secao1_conceitos_gerais"]["usuarios_principais"] = coletar_resposta(
        "1.3. Quem são os principais usuários deste sistema?"
    )
    
    # SEÇÃO 2: ATORES
    print("\n" + "=" * 70)
    print("SEÇÃO 2: CONCEITOS SOBRE ATORES")
    print("=" * 70)
    
    dados["secao2_atores"]["definicao_ator"] = coletar_resposta(
        "2.1. O que é um ATOR no contexto deste sistema?"
    )
    
    dados["secao2_atores"]["empresa_incubada"] = coletar_resposta(
        "2.2. O que significa 'EMPRESA INCUBADA'?"
    )
    
    print("\n2.3. Quais são os diferentes TIPOS DE ATORES?")
    dados["secao2_atores"]["tipos_ator"] = coletar_multiplas_respostas(
        "Digite os tipos de atores (ex: Empresa, Startup, Laboratório):"
    )
    
    print("\n2.4. O que significa 'TAMANHO_ATOR'?")
    dados["secao2_atores"]["tamanho_ator"] = coletar_multiplas_respostas(
        "Digite os valores possíveis (ex: Pequeno, Médio, Grande):"
    )
    
    dados["secao2_atores"]["criterio_tamanho"] = coletar_resposta(
        "2.4. Qual é o critério para classificar o tamanho do ator?"
    )
    
    dados["secao2_atores"]["participa_programa"] = coletar_resposta(
        "2.5. O que significa 'PARTICIPA_PROGRAMA'? Quando um ator participa?"
    )
    
    dados["secao2_atores"]["ator_multiplos_centros"] = coletar_sim_nao(
        "2.6. Um ator pode estar associado a mais de um centro de inovação?"
    )
    
    if dados["secao2_atores"]["ator_multiplos_centros"]:
        dados["secao2_atores"]["explicacao_multiplos_centros"] = coletar_resposta(
            "Como isso funciona quando um ator está em múltiplos centros?"
        )
    
    # SEÇÃO 3: PROGRAMAS
    print("\n" + "=" * 70)
    print("SEÇÃO 3: CONCEITOS SOBRE PROGRAMAS")
    print("=" * 70)
    
    dados["secao3_programas"]["definicao_programa"] = coletar_resposta(
        "3.1. O que é um PROGRAMA no contexto deste sistema?"
    )
    
    print("\n3.2. Quais são os tipos de programas que podem existir?")
    dados["secao3_programas"]["tipos_programa"] = coletar_multiplas_respostas(
        "Digite os tipos (ex: Incubação, Aceleração, Mentoria):"
    )
    
    dados["secao3_programas"]["diferenca_projeto"] = coletar_resposta(
        "3.3. Qual é a diferença entre um programa e um projeto?"
    )
    
    dados["secao3_programas"]["ano_inicio"] = coletar_resposta(
        "3.4. O que significa 'ANO_INICIO' de um programa?"
    )
    
    dados["secao3_programas"]["programa_multiplos_atores"] = coletar_sim_nao(
        "3.5. Um programa pode ser oferecido por mais de um ator?"
    )
    
    dados["secao3_programas"]["ator_multiplos_programas"] = coletar_sim_nao(
        "3.6. Um ator pode ter mais de um programa?"
    )
    
    # SEÇÃO 4: CENTROS
    print("\n" + "=" * 70)
    print("SEÇÃO 4: CONCEITOS SOBRE CENTROS DE INOVAÇÃO")
    print("=" * 70)
    
    dados["secao4_centros"]["ano_fundacao"] = coletar_resposta(
        "4.1. O que significa 'ANO_FUNDACAO'? É data exata ou apenas ano?"
    )
    
    dados["secao4_centros"]["multiplos_enderecos"] = coletar_sim_nao(
        "4.2. Um centro pode ter mais de um endereço?"
    )
    
    if dados["secao4_centros"]["multiplos_enderecos"]:
        dados["secao4_centros"]["quando_multiplos_enderecos"] = coletar_resposta(
            "Em que situações um centro tem múltiplos endereços?"
        )
    
    dados["secao4_centros"]["multiplos_contatos"] = coletar_sim_nao(
        "4.3. Um centro pode ter mais de um contato (email/telefone)?"
    )
    
    dados["secao4_centros"]["relacao_atores"] = coletar_resposta(
        "4.4. Qual é a relação entre centro e atores? (clientes, parceiros, membros?)"
    )
    
    # SEÇÃO 5: ENDEREÇOS
    print("\n" + "=" * 70)
    print("SEÇÃO 5: CONCEITOS SOBRE ENDEREÇOS")
    print("=" * 70)
    
    print("\n5.1. Quais são os TIPOS DE LOGRADOURO mais comuns?")
    dados["secao5_enderecos"]["tipos_logradouro"] = coletar_multiplas_respostas(
        "Digite os tipos (ex: Rua, Avenida, Rodovia):"
    )
    
    dados["secao5_enderecos"]["numero_obrigatorio"] = coletar_sim_nao(
        "5.2. O número do endereço é obrigatório?"
    )
    
    if not dados["secao5_enderecos"]["numero_obrigatorio"]:
        dados["secao5_enderecos"]["sem_numero"] = coletar_resposta(
            "O que fazer quando não há número (ex: sítio, chácara)?"
        )
    
    dados["secao5_enderecos"]["hierarquia"] = coletar_resposta(
        "5.3. Como funciona a hierarquia Estado → Cidade → Bairro?"
    )
    
    # SEÇÃO 6: CONTATOS
    print("\n" + "=" * 70)
    print("SEÇÃO 6: CONCEITOS SOBRE CONTATOS")
    print("=" * 70)
    
    dados["secao6_contatos"]["definicao_contato"] = coletar_resposta(
        "6.1. O que é um CONTATO no sistema?"
    )
    
    dados["secao6_contatos"]["multiplos_telefones"] = coletar_sim_nao(
        "6.2. Um contato pode ter mais de um telefone?"
    )
    
    dados["secao6_contatos"]["email_obrigatorio"] = coletar_sim_nao(
        "6.3. O email é obrigatório para um contato?"
    )
    
    dados["secao6_contatos"]["codigo_area"] = coletar_resposta(
        "6.4. O que significa 'CODIGO_AREA'? É sempre obrigatório?"
    )
    
    # SEÇÃO 7: REGRAS DE NEGÓCIO
    print("\n" + "=" * 70)
    print("SEÇÃO 7: REGRAS DE NEGÓCIO")
    print("=" * 70)
    
    dados["secao7_regras_negocio"]["regras_cnpj"] = coletar_resposta(
        "7.1. Existem regras específicas para o CNPJ de um ator?"
    )
    
    print("\n7.2. Existem valores permitidos para campos específicos?")
    dados["secao7_regras_negocio"]["valores_permitidos"] = coletar_multiplas_respostas(
        "Digite campo e valores permitidos (ex: tamanho_ator: Pequeno, Médio, Grande):"
    )
    
    dados["secao7_regras_negocio"]["campos_opcionais_temporarios"] = coletar_resposta(
        "7.3. Existem campos obrigatórios que podem ficar vazios temporariamente?"
    )
    
    dados["secao7_regras_negocio"]["exclusao_centro"] = coletar_resposta(
        "7.4. O que acontece quando um centro é excluído? (atores, programas?)"
    )
    
    # SEÇÃO 8: TERMINOLOGIA
    print("\n" + "=" * 70)
    print("SEÇÃO 8: TERMINOLOGIA E SINÔNIMOS")
    print("=" * 70)
    
    dados["secao8_terminologia"]["sinonimos_centro"] = coletar_resposta(
        "8.1. Outros termos para 'Centro de Inovação'? (Hub, Parque Tecnológico, etc.)"
    )
    
    dados["secao8_terminologia"]["sinonimos_ator"] = coletar_resposta(
        "8.2. Outros termos para 'Ator'? (Empresa, Organização, etc.)"
    )
    
    dados["secao8_terminologia"]["sinonimos_programa"] = coletar_resposta(
        "8.3. Outros termos para 'Programa'? (Projeto, Iniciativa, etc.)"
    )
    
    # SEÇÃO 9: CONTEXTO
    print("\n" + "=" * 70)
    print("SEÇÃO 9: CONTEXTO E OBJETIVOS")
    print("=" * 70)
    
    dados["secao9_contexto"]["uso_principal"] = coletar_resposta(
        "9.1. Para que este sistema será usado principalmente?"
    )
    
    print("\n9.2. Quais são as principais consultas/relatórios?")
    dados["secao9_contexto"]["consultas_principais"] = coletar_multiplas_respostas(
        "Digite as consultas principais:"
    )
    
    print("\n9.3. Quais são as métricas ou indicadores importantes?")
    dados["secao9_contexto"]["metricas"] = coletar_multiplas_respostas(
        "Digite as métricas:"
    )
    
    # SEÇÃO 10: ADICIONAIS
    print("\n" + "=" * 70)
    print("SEÇÃO 10: INFORMAÇÕES ADICIONAIS")
    print("=" * 70)
    
    dados["secao10_adicionais"]["documentacao_referencia"] = coletar_resposta(
        "10.1. Existe documentação, norma ou padrão que define esses conceitos?"
    )
    
    dados["secao10_adicionais"]["informacoes_adicionais"] = coletar_resposta(
        "10.2. Há alguma informação adicional importante para o dicionário?"
    )
    
    dados["secao10_adicionais"]["campos_futuros"] = coletar_resposta(
        "10.3. Existem campos ou conceitos que você gostaria de adicionar no futuro?"
    )
    
    # Salvar respostas
    arquivo_respostas = "respostas_dicionario_dados.json"
    with open(arquivo_respostas, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 70)
    print("✅ QUESTIONÁRIO CONCLUÍDO!")
    print("=" * 70)
    print(f"\n📄 Respostas salvas em: {arquivo_respostas}")
    print("\n💡 Próximo passo: Execute 'gerar_dicionario_dados.py' para criar")
    print("   o dicionário de dados completo com base nas suas respostas.")
    print("=" * 70)

if __name__ == "__main__":
    main()

