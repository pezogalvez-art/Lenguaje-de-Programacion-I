"""Proyecto PC03 - Parte B2: Decorador auditor con parámetros y estado propio.

Código universitario: 2155263 | Constantes personales: D = 3, P = 6, K = 2.
"""

from collections.abc import Callable
from typing import Any, Final

D: Final[int] = 3
MAX_LLAMADAS_PERSONAL: Final[int] = 5 + D  # 5 + 3 = 8


def auditar(max_llamadas: int) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Crea un decorador que audita llamadas y limita su ejecución.

    Args:
        max_llamadas: Cantidad máxima de ejecuciones permitidas antes de lanzar error.

    Returns:
        Un decorador que envuelve la función con historial, límite y reiniciar().

    Raises:
        ValueError: Si max_llamadas es menor que 1.
    """
    if max_llamadas < 1:
        raise ValueError("max_llamadas debe ser al menos 1")

    def decorador(func: Callable[..., Any]) -> Callable[..., Any]:
        llamadas: int = 0
        historial: list[tuple[tuple[Any, ...], Any]] = []

        def envoltura(*args: Any, **kwargs: Any) -> Any:
            nonlocal llamadas
            if llamadas >= max_llamadas:
                raise RuntimeError(
                    f"La función '{func.__name__}' superó el límite de {max_llamadas} llamadas"
                )
            resultado = func(*args, **kwargs)
            llamadas += 1
            argumentos = args if not kwargs else (args, kwargs)
            historial.append((argumentos, resultado))
            return resultado

        def reiniciar() -> None:
            """Reinicia el conteo de llamadas y vacía el historial de la función."""
            nonlocal llamadas
            llamadas = 0
            historial.clear()

        envoltura.__name__ = func.__name__
        envoltura.__doc__ = func.__doc__
        envoltura.historial = historial  # type: ignore[attr-defined]
        envoltura.reiniciar = reiniciar  # type: ignore[attr-defined]
        return envoltura

    return decorador


@auditar(MAX_LLAMADAS_PERSONAL)
def es_primo(n: int) -> bool:
    """Determina si un número entero n es primo.

    Args:
        n: Número entero a evaluar.

    Returns:
        True si n es primo; False en caso contrario.
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    divisor = 3
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 2
    return True


@auditar(2)
def doble(x: int) -> int:
    """Devuelve el doble de un entero x."""
    return x * 2


def main() -> None:
    """Prueba con assert todas las funcionalidades del decorador auditar."""
    # 1. Ejecutar es_primo exactamente MAX_LLAMADAS_PERSONAL (8) veces
    pruebas = [1, 2, 3, 4, 5, 9, 11, 15]
    esperados = [False, True, True, False, True, False, True, False]
    resultados = [es_primo(num) for num in pruebas]
    assert resultados == esperados

    # 2. Verificar que el historial guardó las 8 tuplas ((n,), resultado)
    assert len(es_primo.historial) == MAX_LLAMADAS_PERSONAL
    assert es_primo.historial[0] == ((1,), False)
    assert es_primo.historial[1] == ((2,), True)
    assert es_primo.historial[-1] == ((15,), False)

    # 3. La llamada número 9 debe lanzar RuntimeError con el nombre 'es_primo'
    error_lanzado = False
    try:
        es_primo(17)
    except RuntimeError as exc:
        error_lanzado = True
        assert "es_primo" in str(exc)
    assert error_lanzado, "Debió lanzar RuntimeError al superar el límite"

    # 4. Verificar que otra función decorada ('doble') tiene su propio conteo independiente
    assert doble(10) == 20
    assert len(doble.historial) == 1
    assert len(es_primo.historial) == 8

    # 5. Verificar que reiniciar() limpia historial y permite volver a llamar
    es_primo.reiniciar()
    assert len(es_primo.historial) == 0
    assert es_primo(7) is True
    assert len(es_primo.historial) == 1
    assert es_primo.historial[0] == ((7,), True)

    print("Todas las pruebas de pc3_b2.py pasaron correctamente.")


if __name__ == "__main__":
    main()

# ==============================================================================
# DIAGRAMA DE LOS TRES NIVELES DE FUNCIONES ANIDADAS Y ÁMBITOS (LEGB)
# ==============================================================================
#
# NIVEL 0 — Ámbito Global (módulo pc3_b2):
#   Nombres: D, MAX_LLAMADAS_PERSONAL, auditar, es_primo, doble, main
#
# ┌─ NIVEL 1: def auditar(max_llamadas)  [Ámbito Enclosing externo] ───────────┐
# │  Nombres locales a auditar:                                                │
# │    - max_llamadas  (parámetro recibido: ej. 8 para es_primo, 2 para doble) │
# │    - decorador     (función interna definida aquí)                         │
# │                                                                            │
# │  ┌─ NIVEL 2: def decorador(func)  [Ámbito Enclosing intermedio] ────────┐  │
# │  │  Nombres locales a decorador (estado privado por función decorada):  │  │
# │  │    - func       (función original recibida: es_primo o doble)        │  │
# │  │    - llamadas   (contador entero iniciado en 0)                      │  │
# │  │    - historial  (lista de tuplas (argumentos, resultado))            │  │
# │  │    - envoltura  (función wrapper que reemplaza a func)               │  │
# │  │    - reiniciar  (función auxiliar adjuntada como atributo)           │  │
# │  │                                                                      │  │
# │  │  ┌─ NIVEL 3: def envoltura(*args, **kwargs)  [Ámbito Local] ──────┐  │  │
# │  │  │  Nombres locales: args, kwargs, resultado, argumentos          │  │  │
# │  │  │  Usa 'nonlocal llamadas' (Nivel 2) y lee 'historial' (Nivel 2),│  │  │
# │  │  │  'func' (Nivel 2) y 'max_llamadas' (Nivel 1).                  │  │  │
# │  │  └────────────────────────────────────────────────────────────────┘  │  │
# │  │  ┌─ NIVEL 3: def reiniciar()  [Ámbito Local] ─────────────────────┐  │  │
# │  │  │  Usa 'nonlocal llamadas' (Nivel 2) y muta 'historial.clear()'. │  │  │
# │  │  └────────────────────────────────────────────────────────────────┘  │  │
# │  └──────────────────────────────────────────────────────────────────────┘  │
# └────────────────────────────────────────────────────────────────────────────┘