from logica import *

import termcolor

mostarda = Simbolo("AmigoMostarda")
ameixa = Simbolo("Professor. Ameixa")
damasco = Simbolo("Srta. Damasco")
personagens = [mostarda, ameixa, damasco]

salao = Simbolo("salao")
cozinha = Simbolo("cozinha")
biblioteca = Simbolo("biblioteca")
comodos = [salao, cozinha, biblioteca]

faca = Simbolo("faca")
revolver = Simbolo("revolver")
chave_inglesa = Simbolo("chave_inglesa")
armas = [faca, revolver, chave_inglesa]

simbolos = personagens + comodos + armas

def verificar_conhecimento(conhecimento):
    for simbolo in simbolos:
        if verificar_modelo(conhecimento, simbolo):
            termcolor.cprint(f"{simbolo}: SIM", "green")
        elif not verificar_modelo(conhecimento, Nao(simbolo)):
            print(f"{simbolo}: TALVEZ")

# Deve haver uma pessoa, um comodo e uma arma

conhecimento = E(
    Ou(mostarda, ameixa, damasco),
    Ou(salao, cozinha, biblioteca),
    Ou(faca, revolver, chave_inglesa)
)

# Cartas iniciais
conhecimento.adicionar(E(
    Nao(mostarda), Nao(cozinha), Nao(revolver)
))

# Carta desconhecida
conhecimento.adicionar(Ou(
    Nao(damasco), Nao(biblioteca), Nao(chave_inglesa)
))

conhecimento.adicionar(Nao(ameixa))
conhecimento.adicionar(Nao(salao))


verificar_conhecimento(conhecimento)