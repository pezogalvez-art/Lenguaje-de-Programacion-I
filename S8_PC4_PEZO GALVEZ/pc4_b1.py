"""Proyecto PC04 - Parte B1: Ranking de registros con inserción y búsqueda binaria.

Código universitario: 2155263 | Constantes personales: D = 3, P = 6, K = 2.
"""

import random
import unicodedata
from typing import Final

CODIGO_UNIVERSITARIO: Final[int] = 2155263
D: Final[int] = 3
P: Final[int] = 6
K: Final[int] = 2

Registro = tuple[str, float, int]


def generar_registros(tu_codigo: int) -> list[Registro]:
    """Genera 25 tuplas deterministas (apellido, nota, edad) a partir del código."""
    rng = random.Random(tu_codigo)
    apellidos_base = (
        "Ávila", "Alvarado", "Báez", "Benítez", "Cárdenas",
        "Chávez", "Díaz", "Escobar", "Fernández", "Gómez",
        "Gutiérrez", "Huamán", "Jiménez", "López", "Martínez",
        "Méndez", "Núñez", "Ñahui", "Ortega", "Pérez",
        "Quispe", "Ramírez", "Sánchez", "Torres", "Vásquez",
    )
    registros: list[Registro] = []
    for _ in range(25):
        apellido = rng.choice(apellidos_base)
        # Notas en pasos de 0.5 para garantizar empates reales en el ranking
        nota = rng.randint(18, 40) / 2.0
        edad = rng.randint(18, 26)
        registros.append((apellido, nota, edad))
    return registros


def normalizar(texto: str) -> str:
    """Elimina tildes y diacríticos manteniendo caracteres base en mayúsculas/minúsculas."""
    descompuesto = unicodedata.normalize("NFD", texto)
    sin_tildes = "".join(
        ch for ch in descompuesto if unicodedata.category(ch) != "Mn"
    )
    return sin_tildes.casefold()


def _es_menor_clave(a: Registro, b: Registro) -> bool:
    """Devuelve True si el registro 'a' debe ir antes que 'b' en el ranking.

    Criterio:
      1. Nota descendente (a[1] > b[1]).
      2. Edad ascendente (a[2] < b[2]).
      3. Apellido ascendente sin tildes (normalizar(a[0]) < normalizar(b[0])).
    """
    if a[1] != b[1]:
        return a[1] > b[1]
    if a[2] != b[2]:
        return a[2] < b[2]
    return normalizar(a[0]) < normalizar(b[0])


def ordenar_registros(regs: list[Registro]) -> list[Registro]:
    """Ordena una copia de los registros mediante inserción propia.

    Args:
        regs: Lista original de tuplas (apellido, nota, edad).

    Returns:
        Nueva lista ordenada sin mutar la lista original.
    """
    resultado = regs[:]
    n = len(resultado)
    for i in range(1, n):
        clave = resultado[i]
        j = i - 1
        while j >= 0 and _es_menor_clave(clave, resultado[j]):
            resultado[j + 1] = resultado[j]
            j -= 1
        resultado[j + 1] = clave
    return resultado


def buscar_por_nota(regs_ordenados: list[Registro], nota: float) -> list[Registro]:
    """Devuelve todos los registros con 'nota' mediante búsqueda binaria en O(log n + k).

    Args:
        regs_ordenados: Lista ordenada por nota descendente.
        nota: Calificación exacta a buscar.

    Returns:
        Sublista con todos los registros que tienen esa nota (en el orden del ranking).
    """
    n = len(regs_ordenados)
    if n == 0:
        return []

    # 1. Búsqueda binaria de la primera aparición (límite izquierdo)
    lo, hi = 0, n - 1
    inicio = -1
    while lo <= hi:
        m = (lo + hi) // 2
        nota_m = regs_ordenados[m][1]
        if nota_m == nota:
            inicio = m
            hi = m - 1  # Seguir buscando hacia la izquierda
        elif nota_m > nota:
            lo = m + 1  # Como está descendente, notas menores están a la derecha
        else:
            hi = m - 1

    if inicio == -1:
        return []

    # 2. Búsqueda binaria de la última aparición (límite derecho)
    lo, hi = inicio, n - 1
    fin = inicio
    while lo <= hi:
        m = (lo + hi) // 2
        nota_m = regs_ordenados[m][1]
        if nota_m == nota:
            fin = m
            lo = m + 1  # Seguir buscando hacia la derecha
        elif nota_m > nota:
            lo = m + 1
        else:
            hi = m - 1

    return regs_ordenados[inicio : fin + 1]


def imprimir_top_5(regs_ordenados: list[Registro]) -> None:
    """Imprime los primeros 5 registros del ranking en una tabla alineada."""
    print("=" * 42)
    print(f"{'PUESTO':<8}{'APELLIDO':<16}{'NOTA':>8}{'EDAD':>8}")
    print("-" * 42)
    limite = 5 if len(regs_ordenados) >= 5 else len(regs_ordenados)
    for idx in range(limite):
        apellido, nota, edad = regs_ordenados[idx]
        print(f"{idx + 1:<8}{apellido:<16}{nota:>8.2f}{edad:>8}")
    print("=" * 42)


def main() -> None:
    """Ejecuta el ordenamiento, verificación assert y búsqueda binaria por nota."""
    registros = generar_registros(CODIGO_UNIVERSITARIO)
    ranking = ordenar_registros(registros)

    # Verificar que no se mutó la lista original y que coincide con sorted()
    assert len(ranking) == 25
    assert ranking is not registros
    esperado = sorted(
        registros,
        key=lambda r: (-r[1], r[2], normalizar(r[0])),
    )
    assert ranking == esperado, "El ordenamiento por inserción no coincide con sorted"

    print("Top 5 del ranking de registros:")
    imprimir_top_5(ranking)

    # Probar búsqueda binaria con una nota existente (la del primer puesto) y una inexistente
    nota_objetivo = ranking[0][1]
    encontrados = buscar_por_nota(ranking, nota_objetivo)
    assert len(encontrados) >= 1
    for reg in encontrados:
        assert reg[1] == nota_objetivo

    assert buscar_por_nota(ranking, 99.0) == []

    print(f"\nRegistros encontrados con nota {nota_objetivo:.2f} ({len(encontrados)}):")
    for apellido, nota, edad in encontrados:
        print(f"  - {apellido:<14} | Nota: {nota:.2f} | Edad: {edad}")


if __name__ == "__main__":
    main()