# Compilador de lenguaje natural a Python

Este proyecto implementa un compilador/transpilador sencillo usando **Python + PLY**.

El programa recibe instrucciones en español natural controlado y genera código fuente Python.

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

```bash
python main.py ejemplos/ejemplo1.txt salida.py
python salida.py
```

## Ejemplo de entrada

```txt
Programa Inicio.
crear una variable entera llamada edad con valor 20.
si edad es mayor o igual que 18 entonces
    mostrar "Puede ingresar".
fin si.
fin.
```

## Salida en Python

```python
edad = 20
if edad >= 18:
    print("Puede ingresar")
```

## Lenguaje soportado

- Crear variables: `crear una variable entera llamada edad con valor 20.`
- Mostrar: `mostrar "Hola".`
- Condicional: `si edad es mayor o igual que 18 entonces ... fin si.`
- Condicional con sino: `si ... entonces ... sino ... fin si.`
- Mientras: `mientras contador es menor que 5 hacer ... fin mientras.`
- Repetir: `repetir 3 veces hacer ... fin repetir.`
- Para: `para i desde 1 hasta 5 hacer ... fin para.`
- Operaciones: `a mas b`, `a menos b`, `a por b`, `a entre b`.
