import itertools

class Sentenca():

    def avaliar(self, modelo):
        """Avalia a sentença lógica."""
        raise Exception("nada para avaliar")

    def formula(self):
        """Retorna a fórmula em string que representa a sentença lógica."""
        return ""

    def simbolos(self):
        """Retorna um conjunto de todos os símbolos na sentença lógica."""
        return set()

    @classmethod
    def validar(cls, sentenca):
        if not isinstance(sentenca, Sentenca):
            raise TypeError("deve ser uma sentença lógica")

    @classmethod
    def entreparenteses(cls, s):
        """Coloca a expressão entre parênteses, se ainda não estiver entre parênteses."""
        def balanceado(s):
            """Verifica se uma string possui parênteses balanceados."""
            count = 0
            for c in s:
                if c == "(":
                    count += 1
                elif c == ")":
                    if count <= 0:
                        return False
                    count -= 1
            return count == 0
        if not len(s) or s.isalpha() or (
            s[0] == "(" and s[-1] == ")" and balanceado(s[1:-1])
        ):
            return s
        else:
            return f"({s})"


class Simbolo(Sentenca):

    def __init__(self, nome):
        self.nome = nome

    def __eq__(self, outro):
        return isinstance(outro, Simbolo) and self.nome == outro.nome

    def __hash__(self):
        return hash(("simbolo", self.nome))

    def __repr__(self):
        return self.nome

    def avaliar(self, modelo):
        try:
            return bool(modelo[self.nome])
        except KeyError:
            raise Exception(f"variável {self.nome} não está no modelo")

    def formula(self):
        return self.nome

    def simbolos(self):
        return {self.nome}


class Nao(Sentenca):
    def __init__(self, operando):
        Sentenca.validar(operando)
        self.operando = operando

    def __eq__(self, outro):
        return isinstance(outro, Nao) and self.operando == outro.operando

    def __hash__(self):
        return hash(("nao", hash(self.operando)))

    def __repr__(self):
        return f"Nao({self.operando})"

    def avaliar(self, modelo):
        return not self.operando.avaliar(modelo)

    def formula(self):
        return "¬" + Sentenca.entreparenteses(self.operando.formula())

    def simbolos(self):
        return self.operando.simbolos()


class E(Sentenca):
    def __init__(self, *conjuntos):
        for conjunto in conjuntos:
            Sentenca.validar(conjunto)
        self.conjuntos = list(conjuntos)

    def __eq__(self, outro):
        return isinstance(outro, E) and self.conjuntos == outro.conjuntos

    def __hash__(self):
        return hash(
            ("e", tuple(hash(conjunto) for conjunto in self.conjuntos))
        )

    def __repr__(self):
        conjuncoes = ", ".join(
            [str(conjunto) for conjunto in self.conjuntos]
        )
        return f"E({conjuncoes})"

    def adicionar(self, conjunto):
        Sentenca.validar(conjunto)
        self.conjuntos.append(conjunto)

    def avaliar(self, modelo):
        return all(conjunto.avaliar(modelo) for conjunto in self.conjuntos)

    def formula(self):
        if len(self.conjuntos) == 1:
            return self.conjuntos[0].formula()
        return " ∧ ".join([Sentenca.entreparenteses(conjunto.formula())
                           for conjunto in self.conjuntos])

    def simbolos(self):
        return set.union(*[conjunto.simbolos() for conjunto in self.conjuntos])


class Ou(Sentenca):
    def __init__(self, *disjuntos):
        for disjunto in disjuntos:
            Sentenca.validar(disjunto)
        self.disjuntos = list(disjuntos)

    def __eq__(self, outro):
        return isinstance(outro, Ou) and self.disjuntos == outro.disjuntos

    def __hash__(self):
        return hash(
            ("ou", tuple(hash(disjunto) for disjunto in self.disjuntos))
        )

    def __repr__(self):
        disjuntos = ", ".join([str(disjunto) for disjunto in self.disjuntos])
        return f"Ou({disjuntos})"

    def avaliar(self, modelo):
        return any(disjunto.avaliar(modelo) for disjunto in self.disjuntos)

    def formula(self):
        if len(self.disjuntos) == 1:
            return self.disjuntos[0].formula()
        return " ∨  ".join([Sentenca.entreparenteses(disjunto.formula())
                            for disjunto in self.disjuntos])

    def simbolos(self):
        return set.union(*[disjunto.simbolos() for disjunto in self.disjuntos])


