import threading 

# Mutex para controle de concorrência na leitura e escrita
trava_bd = threading.Lock()
arquivo_bd = 'banco.txt'

def executar_query(comando):
    # Separa o comando (ex: "insert bla bla bla"
    partes = comando.split(" ", 1)
    acao = partes[0].upper()
    
    # Pega o lock antes de mexer no arquivo
    with trava_bd:
        if acao == "INSERT":
            dados = partes[1]
            with open(arquivo_bd, 'a') as f:
                f.write(dados + '\n')
            return "Insert realizado"
            
        elif acao == "SELECT":
            try:
                with open(arquivo_bd, 'r') as f:
                    linhas = f.readlines()
                return "".join(linhas) if linhas else "Banco vazio."
            except FileNotFoundError:
                return "Banco vazio."
        
        # Falta adicionar DELETE e UPDATE, rapazes!
        else:
            return "Comando SQL desconhecido"