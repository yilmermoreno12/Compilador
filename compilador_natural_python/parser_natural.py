# parser_natural.py
# Parser con PLY que traduce lenguaje natural controlado en español a Python.

import ply.yacc as yacc
from lexer_natural import tokens


def indentar(codigo: str, espacios: int = 4) -> str:
    """Agrega indentación a cada línea no vacía."""
    prefijo = ' ' * espacios
    lineas = codigo.split('\n')
    return '\n'.join((prefijo + linea if linea.strip() else linea) for linea in lineas)


def unir(instrucciones):
    """Une instrucciones evitando líneas vacías innecesarias."""
    return '\n'.join(i for i in instrucciones if i is not None and str(i).strip() != '')

# Precedencia de operaciones matemáticas
precedence = (
    ('left', 'MAS', 'MENOS', 'MAS_PAL', 'MENOS_PAL'),
    ('left', 'MULT', 'DIV', 'POR_PAL', 'ENTRE_PAL'),
)

# ----------------------
# Programa principal
# ----------------------

def p_programa(p):
    '''programa : encabezado instrucciones cierre
                | instrucciones'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]


def p_encabezado(p):
    '''encabezado : PROGRAMA INICIO separador_opt
                  | PROGRAMA separador_opt
                  | INICIO separador_opt'''
    p[0] = None


def p_cierre(p):
    '''cierre : FIN separador_opt
              | empty'''
    p[0] = None


def p_instrucciones_lista(p):
    '''instrucciones : instrucciones instruccion
                     | instruccion'''
    if len(p) == 3:
        p[0] = unir([p[1], p[2]])
    else:
        p[0] = p[1]


def p_instruccion(p):
    '''instruccion : declaracion separador_opt
                   | asignacion separador_opt
                   | mostrar separador_opt
                   | condicional separador_opt
                   | ciclo_mientras separador_opt
                   | ciclo_repetir separador_opt
                   | ciclo_para separador_opt'''
    p[0] = p[1]

# ----------------------
# Declaraciones y asignaciones
# ----------------------

def p_declaracion_natural(p):
    '''declaracion : CREAR articulo_opt VARIABLE tipo LLAMADA ID CON VALOR expresion
                   | DECLARAR articulo_opt VARIABLE tipo LLAMADA ID CON VALOR expresion
                   | tipo ID IGUAL expresion'''
    if len(p) == 10:
        nombre = p[6]
        valor = p[9]
    else:
        nombre = p[2]
        valor = p[4]
    p[0] = f"{nombre} = {valor}"


def p_tipo(p):
    '''tipo : ENTERO
            | DECIMAL
            | TEXTO'''
    # Python no necesita declarar el tipo, pero se reconoce para validar el lenguaje.
    p[0] = p[1]


def p_asignacion(p):
    '''asignacion : ID IGUAL expresion
                  | ID ES expresion
                  | cambiar_valor ID CON VALOR expresion'''
    if len(p) == 4:
        p[0] = f"{p[1]} = {p[3]}"
    else:
        p[0] = f"{p[2]} = {p[5]}"


def p_cambiar_valor(p):
    '''cambiar_valor : CREAR
                     | DECLARAR'''
    # Permite frases tipo: "declara edad con valor 21" aunque lo común es usar variable.
    p[0] = p[1]

# ----------------------
# Mostrar / imprimir
# ----------------------

def p_mostrar(p):
    '''mostrar : MOSTRAR expresion
               | MOSTRAR PAREN_ABRE expresion PAREN_CIERRA'''
    if len(p) == 3:
        p[0] = f"print({p[2]})"
    else:
        p[0] = f"print({p[3]})"

# ----------------------
# Condicionales
# ----------------------

def p_condicional_si(p):
    '''condicional : SI condicion ENTONCES instrucciones FIN SI
                   | SI condicion LLAVE_ABRE instrucciones LLAVE_CIERRA'''
    p[0] = f"if {p[2]}:\n{indentar(p[4])}"


def p_condicional_si_sino(p):
    '''condicional : SI condicion ENTONCES instrucciones SINO instrucciones FIN SI'''
    p[0] = f"if {p[2]}:\n{indentar(p[4])}\nelse:\n{indentar(p[6])}"

# ----------------------
# Ciclos
# ----------------------

def p_ciclo_mientras(p):
    '''ciclo_mientras : MIENTRAS condicion HACER instrucciones FIN MIENTRAS'''
    p[0] = f"while {p[2]}:\n{indentar(p[4])}"


def p_ciclo_repetir(p):
    '''ciclo_repetir : REPETIR expresion VECES HACER instrucciones FIN REPETIR'''
    p[0] = f"for _ in range({p[2]}):\n{indentar(p[5])}"


def p_ciclo_para(p):
    '''ciclo_para : PARA ID DESDE expresion HASTA expresion HACER instrucciones FIN PARA
                  | PARA ID DESDE expresion HASTA expresion AUMENTANDO EN expresion HACER instrucciones FIN PARA'''
    variable = p[2]
    inicio = p[4]
    fin = p[6]
    if len(p) == 11:
        paso = '1'
        cuerpo = p[8]
    else:
        paso = p[9]
        cuerpo = p[11]
    p[0] = f"for {variable} in range({inicio}, {fin} + 1, {paso}):\n{indentar(cuerpo)}"

# ----------------------
# Condiciones naturales y simbólicas
# ----------------------

def p_condicion_binaria(p):
    '''condicion : expresion operador_comparacion expresion'''
    p[0] = f"{p[1]} {p[2]} {p[3]}"


def p_operador_comparacion_simbolo(p):
    '''operador_comparacion : MAYOR_IGUAL
                            | MENOR_IGUAL
                            | MAYOR
                            | MENOR
                            | IGUALDAD
                            | DIFERENTE'''
    p[0] = p[1]


def p_operador_comparacion_natural(p):
    '''operador_comparacion : ES MAYOR_PAL O IGUAL_PAL QUE
                            | ES MENOR_PAL O IGUAL_PAL QUE
                            | ES MAYOR_PAL QUE
                            | ES MENOR_PAL QUE
                            | ES IGUAL_PAL ID
                            | ES IGUAL_PAL QUE
                            | ES DIFERENTE_PAL DE'''
    texto = ' '.join(str(x).lower() for x in p[1:])
    if 'mayor o igual' in texto:
        p[0] = '>='
    elif 'menor o igual' in texto:
        p[0] = '<='
    elif 'mayor' in texto:
        p[0] = '>'
    elif 'menor' in texto:
        p[0] = '<'
    elif 'diferente' in texto:
        p[0] = '!='
    else:
        p[0] = '=='

# ----------------------
# Expresiones
# ----------------------

def p_expresion_binaria(p):
    '''expresion : expresion MAS expresion
                 | expresion MENOS expresion
                 | expresion MULT expresion
                 | expresion DIV expresion
                 | expresion MAS_PAL expresion
                 | expresion MENOS_PAL expresion
                 | expresion POR_PAL expresion
                 | expresion ENTRE_PAL expresion'''
    op = p[2]
    traduccion = {
        'mas': '+', 'más': '+', '+': '+',
        'menos': '-', '-': '-',
        'por': '*', '*': '*',
        'entre': '/', '/': '/',
    }
    p[0] = f"{p[1]} {traduccion.get(str(op).lower(), op)} {p[3]}"


def p_expresion_parentesis(p):
    '''expresion : PAREN_ABRE expresion PAREN_CIERRA'''
    p[0] = f"({p[2]})"


def p_expresion_valores(p):
    '''expresion : NUMERO
                 | CADENA
                 | ID'''
    if isinstance(p[1], str):
        p[0] = p[1]
    else:
        p[0] = str(p[1])

# ----------------------
# Opcionales y separadores
# ----------------------

def p_articulo_opt(p):
    '''articulo_opt : ARTICULO
                    | empty'''
    p[0] = None


def p_separador_opt(p):
    '''separador_opt : separador_opt separador
                     | separador
                     | empty'''
    p[0] = None


def p_separador(p):
    '''separador : PUNTO
                 | PUNTO_COMA
                 | COMA'''
    p[0] = None


def p_empty(p):
    'empty :'
    p[0] = None


def p_error(p):
    if p:
        raise SyntaxError(f"Error de sintaxis cerca de {p.value!r} en token {p.type}")
    raise SyntaxError('Error de sintaxis: entrada incompleta')

parser = yacc.yacc()


def traducir(texto: str) -> str:
    """Traduce lenguaje natural controlado a código Python."""
    codigo = parser.parse(texto)
    encabezado = '# Código generado automáticamente por el compilador natural\n'
    return encabezado + (codigo or '') + '\n'