class Implicacao(Sentenca):
    def __init__(self, antecedente, consequente):
        Sentenca.validar(antecedente)
        Sentenca.validar(consequente)
        self.antecedente = antecedente
        self.consequente = consequente

    def __eq__(self, outro):
        return (isinstance(outro, Implicacao)
                and self.antecedente == outro.antecedente
                and self.consequente == outro.consequente)

    def __hash__(self):
        return hash(("implica", hash(self.antecedente), hash(self.consequente)))

    def __repr__(self):
        return f"Implicacao({self.antecedente}, {self.consequente})"

    def avaliar(self, modelo):
        return ((not self.antecedente.avaliar(modelo))
                or self.consequente.avaliar(modelo))

    def formula(self):
        antecedente = Sentenca.entreparenteses(self.antecedente.formula())
        consequente = Sentenca.entreparenteses(self.consequente.formula())
        return f"{antecedente} => {consequente}"

    def simbolos(self):
        return set.union(self.antecedente.simbolos(), self.consequente.simbolos())


class Bicondicional(Sentenca):
    def __init__(self, esquerda, direita):
        Sentenca.validar(esquerda)
        Sentenca.validar(direita)
        self.esquerda = esquerda
        self.direita = direita

    def __eq__(self, outro):
        return (isinstance(outro, Bicondicional)
                and self.esquerda == outro.esquerda
                and self.direita == outro.direita)

    def __hash__(self):
        return hash(("bicondicional", hash(self.esquerda), hash(self.direita)))

    def __repr__(self):
        return f"Bicondicional({self.esquerda}, {self.direita})"

    def avaliar(self, modelo):
        return ((self.esquerda.avaliar(modelo)
                 and self.direita.avaliar(modelo))
                or (not self.esquerda.avaliar(modelo)
                    and not self.direita.avaliar(modelo)))

    def formula(self):
        esquerda = Sentenca.entreparenteses(str(self.esquerda))
        direita = Sentenca.entreparenteses(str(self.direita))
        return f"{esquerda} <=> {direita}"

    def simbolos(self):
        return set.union(self.esquerda.simbolos(), self.direita.simbolos())


def verificar_modelo(base_conhecimento, consulta):
    """Verifica se a base de conhecimento implica na consulta."""

    def verificar_todos(base_conhecimento, consulta, simbolos, modelo):
        """Verifica se a base de conhecimento implica na consulta, dado um modelo específico."""

        # Se o modelo tiver uma atribuição para cada símbolo
        if not simbolos:

            # Se a base de conhecimento for verdadeira no modelo, então a consulta também deve ser verdadeira
            if base_conhecimento.avaliar(modelo):
                return consulta.avaliar(modelo)
            return True
        else:

            # Escolhe um dos símbolos não utilizados restantes
            restantes = simbolos.copy()
            p = restantes.pop()

            # Cria um modelo onde o símbolo é verdadeiro
            modelo_verdade = modelo.copy()
            modelo_verdade[p] = True

            # Cria um modelo onde o símbolo é falso
            modelo_falso = modelo.copy()
            modelo_falso[p] = False

            # Garante que a implicação seja mantida em ambos os modelos
            return (verificar_todos(base_conhecimento, consulta, restantes, modelo_verdade) and
                    verificar_todos(base_conhecimento, consulta, restantes, modelo_falso))

    # Obter todos os símbolos na base de conhecimento e na consulta
    simbolos = set.union(base_conhecimento.simbolos(), consulta.simbolos())

    # Verificar se a base de conhecimento implica na consulta
    return verificar_todos(base_conhecimento, consulta, simbolos, dict())
