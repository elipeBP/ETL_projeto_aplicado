@echo off
chcp 65001 >nul
echo ========================================================================
echo SUBINDO ARQUIVOS PARA O GITHUB
echo ========================================================================
echo.

cd /d "%~dp0"
echo Diretório: %CD%
echo.

echo [1/6] Verificando Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git não está instalado!
    pause
    exit /b 1
)
echo ✅ Git está instalado
echo.

echo [2/6] Inicializando repositório (se necessário)...
if not exist ".git" (
    git init
    echo ✅ Repositório inicializado
) else (
    echo ✅ Repositório já inicializado
)
echo.

echo [3/6] Verificando remote...
git remote -v >nul 2>&1
if errorlevel 1 (
    echo ⚠️  ATENÇÃO: Remote não configurado!
    echo.
    echo Você precisa executar:
    echo    git remote add origin https://github.com/SEU_USUARIO/ETL_projeto_aplicado.git
    echo.
    echo (Substitua SEU_USUARIO pelo seu nome de usuário do GitHub)
    echo.
    set /p continuar="Deseja continuar mesmo assim? (s/n): "
    if /i not "%continuar%"=="s" if /i not "%continuar%"=="sim" exit /b 0
) else (
    echo ✅ Remote configurado
)
echo.

echo [4/6] Adicionando arquivos...
git add .
echo ✅ Arquivos adicionados
echo.

echo [5/6] Fazendo commit...
git commit -m "Initial commit: Sistema ETL para migração Excel -> PostgreSQL" 2>nul
if errorlevel 1 (
    echo ℹ️  Nada para commitar ou commit já existe
) else (
    echo ✅ Commit realizado
)
echo.

echo [6/6] Configurando branch e fazendo push...
git branch -M main 2>nul
echo.
echo ⚠️  IMPORTANTE: Se pedir autenticação, use um Personal Access Token
echo    (não use sua senha do GitHub)
echo.
git push -u origin main
if errorlevel 1 (
    echo.
    echo ❌ Erro ao fazer push!
    echo.
    echo 💡 Possíveis soluções:
    echo    1. Configure o remote: git remote add origin https://github.com/SEU_USUARIO/ETL_projeto_aplicado.git
    echo    2. Use Personal Access Token para autenticação
    echo    3. Verifique se o repositório existe no GitHub
    echo.
) else (
    echo.
    echo ✅ Arquivos enviados com sucesso para o GitHub!
    echo.
)

pause

