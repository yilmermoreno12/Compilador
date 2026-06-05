# main.py
# Uso:
#   python main.py ejemplos/ejemplo1.txt
#   python main.py ejemplos/ejemplo1.txt salida.py

import sys
from pathlib import Path
from parser_natural import traducir


def main():
    if len(sys.argv) < 2:
        print('Uso: python main.py archivo_entrada.txt [archivo_salida.py]')
        sys.exit(1)

    archivo_entrada = Path(sys.argv[1])
    archivo_salida = Path(sys.argv[2]) if len(sys.argv) >= 3 else Path('salida.py')

    if not archivo_entrada.exists():
        print(f'No existe el archivo: {archivo_entrada}')
        sys.exit(1)

    texto = archivo_entrada.read_text(encoding='utf-8')

    try:
        codigo_python = traducir(texto)
    except Exception as error:
        print('No se pudo compilar el archivo.')
        print(f'Detalle: {error}')
        sys.exit(1)

    archivo_salida.write_text(codigo_python, encoding='utf-8')
    print('Compilación exitosa.')
    print(f'Archivo generado: {archivo_salida}')
    print('\n--- Código Python generado ---')
    print(codigo_python)


if __name__ == '__main__':
    main()
