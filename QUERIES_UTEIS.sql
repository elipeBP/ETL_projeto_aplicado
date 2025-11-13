-- =====================================================
-- QUERIES SQL ÚTEIS - SISTEMA DE CENTROS DE INOVAÇÃO
-- Banco: Projeto_Aplicado
-- =====================================================

-- =====================================================
-- 1. ESTATÍSTICAS GERAIS DO SISTEMA
-- =====================================================

-- Contagem de registros por tabela
SELECT 
    'Estado' AS tabela, COUNT(*) AS total FROM estado
UNION ALL
SELECT 'Cidade', COUNT(*) FROM cidade
UNION ALL
SELECT 'Bairro', COUNT(*) FROM bairro
UNION ALL
SELECT 'Tipo Logradouro', COUNT(*) FROM tipo_logradouro
UNION ALL
SELECT 'Endereço', COUNT(*) FROM endereco
UNION ALL
SELECT 'Telefone', COUNT(*) FROM telefone
UNION ALL
SELECT 'Contato', COUNT(*) FROM contato
UNION ALL
SELECT 'Contato Telefone', COUNT(*) FROM contato_telefone
UNION ALL
SELECT 'Centros de Inovação', COUNT(*) FROM centros_inovacao
UNION ALL
SELECT 'Endereço Centro', COUNT(*) FROM endereco_centro
UNION ALL
SELECT 'Ator', COUNT(*) FROM ator
UNION ALL
SELECT 'Programa', COUNT(*) FROM programa
ORDER BY tabela;

-- =====================================================
-- 2. CENTROS DE INOVAÇÃO - VISÃO COMPLETA
-- =====================================================

-- Lista todos os centros com informações completas
SELECT 
    ci.id_centro,
    ci.nome AS centro_nome,
    ci.ano_fundacao,
    c.email,
    t.codigo_area,
    t.numero AS telefone,
    e.nome_logradouro,
    e.numero AS numero_endereco,
    tl.nome AS tipo_logradouro,
    b.nome AS bairro,
    cd.nome AS cidade,
    es.nome AS estado,
    es.sigla
FROM centros_inovacao ci
INNER JOIN contato c ON ci.id_contato = c.id_contato
INNER JOIN telefone t ON c.id_telefone = t.id_telefone
LEFT JOIN endereco_centro ec ON ci.id_centro = ec.id_centro
LEFT JOIN endereco e ON ec.id_endereco = e.id_endereco
LEFT JOIN tipo_logradouro tl ON e.id_tipo_logradouro = tl.id_tipo_de_logradouro
LEFT JOIN bairro b ON e.id_bairro = b.id_bairro
LEFT JOIN cidade cd ON b.id_cidade = cd.id_cidade
LEFT JOIN estado es ON cd.id_estado = es.id_estado
ORDER BY ci.nome;

-- =====================================================
-- 3. CENTROS POR ESTADO
-- =====================================================

-- Distribuição de centros por estado
SELECT 
    es.nome AS estado,
    es.sigla,
    COUNT(DISTINCT ci.id_centro) AS total_centros
FROM centros_inovacao ci
INNER JOIN endereco_centro ec ON ci.id_centro = ec.id_centro
INNER JOIN endereco e ON ec.id_endereco = e.id_endereco
INNER JOIN bairro b ON e.id_bairro = b.id_bairro
INNER JOIN cidade cd ON b.id_cidade = cd.id_cidade
INNER JOIN estado es ON cd.id_estado = es.id_estado
GROUP BY es.id_estado, es.nome, es.sigla
ORDER BY total_centros DESC, es.nome;

-- =====================================================
-- 4. ATORES POR CENTRO
-- =====================================================

-- Lista todos os atores com seus centros
SELECT 
    ci.nome AS centro_nome,
    a.id_ator,
    a.nome AS ator_nome,
    a.tipo_ator,
    a.tamanho_ator,
    a.participa_programa,
    a.cnpj
FROM ator a
INNER JOIN centros_inovacao ci ON a.id_centro = ci.id_centro
ORDER BY ci.nome, a.nome;

-- Contagem de atores por centro
SELECT 
    ci.nome AS centro_nome,
    COUNT(a.id_ator) AS total_atores,
    COUNT(CASE WHEN a.participa_programa = 'Sim' THEN 1 END) AS atores_com_programa
FROM centros_inovacao ci
LEFT JOIN ator a ON ci.id_centro = a.id_centro
GROUP BY ci.id_centro, ci.nome
ORDER BY total_atores DESC;

-- =====================================================
-- 5. PROGRAMAS POR ATOR E CENTRO
-- =====================================================

