# TRABALHO_SO

## Criado por:

- Lucas de Amorim Coelho
- Matheus Jaques Winter
- Nilson Hoffmann Neto.  

Trabalho da disciplina de Sistemas Operacionais — Professor Felipe Viel.

---

## Como executar

O sistema é composto por dois processos separados que se comunicam via memória compartilhada. Por isso, é necessário abrir **dois terminais**.

**Primeiro passo: terminal — inicie o servidor:**

**Segundo passo: terminal — inicie o cliente:**

O servidor precisa estar rodando antes do cliente, caso contrário a memória compartilhada ainda não existe e o cliente vai retornar um erro.

Com o cliente aberto, basta digitar os comandos SQL, exemplo:

```
SQL> INSERT 1, Lucas
SQL> SELECT WHERE id=1
SQL> UPDATE id=1 Lucas Atualizado
SQL> DELETE WHERE id=1
SQL> sair
```

As respostas ficam salvas no arquivo `respostas.log`. E a execução dos comandos bem-sucedidos ficam salvos no arquivo `banco.txt`.

---

## Observação

O projeto usa **mmap** com o parâmetro *tagname* para criar a memória compartilhada entre os processos. Esse parâmetro **só existe no Windows** — no Linux e no Mac o **mmap** funciona de forma diferente e não aceita **tagname**. Ou seja, o projeto foi desenvolvido e testado no Windows e não vai rodar em outros sistemas operacionais sem adaptação.
