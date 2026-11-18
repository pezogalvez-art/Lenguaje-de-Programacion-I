"""Proyecto PC05 - B2: Ordenamiento nativo con libc.qsort y comparador CFUNCTYPE.

Código universitario: 2155263 | Estudiante: Pezo | Constantes: D = 3, P = 6, K = 2.
"""

import ctypes
import ctypes.util
import os
from typing import Callable, Final
from generadores_u3 import arreglo_personal

CODIGO_UNIVERSITARIO: Final[int] = 2155263
N: Final[int] = 12


def _cargar_libc() -> ctypes.CDLL:
    """Carga la biblioteca estándar de C según el sistema operativo."""
    if os.name == "nt":
        return ctypes.cdll.msvcrt
    ruta_c = ctypes.util.find_library("c")
    if ruta_c is None:
        raise RuntimeError("No se encontró la biblioteca estándar de C (libc).")
    return ctypes.CDLL(ruta_c)


def suma_digitos_abs(x: int) -> int:
    """Calcula la suma de los dígitos del valor absoluto de x."""
    n = abs(x)
    total = 0
    while n > 0:
        total += n % 10
        n //= 10
    return total


def crear_comparador_qsort() -> tuple[ctypes._CFuncPtr, Callable[[], int]]:
    """Construye el callback CFUNCTYPE y un closure contador de invocaciones."""
    llamadas = 0
    CMP_FUNC = ctypes.CFUNCTYPE(
        ctypes.c_int,
        ctypes.POINTER(ctypes.c_int),
        ctypes.POINTER(ctypes.c_int),
    )

    def _comparar(ptr_a: ctypes.POINTER(ctypes.c_int), ptr_b: ctypes.POINTER(ctypes.c_int)) -> int:
        nonlocal llamadas
        llamadas += 1
        a = ptr_a.contents.value
        b = ptr_b.contents.value

        sa = suma_digitos_abs(a)
        sb = suma_digitos_abs(b)

        # 1. Mayor suma de dígitos primero (descendente)
        if sa != sb:
            return -1 if sa > sb else 1
        # 2. En caso de empate, menor valor primero (ascendente)
        if a != b:
            return -1 if a < b else 1
        return 0

    def obtener_llamadas() -> int:
        return llamadas

    # Envolvemos la función Python en el tipo nativo de C
    callback_c = CMP_FUNC(_comparar)
    return callback_c, obtener_llamadas


def main() -> None:
    """Ordena el arreglo personal usando qsort de C y verifica con assert."""
    datos = arreglo_personal(CODIGO_UNIVERSITARIO)
    bloque = (ctypes.c_int * N)(*datos)

    libc = _cargar_libc()
    libc.qsort.argtypes = [
        ctypes.c_void_p,
        ctypes.c_size_t,
        ctypes.c_size_t,
        ctypes.c_void_p,
    ]
    libc.qsort.restype = None

    # IMPORTANTE: Guardamos el objeto callback en la variable `comparador_c` durante toda
    # la ejecución de qsort. C solo recibe la dirección de memoria cruda del trampoline
    # y no incrementa el contador de referencias de Python (ob_refcnt); si no se conserva
    # una referencia viva en Python, el recolector liberaría el callback en medio de
    # la ejecución de qsort provocando un fallo de segmentación (SIGSEGV / Access Violation).
    comparador_c, total_llamadas = crear_comparador_qsort()

    libc.qsort(bloque, N, ctypes.sizeof(ctypes.c_int), comparador_c)

    resultado = [bloque[i] for i in range(N)]
    esperado = sorted(datos, key=lambda x: (-suma_digitos_abs(x), x))

    assert resultado == esperado, f"Error en ordenamiento: {resultado} != {esperado}"

    print("Arreglo original :", datos)
    print("Arreglo ordenado :", resultado)
    print(f"Comparaciones realizadas por qsort: {total_llamadas()}")
    print("Verificación assert contra sorted(): OK")


if __name__ == "__main__":
    main()