-- Lista todos os programas com informações completas
SELECT 
    ci.nome AS centro_nome,
    a.nome AS ator_nome,
    a.tipo_ator,
    p.id_programa,
    p.nome AS programa_nome,
    p.ano_inicio,
    p.descricao
FROM programa p
INNER JOIN ator a ON p.id_ator = a.id_ator
INNER JOIN centros_inovacao ci ON a.id_centro = ci.id_centro
ORDER BY ci.nome, a.nome, p.nome;

-- Contagem de programas por centro
SELECT 
    ci.nome AS centro_nome,
    COUNT(DISTINCT p.id_programa) AS total_programas,
    COUNT(DISTINCT a.id_ator) AS total_atores_com_programa
FROM centros_inovacao ci
LEFT JOIN ator a ON ci.id_centro = a.id_centro
LEFT JOIN programa p ON a.id_ator = p.id_ator
GROUP BY ci.id_centro, ci.nome
ORDER BY total_programas DESC;

-- =====================================================
-- 6. ANÁLISE DE TIPOS DE ATORES
-- =====================================================

-- Distribuição de atores por tipo
SELECT 
    tipo_ator,
    COUNT(*) AS total,
    COUNT(CASE WHEN participa_programa = 'Sim' THEN 1 END) AS com_programa,
    COUNT(CASE WHEN tamanho_ator = 'Pequeno' THEN 1 END) AS pequeno,
    COUNT(CASE WHEN tamanho_ator = 'Médio' THEN 1 END) AS medio,
    COUNT(CASE WHEN tamanho_ator = 'Grande' THEN 1 END) AS grande
FROM ator
WHERE tipo_ator IS NOT NULL
GROUP BY tipo_ator
ORDER BY total DESC;

-- =====================================================
-- 7. CENTROS MAIS ANTIGOS E MAIS NOVOS
-- =====================================================

-- Top 10 centros mais antigos
SELECT 
    nome AS centro_nome,
    ano_fundacao,
    EXTRACT(YEAR FROM ano_fundacao) AS ano,
    (EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM ano_fundacao)) AS anos_existencia
FROM centros_inovacao
WHERE ano_fundacao IS NOT NULL
ORDER BY ano_fundacao ASC
LIMIT 10;

-- Top 10 centros mais novos
SELECT 
    nome AS centro_nome,
    ano_fundacao,
    EXTRACT(YEAR FROM ano_fundacao) AS ano,
    (EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM ano_fundacao)) AS anos_existencia
FROM centros_inovacao
WHERE ano_fundacao IS NOT NULL
ORDER BY ano_fundacao DESC
LIMIT 10;

-- =====================================================
-- 8. BUSCA POR NOME (CENTRO, ATOR OU PROGRAMA)
-- =====================================================

-- Buscar centro por nome (substitua 'NOME' pelo termo desejado)
SELECT 
    ci.id_centro,
    ci.nome AS centro_nome,
    ci.ano_fundacao,
    c.email,
    t.numero AS telefone
FROM centros_inovacao ci
INNER JOIN contato c ON ci.id_contato = c.id_contato
INNER JOIN telefone t ON c.id_telefone = t.id_telefone
WHERE UPPER(ci.nome) LIKE UPPER('%NOME%')
ORDER BY ci.nome;

-- Buscar ator por nome
SELECT 
    a.id_ator,
    a.nome AS ator_nome,
    a.tipo_ator,
    a.cnpj,
    ci.nome AS centro_nome
FROM ator a
INNER JOIN centros_inovacao ci ON a.id_centro = ci.id_centro
WHERE UPPER(a.nome) LIKE UPPER('%NOME%')
ORDER BY a.nome;

-- Buscar programa por nome
SELECT 
    p.id_programa,
    p.nome AS programa_nome,
    p.ano_inicio,
    a.nome AS ator_nome,
    ci.nome AS centro_nome
FROM programa p
INNER JOIN ator a ON p.id_ator = a.id_ator
INNER JOIN centros_inovacao ci ON a.id_centro = ci.id_centro
WHERE UPPER(p.nome) LIKE UPPER('%NOME%')
ORDER BY p.nome;

-- =====================================================
-- 9. RELATÓRIO COMPLETO DE UM CENTRO ESPECÍFICO
-- =====================================================

-- Substitua 'NOME_DO_CENTRO' pelo nome do centro desejado
SELECT 
    '=== INFORMAÇÕES DO CENTRO ===' AS secao,
    ci.id_centro AS id,
    ci.nome AS nome,
    ci.ano_fundacao AS fundacao,
    NULL AS tipo
FROM centros_inovacao ci
WHERE UPPER(ci.nome) = UPPER('NOME_DO_CENTRO')

UNION ALL

