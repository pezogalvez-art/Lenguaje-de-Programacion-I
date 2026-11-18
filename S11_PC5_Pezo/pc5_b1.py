"""Proyecto PC05 - B1: Arreglo personal en memoria cruda con punteros ctypes.

Código universitario: 2155263 | Estudiante: Pezo | Constantes: D = 3, P = 6, K = 2.
Restricción: todo acceso al bloque se realiza por puntero o direcciones (sin indexar
el arreglo original ni usar sum, max o list sobre él).
"""

import ctypes
from typing import Final
from generadores_u3 import arreglo_personal

CODIGO_UNIVERSITARIO: Final[int] = 2155263
D: Final[int] = 3
N: Final[int] = 12


def imprimir_tabla_memoria(p: ctypes.POINTER(ctypes.c_int), n: int) -> None:
    """Imprime índice, dirección hexadecimal, desplazamiento en bytes y valor."""
    dir_base = ctypes.addressof(p.contents)
    tam_elem = ctypes.sizeof(ctypes.c_int)

    print(f"{'ÍNDICE':<8}{'DIRECCIÓN HEX':<20}{'DESPLAZ. (B)':>14}{'VALOR':>10}")
    print("-" * 52)
    for i in range(n):
        desplazamiento = i * tam_elem
        direccion_actual = dir_base + desplazamiento
        valor = ctypes.c_int.from_address(direccion_actual).value
        print(f"{i:<8}{hex(direccion_actual):<20}{desplazamiento:>14}{valor:>10}")


def suma_puntero(p: ctypes.POINTER(ctypes.c_int), n: int) -> int:
    """Calcula la suma de los n elementos accediendo únicamente por direcciones."""
    dir_base = ctypes.addressof(p.contents)
    tam_elem = ctypes.sizeof(ctypes.c_int)
    total = 0
    for i in range(n):
        total += ctypes.c_int.from_address(dir_base + i * tam_elem).value
    return total


def maximo_puntero(p: ctypes.POINTER(ctypes.c_int), n: int) -> tuple[int, int]:
    """Devuelve (valor_maximo, desplazamiento_bytes) de la primera aparición."""
    dir_base = ctypes.addressof(p.contents)
    tam_elem = ctypes.sizeof(ctypes.c_int)

    max_val = ctypes.c_int.from_address(dir_base).value
    max_desplaz = 0

    for i in range(1, n):
        desplaz = i * tam_elem
        val = ctypes.c_int.from_address(dir_base + desplaz).value
        if val > max_val:
            max_val = val
            max_desplaz = desplaz

    return max_val, max_desplaz


def _invertir_tramo(p: ctypes.POINTER(ctypes.c_int), ini: int, fin: int) -> None:
    """Invierte en el sitio el subrango [ini, fin] usando direcciones crudas."""
    dir_base = ctypes.addressof(p.contents)
    tam_elem = ctypes.sizeof(ctypes.c_int)

    while ini < fin:
        celda_izq = ctypes.c_int.from_address(dir_base + ini * tam_elem)
        celda_der = ctypes.c_int.from_address(dir_base + fin * tam_elem)
        tmp = celda_izq.value
        celda_izq.value = celda_der.value
        celda_der.value = tmp
        ini += 1
        fin -= 1


def rotar_izquierda(p: ctypes.POINTER(ctypes.c_int), n: int, k: int) -> None:
    """Rota el arreglo k posiciones a la izquierda en O(n) con tres inversiones."""
    if n <= 1:
        return
    pasos = k % n
    if pasos == 0:
        return
    _invertir_tramo(p, 0, pasos - 1)
    _invertir_tramo(p, pasos, n - 1)
    _invertir_tramo(p, 0, n - 1)


def obtener_como_texto(p: ctypes.POINTER(ctypes.c_int), n: int) -> str:
    """Formatea los valores del bloque como cadena leyendo por direcciones."""
    dir_base = ctypes.addressof(p.contents)
    tam_elem = ctypes.sizeof(ctypes.c_int)
    partes: list[str] = []
    for i in range(n):
        val = ctypes.c_int.from_address(dir_base + i * tam_elem).value
        partes.append(str(val))
    return "[" + ", ".join(partes) + "]"


def main() -> None:
    """Ejecuta las operaciones de memoria cruda sobre el arreglo personal."""
    datos_origen = arreglo_personal(CODIGO_UNIVERSITARIO)
    bloque = (ctypes.c_int * N)(*datos_origen)
    p = ctypes.cast(bloque, ctypes.POINTER(ctypes.c_int))

    print("=== TABLA DE MEMORIA CRUDA (c_int * 12) ===")
    imprimir_tabla_memoria(p, N)

    total = suma_puntero(p, N)
    val_max, desp_max = maximo_puntero(p, N)
    print(f"\nSuma total       : {total}")
    print(f"Valor máximo     : {val_max} (desplazamiento: {desp_max} bytes)")

    k = D % N
    rotar_izquierda(p, N, k)
    print(f"\nArreglo rotado k = {k} posiciones a la izquierda:")
    print(obtener_como_texto(p, N))


if __name__ == "__main__":
    main()