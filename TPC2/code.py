from lark import Lark, Tree

# ------------------------------------------------------------
# Gramática para Intervalos (Definição Sintática + Verificação)
# ------------------------------------------------------------

grammar = r"""
?start: signal intervals DOT

signal: "+" -> plus
      | "-" -> minus

intervals: interval+

interval: "[" NUMBER ":" NUMBER "]"

DOT: "."
NUMBER: /-?\d+(\.\d+)?/

%import common.WS
%ignore WS
"""

# ------------------------------------------------------------
# Função para verificação da ordem dentro de cada intervalo
# ------------------------------------------------------------

def verificar_ordem(tree):
    """Verifica se cada intervalo segue a ordem correta de acordo com o sinal."""
    signal = tree.children[0].data  # 'plus' ou 'minus'
    erro = False

    for interval in tree.children[1].children:  # Percorre cada "interval"
        nums = [float(num) for num in interval.children if isinstance(num, str)]
        
        if len(nums) == 2:  # Cada intervalo deve ter dois números
            inicio, fim = nums
            
            if signal == "plus" and inicio >= fim:
                print(f"Erro: Intervalo [{inicio}:{fim}] não é crescente.")
                erro = True
            elif signal == "minus" and inicio <= fim:
                print(f"Erro: Intervalo [{inicio}:{fim}] não é decrescente.")
                erro = True

    if erro:
        return "Erro semântico"
    else:
        return "Frase correta"

# ------------------------------------------------------------
# Criar o parser
# ------------------------------------------------------------
parser = Lark(grammar, parser="lalr")

# ------------------------------------------------------------
# Testes
# ------------------------------------------------------------
inputs = [
    "+ [1:2] [3:4] [5:6] .",  # Correto (cada intervalo é crescente)
    "+ [3:1] .",              # Erro (intervalo individual está incorreto)
    "- [5:2] [2:0] .",        # Correto (cada intervalo é decrescente)
    "- [5:2] [1:3] .",        # Erro (segundo intervalo [1:3] está incorreto)
    "- [6:5] [6:1] ."         # Correto (cada intervalo individual está correto)
]

for frase in inputs:
    print(f"\nVerificando: {frase}")
    try:
        tree = parser.parse(frase)
        print(tree.pretty())  # Mostra a árvore de parsing
        resultado = verificar_ordem(tree)
        print(resultado)
    except Exception as e:
        print(f"Erro ao processar entrada: {e}")