SELECT 
    '=== CONTATO ===',
    c.id_contato,
    c.email,
    NULL,
    CONCAT(t.codigo_area, ' ', t.numero)
FROM centros_inovacao ci
INNER JOIN contato c ON ci.id_contato = c.id_contato
INNER JOIN telefone t ON c.id_telefone = t.id_telefone
WHERE UPPER(ci.nome) = UPPER('NOME_DO_CENTRO')

UNION ALL

SELECT 
    '=== ENDEREÇO ===',
    e.id_endereco,
    CONCAT(tl.nome, ' ', e.nome_logradouro, ', ', e.numero),
    NULL,
    CONCAT(b.nome, ' - ', cd.nome, '/', es.sigla)
FROM centros_inovacao ci
INNER JOIN endereco_centro ec ON ci.id_centro = ec.id_centro
INNER JOIN endereco e ON ec.id_endereco = e.id_endereco
INNER JOIN tipo_logradouro tl ON e.id_tipo_logradouro = tl.id_tipo_de_logradouro
INNER JOIN bairro b ON e.id_bairro = b.id_bairro
INNER JOIN cidade cd ON b.id_cidade = cd.id_cidade
INNER JOIN estado es ON cd.id_estado = es.id_estado
WHERE UPPER(ci.nome) = UPPER('NOME_DO_CENTRO');

-- =====================================================
-- 10. ATORES E PROGRAMAS DE UM CENTRO
-- =====================================================

-- Lista completa de atores e seus programas de um centro específico
SELECT 
    ci.nome AS centro_nome,
    a.id_ator,
    a.nome AS ator_nome,
    a.tipo_ator,
    a.tamanho_ator,
    a.participa_programa,
    p.id_programa,
    p.nome AS programa_nome,
    p.ano_inicio AS programa_inicio
FROM centros_inovacao ci
INNER JOIN ator a ON ci.id_centro = a.id_centro
LEFT JOIN programa p ON a.id_ator = p.id_ator
WHERE UPPER(ci.nome) = UPPER('NOME_DO_CENTRO')
ORDER BY a.nome, p.nome;

-- =====================================================
-- 11. ESTATÍSTICAS DE PROGRAMAS
-- =====================================================

-- Programas por ano de início
SELECT 
    EXTRACT(YEAR FROM ano_inicio) AS ano,
    COUNT(*) AS total_programas
FROM programa
WHERE ano_inicio IS NOT NULL
GROUP BY EXTRACT(YEAR FROM ano_inicio)
ORDER BY ano DESC;

-- Programas mais antigos
SELECT 
    p.nome AS programa_nome,
    p.ano_inicio,
    a.nome AS ator_nome,
    ci.nome AS centro_nome
FROM programa p
INNER JOIN ator a ON p.id_ator = a.id_ator
INNER JOIN centros_inovacao ci ON a.id_centro = ci.id_centro
WHERE p.ano_inicio IS NOT NULL
ORDER BY p.ano_inicio ASC
LIMIT 10;

-- =====================================================
-- 12. CIDADES COM MAIS CENTROS
-- =====================================================

-- Top 20 cidades com mais centros de inovação
SELECT 
    cd.nome AS cidade,
    es.nome AS estado,
    es.sigla,
    COUNT(DISTINCT ci.id_centro) AS total_centros
FROM centros_inovacao ci
INNER JOIN endereco_centro ec ON ci.id_centro = ec.id_centro
INNER JOIN endereco e ON ec.id_endereco = e.id_endereco
INNER JOIN bairro b ON e.id_bairro = b.id_bairro
INNER JOIN cidade cd ON b.id_cidade = cd.id_cidade
INNER JOIN estado es ON cd.id_estado = es.id_estado
GROUP BY cd.id_cidade, cd.nome, es.nome, es.sigla
ORDER BY total_centros DESC
LIMIT 20;

-- =====================================================
-- 13. CENTROS SEM ATORES
-- =====================================================

-- Centros que não possuem atores cadastrados
SELECT 
    ci.id_centro,
    ci.nome AS centro_nome,
    ci.ano_fundacao,
    c.email
FROM centros_inovacao ci
INNER JOIN contato c ON ci.id_contato = c.id_contato
LEFT JOIN ator a ON ci.id_centro = a.id_centro
WHERE a.id_ator IS NULL
ORDER BY ci.nome;

-- =====================================================
-- 14. ATORES SEM PROGRAMAS
-- =====================================================

-- Atores que não possuem programas cadastrados
SELECT 
    a.id_ator,
    a.nome AS ator_nome,
    a.tipo_ator,
    a.participa_programa,
    ci.nome AS centro_nome
