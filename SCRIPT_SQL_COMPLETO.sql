-- =====================================================
-- SCRIPT SQL POSTGRESQL - ESTRUTURA COMPLETA DO BANCO
-- Sistema de Gestão de Centros de Inovação
-- PostgreSQL - pgAdmin
-- =====================================================

-- Criar banco de dados (descomente se necessário)
-- CREATE DATABASE centros_inovacao
--     WITH 
--     OWNER = postgres
--     ENCODING = 'UTF8'
--     LC_COLLATE = 'pt_BR.UTF-8'
--     LC_CTYPE = 'pt_BR.UTF-8'
--     TABLESPACE = pg_default
--     CONNECTION LIMIT = -1;

-- Conectar ao banco (execute no pgAdmin)
-- \c centros_inovacao;

-- =====================================================
-- 1. TABELA ESTADO
-- =====================================================
CREATE TABLE estado (
    id_estado INTEGER PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    sigla CHAR(2) NOT NULL UNIQUE
);

COMMENT ON TABLE estado IS 'Tabela com todos os estados brasileiros e Distrito Federal';
COMMENT ON COLUMN estado.id_estado IS 'Chave primária';
COMMENT ON COLUMN estado.nome IS 'Nome completo do estado';
COMMENT ON COLUMN estado.sigla IS 'Sigla do estado (ex: SC, SP, RJ)';

-- Índice para busca por sigla
CREATE INDEX idx_estado_sigla ON estado(sigla);

-- =====================================================
-- 2. TABELA CIDADE
-- =====================================================
CREATE TABLE cidade (
    id_cidade INTEGER PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    id_estado INTEGER NOT NULL,
    CONSTRAINT fk_cidade_estado FOREIGN KEY (id_estado) 
        REFERENCES estado(id_estado) 
        ON DELETE RESTRICT 
        ON UPDATE CASCADE
);

COMMENT ON TABLE cidade IS 'Tabela com todas as cidades brasileiras';
COMMENT ON COLUMN cidade.id_cidade IS 'Chave primária';
COMMENT ON COLUMN cidade.nome IS 'Nome da cidade';
COMMENT ON COLUMN cidade.id_estado IS 'Chave estrangeira para estado';

-- Índices
CREATE INDEX idx_cidade_estado ON cidade(id_estado);
CREATE INDEX idx_cidade_nome ON cidade(nome);

-- =====================================================
-- 3. TABELA BAIRRO
-- =====================================================
CREATE TABLE bairro (
    id_bairro INTEGER PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    id_cidade INTEGER NOT NULL,
    CONSTRAINT fk_bairro_cidade FOREIGN KEY (id_cidade) 
        REFERENCES cidade(id_cidade) 
        ON DELETE RESTRICT 
        ON UPDATE CASCADE
);

COMMENT ON TABLE bairro IS 'Bairros das cidades';
COMMENT ON COLUMN bairro.id_bairro IS 'Chave primária';
COMMENT ON COLUMN bairro.nome IS 'Nome do bairro';
COMMENT ON COLUMN bairro.id_cidade IS 'Chave estrangeira para cidade';

-- Índices
CREATE INDEX idx_bairro_cidade ON bairro(id_cidade);
CREATE INDEX idx_bairro_nome ON bairro(nome);

