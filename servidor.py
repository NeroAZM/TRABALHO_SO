import mmap # ler e editar arquivos pesados como se fossem leves, e garantir uma velocidade bem rapida nesse processo
import time
import threading # multiprocessamento, recebe varias requisições e lida ocm elas em paralelo
import banco # controle de concorrencias na leitura e escrita, além de ter a lógica dos comandos sql
from concurrent.futures import ThreadPoolExecutor

TAMANHO_POOL = 4

def processar(comando):
    # O banco já tem o Mutex protegendo o .txt
    resposta = banco.executar_query(comando)
    # Salva a resposta no log
    with open("respostas.log", "a") as f:
        f.write(f"{comando} / Resposta: {resposta}\n")
    print(f"Processado: {comando}")

def iniciar_servidor():
    # criando arquivo mapeado em memoria (mmap), o -1 ele serve pra pegar um pedaço da RAM solta, sem ler nenhum arquivo em especifico, fazendo com que o servidor
    # e o cliente possam conversar. O -1 serve pra reservar um espaço temporário na RAM. O 1024 é só pra definir o tamanho, como são arquivos pequenos
    # 1kb tá bom dms, tagname é autoexplicativo, ele cria um nome pra identificar e permitir que o cliente e o servidor usem.
    memoria = mmap.mmap(-1, 1024, tagname="SGBD_IPC")

    # Define a posição como Livre (0)
    memoria[0] = 0

    print("Servidor monitorando memória compartilhada")

    with ThreadPoolExecutor(max_workers=TAMANHO_POOL) as pool:
        while True:
            # Se a posição 0 for igual a 1, o cliente mandou algo
            if memoria[0] == 1:
                # rstrip(b'\x00') limpa todo o espaço vazio (zeros) do final de uma vez só
                comando = memoria[1:].rstrip(b'\x00').decode('utf-8')

                # Envia para o pool em vez de criar thread avulsa
                pool.submit(processar, comando)

                # Libera a memória NA MESMA HORA para o próximo cliente usar
                memoria[0] = 0

            time.sleep(0.1)

if __name__ == "__main__":
    iniciar_servidor()