import mmap # ler e editar arquivos pesados como se fossem leves, e garantir uma velocidade bem rapida nesse processo
import time

def iniciar_cliente():
    try:
        # criando arquivo mapeado em memoria (mmap), o -1 ele serve pra pegar um pedaço da RAM solta, sem ler nenhum arquivo em especifico, fazendo com que o servidor
        # e o cliente possam conversar. O -1 serve pra reservar um espaço temporário na RAM. O 1024 é só pra definir o tamanho, como são arquivos pequenos
        # 1kb tá bom dms, tagname é autoexplicativo, ele cria um nome pra identificar e permitir que o cliente e o servidor usem.
        memoria = mmap.mmap(-1, 1024, tagname="SGBD_IPC")
    except Exception:
        print("Erro: Precisa iniciar o servidor primeiro")
        return

    print("\n Conectado.\n Comandos disponiveis atualmente: INSERT e SELECT \n Ex: INSERT 1, Lucas \n Digite 'sair' para fechar.")
    
    while True:
        comando = input("\nSQL> ")
        if comando.lower() == 'sair':
            break
        # Trava aqui enquanto a memória não estiver Livre (0)
        while memoria[0] != 0:
            time.sleep(0.1)

        # antes de escrever limpa a memória com zeros, pra prevenir lixo de memoria
        memoria[1:] = b'\x00' * 1023

        # escreve o comando novo
        comando_bytes = comando.encode('utf-8')
        memoria[1:] = comando_bytes.ljust(1023, b'\x00') # justifica a esquerda e preenche o espaço restante com zero, pra nao dar conflito de lixo de memoria
        
        # Muda a posição de 0 para 1 (avisando o servidor q já pode ler)
        memoria[0] = 1
        
        print("Enviado! Só olhar o arquivo respostas.log")

if __name__ == "__main__":
    iniciar_cliente()