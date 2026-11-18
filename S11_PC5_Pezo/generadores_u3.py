"""Generadores deterministas de datos personales para la Unidad III (LP1 - UNAP).

Semilla determinista basada en el código universitario (2155263).
Provee entradas reproducibles para PC05, PC06 y EU3.
"""

import random


def arreglo_personal(tu_codigo: int) -> list[int]:
    """Devuelve una lista determinista de 12 enteros con positivos, negativos y empates."""
    rng = random.Random(tu_codigo)
    # Garantizamos valores variados incluyendo negativos y empates de suma de dígitos
    base = [rng.randint(-45, 89) for _ in range(10)]
    # Añadimos dos elementos controlados para forzar empate en suma de dígitos (ej. 14 y -23 -> suma 5)
    base.append(14)
    base.append(-23)
    rng.shuffle(base)
    return base


def expresion_rpn(tu_codigo: int) -> str:
    """Devuelve una expresión RPN válida determinista usando +, -, *, /, ^ y %."""
    rng = random.Random(tu_codigo + 101)
    a = rng.randint(12, 25)
    b = rng.randint(3, 8)
    c = rng.randint(2, 4)
    d = rng.randint(4, 9)
    e = rng.randint(2, 5)
    f = rng.randint(2, 6)
    g = rng.randint(1, 7)
    # (((a + b) * c - d) ^ 2) / e % f + g  -> sin división por cero garantizado
    return f"{a} {b} + {c} * {d} - 2 ^ {e} / {f} % {g} +"