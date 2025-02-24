import math
import ply.yacc as yacc
from lex import tokens

# Examples:
# + [ 1.0   :9.0 ]  [15.5 :19.0]   .
# - [ 100.0 : 40.0 ] [  5.0 :  1.0 ] .
# - [ 15.0 : 14.0 ] [  1.0 :  0.0 ] [ -1.0 : -2.0 ] .

## Grammar from class
#
# P = { p1: Sentence  : Signal Intervals '.'
#          p6: Signal : '+'
#                   parser.sentido = 1
#          p7: Signal : '-'		
#                   parser.sentido = -1
#          p2: Intervals : Interval RemainingIntervals
#          p3: RemainingIntervals : 
#          p4: RemainingIntervals : Interval RemainingIntervals
#          p5: Interval  : '[' num ':' num ']'   
# 		            CC1:    p[4] > p[2]  &
# 		            CC2:    p[2] >= parser.anterior
# 		            parser.anterior = p[4]
# 		            parser.erro = not (CC1) or not (CC2)
#     }

## Grammar for the parser
#
#   Sentence : Signal Intervals DOT

#   Signal : PLUS
#          | MINUS

#   Intervals : Interval RemainingIntervals

#   RemainingIntervals : Interval RemainingIntervals
#                      | 
# 
#   Interval : ESQ NUMBER COLON NUMBER DIR
#
#
#

def p_sentence(p):
    '''Sentence : Signal Intervals DOT'''
    all_intervals = p[2]
    
    # After parsing the sentence, check if there was any error
    
    error = False
    for i in range(len(all_intervals)):
        if parser.sentido == 1:
            if all_intervals[i][0] >= all_intervals[i][1]:
                print("Error: Interval " + str(i+1) + " is not valid.")
                error = True
            if i > 0 and all_intervals[i][0] < all_intervals[i-1][1]:
                print("Error: Interval " + str(i) + " is not valid.")
                error = True
        
        elif parser.sentido == -1:
            if all_intervals[i][0] <= all_intervals[i][1]:
                print("Error: Interval " + str(i+1) + " is not valid.")
                error = True
            if i > 0 and all_intervals[i][0] > all_intervals[i-1][1]:
                print("Error: Interval " + str(i) + " is not valid.")
                error = True
            
    if error:
        print("There was an error in the sentence.\n")
    else:
        print("\nThe sentence is valid.\n")
    
    
def p_plus(p):
    '''Signal : PLUS'''
    p[0] = p[1]
    
    parser.sentido = 1
    parser.anterior = -math.inf
    
def p_minus(p):
    '''Signal : MINUS'''
    p[0] = p[1]
    
    parser.sentido = -1
    parser.anterior = -math.inf
    
def p_intervals(p):
    '''Intervals : Interval RemainingIntervals'''
    p[0] = [p[1]] + p[2]
    
    
def p_remaining_intervals(p):
    '''RemainingIntervals : Interval RemainingIntervals
                            | '''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []
    
    
def p_interval(p):
    '''Interval : ESQ NUMBER COLON NUMBER DIR'''
    p[0] = [p[2], p[4]]

def p_error(p):
    print("Syntax error in input!")

parser = yacc.yacc()

# Initialize parser attributes
parser.erro = False
parser.sentido = 0
parser.anterior = 0

parser.parse('+ [ 1.0   :9.0 ]  [15.5 :19.0]   .')
parser.parse('- [ 30.0 : 40.0 ] [  5.0 :  1.0 ] .')
