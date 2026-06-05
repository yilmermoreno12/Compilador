# lexer_natural.py
# Analizador léxico con PLY para un lenguaje natural controlado en español.

import ply.lex as lex

# Palabras reservadas del lenguaje natural controlado
reserved = {
    'programa': 'PROGRAMA',
    'inicio': 'INICIO',
    'fin': 'FIN',
    'crear': 'CREAR',
    'crea': 'CREAR',
    'declarar': 'DECLARAR',
    'declara': 'DECLARAR',
    'variable': 'VARIABLE',
    'llamada': 'LLAMADA',
    'llamado': 'LLAMADA',
    'con': 'CON',
    'valor': 'VALOR',
    'entero': 'ENTERO',
    'entera': 'ENTERO',
    'decimal': 'DECIMAL',
    'texto': 'TEXTO',
    'cadena': 'TEXTO',
    'si': 'SI',
    'entonces': 'ENTONCES',
    'sino': 'SINO',
    'mostrar': 'MOSTRAR',
    'muestra': 'MOSTRAR',
    'imprimir': 'MOSTRAR',
    'imprime': 'MOSTRAR',
    'mientras': 'MIENTRAS',
    'hacer': 'HACER',
    'haga': 'HACER',
    'repetir': 'REPETIR',
    'repite': 'REPETIR',
    'veces': 'VECES',
    'para': 'PARA',
    'desde': 'DESDE',
    'hasta': 'HASTA',
    'aumentando': 'AUMENTANDO',
    'en': 'EN',
    'sumar': 'SUMAR',
    'restar': 'RESTAR',
    'multiplicar': 'MULTIPLICAR_PAL',
    'dividir': 'DIVIDIR_PAL',
    'mas': 'MAS_PAL',
    'más': 'MAS_PAL',
    'menos': 'MENOS_PAL',
    'por': 'POR_PAL',
    'entre': 'ENTRE_PAL',
    'es': 'ES',
    'sea': 'ES',
    'mayor': 'MAYOR_PAL',
    'menor': 'MENOR_PAL',
    'igual': 'IGUAL_PAL',
    'diferente': 'DIFERENTE_PAL',
    'que': 'QUE',
    'o': 'O',
    'al': 'AL',
    'de': 'DE',
    'la': 'ARTICULO',
    'el': 'ARTICULO',
    'un': 'ARTICULO',
    'una': 'ARTICULO',
    'del': 'ARTICULO',
}

tokens = [
    'ID', 'NUMERO', 'CADENA',
    'PUNTO', 'PUNTO_COMA', 'COMA',
    'IGUAL', 'MAS', 'MENOS', 'MULT', 'DIV',
    'MAYOR_IGUAL', 'MENOR_IGUAL', 'IGUALDAD', 'DIFERENTE', 'MAYOR', 'MENOR',
    'PAREN_ABRE', 'PAREN_CIERRA', 'LLAVE_ABRE', 'LLAVE_CIERRA'
] + list(set(reserved.values()))

# Símbolos
t_MAYOR_IGUAL = r'>='
t_MENOR_IGUAL = r'<='
t_IGUALDAD = r'=='
t_DIFERENTE = r'!='
t_IGUAL = r'='
t_MAYOR = r'>'
t_MENOR = r'<'
t_MAS = r'\+'
t_MENOS = r'-'
t_MULT = r'\*'
t_DIV = r'/'
t_PAREN_ABRE = r'\('
t_PAREN_CIERRA = r'\)'
t_LLAVE_ABRE = r'\{'
t_LLAVE_CIERRA = r'\}'
t_PUNTO_COMA = r';'
t_COMA = r','
t_PUNTO = r'\.'

t_ignore = ' \t\r'


def t_CADENA(t):
    r'"([^\\\n]|(\\.))*?"|\'([^\\\n]|(\\.))*?\''
    return t


def t_NUMERO(t):
    r'\d+(\.\d+)?'
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t


def t_ID(t):
    r'[A-Za-zÁÉÍÓÚáéíóúÑñ_][A-Za-zÁÉÍÓÚáéíóúÑñ_0-9]*'
    palabra = t.value.lower()
    t.type = reserved.get(palabra, 'ID')
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    raise SyntaxError(f"Caracter no reconocido: {t.value[0]!r} en línea {t.lexer.lineno}")

lexer = lex.lex()
