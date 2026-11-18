"""Proyecto PC03 - Parte B3: Cambio de monedas con recursividad y memoización.

Código: 2155263 | Constantes personales: D = 3, P = 6, K = 2.
"""

from typing import Final

D: Final[int] = 3
MONTO_PERSONAL: Final[int] = 50 + 7 * D  # 50 + 21 = 71 soles
MONEDAS: Final[tuple[int, ...]] = (1, 2, 5, 10, 20)


def formas(m: int, i: int = 0, memo: dict[tuple[int, int], int] | None = None) -> int:
    """Cuenta combinaciones distintas para pagar m usando monedas desde el índice i.

    Args:
        m: Monto restante por pagar.
        i: Índice actual en la tupla MONEDAS.
        memo: Diccionario propio de memoización {(m, i): cantidad}.

    Returns:
        Número de combinaciones distintas sin importar el orden.

    Raises:
        ValueError: Si m o i son negativos.
    """
    if m < 0 or i < 0:
        raise ValueError("m e i deben ser enteros no negativos")
    if memo is None:
        memo = {}
    if m == 0:
        return 1
    if i >= len(MONEDAS):
        return 0
    estado = (m, i)
    if estado in memo:
        return memo[estado]

    moneda = MONEDAS[i]
    # Opción 1: usar al menos una moneda de MONEDAS[i] (si cabe) + Opción 2: pasar a i + 1
    usar = formas(m - moneda, i, memo) if moneda <= m else 0
    saltar = formas(m, i + 1, memo)
    memo[estado] = usar + saltar
    return memo[estado]


def minimo_monedas(m: int) -> int:
    """Calcula la menor cantidad de monedas para pagar m usando enfoque voraz.

    Args:
        m: Monto entero no negativo en soles.

    Returns:
        Cantidad mínima de monedas necesarias.

    Raises:
        ValueError: Si m es negativo.
    """
    if m < 0:
        raise ValueError("El monto m debe ser no negativo")
    restante = m
    total_monedas = 0
    for moneda in reversed(MONEDAS):
        cantidad = restante // moneda
        total_monedas += cantidad
        restante %= moneda
    return total_monedas


# Justificación del método voraz:
# 1. Por qué es correcto para (1, 2, 5, 10, 20): Este sistema es canónico; cada
#    denominación mayor cumple que reemplazar combinaciones de monedas menores
#    (por ejemplo: 1+1=2, 2+2+1=5, 5+5=10, 10+10=20) nunca requiere más monedas
#    que tomar primero la moneda más grande posible. Por ello, elegir siempre la
#    moneda de mayor valor que no exceda el monto restante garantiza el óptimo global.
# 2. Contraejemplo donde el método voraz falla: Con el sistema (1, 3, 4) y monto
#    m = 6, el algoritmo voraz elige primero 4 y completa con dos de 1 (4 + 1 + 1),
#    usando 3 monedas, cuando la solución óptima es 3 + 3 (solo 2 monedas).


def formas_con_tope(
    m: int,
    i: int = 0,
    k: int = 0,
    memo: dict[tuple[int, int, int], int] | None = None,
) -> int:
    """Cuenta combinaciones distintas para pagar m usando a lo más k monedas.

    Args:
        m: Monto restante por pagar.
        i: Índice actual en la tupla MONEDAS.
        k: Máximo de monedas permitidas.
        memo: Diccionario propio de memoización {(m, i, k): cantidad}.

    Returns:
        Cantidad de combinaciones distintas con at most k monedas.

    Raises:
        ValueError: Si m, i o k son negativos.
    """
    if m < 0 or i < 0 or k < 0:
        raise ValueError("m, i y k deben ser enteros no negativos")
    if memo is None:
        memo = {}
    if m == 0:
        return 1
    if i >= len(MONEDAS) or k == 0:
        return 0
    estado = (m, i, k)
    if estado in memo:
        return memo[estado]

    moneda = MONEDAS[i]
    usar = formas_con_tope(m - moneda, i, k - 1, memo) if moneda <= m else 0
    saltar = formas_con_tope(m, i + 1, k, memo)
    memo[estado] = usar + saltar
    return memo[estado]


def listar_combinaciones_tope(m: int, k: int) -> list[str]:
    """Genera todas las combinaciones de m con a lo más k monedas en formato '20×3 + ...'.

    Args:
        m: Monto total a pagar.
        k: Límite máximo de monedas.

    Returns:
        Lista de cadenas formateadas de mayor a menor denominación.
    """
    monedas_desc = tuple(reversed(MONEDAS))
    resultados: list[str] = []

    def backtrack(idx: int, restante: int, cupo: int, actual: list[tuple[int, int]]) -> None:
        if restante == 0:
            texto = " + ".join(f"{valor}×{cant}" for valor, cant in actual)
            resultados.append(texto)
            return
        if idx >= len(monedas_desc) or cupo == 0:
            return

        valor = monedas_desc[idx]
        max_posible = min(restante // valor, cupo)
        for cant in range(max_posible, -1, -1):
            if cant > 0:
                actual.append((valor, cant))
            backtrack(idx + 1, restante - valor * cant, cupo - cant, actual)
            if cant > 0:
                actual.pop()

    backtrack(0, m, k, [])
    return resultados


def main() -> None:
    """Ejecuta reportes, verificaciones con assert e impresión de combinaciones."""
    # Pruebas de control con assert
    assert formas(0, 0) == 1
    assert formas(5, 0) == 4  # (5), (2+2+1), (2+1+1+1), (1*5)
    assert minimo_monedas(0) == 0
    assert minimo_monedas(MONTO_PERSONAL) == 5  # 20*3 + 10*1 + 1*1

    # 1. Total de formas para M = 71 soles
    total_formas = formas(MONTO_PERSONAL, 0)
    print(f"Monto personal M = {MONTO_PERSONAL} soles (D = {D})")
    print(f"1. Total de combinaciones distintas formas({MONTO_PERSONAL}, 0): {total_formas}")

    # 2. Mínimo de monedas
    minimo = minimo_monedas(MONTO_PERSONAL)
    print(f"2. Mínimo de monedas para {MONTO_PERSONAL} soles: {minimo}")

    # 3. Combinaciones con tope k = minimo + 2
    tope_k = minimo + 2
    total_tope = formas_con_tope(MONTO_PERSONAL, 0, tope_k)
    combinaciones = listar_combinaciones_tope(MONTO_PERSONAL, tope_k)
    assert total_tope == len(combinaciones)

    print(f"3. Formas con a lo más k = {tope_k} monedas: {total_tope}")
    print(f"4. Listado de las {total_tope} combinaciones (formato valor×cantidad):")
    for idx, comb in enumerate(combinaciones, start=1):
        print(f"   {idx:>2}. {comb}")


if __name__ == "__main__":
    main()