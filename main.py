import time

pessoas_declaradas = []

def se_declarar_viado():
    nome = input("Qual teu nome viado? -> ")
    idade = input("Qual tua idade viado? -> ")
    escolaridade = input("Tu é uma anta ou faz algo? -> ")
    trabalho = input("Trabalha de que? -> ")

    dados = [nome, idade, escolaridade, trabalho]
    pessoas_declaradas.append(dados)

def ver_lista_de_gls():
    tarefas = ['nome','idade', 'escolaridade', 'trabalho']
    for pessoa in pessoas_declaradas:
        contador = 0
        for dados in pessoa:
            print(f'{tarefas[contador]} -> {dados}')
            contador += 1

while True:
    time.sleep(2)
    print("""
---------- LOJINHA DA VIADA ( MARYY ) ----------
1 - Se declarar viado
2 - Ver lista de viados declarados
3 - Remover algum viado declarado
0 - Sair""")
    entrada = int(input("INSIRA UMA OPÇÃO! -> "))

    if entrada == 0:
        print("SAINDO DA LOJINHA DA VIADA!")
        break
    elif entrada == 1:
        print('Vamos fazer voce se declarar viado')
        se_declarar_viado()
        print(pessoas_declaradas)
    elif entrada == 2:
        print('Quer ver a lista dos GLS pra que em viado')
        ver_lista_de_gls()
    elif entrada == 3:
        print('Quem que tu quer remover dos viado seu inxerido?')
    else:
        print("Deu ruim!")
