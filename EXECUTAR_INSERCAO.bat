@echo off
chcp 65001 >nul
cd /d "%~dp0"
python inserir_dados_banco.py
pause

