#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para criar um novo repositório Git do zero e subir para o GitHub
"""
import os
import subprocess
import sys
import shutil

# Navegar para o diretório do script
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
print("=" * 70)
print("CRIANDO NOVO REPOSITÓRIO GIT")
print("=" * 70)
print(f"\n📂 Diretório: {os.getcwd()}\n")

# Verificar se Git está instalado
try:
    result = subprocess.run(['git', '--version'], check=True, capture_output=True, text=True)
    print(f"✅ Git está instalado: {result.stdout.strip()}\n")
except:
    print("❌ Git não está instalado!")
    print("   Instale o Git em: https://git-scm.com/downloads")
    sys.exit(1)

# Remover .git existente se houver
if os.path.exists('.git'):
    print("🗑️  Removendo repositório Git existente...")
    try:
        shutil.rmtree('.git')
        print("✅ Repositório antigo removido\n")
    except Exception as e:
        print(f"⚠️  Aviso ao remover .git: {e}\n")

# Inicializar novo repositório
print("🔧 Inicializando novo repositório Git...")
try:
    subprocess.run(['git', 'init'], check=True, stdout=subprocess.DEVNULL)
    print("✅ Novo repositório inicializado\n")
except Exception as e:
    print(f"❌ Erro ao inicializar: {e}\n")
    sys.exit(1)

# Configurar branch padrão como main
print("🌿 Configurando branch padrão como 'main'...")
subprocess.run(['git', 'branch', '-M', 'main'], check=True)
print("✅ Branch 'main' configurada\n")

# Solicitar informações do GitHub
print("=" * 70)
print("CONFIGURAÇÃO DO GITHUB")
print("=" * 70)
print()
usuario = input("📝 Digite seu nome de usuário do GitHub: ").strip()
if not usuario:
    print("❌ Nome de usuário não pode estar vazio!")
    sys.exit(1)

repo_nome = "ETL_projeto_aplicado"
print(f"📦 Nome do repositório: {repo_nome}")
confirmar = input(f"   Confirmar? (s/n) [s]: ").strip().lower()
if confirmar and confirmar not in ['s', 'sim', 'y', 'yes']:
    repo_nome = input("   Digite o nome do repositório: ").strip()
    if not repo_nome:
        repo_nome = "ETL_projeto_aplicado"

# Adicionar remote
remote_url = f"https://github.com/{usuario}/{repo_nome}.git"
print(f"\n🔗 Adicionando remote: {remote_url}")
try:
    subprocess.run(['git', 'remote', 'add', 'origin', remote_url], 
                  check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("✅ Remote adicionado\n")
except subprocess.CalledProcessError:
    # Se já existe, remover e adicionar novamente
    subprocess.run(['git', 'remote', 'remove', 'origin'], 
                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['git', 'remote', 'add', 'origin', remote_url], check=True)
    print("✅ Remote atualizado\n")

# Adicionar todos os arquivos
print("📦 Adicionando arquivos ao staging...")
try:
    subprocess.run(['git', 'add', '.'], check=True, stdout=subprocess.DEVNULL)
    print("✅ Arquivos adicionados\n")
except Exception as e:
    print(f"⚠️  Aviso ao adicionar arquivos: {e}\n")

# Verificar o que será commitado
print("📊 Arquivos que serão commitados:")
subprocess.run(['git', 'status', '--short'])
print()

# Fazer commit inicial
print("💾 Fazendo commit inicial...")
try:
    subprocess.run(['git', 'commit', '-m', 'Initial commit: Sistema ETL para migração Excel -> PostgreSQL'], 
                  check=True, stdout=subprocess.DEVNULL)
    print("✅ Commit realizado\n")
except subprocess.CalledProcessError as e:
    print(f"❌ Erro no commit: {e}\n")
    print("💡 Verifique se há arquivos para commitar")
    sys.exit(1)

# Mostrar informações antes do push
print("=" * 70)
print("PRONTO PARA ENVIAR AO GITHUB")
print("=" * 70)
print(f"\n📤 Repositório: {remote_url}")
print(f"🌿 Branch: main")
print(f"📝 Commit: Initial commit: Sistema ETL para migração Excel -> PostgreSQL")
print()

# Verificar se repositório existe no GitHub
print("⚠️  IMPORTANTE:")
print("   1. Certifique-se de que o repositório 'ETL_projeto_aplicado' existe no GitHub")
print("   2. Se pedir autenticação, use um Personal Access Token (não a senha)")
print("   3. Para criar token: GitHub → Settings → Developer settings → Personal access tokens")
print()

confirmar_push = input("🚀 Deseja fazer push agora? (s/n) [s]: ").strip().lower()
if confirmar_push and confirmar_push not in ['s', 'sim', 'y', 'yes']:
    print("\n✅ Repositório configurado! Execute manualmente:")
    print(f"   git push -u origin main")
    sys.exit(0)

# Fazer push
print("\n🚀 Enviando para o GitHub...")
print("   (Se pedir autenticação, use Personal Access Token)\n")

try:
    subprocess.run(['git', 'push', '-u', 'origin', 'main'], check=True)
    print("\n" + "=" * 70)
    print("✅ SUCESSO! Arquivos enviados para o GitHub!")
    print("=" * 70)
    print(f"\n🔗 Repositório: {remote_url}\n")
except subprocess.CalledProcessError as e:
    print("\n" + "=" * 70)
    print("❌ ERRO AO FAZER PUSH")
    print("=" * 70)
    print(f"\nErro: {e}")
    print("\n💡 Possíveis soluções:")
    print("   1. Verifique se o repositório existe no GitHub")
    print("   2. Crie o repositório em: https://github.com/new")
    print("   3. Use Personal Access Token para autenticação")
    print("   4. Execute manualmente: git push -u origin main")
    print()
    print("📝 Comandos para executar manualmente:")
    print(f"   git push -u origin main")
    sys.exit(1)

print("\n✅ Processo concluído com sucesso!")

