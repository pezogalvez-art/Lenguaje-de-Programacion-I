"""Generadores deterministas de datos personales para la Unidad III (LP1 - UNAP).

Semilla determinista basada en el código universitario (2155263).
Provee entradas reproducibles para PC05, PC06 y EU3.
"""

import random


def arreglo_personal(tu_codigo: int) -> list[int]:
    """Devuelve una lista determinista de 12 enteros con positivos, negativos y empates."""
    rng = random.Random(tu_codigo)
    base = [rng.randint(-45, 89) for _ in range(10)]
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
    return f"{a} {b} + {c} * {d} - 2 ^ {e} / {f} % {g} +"


def operaciones_lista(tu_codigo: int) -> list[tuple]:
    """Devuelve 14 operaciones deterministas para ListaEnlazada."""
    rng = random.Random(tu_codigo + 202)
    v1 = rng.randint(10, 30)
    v2 = rng.randint(31, 50)
    v3 = rng.randint(51, 70)
    v4 = rng.randint(71, 90)
    v5 = rng.randint(11, 29)
    v6 = rng.randint(32, 49)
    v7 = rng.randint(52, 69)
    return [
        ("insertar_inicio", v1),
        ("insertar_final", v2),
        ("insertar_inicio", v3),
        ("insertar_final", v4),
        ("insertar_en", 2, v5),
        ("eliminar", v2),
        ("insertar_final", v6),
        ("invertir",),
        ("insertar_en", 1, v7),
        ("eliminar", 999),  # No existe: no debe alterar la lista
        ("insertar_inicio", v2),
        ("eliminar", v1),
        ("invertir",),
        ("insertar_final", v3),
    ]


def lineas_ventas(tu_codigo: int) -> list[str]:
    """Devuelve líneas CSV (cabecera + válidas con comas entre comillas + inválidas)."""
    rng = random.Random(tu_codigo + 303)
    q1 = rng.randint(2, 6)
    q2 = rng.randint(1, 5)
    q3 = rng.randint(3, 8)
    q4 = rng.randint(2, 7)
    q5 = rng.randint(1, 4)
    q6 = rng.randint(4, 9)
    return [
        "fecha,producto,categoria,cantidad,precio",
        f'2026-11-01,"Laptop Pro, 16GB RAM",Electrónica,{q1},3250.50',
        f"2026-11-01,Cuaderno A4 Rayado,Papelería,{q2},8.40",
        "2026-11-02,Error Cantidad Cero,Electrónica,0,150.00",
        f'2026-11-02,"Café Amazónico, Tostado 500g",Alimentación,{q3},24.90',
        "2026-11-03,Fila Incompleta,Papelería,4",
        f"2026-11-03,Silla Ergonómica Oficina,Mueblería,{q4},480.00",
        "2026-11-04,Precio Negativo,Alimentación,3,-12.50",
        f'2026-11-04,"Mouse Inalámbrico, Óptico",Electrónica,{q5},65.25',
        f"2026-11-05,Archivador Palanca Oficio,Papelería,{q6},14.75",
        "2026-11-05,Cantidad Texto,Mueblería,dos,210.00",
    ]