-- =====================================================
-- 4. TABELA TIPO_LOGRADOURO
-- =====================================================
CREATE TABLE tipo_logradouro (
    id_tipo_de_logradouro INTEGER PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

COMMENT ON TABLE tipo_logradouro IS 'Tipos de logradouro (Rua, Avenida, Rodovia, etc.)';
COMMENT ON COLUMN tipo_logradouro.id_tipo_de_logradouro IS 'Chave primária';
COMMENT ON COLUMN tipo_logradouro.nome IS 'Nome do tipo de logradouro';

-- Índice para busca por nome
CREATE INDEX idx_tipo_logradouro_nome ON tipo_logradouro(nome);

-- =====================================================
-- 5. TABELA ENDERECO
-- =====================================================
CREATE TABLE endereco (
    id_endereco INTEGER PRIMARY KEY,
    nome_logradouro VARCHAR(100) NOT NULL,
    numero INTEGER,
    id_tipo_logradouro INTEGER NOT NULL,
    id_bairro INTEGER NOT NULL,
    CONSTRAINT fk_endereco_tipo_logradouro FOREIGN KEY (id_tipo_logradouro) 
        REFERENCES tipo_logradouro(id_tipo_de_logradouro) 
        ON DELETE RESTRICT 
        ON UPDATE CASCADE,
    CONSTRAINT fk_endereco_bairro FOREIGN KEY (id_bairro) 
        REFERENCES bairro(id_bairro) 
        ON DELETE RESTRICT 
        ON UPDATE CASCADE
);

COMMENT ON TABLE endereco IS 'Endereços completos';
COMMENT ON COLUMN endereco.id_endereco IS 'Chave primária';
COMMENT ON COLUMN endereco.nome_logradouro IS 'Nome do logradouro';
COMMENT ON COLUMN endereco.numero IS 'Número do endereço';
COMMENT ON COLUMN endereco.id_tipo_logradouro IS 'Chave estrangeira para tipo de logradouro';
COMMENT ON COLUMN endereco.id_bairro IS 'Chave estrangeira para bairro';

-- Índices
CREATE INDEX idx_endereco_tipo_logradouro ON endereco(id_tipo_logradouro);
CREATE INDEX idx_endereco_bairro ON endereco(id_bairro);

-- =====================================================
-- 6. TABELA TELEFONE
-- =====================================================
CREATE TABLE telefone (
    id_telefone INTEGER PRIMARY KEY,
    codigo_area CHAR(2),
    numero VARCHAR(30)
);

COMMENT ON TABLE telefone IS 'Números de telefone';
COMMENT ON COLUMN telefone.id_telefone IS 'Chave primária';
COMMENT ON COLUMN telefone.codigo_area IS 'Código de área (ex: 47, 48)';
COMMENT ON COLUMN telefone.numero IS 'Número do telefone';

-- Índice para busca
CREATE INDEX idx_telefone_numero ON telefone(numero);

-- =====================================================
-- 7. TABELA CONTATO
-- =====================================================
CREATE TABLE contato (
    id_contato INTEGER PRIMARY KEY,
    email VARCHAR(100) NOT NULL,
    id_telefone INTEGER NOT NULL,
    CONSTRAINT fk_contato_telefone FOREIGN KEY (id_telefone) 
        REFERENCES telefone(id_telefone) 
        ON DELETE RESTRICT 
        ON UPDATE CASCADE
);

COMMENT ON TABLE contato IS 'Contatos (emails e telefones)';
COMMENT ON COLUMN contato.id_contato IS 'Chave primária';
COMMENT ON COLUMN contato.email IS 'Email de contato';
COMMENT ON COLUMN contato.id_telefone IS 'Chave estrangeira para telefone';

-- Índices
CREATE INDEX idx_contato_telefone ON contato(id_telefone);
CREATE INDEX idx_contato_email ON contato(email);

-- =====================================================
-- 8. TABELA CONTATO_TELEFONE (N-N)
-- =====================================================
-- Relacionamento N-N entre CONTATO e TELEFONE
-- Permite que um contato tenha múltiplos telefones
-- e um telefone possa estar em múltiplos contatos
CREATE TABLE contato_telefone (
    id_contato_telefone INTEGER PRIMARY KEY,
    id_contato INTEGER NOT NULL,
    id_telefone INTEGER NOT NULL,
    CONSTRAINT fk_contato_telefone_contato FOREIGN KEY (id_contato) 
        REFERENCES contato(id_contato) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    CONSTRAINT fk_contato_telefone_telefone FOREIGN KEY (id_telefone) 
        REFERENCES telefone(id_telefone) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    CONSTRAINT uk_contato_telefone UNIQUE (id_contato, id_telefone)
);

COMMENT ON TABLE contato_telefone IS 'Relacionamento N-N entre CONTATO e TELEFONE';
COMMENT ON COLUMN contato_telefone.id_contato_telefone IS 'Chave primária';
COMMENT ON COLUMN contato_telefone.id_contato IS 'Chave estrangeira para contato';
COMMENT ON COLUMN contato_telefone.id_telefone IS 'Chave estrangeira para telefone';

-- Índices
CREATE INDEX idx_contato_telefone_contato ON contato_telefone(id_contato);
CREATE INDEX idx_contato_telefone_telefone ON contato_telefone(id_telefone);

-- =====================================================
-- 9. TABELA CENTROS_INOVACAO
-- =====================================================
CREATE TABLE centros_inovacao (
    id_centro INTEGER PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    ano_fundacao DATE,
    id_contato INTEGER NOT NULL,
    CONSTRAINT fk_centros_inovacao_contato FOREIGN KEY (id_contato) 
        REFERENCES contato(id_contato) 
        ON DELETE RESTRICT 
        ON UPDATE CASCADE
);

COMMENT ON TABLE centros_inovacao IS 'Centros de inovação e seus dados principais';
COMMENT ON COLUMN centros_inovacao.id_centro IS 'Chave primária';
COMMENT ON COLUMN centros_inovacao.nome IS 'Nome do centro de inovação';
COMMENT ON COLUMN centros_inovacao.ano_fundacao IS 'Ano de fundação do centro';
COMMENT ON COLUMN centros_inovacao.id_contato IS 'Chave estrangeira para contato';

-- Índices
CREATE INDEX idx_centros_inovacao_contato ON centros_inovacao(id_contato);
CREATE INDEX idx_centros_inovacao_nome ON centros_inovacao(nome);

-- =====================================================
-- 10. TABELA ENDERECO_CENTRO (N-N)
-- =====================================================
-- Relacionamento N-N entre CENTROS_INOVACAO e ENDERECO
-- Permite que um centro tenha múltiplos endereços
-- e um endereço possa estar vinculado a múltiplos centros
CREATE TABLE endereco_centro (
    id_endereco_centro INTEGER PRIMARY KEY,
    id_endereco INTEGER NOT NULL,
    id_centro INTEGER NOT NULL,
    CONSTRAINT fk_endereco_centro_endereco FOREIGN KEY (id_endereco) 
        REFERENCES endereco(id_endereco) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    CONSTRAINT fk_endereco_centro_centro FOREIGN KEY (id_centro) 
        REFERENCES centros_inovacao(id_centro) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    CONSTRAINT uk_endereco_centro UNIQUE (id_endereco, id_centro)
);

COMMENT ON TABLE endereco_centro IS 'Relacionamento N-N entre CENTROS_INOVACAO e ENDERECO';
COMMENT ON COLUMN endereco_centro.id_endereco_centro IS 'Chave primária';
COMMENT ON COLUMN endereco_centro.id_endereco IS 'Chave estrangeira para endereço';
COMMENT ON COLUMN endereco_centro.id_centro IS 'Chave estrangeira para centro de inovação';

-- Índices
CREATE INDEX idx_endereco_centro_endereco ON endereco_centro(id_endereco);
CREATE INDEX idx_endereco_centro_centro ON endereco_centro(id_centro);

-- =====================================================
-- 11. TABELA ATOR
-- =====================================================
CREATE TABLE ator (
    id_ator INTEGER PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo_ator VARCHAR(50),
    participa_programa VARCHAR(50),
    tamanho_ator VARCHAR(50),
    cnpj CHAR(14),
    id_centro INTEGER NOT NULL,
    CONSTRAINT fk_ator_centro FOREIGN KEY (id_centro) 
        REFERENCES centros_inovacao(id_centro) 
        ON DELETE RESTRICT 
        ON UPDATE CASCADE
);

COMMENT ON TABLE ator IS 'Atores que participam dos centros de inovação';
COMMENT ON COLUMN ator.id_ator IS 'Chave primária';
COMMENT ON COLUMN ator.nome IS 'Nome do ator';
COMMENT ON COLUMN ator.tipo_ator IS 'Tipo do ator (Empresa, Startup, Laboratório)';
COMMENT ON COLUMN ator.participa_programa IS 'Se participa de programas (Sim/Não)';
COMMENT ON COLUMN ator.tamanho_ator IS 'Tamanho do ator (Pequeno, Médio, Grande)';
COMMENT ON COLUMN ator.cnpj IS 'CNPJ do ator';
COMMENT ON COLUMN ator.id_centro IS 'Chave estrangeira para centro de inovação';

-- Índices
CREATE INDEX idx_ator_centro ON ator(id_centro);
CREATE INDEX idx_ator_nome ON ator(nome);
CREATE INDEX idx_ator_cnpj ON ator(cnpj);

-- =====================================================
-- 12. TABELA PROGRAMA
-- =====================================================
CREATE TABLE programa (
    id_programa INTEGER PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    ano_inicio DATE,
    descricao TEXT,
    id_ator INTEGER NOT NULL,
    CONSTRAINT fk_programa_ator FOREIGN KEY (id_ator) 
        REFERENCES ator(id_ator) 
        ON DELETE RESTRICT 
        ON UPDATE CASCADE
);

COMMENT ON TABLE programa IS 'Programas oferecidos pelos atores';
COMMENT ON COLUMN programa.id_programa IS 'Chave primária';
COMMENT ON COLUMN programa.nome IS 'Nome do programa';
COMMENT ON COLUMN programa.ano_inicio IS 'Ano de início do programa';
COMMENT ON COLUMN programa.descricao IS 'Descrição detalhada do programa';
COMMENT ON COLUMN programa.id_ator IS 'Chave estrangeira para ator';

-- Índices
CREATE INDEX idx_programa_ator ON programa(id_ator);
CREATE INDEX idx_programa_nome ON programa(nome);

-- =====================================================
-- VERIFICAÇÃO DA ESTRUTURA CRIADA
-- =====================================================

-- Listar todas as tabelas criadas
SELECT 
    schemaname,
    tablename,
    tableowner
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY tablename;

-- Verificar relacionamentos (Foreign Keys)
SELECT 
    tc.table_name AS tabela_origem,
    kcu.column_name AS coluna_origem,
    ccu.table_name AS tabela_destino,
    ccu.column_name AS coluna_destino,
    tc.constraint_name AS nome_constraint
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
    AND tc.table_schema = kcu.table_schema
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
    AND ccu.table_schema = tc.table_schema
WHERE tc.constraint_type = 'FOREIGN KEY'
    AND tc.table_schema = 'public'
ORDER BY tc.table_name, kcu.column_name;

-- =====================================================
-- FIM DO SCRIPT
-- =====================================================

