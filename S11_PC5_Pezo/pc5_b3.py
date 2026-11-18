"""Proyecto PC05 - B3: Calculadora RPN extensible mediante tabla de despacho.

Código universitario: 2155263 | Estudiante: Pezo | Constantes: D = 3, P = 6, K = 2.
"""

from typing import Callable, Final
from generadores_u3 import expresion_rpn

CODIGO_UNIVERSITARIO: Final[int] = 2155263

# Cada entrada de la tabla almacena (aridad, funcion_operacion).
# Extensibilidad sin modificar el bucle principal:
# Al desacoplar las operaciones en un diccionario {simbolo: (aridad, funcion)},
# el bucle de evaluacion solo consulta la aridad declarada en la tabla, extrae
# exactamente esa cantidad de operandos de la pila e invoca la funcion con *args.
# Por ello, agregar operadores binarios como 'max' (aridad 2) o unarios como 'neg'
# (aridad 1) consiste unicamente en registrar nuevas entradas en TABLA_OPERACIONES.
OperacionRPN = tuple[int, Callable[..., float]]


def _dividir(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Error matemático: división entre cero en expresión RPN.")
    return a / b


def _modulo(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Error matemático: módulo entre cero en expresión RPN.")
    return a % b


TABLA_OPERACIONES: dict[str, OperacionRPN] = {
    "+": (2, lambda a, b: a + b),
    "-": (2, lambda a, b: a - b),
    "*": (2, lambda a, b: a * b),
    "/": (2, _dividir),
    "^": (2, lambda a, b: a ** b),
    "%": (2, _modulo),
    "max": (2, lambda a, b: a if a >= b else b),
    "neg": (1, lambda a: -a),
}


def _es_numero(token: str) -> bool:
    """Comprueba si un token representa un literal numérico válido."""
    try:
        float(token)
        return True
    except ValueError:
        return False


def evaluar_rpn(
    expr: str,
    tabla: dict[str, OperacionRPN] = TABLA_OPERACIONES,
) -> float:
    """Evalúa una expresión en notación polaca inversa usando pila y tabla de despacho."""
    tokens = expr.strip().split()
    if not tokens:
        raise ValueError("Expresión vacía: no hay operandos para evaluar.")

    pila: list[float] = []

    for token in tokens:
        if _es_numero(token):
            pila.append(float(token))
        elif token in tabla:
            aridad, funcion = tabla[token]
            if len(pila) < aridad:
                raise ValueError(
                    f"Faltan operandos para el operador '{token}' (requiere {aridad})."
                )
            # Extraemos los operandos respetando el orden en que entraron a la pila
            args = [pila.pop() for _ in range(aridad)][::-1]
            pila.append(funcion(*args))
        else:
            raise ValueError(f"Símbolo desconocido en la expresión RPN: '{token}'.")

    if len(pila) != 1:
        raise ValueError(
            f"Expresión RPN mal formada: quedaron {len(pila)} valores sin operar en la pila."
        )

    return pila[0]


def ejecutar_pruebas() -> None:
    """Ejecuta 6 pruebas con assert cubriendo casos normales, extensiones y errores."""
    # 1. Caso normal con operadores aritméticos básicos
    assert evaluar_rpn("3 4 + 2 * 5 -") == 9.0

    # 2. Caso normal con potencia y módulo
    assert evaluar_rpn("2 3 ^ 5 %") == 3.0

    # 3. Caso de extensión sin tocar el bucle: operador binario 'max' y unario 'neg'
    assert evaluar_rpn("10 25 max neg 4 +") == -21.0

    # 4. Caso de error: faltan operandos
    try:
        evaluar_rpn("5 +")
        assert False, "Debió lanzar ValueError por falta de operandos"
    except ValueError:
        pass

    # 5. Caso de error: símbolo desconocido y sobran operandos al final
    try:
        evaluar_rpn("4 5 @")
        assert False, "Debió lanzar ValueError por símbolo desconocido"
    except ValueError:
        pass

    try:
        evaluar_rpn("4 5 6 +")
        assert False, "Debió lanzar ValueError por exceso de operandos sin operar"
    except ValueError:
        pass

    # 6. Caso de error: división entre cero con ZeroDivisionError propio
    try:
        evaluar_rpn("12 0 /")
        assert False, "Debió lanzar ZeroDivisionError por división entre cero"
    except ZeroDivisionError:
        pass


def main() -> None:
    """Ejecuta las pruebas y evalúa la expresión RPN personal."""
    ejecutar_pruebas()
    expr_personal = expresion_rpn(CODIGO_UNIVERSITARIO)
    resultado = evaluar_rpn(expr_personal)

    print(f"Expresión RPN personal ({CODIGO_UNIVERSITARIO}): {expr_personal}")
    print(f"Resultado evaluado: {resultado:.2f}")
    print("Pruebas unitarias (6/6 assert): OK")


if __name__ == "__main__":
    main()