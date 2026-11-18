"""Proyecto PC03 - Parte B1: Sucesión personal t(n).

Código: 2155263 | Constantes personales: D = 3, P = 6, K = 2.
"""

from typing import Final

D: Final[int] = 3
P: Final[int] = 6
MOD: Final[int] = 1009

llamadas_rec: int = 0


def t_rec(n: int) -> int:
    """Calcula t(n) de forma recursiva directa e incrementa el contador global.

    Args:
        n: Índice no negativo de la sucesión.

    Returns:
        El término t(n) módulo 1009.

    Raises:
        ValueError: Si n es negativo.
    """
    if n < 0:
        raise ValueError("n debe ser un entero no negativo")
    global llamadas_rec
    llamadas_rec += 1
    if n == 0:
        return (D + 1) % MOD
    if n == 1:
        return (P + 1) % MOD
    return (t_rec(n - 1) + 2 * t_rec(n - 2) + n) % MOD


def t_memo(n: int, memo: dict[int, int] | None = None) -> int:
    """Calcula t(n) de forma recursiva con diccionario de memoización propio.

    Args:
        n: Índice no negativo de la sucesión.
        memo: Diccionario opcional para almacenar subproblemas resueltos.

    Returns:
        El término t(n) módulo 1009.

    Raises:
        ValueError: Si n es negativo.
    """
    if n < 0:
        raise ValueError("n debe ser un entero no negativo")
    if memo is None:
        memo = {0: (D + 1) % MOD, 1: (P + 1) % MOD}
    if n in memo:
        return memo[n]
    memo[n] = (t_memo(n - 1, memo) + 2 * t_memo(n - 2, memo) + n) % MOD
    return memo[n]


def t_it(n: int) -> int:
    """Calcula t(n) de forma iterativa con complejidad espacial O(1).

    Args:
        n: Índice no negativo de la sucesión.

    Returns:
        El término t(n) módulo 1009.

    Raises:
        ValueError: Si n es negativo.
    """
    if n < 0:
        raise ValueError("n debe ser un entero no negativo")
    if n == 0:
        return (D + 1) % MOD
    if n == 1:
        return (P + 1) % MOD

    anterior_2 = (D + 1) % MOD  # t(0) = 4
    anterior_1 = (P + 1) % MOD  # t(1) = 7
    for i in range(2, n + 1):
        actual = (anterior_1 + 2 * anterior_2 + i) % MOD
        anterior_2 = anterior_1
        anterior_1 = actual
    return anterior_1


def main() -> None:
    """Ejecuta las verificaciones con assert y muestra el reporte solicitado."""
    global llamadas_rec

    # 1. Conteo de llamadas de t_rec(20)
    llamadas_rec = 0
    valor_20 = t_rec(20)
    print(f"t_rec(20) = {valor_20} | Llamadas realizadas: {llamadas_rec}")

    # 2. Verificación de equivalencia para n de 0 a 22
    for n in range(23):
        r_rec = t_rec(n)
        r_memo = t_memo(n)
        r_it = t_it(n)
        assert r_rec == r_memo == r_it, f"Discrepancia en n={n}"
    print("Verificación exitosa: t_rec, t_memo y t_it coinciden para n = 0..22.")

    # 3. Reporte de t(30), t(200) y t(5000)
    print(f"t(30)   = {t_it(30)}")
    print(f"t(200)  = {t_it(200)}")
    print(f"t(5000) = {t_it(5000)}")

    # 4. Intento de t_memo(5000) y captura del error de recursión
    try:
        t_memo(5000)
    except RecursionError as error:
        print(f"Error capturado al ejecutar t_memo(5000): {type(error).__name__} -> {error}")

    # Explicación:
    # t_memo(5000) falla con RecursionError porque antes de resolver t_memo(5000)
    # debe apilar 5000 marcos de llamada descendentes (4999, 4998, ..., 1) en la pila
    # de ejecución de Python, superando el límite por defecto (~1000 marcos).
    # En cambio, t_it(5000) no lo sufre porque utiliza un bucle iterativo 'for' con
    # un único marco de función y dos variables locales (memoria constante O(1)).


if __name__ == "__main__":
    main()