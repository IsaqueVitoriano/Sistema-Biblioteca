CREATE TABLE IF NOT EXISTS editora (
    id VARCHAR(50) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS categoria (
    id VARCHAR(50) PRIMARY KEY,
    nome VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS autor (
    id VARCHAR(50) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS usuario (
    id VARCHAR(50) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    data_criacao TIMESTAMP NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    matricula VARCHAR(255) NOT NULL UNIQUE,
    tipo_usuario VARCHAR(20) CHECK (tipo_usuario IN ('SERVIDOR', 'PROFESSOR', 'ALUNO', 'ADMINISTRADOR'))
);

CREATE TABLE IF NOT EXISTS livro (
    id VARCHAR(50) PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    ano_publicacao DATE NOT NULL,
    id_editora VARCHAR(36) NOT NULL,
    id_categoria VARCHAR(36) NOT NULL,
    CONSTRAINT fk_livro_editora FOREIGN KEY (id_editora) REFERENCES editora(id),
    CONSTRAINT fk_livro_categoria FOREIGN KEY (id_categoria) REFERENCES categoria(id)
);

CREATE TABLE IF NOT EXISTS livro_autor (
    livro_id VARCHAR(50) NOT NULL,
    autor_id VARCHAR(36) NOT NULL,
    PRIMARY KEY (livro_id, autor_id),
    CONSTRAINT fk_livro_autor_livro FOREIGN KEY (livro_id) REFERENCES livro(id) ON DELETE CASCADE,
    CONSTRAINT fk_livro_autor_autor FOREIGN KEY (autor_id) REFERENCES autor(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS exemplar (
    id VARCHAR(50) PRIMARY KEY,
    situacao VARCHAR(30) NOT NULL DEFAULT 'DISPONIVEL'
        CHECK (situacao IN ('DISPONIVEL', 'DANIFICADO', 'EM_EMPRESTIMO', 'RETIRADO_DE_CIRCULACAO')),
    id_livro VARCHAR(36) NOT NULL,
    CONSTRAINT fk_exemplar_livro FOREIGN KEY (id_livro) REFERENCES livro(id)
);

CREATE TABLE IF NOT EXISTS emprestimo (
    id VARCHAR(50) PRIMARY KEY,
    situacao_emprestimo VARCHAR(20) NOT NULL DEFAULT 'PENDENTE'
        CHECK (situacao_emprestimo IN ('DEVOLVIDO', 'PENDENTE', 'ATRASADO')),
    data_emprestimo TIMESTAMP NOT NULL,
    data_devolucao_efetiva TIMESTAMP NULL,
    data_prazo_devolucao_efetiva TIMESTAMP NULL,
    id_usuario VARCHAR(50) NOT NULL,
    id_exemplar VARCHAR(50) NOT NULL,
    CONSTRAINT fk_emprestimo_usuario FOREIGN KEY (id_usuario) REFERENCES usuario(id),
    CONSTRAINT fk_emprestimo_exemplar FOREIGN KEY (id_exemplar) REFERENCES exemplar(id)
);