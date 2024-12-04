# Web Scraping de Plantas Medicinais para Fitoterapia

Este script realiza um **web scraping** na página da Wikipédia "Lista de plantas usadas em fitoterapia" para extrair informações sobre as plantas e suas respectivas funções. Ele processa esses dados e os insere em um banco de dados MySQL, verificando previamente se os itens já existem na base para evitar duplicatas.

## Funcionalidades

- **Web Scraping**: Utiliza o Selenium WebDriver para acessar a página da Wikipédia e extrair uma lista de itens.
- **Processamento de Dados**: Divide cada item em nome e função, limpa os dados removendo conteúdo indesejado entre colchetes.
- **Banco de Dados MySQL**: Insere novos itens no banco de dados, evitando duplicatas.

## Requisitos

Antes de executar o script, certifique-se de que o ambiente esteja configurado corretamente:

- **Python 3.6+**
- **MySQL Database** para armazenar os dados extraídos. 

As bibliotecas a seguir (instale-as usando `pip install`):

```bash
pip install selenium mysql-connector-python webdriver-manager
```

## Dependências
- **Selenium**: Para automação do navegador e web scraping.
- **webdriver-manager**: Para gerenciar o ChromeDriver automaticamente.
- **re (expressões regulares)**: Para limpar as funções, removendo conteúdo entre colchetes.
- **MySQL**: Para armazenar os dados extraídos.

## Como Usar
### 1- Configuração do Banco de Dados

Certifique-se de ter um banco de dados MySQL configurado. O script assume que você tem uma classe MySQLConnection 
(importada de conexao.py) configurada para se conectar ao banco de dados e inserir dados.

Caso ainda não tenha configurado o banco de dados, você pode modificar a classe MySQLConnection ou criar um banco 
de dados com a seguinte estrutura:

```bash
CREATE DATABASE fitoterapia;
USE fitoterapia;

CREATE TABLE plantas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    funcao TEXT
);
```


### 2- Configuração do Script

Modifique a URL da página da Wikipédia e a classe da 'div' que contém a lista de plantas (caso necessário).
Certifique-se de que o MySQL esteja acessível e a classe MySQLConnection esteja configurada corretamente.


### 3- Execução

Para rodar o script, basta executá-lo diretamente:
```bash
python nome_do_script.py
```

#### O script irá:

- Acessar a página da Wikipédia.
- Extrair a lista de plantas e suas funções.
- Processar e limpar os dados.
- Inserir os dados no banco de dados MySQL (somente os novos itens).


## Estrutura do Código
- **getDateTime()**: Retorna a data e hora atual formatada como string.
- **setup_driver()**: Configura e retorna uma instância do WebDriver.
- **fetch_page_content()**: Acessa uma página usando o WebDriver.
- **extract_list_after_div()**: Localiza e extrai a lista de itens que vem após uma <div> com a classe fornecida.
- **clean_function()**: Limpa a função, removendo conteúdo entre colchetes.
- **process_items()**: Processa a lista extraída, separando o nome e a função de cada item.
- **main()**: Controla o fluxo principal, realizando as etapas de scraping, processamento e inserção no banco de dados.


## Exemplo de Saída
Ao rodar o script, você verá no terminal uma saída semelhante a esta:
```bash
Execução em 04/12/2024 22:44:06
xxx itens inseridos com sucesso!
```

Se não houver novos itens para inserir:
```bash
Execução em 04/12/2024 22:44:06
Nenhum novo item para inserir.
```

## Licença
Este projeto está licenciado sob a [MIT License](https://opensource.org/license/mit).

### Explicação do conteúdo:

- **Introdução**: Explica o que o script faz, ou seja, realiza web scraping na Wikipédia para obter informações sobre 
plantas usadas em fitoterapia e insere essas informações em um banco de dados MySQL.
- **Requisitos**: Lista as bibliotecas necessárias para rodar o script, com o comando para instalá-las.
- **Como Usar**: Instruções detalhadas sobre como configurar e executar o script, incluindo a configuração do banco 
de dados e a execução do script.
- **Estrutura do Código**: Explica brevemente o que cada função faz dentro do código.
- **Exemplo de Saída**: Mostra exemplos de como o script pode se comportar quando executado.
- **Licença**: Um aviso de licença, caso você queira disponibilizar o código sob uma licença aberta, como a MIT.

Este `README.md` fornece uma explicação clara de como usar o script, o que ele faz e como configurá-lo corretamente.


## Autor
Este projeto foi desenvolvido por [Jonathan Alves](https://www.linkedin.com/in/jonathan-s-alves/). 

