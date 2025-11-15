# 📚 Guia para Criação do Dicionário de Dados

Este guia explica como criar um dicionário de dados completo para o sistema de gestão de centros de inovação.

## 📋 O que é um Dicionário de Dados?

Um dicionário de dados é um documento que descreve:
- **Tabelas**: O que cada tabela representa no sistema
- **Colunas**: O significado de cada campo
- **Conceitos de negócio**: Definições dos termos usados
- **Regras de negócio**: Validações e comportamentos esperados
- **Relacionamentos**: Como as tabelas se relacionam

## 🚀 Como Usar

### Opção 1: Questionário em Texto (Recomendado para revisão)

1. Abra o arquivo `QUESTIONARIO_DICIONARIO_DADOS.txt`
2. Preencha todas as perguntas com suas respostas
3. Envie o arquivo preenchido para gerar o dicionário

### Opção 2: Questionário Interativo (Recomendado para uso)

1. Execute o script interativo:
   ```bash
   python coletar_dicionario_dados.py
   ```

2. Responda todas as perguntas que aparecerem no terminal

3. As respostas serão salvas automaticamente em `respostas_dicionario_dados.json`

4. Gere o dicionário de dados:
   ```bash
   python gerar_dicionario_dados.py
   ```

5. O dicionário completo será salvo em `DICIONARIO_DADOS.txt`

## 📝 Exemplos de Perguntas

O questionário inclui perguntas como:

- **O que é um Centro de Inovação?**
- **O que significa "Empresa Incubada"?**
- **Quais são os tipos de atores?** (Empresa, Startup, Laboratório, etc.)
- **O que significa "Tamanho do Ator"?** (Pequeno, Médio, Grande)
- **O que é um Programa?**
- **Um ator pode estar em múltiplos centros?**
- E muitas outras...

## 📄 Arquivos Gerados

Após executar os scripts, você terá:

- `respostas_dicionario_dados.json` - Suas respostas em formato JSON
- `DICIONARIO_DADOS.txt` - Dicionário completo formatado

## ✨ O que o Dicionário Inclui

O dicionário gerado contém:

1. **Introdução**: Definições gerais do sistema
2. **Glossário de Termos**: Explicações de conceitos importantes
3. **Estrutura das Tabelas**: Descrição detalhada de cada tabela e coluna
4. **Regras de Negócio**: Validações e comportamentos
5. **Relacionamentos**: Como as tabelas se conectam

## 💡 Dicas

- **Seja específico**: Quanto mais detalhadas suas respostas, melhor será o dicionário
- **Use exemplos**: Exemplos ajudam a entender melhor os conceitos
- **Não deixe em branco**: Se não souber, escreva "Não sei" ou "A definir"
- **Revise depois**: Você pode executar o script novamente para atualizar

## 🔄 Atualizar o Dicionário

Se você quiser atualizar o dicionário:

1. Execute `python coletar_dicionario_dados.py` novamente
2. Responda apenas as perguntas que mudaram (ou todas)
3. Execute `python gerar_dicionario_dados.py` para gerar a nova versão

## 📚 Estrutura do Questionário

O questionário está dividido em 10 seções:

1. **Conceitos Gerais**: Visão geral do sistema
2. **Atores**: Definições sobre atores e empresas incubadas
3. **Programas**: Conceitos sobre programas oferecidos
4. **Centros**: Informações sobre centros de inovação
5. **Endereços**: Conceitos sobre localização
6. **Contatos**: Informações de contato
7. **Regras de Negócio**: Validações e comportamentos
8. **Terminologia**: Sinônimos e termos alternativos
9. **Contexto**: Objetivos e uso do sistema
10. **Adicionais**: Informações extras

## ⚠️ Importante

- O arquivo `respostas_dicionario_dados.json` contém suas respostas e **não deve** ser commitado no Git (já está no `.gitignore`)
- O dicionário final (`DICIONARIO_DADOS.txt`) pode ser commitado normalmente

## 🆘 Problemas?

Se encontrar algum problema:

1. Verifique se o Python está instalado
2. Certifique-se de estar no diretório correto do projeto
3. Verifique se todas as dependências estão instaladas

