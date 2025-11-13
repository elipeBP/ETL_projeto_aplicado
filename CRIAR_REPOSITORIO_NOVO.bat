@echo off
chcp 65001 >nul
cls
echo ========================================================================
echo CRIANDO NOVO REPOSITÓRIO GIT DO ZERO
echo ========================================================================
echo.

cd /d "%~dp0"
echo Diretório: %CD%
echo.

:: Verificar Git
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git não está instalado!
    echo    Instale em: https://git-scm.com/downloads
    pause
    exit /b 1
)
echo ✅ Git está instalado
echo.

:: Remover .git existente
if exist ".git" (
    echo 🗑️  Removendo repositório Git existente...
    rmdir /s /q .git
    echo ✅ Repositório antigo removido
    echo.
)

:: Inicializar novo repositório
echo 🔧 Inicializando novo repositório Git...
git init
if errorlevel 1 (
    echo ❌ Erro ao inicializar repositório
    pause
    exit /b 1
)
echo ✅ Novo repositório inicializado
echo.

:: Configurar branch main
echo 🌿 Configurando branch 'main'...
git branch -M main
echo ✅ Branch configurada
echo.

:: Solicitar usuário do GitHub
echo ========================================================================
echo CONFIGURAÇÃO DO GITHUB
echo ========================================================================
echo.
set /p usuario="📝 Digite seu nome de usuário do GitHub: "
if "%usuario%"=="" (
    echo ❌ Nome de usuário não pode estar vazio!
    pause
    exit /b 1
)

set repo_nome=ETL_projeto_aplicado
echo.
echo 📦 Nome do repositório: %repo_nome%
set /p confirmar="   Confirmar? (s/n) [s]: "
if not "%confirmar%"=="" if /i not "%confirmar%"=="s" (
    set /p repo_nome="   Digite o nome do repositório: "
    if "%repo_nome%"=="" set repo_nome=ETL_projeto_aplicado
)

:: Adicionar remote
set remote_url=https://github.com/%usuario%/%repo_nome%.git
echo.
echo 🔗 Adicionando remote: %remote_url%
git remote remove origin >nul 2>&1
git remote add origin %remote_url%
if errorlevel 1 (
    echo ❌ Erro ao adicionar remote
    pause
    exit /b 1
)
echo ✅ Remote adicionado
echo.

:: Adicionar arquivos
echo 📦 Adicionando arquivos...
git add .
if errorlevel 1 (
    echo ⚠️  Aviso ao adicionar arquivos
) else (
    echo ✅ Arquivos adicionados
)
echo.

:: Mostrar status
echo 📊 Arquivos que serão commitados:
git status --short
echo.

:: Fazer commit
echo 💾 Fazendo commit inicial...
git commit -m "Initial commit: Sistema ETL para migração Excel -> PostgreSQL"
if errorlevel 1 (
    echo ❌ Erro no commit
    pause
    exit /b 1
)
echo ✅ Commit realizado
echo.

:: Informações finais
echo ========================================================================
echo PRONTO PARA ENVIAR AO GITHUB
echo ========================================================================
echo.
echo 📤 Repositório: %remote_url%
echo 🌿 Branch: main
echo 📝 Commit: Initial commit: Sistema ETL para migração Excel -> PostgreSQL
echo.
echo ⚠️  IMPORTANTE:
echo    1. Certifique-se de que o repositório '%repo_nome%' existe no GitHub
echo    2. Se pedir autenticação, use um Personal Access Token (não a senha)
echo    3. Para criar token: GitHub → Settings → Developer settings → Personal access tokens
echo.
set /p confirmar_push="🚀 Deseja fazer push agora? (s/n) [s]: "
if not "%confirmar_push%"=="" if /i not "%confirmar_push%"=="s" (
    echo.
    echo ✅ Repositório configurado! Execute manualmente:
    echo    git push -u origin main
    pause
    exit /b 0
)

:: Fazer push
echo.
echo 🚀 Enviando para o GitHub...
echo    (Se pedir autenticação, use Personal Access Token)
echo.
git push -u origin main
if errorlevel 1 (
    echo.
    echo ========================================================================
    echo ❌ ERRO AO FAZER PUSH
    echo ========================================================================
    echo.
    echo 💡 Possíveis soluções:
    echo    1. Verifique se o repositório existe no GitHub
    echo    2. Crie o repositório em: https://github.com/new
    echo    3. Use Personal Access Token para autenticação
    echo    4. Execute manualmente: git push -u origin main
    echo.
) else (
    echo.
    echo ========================================================================
    echo ✅ SUCESSO! Arquivos enviados para o GitHub!
    echo ========================================================================
    echo.
    echo 🔗 Repositório: %remote_url%
    echo.
)

pause

