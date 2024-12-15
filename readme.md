
# Sistema de Tomada de Decisão

## Contexto da Atividade

Este sistema foi desenvolvido como parte de uma atividade prática para implementar uma parte de um sistema voltado para tomada de decisão. O sistema segue uma **Arquitetura em Camadas**, onde cada camada é responsável por uma parte do fluxo de dados e lógica. As camadas implementadas são:

1. **Camada de Acesso a Dados**: Responsável pela comunicação com o banco de dados e recuperação dos dados necessários.
2. **Camada de Modelo (Abstração)**: Definição das entidades do sistema, como `Ativo`, `Categoria` e `Indicador`.
3. **Camada de Controle (Regras de Negócios)**: Responsável pela implementação das regras de negócios que controlam o fluxo de dados, como o controle dos indicadores e a relação entre ativos e categorias.
4. **Camada de Interface Gráfica/Visualização (View)**: Apresentação de dados ao usuário, utilizando a biblioteca `Streamlit` para criar uma interface interativa.

### Objetivos do Sistema:

- Implementar funcionalidades para gerenciar ativos, categorias e indicadores financeiros.
- Oferecer uma interface gráfica interativa que permita ao usuário tomar decisões com base nos indicadores de ativos.
- Seguir a arquitetura em camadas para organizar o código de forma modular.

## Como Rodar

### 1. Instalar Dependências

Crie um ambiente virtual e instale as dependências listadas no arquivo `requirements.txt`. Você pode usar o seguinte comando:

```bash
pip install -r requirements.txt
```

As dependências necessárias para rodar o sistema são:

- `psycopg[binary] == 3.2.3`
- `python-dotenv == 1.0.1`
- `fastapi==0.115.6`
- `streamlit==1.40.2`

### 2. Configuração do Banco de Dados

Crie um arquivo `.env` na raiz do projeto e defina as variáveis de ambiente para a conexão com o banco de dados. O formato do arquivo `.env` deve ser o seguinte:

```env
DB_NAME=seu_nome_do_banco
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
```

### 3. Executar o Backend (API)

Primeiro, execute o arquivo `app.py` para rodar a API backend. No terminal, execute:

```bash
python app.py
```

Isso iniciará a API FastAPI no endereço padrão `http://localhost:8000`.

### 4. Executar o Frontend (Streamlit)

Após iniciar a API, execute o Streamlit para rodar a interface gráfica:

```bash
streamlit run streamlit_app.py
```

Isso abrirá a interface de administração e visualização dos dados no navegador.

## Estrutura do Banco de Dados

O banco de dados deve conter as seguintes tabelas:

### Tabela: public.assets

```sql
-- Table: public.assets

-- DROP TABLE IF EXISTS public.assets;

CREATE TABLE IF NOT EXISTS public.assets
(
    id integer NOT NULL DEFAULT nextval('assets_id_seq'::regclass),
    name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    type character varying(50) COLLATE pg_catalog."default" NOT NULL,
    category_id integer,
    CONSTRAINT assets_pkey PRIMARY KEY (id),
    CONSTRAINT assets_category_fkey FOREIGN KEY (category_id)
        REFERENCES public.categories (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE SET NULL
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.assets
    OWNER to postgres;
```

### Tabela: public.categories

```sql
-- Table: public.categories

-- DROP TABLE IF EXISTS public.categories;

CREATE TABLE IF NOT EXISTS public.categories
(
    id integer NOT NULL DEFAULT nextval('categories_id_seq'::regclass),
    name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    description text COLLATE pg_catalog."default",
    CONSTRAINT categories_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.categories
    OWNER to postgres;
```

### Tabela: public.indicators

```sql
-- Table: public.indicators

-- DROP TABLE IF EXISTS public.indicators;

CREATE TABLE IF NOT EXISTS public.indicators
(
    id integer NOT NULL DEFAULT nextval('indicators_id_seq'::regclass),
    name character varying(100) COLLATE pg_catalog."default" NOT NULL,
    value numeric(10,2) NOT NULL,
    asset_id integer NOT NULL,
    CONSTRAINT indicators_pkey PRIMARY KEY (id),
    CONSTRAINT indicators_asset_id_fkey FOREIGN KEY (asset_id)
        REFERENCES public.assets (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.indicators
    OWNER to postgres;
```

## Implementação das Camadas

