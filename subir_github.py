#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para subir arquivos para o GitHub
"""
import os
import subprocess
import sys

# Navegar para o diretório do script
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
print(f"📂 Diretório: {os.getcwd()}\n")

# Verificar se Git está instalado
try:
    subprocess.run(['git', '--version'], check=True, capture_output=True)
    print("✅ Git está instalado\n")
except:
    print("❌ Git não está instalado!")
    sys.exit(1)

# Verificar se já está inicializado
if not os.path.exists('.git'):
    print("🔧 Inicializando repositório Git...")
    subprocess.run(['git', 'init'], check=True)
    print("✅ Repositório inicializado\n")
else:
    print("✅ Repositório Git já inicializado\n")

# Verificar se remote já existe
result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
if 'origin' not in result.stdout:
    print("⚠️  ATENÇÃO: Você precisa adicionar o remote do GitHub!")
    print("   Execute manualmente:")
    print("   git remote add origin https://github.com/SEU_USUARIO/ETL_projeto_aplicado.git")
    print("   (Substitua SEU_USUARIO pelo seu nome de usuário)\n")
    resposta = input("Deseja continuar mesmo assim? (s/n): ").lower().strip()
    if resposta not in ['s', 'sim', 'y', 'yes']:
        sys.exit(0)
else:
    print("✅ Remote já configurado\n")

# Adicionar todos os arquivos
print("📦 Adicionando arquivos...")
subprocess.run(['git', 'add', '.'], check=True)
print("✅ Arquivos adicionados\n")

# Verificar status
print("📊 Status dos arquivos:")
subprocess.run(['git', 'status', '--short'], check=True)
print()

# Fazer commit
print("💾 Fazendo commit...")
try:
    subprocess.run(['git', 'commit', '-m', 'Initial commit: Sistema ETL para migração Excel -> PostgreSQL'], 
                   check=True)
    print("✅ Commit realizado\n")
except subprocess.CalledProcessError as e:
    if 'nothing to commit' in str(e):
        print("ℹ️  Nada para commitar (arquivos já estão commitados)\n")
    else:
        print(f"❌ Erro no commit: {e}\n")
        sys.exit(1)

# Verificar branch
result = subprocess.run(['git', 'branch', '--show-current'], capture_output=True, text=True)
branch_atual = result.stdout.strip()
print(f"🌿 Branch atual: {branch_atual}\n")

# Tentar renomear para main se estiver em master
if branch_atual == 'master':
    print("🔄 Renomeando branch para 'main'...")
    subprocess.run(['git', 'branch', '-M', 'main'], check=True)
    print("✅ Branch renomeada\n")

# Tentar fazer push
print("🚀 Tentando fazer push para o GitHub...")
print("⚠️  Se pedir autenticação, use um Personal Access Token (não a senha)\n")

try:
    subprocess.run(['git', 'push', '-u', 'origin', 'main'], check=True)
    print("\n✅ Arquivos enviados com sucesso para o GitHub!")
except subprocess.CalledProcessError as e:
    print(f"\n❌ Erro ao fazer push: {e}")
    print("\n💡 Possíveis causas:")
    print("   1. Remote não configurado - execute: git remote add origin https://github.com/SEU_USUARIO/ETL_projeto_aplicado.git")
    print("   2. Problema de autenticação - use Personal Access Token")
    print("   3. Repositório não existe no GitHub - crie o repositório primeiro")
    print("\n📝 Execute manualmente:")
    print("   git push -u origin main")
except FileNotFoundError:
    print("\n⚠️  Remote não configurado. Configure primeiro:")
    print("   git remote add origin https://github.com/SEU_USUARIO/ETL_projeto_aplicado.git")

print("\n✅ Processo concluído!")

