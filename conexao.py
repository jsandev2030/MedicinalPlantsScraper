import mysql.connector
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

class MySQLConnection:
    def __init__(self):
        """
        Inicializa a classe e carrega as variáveis de ambiente.
        """
        self.host = os.getenv("DB_HOST")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_DATABASE")
        self.conn = None
        self.cursor = None

    def connect(self):
        """
        Estabelece uma conexão com o banco de dados MySQL.
        :return: A conexão e o cursor do banco de dados.
        """
        if not self.conn or not self.conn.is_connected():
            try:
                self.conn = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database
                )
                self.cursor = self.conn.cursor()
                #print("Conexão estabelecida com sucesso!")
            except mysql.connector.Error as err:
                print(f"Erro ao conectar ao banco de dados: {err}")
                raise

        return self.conn, self.cursor

    def close(self):
        """
        Fecha a conexão e o cursor com o banco de dados.
        """
        if self.cursor:
            self.cursor.close()
        if self.conn and self.conn.is_connected():
            self.conn.close()
            #print("Conexão fechada com sucesso.")

    def insert_item(self, nome, funcao):
        """
        Insere um item na tabela com o índice e a função.
        :param nome: Nome da planta.
        :param funcao: Função/descrição da planta.
        """
        conn, cursor = self.connect()
        try:
            cursor.execute(f"INSERT INTO plantas_medicinais (nome, funcao) VALUES (%s, %s)", (nome, funcao))
            conn.commit()
            print(f"Item '{nome}' inserido com sucesso!")
        except mysql.connector.Error as err:
            print(f"Erro ao inserir item '{nome}': {err}")
        finally:
            self.close()

    def insert_items(self, items):
        """
        Insere múltiplos itens de uma vez na tabela.
        :param items: Lista de tuples, cada tupla deve ser (nome da planta, função).
        """
        conn, cursor = self.connect()
        try:
            cursor.executemany(
                "INSERT INTO plantas_medicinais (nome, funcao) VALUES (%s, %s)",
                items  # Agora a lista de items já tem apenas dois elementos (nome, funcao)
            )
            conn.commit()
            print(f"{len(items)} itens inseridos com sucesso!")
        except mysql.connector.Error as err:
            print(f"Erro ao inserir itens: {err}")
        finally:
            self.close()

    def item_exists(self, nome):
        """
        Verifica se o item já existe no banco de dados.
        :param nome: Nome da planta a ser verificado.
        :return: True se o item existir, False caso contrário.
        """
        conn, cursor = self.connect()
        try:
            cursor.execute("SELECT COUNT(*) FROM plantas_medicinais WHERE nome = %s", (nome,))
            result = cursor.fetchone()
            return result[0] > 0  # Retorna True se houver pelo menos um item com esse nome
        except mysql.connector.Error as err:
            print(f"Erro ao verificar a existência do item '{nome}': {err}")
            return False
        finally:
            self.close()
