from modelos.livro import Livro
import os

def menu():
    print('Escolha o que deseja fazer.\n')
    print('1- Adicionar livro')
    print('2- Listar livro(s)')
    print('3- Mudar status')
    print('4- Pesquisar livro')
    print('5- Transformar em .CSV')
    print('6- remover item') 
    print('7- resetar banco de dados\n')
    
    try:
        return int(input('Resposta: '))
    except ValueError:
        print('Entrada inválida')
        return 0 

def adicionar():
    print('Adicionar novo livro\n')
    nome = input('Nome do livro: ')

    try:
        pagina = int(input('Número de páginas: '))
    except ValueError:
        print('Dado inválido')
        return
    
    categoria = input('Categoria principal: ')
    status = input('1 para "Lindo" ou 2 para "Na fila": ')
    status_lido = True if status.strip() == '1' else False

    try:
        livro = Livro(nome, pagina, status_lido, categoria)
        livro.salvar() 
    except ValueError as e:
        print(f'Erro ao adicionar livro: {e}')

def alterar():
    print('Mudando o status do livro')
    try:
        id = int(input('Coloque o id do livro que vc deseja alterar: '))
    except ValueError:
        print('Dado inválido')
        return
    Livro.alterar_status(id)

def pesquisar():
    pesquisa = input('O que deseja procurar: ')
    Livro.filtrar(pesquisa)

def remover():
    print('Removendo Livro: \n')
    try:
        id_livro = int(input('Id do livro a ser excluido: ')
    except ValueError:
        print('Dado inválido')
        return
    Livro.deletar_item(id_livro)

def executar(resposta:int) -> None:
    try:
        match resposta:
            case 1:
                adicionar()
            case 2:
                print('Listando os livros\n')
                Livro.listar()
            case 3:
                alterar()
            case 4:
                pesquisar()
            case 5:
                print('Transformando em arquivo CSV: ')
                Livro.exporta_csv()
            case 6:
                remover()
            case 7:
                print('Resetando Banco de dados')
                Livro.resetar_banco()
            case _:
                print('Opção inválida')
    except ValueError as e:
        print(f'Erro de valor: {e}')
    except Exception as e:
        print(f'Ocorreu um erro: {e}')

def limpar():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    try: 
        while True:
            limpar()
            resposta = menu()
            limpar()
            executar(resposta)

            if input('Deseja continuar? (s/n): ').strip().lower() != 's':
                break
    except KeyboardInterrupt:
        print('Interrompido pelo usuário')
    
if __name__ == '__main__':
    main()