FROM ator a
INNER JOIN centros_inovacao ci ON a.id_centro = ci.id_centro
LEFT JOIN programa p ON a.id_ator = p.id_ator
WHERE p.id_programa IS NULL
ORDER BY ci.nome, a.nome;

-- =====================================================
-- 15. DASHBOARD RESUMIDO
-- =====================================================

-- Visão geral completa do sistema
SELECT 
    (SELECT COUNT(*) FROM centros_inovacao) AS total_centros,
    (SELECT COUNT(*) FROM ator) AS total_atores,
    (SELECT COUNT(*) FROM programa) AS total_programas,
    (SELECT COUNT(DISTINCT es.id_estado) FROM centros_inovacao ci
     INNER JOIN endereco_centro ec ON ci.id_centro = ec.id_centro
     INNER JOIN endereco e ON ec.id_endereco = e.id_endereco
     INNER JOIN bairro b ON e.id_bairro = b.id_bairro
     INNER JOIN cidade cd ON b.id_cidade = cd.id_cidade
     INNER JOIN estado es ON cd.id_estado = es.id_estado) AS estados_com_centros,
    (SELECT COUNT(DISTINCT cd.id_cidade) FROM centros_inovacao ci
     INNER JOIN endereco_centro ec ON ci.id_centro = ec.id_centro
     INNER JOIN endereco e ON ec.id_endereco = e.id_endereco
     INNER JOIN bairro b ON e.id_bairro = b.id_bairro
     INNER JOIN cidade cd ON b.id_cidade = cd.id_cidade) AS cidades_com_centros,
    (SELECT COUNT(*) FROM ator WHERE participa_programa = 'Sim') AS atores_com_programa,
    (SELECT ROUND(AVG(EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM ano_fundacao)), 1)
     FROM centros_inovacao WHERE ano_fundacao IS NOT NULL) AS idade_media_centros;

-- =====================================================
-- 16. BUSCA AVANÇADA POR MÚLTIPLOS CRITÉRIOS
-- =====================================================

-- Buscar centros por estado e tipo de ator
SELECT DISTINCT
    ci.id_centro,
    ci.nome AS centro_nome,
    es.nome AS estado,
    a.tipo_ator,
    COUNT(DISTINCT a.id_ator) AS total_atores_tipo
FROM centros_inovacao ci
INNER JOIN endereco_centro ec ON ci.id_centro = ec.id_centro
INNER JOIN endereco e ON ec.id_endereco = e.id_endereco
INNER JOIN bairro b ON e.id_bairro = b.id_bairro
INNER JOIN cidade cd ON b.id_cidade = cd.id_cidade
INNER JOIN estado es ON cd.id_estado = es.id_estado
INNER JOIN ator a ON ci.id_centro = a.id_centro
WHERE es.sigla = 'SC'  -- Substitua pelo estado desejado
  AND a.tipo_ator = 'Empresa'  -- Substitua pelo tipo desejado
GROUP BY ci.id_centro, ci.nome, es.nome, a.tipo_ator
ORDER BY ci.nome;

-- =====================================================
-- 17. RELATÓRIO DE CONTATOS
-- =====================================================

-- Lista todos os contatos com telefones
SELECT 
    c.id_contato,
    c.email,
    t.codigo_area,
    t.numero AS telefone,
    CONCAT(t.codigo_area, ' ', t.numero) AS telefone_completo,
    ci.nome AS centro_associado
FROM contato c
INNER JOIN telefone t ON c.id_telefone = t.id_telefone
LEFT JOIN centros_inovacao ci ON c.id_contato = ci.id_contato
ORDER BY c.email;

-- =====================================================
-- 18. ANÁLISE TEMPORAL
-- =====================================================

-- Evolução de criação de centros por década
SELECT 
    CASE 
        WHEN EXTRACT(YEAR FROM ano_fundacao) < 2000 THEN 'Antes de 2000'
        WHEN EXTRACT(YEAR FROM ano_fundacao) < 2010 THEN '2000-2009'
        WHEN EXTRACT(YEAR FROM ano_fundacao) < 2020 THEN '2010-2019'
        ELSE '2020+'
    END AS decada,
    COUNT(*) AS total_centros
FROM centros_inovacao
WHERE ano_fundacao IS NOT NULL
GROUP BY 
    CASE 
        WHEN EXTRACT(YEAR FROM ano_fundacao) < 2000 THEN 'Antes de 2000'
        WHEN EXTRACT(YEAR FROM ano_fundacao) < 2010 THEN '2000-2009'
        WHEN EXTRACT(YEAR FROM ano_fundacao) < 2020 THEN '2010-2019'
        ELSE '2020+'
    END
ORDER BY decada;

-- =====================================================
-- FIM DAS QUERIES
-- =====================================================

