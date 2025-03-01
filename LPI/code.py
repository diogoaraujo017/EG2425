from lark import Lark


grammar = r"""
start: program

program: ( declaration | instruction | function )* 

declaration: type IDENTIFIER ";"

type: "inteiro" 
    | "set" 
    | "lista" 
    | "tuplo" 
    | "frase" 

instruction: atrib
            | read 
            | write 
            | call
            | conditionals 
            | repetitions  

atrib: IDENTIFIER "=" expression ";"

read: "ler" IDENTIFIER ";"

write: "escrever" expression ";"

call: func_call ";"

func_call: IDENTIFIER "(" (expression ("," expression)*)? ")"

conditionals: if 
            | case

if: "SE" "(" cond_expr ")" "ENTAO" "{" program "}" ("SENAO" "{" program "}")?

case: "CASO" "(" expression ")" "{" case_options "}"

case_options: ( "QUANDO" cond_expr ":" "{" program "}" )+

repetitions: while 
            | for 
            | do_while

while: "ENQUANTO_FOR_VERDADE" "(" cond_expr ")" "{" program "}"

for: "CICLO" "(" varfor ";" cond_expr ";" increment ")" "{" program "}"

varfor : IDENTIFIER "=" expression

increment: expression "++" 
            | expression "--"
            | expression "+=" expression
            | expression "-=" expression

do_while: "REPETIR" "{" program "}" "ENQUANTO_FOR_VERDADE" "(" cond_expr ")" ";"

options: ( declaration | instruction )*

function: "FUNCAO" type IDENTIFIER "(" parameters? ")" "{" options return "}"

parameters: type IDENTIFIER ("," type IDENTIFIER)*

return: "RETORNAR" expression ";"

expression:   expression OPERATOR expression
            | expression COMPARISSON expression
            | "nao" "(" expression ")"
            | "(" expression ")"
            | types
            
cond_expr: expression COMPARISSON expression

types: IDENTIFIER
        | NUMBER
        | STRING
        | array
        | set
        | tuple
        | func_call

array: "[" (expression ("," expression)*)? "]"
set: "{" (expression ("," expression)*)? "}"
tuple: "(" (expression ("," expression)*)? ")"

OPERATOR: "+" | "-" | "*" | "/"
COMPARISSON: "==" | "!=" | "<=" | ">=" | "<" | ">"
NUMBER: /[0-9]+/
STRING: /".*"/
IDENTIFIER: /[a-z]\w*/

%import common.WS
%ignore WS
"""

example1 = """
    inteiro n;
    ler n;
    escrever fatorial(n);

    FUNCAO inteiro fatorial(inteiro x) {
        inteiro resultado;
        resultado = 1;
        CICLO (i = 1; i <= x; i++) {
            resultado = resultado * i;
        }
        RETORNAR resultado;
    }
"""

example2 = """
inteiro op;
escrever "Escolha uma operacao: 1-Soma, 2-Diferenca, 3-Fatorial";
ler op;
CASO (op) {
    QUANDO op == 1: {
         inteiro a;
         inteiro b;
         ler a;
         ler b;
         escrever a + b;
    }
    QUANDO op == 2: {
         inteiro a;
         inteiro b;
         ler a;
         ler b;
         escrever a - b;
    }
    QUANDO op == 3: {
         inteiro n;
         ler n;
         escrever fatorial(n);
    }
}

FUNCAO inteiro fatorial(inteiro x) {
    inteiro resultado;
    resultado = 1;
    CICLO (i = 1; i <= x; i++) {
         resultado = resultado * i;
    }
    RETORNAR resultado;
}
"""
    
parser = Lark(grammar, start='start', parser='earley')

data = parser.parse(example2)

print(data.pretty())