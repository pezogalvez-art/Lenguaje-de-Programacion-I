"""Proyecto PC04 - Parte B2: Operaciones sobre matriz cuadrada personal.

Código universitario: 2155263 | Constantes personales: D = 3, P = 6, K = 2.
"""

import random
from typing import Final

CODIGO_UNIVERSITARIO: Final[int] = 2155263
D: Final[int] = 3
TAMANO_MATRIZ: Final[int] = 4 + (D % 3)  # 4 + (3 % 3) = 4
ROTACIONES_APLICAR: Final[int] = D % 4   # 3 % 4 = 3

Matriz = list[list[int]]


def generar_matriz(tu_codigo: int) -> Matriz:
    """Genera una matriz cuadrada determinista de tamaño 4 + (D mod 3)."""
    rng = random.Random(tu_codigo)
    n = 4 + ((tu_codigo % 10) % 3)
    return [[rng.randint(1, 50) for _ in range(n)] for _ in range(n)]


def _invertir_fila_en_sitio(fila: list[int]) -> None:
    """Invierte los elementos de una lista en el sitio usando dos índices."""
    izq = 0
    der = len(fila) - 1
    while izq < der:
        fila[izq], fila[der] = fila[der], fila[izq]
        izq += 1
        der -= 1


def rotar_90(m: Matriz) -> None:
    """Gira una matriz cuadrada 90 grados en sentido horario en el sitio.

    Args:
        m: Matriz cuadrada (lista de listas) que se modifica directamente.

    Raises:
        ValueError: Si la matriz no es cuadrada.
    """
    n = len(m)
    for fila in m:
        if len(fila) != n:
            raise ValueError("La matriz debe ser cuadrada para rotar 90 grados")

    # 1. Transponer en el sitio (intercambiar m[i][j] con m[j][i] para j > i)
    for i in range(n):
        for j in range(i + 1, n):
            m[i][j], m[j][i] = m[j][i], m[i][j]

    # 2. Invertir cada fila en el sitio
    for i in range(n):
        _invertir_fila_en_sitio(m[i])


def espiral(m: Matriz) -> list[int]:
    """Devuelve los elementos de la matriz recorridos en espiral horaria.

    Args:
        m: Matriz rectangular o cuadrada (no se modifica).

    Returns:
        Lista plana con los elementos en orden espiral.
    """
    if not m or not m[0]:
        return []

    arriba = 0
    abajo = len(m) - 1
    izquierda = 0
    derecha = len(m[0]) - 1
    recorrido: list[int] = []

    while arriba <= abajo and izquierda <= derecha:
        # 1. De izquierda a derecha por la fila superior
        for col in range(izquierda, derecha + 1):
            recorrido.append(m[arriba][col])
        arriba += 1

        # 2. De arriba hacia abajo por la columna derecha
        for fila in range(arriba, abajo + 1):
            recorrido.append(m[fila][derecha])
        derecha -= 1

        # 3. De derecha a izquierda por la fila inferior (si aún queda fila)
        if arriba <= abajo:
            for col in range(derecha, izquierda - 1, -1):
                recorrido.append(m[abajo][col])
            abajo -= 1

        # 4. De abajo hacia arriba por la columna izquierda (si aún queda columna)
        if izquierda <= derecha:
            for fila in range(abajo, arriba - 1, -1):
                recorrido.append(m[fila][izquierda])
            izquierda += 1

    return recorrido


def puntos_silla(m: Matriz) -> list[tuple[int, int, int]]:
    """Encuentra todas las celdas que son mínimo de su fila y máximo de su columna.

    Args:
        m: Matriz rectangular o cuadrada (no se modifica).

    Returns:
        Lista de tuplas (fila, columna, valor); los empates cuentan.
    """
    if not m or not m[0]:
        return []

    filas = len(m)
    cols = len(m[0])

    # Calcular manualmente el mínimo de cada fila
    min_fila: list[int] = []
    for i in range(filas):
        menor = m[i][0]
        for j in range(1, cols):
            if m[i][j] < menor:
                menor = m[i][j]
        min_fila.append(menor)

    # Calcular manualmente el máximo de cada columna
    max_col: list[int] = []
    for j in range(cols):
        mayor = m[0][j]
        for i in range(1, filas):
            if m[i][j] > mayor:
                mayor = m[i][j]
        max_col.append(mayor)

    # Verificar qué celdas cumplen ambas condiciones simultáneamente
    sillas: list[tuple[int, int, int]] = []
    for i in range(filas):
        for j in range(cols):
            valor = m[i][j]
            if valor == min_fila[i] and valor == max_col[j]:
                sillas.append((i, j, valor))

    return sillas


def imprimir_matriz(m: Matriz) -> None:
    """Imprime la matriz formateada por filas y columnas alineadas."""
    for fila in m:
        print("  " + " ".join(f"{val:>4}" for val in fila))


def main() -> None:
    """Ejecuta pruebas con assert y reporta rotación, espiral y puntos de silla."""
    # Pruebas de control con assert (incluyendo rotación en el sitio e identidad de filas)
    prueba_3x3 = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    id_inicial = id(prueba_3x3)
    rotar_90(prueba_3x3)
    assert id(prueba_3x3) == id_inicial
    assert prueba_3x3 == [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
    assert espiral(prueba_3x3) == [7, 4, 1, 2, 3, 6, 9, 8, 5]
    assert puntos_silla([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [(2, 0, 7)]

    # Matriz personal 4x4
    matriz = generar_matriz(CODIGO_UNIVERSITARIO)
    assert len(matriz) == TAMANO_MATRIZ and len(matriz[0]) == TAMANO_MATRIZ

    print(f"Matriz personal original ({TAMANO_MATRIZ}x{TAMANO_MATRIZ}):")
    imprimir_matriz(matriz)

    # 1. Aplicar rotar_90 exactamente D mod 4 = 3 veces en el sitio
    for _ in range(ROTACIONES_APLICAR):
        rotar_90(matriz)

    print(f"\nMatriz tras rotar 90° horario {ROTACIONES_APLICAR} veces (D mod 4):")
    imprimir_matriz(matriz)

    # 2. Recorrido en espiral de la matriz ya rotada
    rec_espiral = espiral(matriz)
    print(f"\nRecorrido en espiral ({len(rec_espiral)} elementos):")
    print(f"  {rec_espiral}")

    # 3. Puntos de silla de la matriz ya rotada
    sillas = puntos_silla(matriz)
    print("\nPuntos de silla (fila, columna, valor):")
    if sillas:
        for f, c, val in sillas:
            print(f"  - Fila {f}, Columna {c}: {val}")
    else:
        print("  sin puntos de silla")


if __name__ == "__main__":
    main()