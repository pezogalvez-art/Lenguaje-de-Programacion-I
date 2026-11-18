"""Generadores deterministas de datos personales para la Unidad III (LP1 - UNAP).

Semilla determinista basada en el código universitario (2155263).
Provee catalogo_bodega y movimientos_bodega reproducibles para EU3.
"""

import random


def catalogo_bodega(tu_codigo: int) -> list[tuple[str, str, str, float, int, int]]:
    """Devuelve 8 productos únicos de una bodega de Iquitos para tu_codigo."""
    rng = random.Random(tu_codigo + 404)
    plantilla = [
        ("P104", "Arroz Superior 5kg", "Abarrotes", 18.50),
        ("P101", "Aceite Vegetal 1L", "Abarrotes", 8.20),
        ("P108", "Azúcar Rubia 1kg", "Abarrotes", 4.10),
        ("P103", "Fariña de Yuca 1kg", "Regionales", 6.50),
        ("P106", "Leche Evaporada 400g", "Lácteos", 4.40),
        ("P102", "Café Amazónico 250g", "Regionales", 14.00),
        ("P107", "Detergente en Polvo 1kg", "Limpieza", 9.80),
        ("P105", "Atún en Trozos 170g", "Conservas", 5.50),
    ]
    catalogo: list[tuple[str, str, str, float, int, int]] = []
    for codigo, nombre, categoria, precio_base in plantilla:
        precio = round(precio_base + rng.choice([0.0, 0.30, 0.50]), 2)
        stock_ini = rng.randint(8, 25)
        stock_min = rng.randint(6, 12)
        catalogo.append((codigo, nombre, categoria, precio, stock_ini, stock_min))
    return catalogo


def movimientos_bodega(tu_codigo: int) -> list[str]:
    """Devuelve líneas CSV 'dia,tipo,codigo,cantidad' con casos válidos y rechazos."""
    rng = random.Random(tu_codigo + 505)
    c1 = rng.randint(4, 9)
    c2 = rng.randint(5, 10)
    c3 = rng.randint(3, 7)
    c4 = rng.randint(6, 12)
    c5 = rng.randint(2, 6)
    return [
        f"02,ENTRADA,P101,{c1}",
        f"03,SALIDA,P104,{c2}",
        "04,DEVOLUCION,P103,5",      # Rechazo: dato inválido (tipo no es ENTRADA ni SALIDA)
        f"05,SALIDA,P108,{c3}",
        "06,SALIDA,P999,4",          # Rechazo: dato inválido (código no existe)
        "07,SALIDA,P105,500",        # Rechazo: stock insuficiente
        f"08,ENTRADA,P102,{c4}",
        f"10,SALIDA,P106,{c5}",
        "12,ENTRADA,P107,-3",        # Rechazo: dato inválido (cantidad <= 0)
        f"15,SALIDA,P101,{c1}",
        f"18,ENTRADA,P104,{c3}",
        "20,SALIDA,P102,400",        # Rechazo: stock insuficiente
        f"24,SALIDA,P103,{c5}",
        f"28,ENTRADA,P107,{c2}",
    ]