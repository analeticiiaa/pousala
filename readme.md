# Pousa.Lá

Projeto desenvolvido por **Ana Letícia Nobre da Silva**, inspirado em plataformas como o Booking.com.

 **Acesse o sistema online:**
👉 https://pousala.pythonanywhere.com/

---

## Sobre o Projeto

O **Pousa.Lá** é um sistema de reservas de hospedagem que permite que usuários encontrem, avaliem e reservem propriedades de forma simples e intuitiva.

A aplicação foi desenvolvida com foco em conceitos de **Programação Orientada a Objetos (POO)**, organização de dados e simulação de um sistema real de reservas, semelhante a plataformas conhecidas do mercado.

---

## Objetivo

O objetivo do projeto é simular um ambiente de hospedagem online onde:

* Hóspedes podem buscar e reservar locais
* Anfitriões podem anunciar propriedades
* Usuários podem interagir, avaliar e favoritar imóveis

---

## Funcionalidades

###  1. Login / Cadastro

* Permite criação de contas e autenticação de usuários
* Vincula ações (reservas, favoritos) ao usuário

---

###  2. Busca de Propriedades

* Filtragem por:
  * Localização
  * Quantidade de pessoas
  * Datas
* Mostra apenas propriedades disponíveis

---

### 3. Favoritos

* Permite salvar propriedades de interesse
* Facilita acesso rápido sem nova busca

---

###  4. Chat de Contato Direto

* Comunicação entre hóspede e anfitrião
* Permite tirar dúvidas sobre a propriedade

---

### 5. Sistema de Reservas

* Reserva propriedades por período
* Após confirmação:
  * o local fica indisponível para outros usuários

---

### 6. Avaliação com Estrelas

* Usuários avaliam propriedades
* Média das notas fica visível

---

### 7. Avaliação com Comentários

* Feedback textual sobre a experiência
* Ajuda outros usuários na decisão

---

###  8. Seção de Dúvidas

* Lista de perguntas frequentes
* Evita contato desnecessário com o anfitrião

---

###  9. Anunciar Propriedade

* Anfitriões podem cadastrar novos imóveis
* Propriedades ficam disponíveis para busca

---

### 10. Minhas Reservas

* Exibe reservas do usuário
* Organização por status:
  * Ativa
  * Concluída

---

##  Conceitos Aplicados

O projeto utiliza fortemente conceitos de **POO**:

* **Herança** → Usuário, Hóspede e Anfitrião
* **Encapsulamento** → Atributos privados e uso de `@property`
* **Polimorfismo** → Métodos como `mostrar_painel()`

---

##  Tecnologias Utilizadas

* Python 
* Programação Orientada a Objetos (POO)
* Banco de Dados 
* PythonAnywhere (deploy)

---

## 📂 Estrutura do Projeto

* `app.py` ➔ Controlador web (Rotas do Flask e integração com o frontend).
* `sistema.py` ➔ Fachada (Facade) e domínio da aplicação contendo as regras de negócio (POO).
* `banco.py` ➔ DAO (Data Access Object) responsável pelas operações de CRUD no banco SQLite.
* `pousala.db` ➔ Banco de dados local.
* `/templates/` ➔ Diretório contendo todas as interfaces (Views) em HTML.

---
##  Como Executar

1. Clone o repositório:

```bash
git clone https://github.com/analeticiiaa/pousala.git
```

2. Acesse a pasta:

```bash
cd pousala
```

3. Execute o projeto (dependendo da estrutura):

```bash
python app.py
```

---

## Deploy

O sistema está disponível online em:

 https://pousala.pythonanywhere.com/

---

## 👩‍💻 Autora

**Ana Letícia Nobre da Silva**