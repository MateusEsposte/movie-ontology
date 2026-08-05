# Movie Recommendation System using Ontologies

Sistema de recomendação de filmes baseado em ontologias, desenvolvido como projeto da disciplina de **Engenharia de Ontologias**.

O projeto utiliza uma ontologia OWL/RDF como base de conhecimento para representar filmes, pessoas, usuários e seus relacionamentos, permitindo a geração de recomendações por meio de diferentes estratégias.

---

## Funcionalidades

### Usuário

- Cadastro e autenticação de usuários
- Consulta ao catálogo de filmes
- Registro de filmes assistidos
- Avaliação de filmes
- Cadastro e gerenciamento de preferências
- Gerenciamento de amizades
- Recomendações personalizadas baseadas em:
  - Preferências
  - Amigos
  - Comunidade
- Logout sem necessidade de reiniciar a aplicação

### Administrador

- Cadastro e remoção de filmes
- Cadastro e remoção de atores
- Cadastro e remoção de diretores
- Cadastro e remoção de roteiristas
- Cadastro e remoção de temas
- Cadastro e remoção de idiomas
- Cadastro e remoção de países
- Importação de filmes em lote por arquivos CSV

---

# Tecnologias Utilizadas

## Linguagem

- Python 3

## Framework

- CustomTkinter

## Bibliotecas

- Owlready2
- Tkinter
- hashlib
- csv

## Web Semântica

- OWL
- RDF/XML

## Ferramentas

- Protégé
- Git
- GitHub

---

# Estrutura do Projeto

```
projeto/
│
├── constants/
├── database/
├── frontend/
│   ├── components/
│   ├── controllers/
│   └── views/
├── models/
├── ontology/
├── services/
│
├── main.py
├── requirements.txt
└── README.md
```

---

# Sistema de Recomendação

O sistema implementa três estratégias distintas de recomendação.

### 1. Recomendação baseada em Preferências

Utiliza as preferências cadastradas pelo usuário.

São consideradas preferências sobre:

- Tema
- Diretor
- Ator
- Filme específico

Cada preferência possui um nível de interesse utilizado como peso durante o cálculo da recomendação.

---

### 2. Recomendação por Amigos

Implementa filtragem colaborativa utilizando apenas usuários que possuem relação de amizade com o usuário autenticado.

A similaridade entre usuários é calculada utilizando Similaridade do Cosseno sobre as avaliações em comum.

---

### 3. Recomendação pela Comunidade

Semelhante à recomendação por amigos, porém considerando todos os usuários cadastrados no sistema.

---

# Arquitetura

A aplicação foi organizada em camadas.

```
Interface (CustomTkinter)
          │
          ▼
      Services
          │
          ▼
Ontology Repository
          │
          ▼
Ontology Manager
          │
          ▼
 movie_ontology.rdf
```

---

# Como Executar

## 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd projeto
```

## 2. Crie um ambiente virtual

Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

## 3. Instale as dependências

```bash
pip install -r requirements.txt
```

## 4. Execute

```bash
python main.py
```

---

# Base de Conhecimento

Toda a persistência do sistema é realizada diretamente na ontologia.

São armazenados:

- Filmes
- Usuários
- Atores
- Diretores
- Roteiristas
- Temas
- Idiomas
- Países
- Preferências
- Avaliações
- Amizades

Não é utilizado banco de dados relacional.

---

# Observações

As recomendações colaborativas dependem da existência de avaliações em comum entre os usuários.

Usuários recém-criados podem inicialmente receber apenas recomendações baseadas em preferências, caracterizando o problema conhecido como **Cold Start**, comum em sistemas de recomendação.

---

# Autores
Mateus da Cruz Esposte (13862650)

Projeto desenvolvido para a disciplina de Engenharia de Ontologias.

**Universidade de São Paulo (USP)**

Curso de Sistemas de Informação

---

# Licença

Este projeto foi desenvolvido exclusivamente para fins acadêmicos.
