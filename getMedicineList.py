# Importação das bibliotecas necessárias para manipulação de dados, scraping e interação com o banco de dados.
import re  # Para expressões regulares, usadas para limpar o texto.
from datetime import datetime  # Para trabalhar com data e hora.
from selenium import webdriver  # Para usar o Selenium WebDriver (automação de navegador).
from selenium.webdriver.common.by import By  # Para localizar elementos no HTML da página.
from selenium.webdriver.chrome.service import Service  # Para gerenciar o serviço do ChromeDriver.
from selenium.webdriver.chrome.options import Options  # Para configurar o WebDriver.
from selenium.webdriver.support.ui import WebDriverWait  # Para aguardar a presença de elementos na página.
from selenium.webdriver.support import expected_conditions as EC  # Para definir as condições de espera.
from webdriver_manager.chrome import ChromeDriverManager  # Para gerenciar o download e instalação do ChromeDriver.
from conexao import MySQLConnection  # Classe de conexão para o MySQL, importada de outro arquivo.


def getDateTime():
    """
    Gera a data e hora atuais.
    :return: Data e hora como string formatada no formato "dia/mês/ano hora:minuto:segundo".
    """
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")  # Retorna a data e hora atuais no formato específico.


def setup_driver(headless=True):
    """
    Configura e retorna uma instância do WebDriver.
    :param headless: Define se o navegador será executado em modo headless (sem interface gráfica).
    :return: Instância configurada do WebDriver.
    """
    chrome_options = Options()  # Criação de um objeto de configuração para o navegador.

    if headless:
        chrome_options.add_argument("--headless")  # Modo headless, para rodar sem interface gráfica.

    # Configurações adicionais para melhorar a performance e evitar erros:
    chrome_options.add_argument("--disable-gpu")  # Desabilita a aceleração de GPU.
    chrome_options.add_argument("--no-sandbox")  # Necessário para rodar o Chrome em containers (por exemplo, Docker).
    chrome_options.add_argument("--ignore-certificate-errors")  # Ignora erros de certificado SSL.
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Desativa a detecção de automação.
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Desativa a detecção do Selenium.
    chrome_options.add_experimental_option("useAutomationExtension",
                                           False)  # Desativa a extensão de automação do Chrome.

    # Cria um serviço com o ChromeDriver e instala o driver automaticamente.
    service = Service(ChromeDriverManager().install())

    # Retorna o WebDriver com as configurações especificadas.
    return webdriver.Chrome(service=service, options=chrome_options)


def fetch_page_content(driver, url):
    """
    Acessa uma página usando o WebDriver.
    :param driver: Instância do WebDriver.
    :param url: URL da página que será acessada.
    """
    try:
        driver.get(url)  # Carrega a página na instância do WebDriver.
    except Exception as e:
        print(f"Erro ao acessar a página {url}: {e}")  # Caso ocorra um erro, é mostrado no console.
        raise  # Levanta a exceção para interromper o fluxo, se necessário.


def extract_list_after_div(driver, div_class):
    """
    Localiza a lista (<ul>) imediatamente após uma <div> com a classe especificada.
    :param driver: Instância do WebDriver.
    :param div_class: Classe da <div> que precede a lista.
    :return: Lista de itens (<li>) como textos.
    """
    # Cria o XPath que localiza a lista (<ul>) logo após a <div> com a classe fornecida.
    div_xpath = f'//div[contains(@class, "{div_class}")]/following-sibling::ul[1]'

    try:
        # Aguarda até que o elemento <ul> esteja presente na página.
        ul_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, div_xpath))
        )
        # Encontra todos os itens de lista (<li>) dentro da <ul> localizada.
        li_elements = ul_element.find_elements(By.TAG_NAME, "li")
        # Retorna os textos de cada item <li>.
        return [li.text for li in li_elements]
    except Exception as e:
        # Caso haja erro, registra no log e retorna uma lista vazia.
        logging.error(f"Erro ao localizar a lista após a div com classe '{div_class}': {e}")
        return []


def clean_function(funcao):
    """
    Limpa a função, removendo o conteúdo entre colchetes (por exemplo, '[2]').
    :param funcao: Função como string.
    :return: Função limpa, sem o conteúdo entre colchetes.
    """
    # Remove o conteúdo entre colchetes e os próprios colchetes usando expressão regular.
    return re.sub(r'\[.*?\]', '', funcao).strip()


def process_items(items):
    """
    Processa os itens da lista, separando pelo caractere ":" para nome e função.
    :param items: Lista de itens, onde cada item pode ter um nome e uma função separados por ":".
    :return: Lista de tuplas com (nome, função).
    """
    processed_items = []  # Lista onde os itens processados serão armazenados.

    for item in items:
        if ":" in item:  # Verifica se o item contém o caractere ":".
            # Se houver ":", divide o item em duas partes: nome e função.
            nome, funcao = item.split(":", 1)  # Limita a divisão em 2 partes no máximo.
            nome = nome.strip()  # Remove espaços extras no nome.
            funcao = funcao.strip()  # Remove espaços extras na função.

            # Limpa o nome e a função, removendo conteúdo entre colchetes.
            nome = clean_function(nome)
            funcao = clean_function(funcao)
        else:
            nome = item.strip()  # Se não houver ":", considera o item como nome e deixa a função vazia.
            funcao = ""  # Função vazia.

        # Adiciona a tupla (nome, função) na lista de itens processados.
        processed_items.append((nome, funcao))

    # Retorna a lista de itens processados.
    return processed_items


def main():
    """
    Função principal que executa o fluxo de scraping, processa os itens e os insere no banco de dados.
    """
    # URLs base e final que formam o endereço completo da página.
    base_url = "https://pt.wikipedia.org/wiki/"
    end_url = "Lista_de_plantas_usadas_em_fitoterapia"
    url = base_url + end_url  # URL completa.

    # Classe da <div> que precede a lista de interesse.
    target_div_class = "mw-heading mw-heading2"

    # Instancia a classe de conexão com o banco de dados MySQL.
    db_connection = MySQLConnection()

    # Configura o WebDriver e abre o navegador.
    driver = setup_driver(headless=True)
    try:
        print(f"Execução em {getDateTime()}")  # Exibe a data e hora da execução.

        # Acessa o conteúdo da página.
        fetch_page_content(driver, url)

        # Extrai a lista de plantas após a <div> com a classe especificada.
        items = extract_list_after_div(driver, target_div_class)

        if items:
            # Processa os itens extraídos da página.
            processed_items = process_items(items)

            new_items = []  # Lista para armazenar itens novos a serem inseridos no banco de dados.

            for nome, funcao in processed_items:
                # Verifica se o item já existe no banco de dados.
                if db_connection.item_exists(nome):
                    continue  # Se o item já existir, pula a inserção.
                else:
                    # Se o item não existir, adiciona à lista de novos itens.
                    new_items.append((nome, funcao))

            # Se houver novos itens, insere-os no banco de dados.
            if new_items:
                db_connection.insert_items(new_items)
            else:
                print("Nenhum novo item para inserir.")  # Caso não haja novos itens.
        else:
            print(f"Nenhuma lista encontrada.")  # Caso não encontre a lista.

    finally:
        # Encerra o driver (fecha o navegador).
        driver.quit()
        # Fecha a conexão com o banco de dados.
        db_connection.close()


# Verifica se o script está sendo executado diretamente e, se sim, chama a função main().
if __name__ == "__main__":
    main()