### Camada de Acesso a Dados

A camada de acesso a dados é responsável pela comunicação com o banco de dados e recuperação dos dados necessários para o sistema. Abaixo temos a implementação de funções para realizar essas operações.

### Camada de Modelo

A camada de modelo define as classes que representam as entidades do sistema, como `Ativo`, `Categoria` e `Indicador`. Essas classes servem como abstração para o armazenamento e manipulação de dados.

### Camada de Controle

A camada de controle contém as regras de negócio que operam sobre os dados. Ela valida, processa e aplica as regras de decisão para manipulação dos dados. Exemplos de regras de negócio:

- Filtrar indicadores com base no ativo ou categoria.
- Mostrar os indicadores de ativos para que os gestores possam tomar decisões de investimento.

### Camada de Interface Gráfica

A camada de interface gráfica é responsável pela apresentação de dados ao usuário. O sistema utiliza `Streamlit` para criar gráficos interativos e apresentar as informações de forma amigável.

## Conclusão

Este sistema exemplifica como organizar um projeto em camadas e aplicar as boas práticas de separação de responsabilidades. A arquitetura facilita a manutenção e a escalabilidade do sistema, permitindo que novas funcionalidades sejam adicionadas com facilidade.

## Como Rodar

1. Configure o banco de dados e o arquivo `.env`.
2. Execute a API com `python app.py`.
3. Execute a interface gráfica com `streamlit run streamlit_app.py`.

## Scripts para Popular o Banco

### categories
```sql
-- Inserir categorias (para a tabela 'categories')
INSERT INTO public.categories (name, description) 
VALUES 
('Tecnologia', 'Produtos e serviços relacionados à tecnologia'),
('Saúde', 'Produtos e serviços relacionados à área de saúde'),
('Alimentos', 'Produtos e serviços relacionados a alimentos e bebidas'),
('Educação', 'Produtos e serviços voltados à educação');
```
### assets
```sql
-- Inserir ativos (para a tabela 'assets')
INSERT INTO public.assets (name, type, category_id) 
VALUES 
('Computador', 'Eletrônico', 1),  -- Categoria 'Tecnologia'
('Smartphone', 'Eletrônico', 1),  -- Categoria 'Tecnologia'
('Máquina de Café', 'Eletrodoméstico', 3),  -- Categoria 'Alimentos'
('Monitor', 'Eletrônico', 1),  -- Categoria 'Tecnologia'
('Ultrassom', 'Equipamento Médico', 2);  -- Categoria 'Saúde'
```
### indicators
```sql
-- Inserir indicadores (para a tabela 'indicators')
INSERT INTO public.indicators (name, value, asset_id) 
VALUES 
-- Indicadores para 'Computador' 
('Rentabilidade', 8.5, 22),   -- Rentabilidade do ativo 'Computador'
('Risco', 3.2, 22),           -- Risco do ativo 'Computador'
('Valor de Mercado', 5000.00, 1),  -- Valor de Mercado do ativo 'Computador'

-- Indicadores para 'Smartphone'
('Rentabilidade', 10.0, 1),  -- Rentabilidade do ativo 'Smartphone'
('Risco', 4.5, 23),           -- Risco do ativo 'Smartphone'
('Valor de Mercado', 3000.00, 23),  -- Valor de Mercado do ativo 'Smartphone'

-- Indicadores para 'Máquina de Café'
('Rentabilidade', 5.0, 3),   -- Rentabilidade do ativo 'Máquina de Café'
('Risco', 2.0, 24),           -- Risco do ativo 'Máquina de Café'
('Valor de Mercado', 1000.00, 24),  -- Valor de Mercado do ativo 'Máquina de Café'

-- Indicadores para 'Monitor' 
('Rentabilidade', 6.0, 4),   -- Rentabilidade do ativo 'Monitor'
('Risco', 3.0, 25),           -- Risco do ativo 'Monitor'
('Valor de Mercado', 1500.00, 25),  -- Valor de Mercado do ativo 'Monitor'

-- Indicadores para 'Ultrassom' 
('Rentabilidade', 12.0, 5),  -- Rentabilidade do ativo 'Ultrassom'
('Risco', 5.0, 26),           -- Risco do ativo 'Ultrassom'
('Valor de Mercado', 15000.00, 26); -- Valor de Mercado do ativo 'Ultrassom'
```
