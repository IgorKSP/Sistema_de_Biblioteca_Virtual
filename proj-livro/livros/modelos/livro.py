import sqlite3
import os
import logging
import csv
from pydantic import BaseModel, Field, ValidationError

# Configuração do log
logging.basicConfig(
    filename='livros.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Modelo de validação com Pydantic
class LivroModel(BaseModel):
    nome: str = Field(min_length=1)
    paginas: int = Field(gt=0)
    status: bool = False
    categoria: str = Field(min_length=1)

class Livro:
    def __init__(self, nome: str, paginas: int, status: bool = False, categoria: str = ""):
        try:
            validado = LivroModel(
                nome=nome.strip(),
                paginas=paginas,
                status=status,
                categoria=categoria.strip()
            )
            self._nome = validado.nome.title()
            self._paginas = validado.paginas
            self._status = validado.status
            self._categoria = validado.categoria.upper()
            self.criar_tabela()
        except ValidationError as e:
            logging.error('Erro de validação: %s', e)
            raise ValueError('Dados inválidos:\n' + str(e))

    @staticmethod
    def chamarbd(sql, params=(), fetch=False, delt=False):
        try:
            with sqlite3.connect('livros.db') as conn:
                cursor = conn.cursor()
                cursor.execute(sql, params)
                resultado = cursor.fetchall() if fetch else None
                delet = cursor.rowcount if delt else None
                conn.commit()
                return resultado if fetch else delet
        except sqlite3.Error as e:
            logging.error('Erro ao executar SQL: %s | Params: %s | Erro: %s', sql, params, e)
            return None

    @staticmethod
    def criar_tabela():
        sql = '''
            CREATE TABLE IF NOT EXISTS livros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                pagina INTEGER NOT NULL,
                status BOOLEAN NOT NULL,
                categoria TEXT
            )
        '''
        Livro.chamarbd(sql)
        logging.info('Tabela criada/verificada.')

    def salvar(self):
        sql = '''
            INSERT INTO livros (nome, pagina, status, categoria)
            VALUES (?, ?, ?, ?)
        '''
        resultado = Livro.chamarbd(sql, (self._nome, self._paginas, self._status, self._categoria))
        if resultado:
            logging.info('Livro salvo: %s', self._nome)
        else:
            logging.error('Falha ao salvar o livro: %s', self._nome)

    @staticmethod
    def listar():
        sql = 'SELECT id, nome, pagina, status, categoria FROM livros'
        livros = Livro.chamarbd(sql, fetch=True)

        if not livros:
            print('Nenhum livro cadastrado.')
            return

        print(f'{"ID":<5}  {"Nome":<25}  {"Páginas":<10}  {"Status":<10}  {"Categoria"}')
        print('-' * 60)
        for livro in livros:
            status = Livro.status_texto(livro[3])
            print(f'{livro[0]:<5} {livro[1]:<25} {livro[2]:<10} {status:<10} {livro[4]}')
        print(f'\nTotal de livros: {len(livros)}')

    @staticmethod
    def alterar_status(id_livro):
        sql = 'SELECT status FROM livros WHERE id = ?'
        resultado = Livro.chamarbd(sql, (id_livro,), fetch=True)
        if resultado:
            novo_status = not resultado[0][0]
            sql_up = 'UPDATE livros SET status = ? WHERE id = ?'
            Livro.chamarbd(sql_up, (novo_status, id_livro))
            logging.info('Status alterado para ID %s: %s', id_livro, novo_status)
        else:
            print('Livro não encontrado.')
            logging.warning('Tentativa de alterar status de ID inexistente: %s', id_livro)

    @staticmethod
    def filtrar(palavra_chave: str):
        palavra = f'%{palavra_chave.strip()}%'
        sql = '''
            SELECT id, nome, pagina, status, categoria
            FROM livros
            WHERE nome LIKE ? OR categoria LIKE ?
        '''
        livros = Livro.chamarbd(sql, (palavra, palavra), fetch=True)
        print('\nLivros encontrados:\n')
        if livros:
            for livro in livros:
                status = Livro.status_texto(livro[3])
                print(f'{livro[0]} | {livro[1]} | {livro[2]} páginas | Status: {status} | Categoria: {livro[4]}')
        else:
            print('Nenhum livro encontrado.')
        logging.info('Filtro aplicado com palavra-chave: %s', palavra_chave)

    @staticmethod
    def status_texto(status: bool) -> str:
        return 'Lido' if status else 'Na fila'

    @staticmethod
    def resetar_banco():
        if os.path.exists('livros.db'):
            os.remove('livros.db')
            logging.warning('Banco de dados removido.')
        Livro.criar_tabela()
        print('Banco de dados resetado.')

    @staticmethod
    def deletar_item(palavra_chave):
        palavra = f'%{palavra_chave.strip()}%'
        sql = '''
            DELETE FROM livros
            WHERE nome LIKE ? OR id LIKE ?
        '''
        deletado = Livro.chamarbd(sql, (palavra, palavra), delt=True)

        if deletado:
            print('Item excluído.')
            logging.info('Livro ID %s excluído', palavra)
        else:
            print('Livro não encontrado.')
            logging.warning('Tentativa de deletar ID inexistente: %s', palavra)

    @staticmethod
    def exporta_csv(caminho='livros_exportado.csv'):
        sql = 'SELECT id, nome, pagina, status, categoria FROM livros'
        livros = Livro.chamarbd(sql, fetch=True)

        if not livros:
            print('Nenhum livro para exportar.')
            return

        try:
            with open(caminho, mode='w', newline='', encoding='utf-8') as arquivo:
                escritor = csv.writer(arquivo)
                escritor.writerow(['ID', 'Nome', 'Páginas', 'Status', 'Categoria'])
                for livro in livros:
                    escritor.writerow([
                        livro[0],
                        livro[1],
                        livro[2],
                        Livro.status_texto(livro[3]),
                        livro[4]
                    ])
            print(f'Exportado com sucesso para "{caminho}".')
            logging.info('Exportação CSV realizada: %s', caminho)
        except Exception as e:
            print(f'Erro ao exportar: {e}')
            logging.error('Erro ao exportar CSV: %s', e)
