## 📚 Painel Administrativo - Sistema de Biblioteca

Este projeto consiste em um painel administrativo para gerenciamento de uma biblioteca, permitindo controle completo de usuários, livros e empréstimos.

🔗 **Acesse o projeto:** https://biblioteca-5e1y.onrender.com/

### 🚀 Funcionalidades

* Dashboard com dados gerais (livros, usuários, empréstimos e atividades)
* Cadastro, listagem e remoção de usuários e livros
* Sistema de empréstimo e devolução de livros
* Visualização de empréstimos em andamento

### 🔐 Controle de Acesso

O sistema possui dois níveis de acesso:

* **Usuário (espectador):** acesso apenas para visualização dos dados e dashboard
* **Administrador:** acesso total a todas as funcionalidades do sistema

### 🛠️ Tecnologias Utilizadas

* **Backend:** Python + Flask
* **Frontend:** HTML, CSS, JavaScript
* **Banco de Dados:** PostgreSQL (Supabase)
* **ORM:** SQLAlchemy

### ⚙️ Estrutura e Arquitetura

* Arquitetura baseada em MVC:

  * `models` (modelos do banco)
  * `services` (regras de negócio)
  * `routes` (rotas e controladores)
  * `templates` (interface)
  * `tests` (testes unitários com pytest)
* Uso de Blueprints para organização do projeto
* Senhas protegidas com hash
* Validações em múltiplas camadas

### 🗄️ Modelos de Dados

* Usuário
* Livro
* Empréstimo
* Espectador

### 🌐 Fluxo de Acesso

* Sistema com páginas de **cadastro**, **login** e **painel**
* Controle de sessão com redirecionamento automático (cadastro → login)

### 🧪 Ambiente

* Banco local para desenvolvimento e testes
* Banco em produção via Supabase (PostgreSQL)

---

Projeto focado em simular um sistema real, com boas práticas de organização, segurança e separação de responsabilidades.
