import threading # Mutex para controle de concorrência

# Mutex para controle de concorrência na leitura e escrita
trava_bd = threading.Lock()
arquivo_bd = 'banco.txt'

def _ler_linhas():
    try:
        with open(arquivo_bd, 'r') as f:
            return f.readlines()
    except FileNotFoundError:
        return []

def _salvar_linhas(linhas):
    with open(arquivo_bd, 'w') as f:
        f.writelines(linhas)

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
            linhas = _ler_linhas()
            if not linhas:
                return "Banco vazio."
            # Filtro opcional: SELECT WHERE id=X
            if len(partes) > 1 and partes[1].upper().startswith("WHERE"):
                criterio = partes[1].split("=", 1)
                if len(criterio) == 2:
                    id_buscado = criterio[1].strip()
                    resultado = [l for l in linhas if l.split(",")[0].strip() == id_buscado]
                    return "".join(resultado) if resultado else "Nenhum registro encontrado."
            return "".join(linhas)

        elif acao == "DELETE":
            if len(partes) < 2 or "=" not in partes[1]:
                return "Sintaxe: DELETE WHERE id=X"
            id_deletar = partes[1].split("=", 1)[1].strip()
            linhas = _ler_linhas()
            novas = [l for l in linhas if l.split(",")[0].strip() != id_deletar]
            if len(novas) == len(linhas):
                return "Nenhum registro encontrado."
            _salvar_linhas(novas)
            return f"Delete realizado ({len(linhas) - len(novas)} registro(s) removido(s))"

        elif acao == "UPDATE":
            # Sintaxe: UPDATE id=X campo=novo_valor
            if len(partes) < 2:
                return "Sintaxe: UPDATE id=X campo=novo_valor"
            try:
                partes_update = partes[1].split(" ", 1)
                id_atualizar = partes_update[0].split("=", 1)[1].strip()
                novo_valor = partes_update[1].strip()
            except (IndexError, ValueError):
                return "Sintaxe: UPDATE id=X campo=novo_valor"
            linhas = _ler_linhas()
            novas = []
            alterados = 0
            for l in linhas:
                if l.split(",")[0].strip() == id_atualizar:
                    novas.append(id_atualizar + ", " + novo_valor + "\n")
                    alterados += 1
                else:
                    novas.append(l)
            if not alterados:
                return "Nenhum registro encontrado."
            _salvar_linhas(novas)
            return f"Update realizado ({alterados} registro(s) alterado(s))"

        else:
            return "Comando SQL desconhecido"
