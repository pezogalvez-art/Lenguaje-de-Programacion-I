"""Proyecto PC06 - B3: Validación de ventas CSV y reporte ordenado sin tildes.

Código universitario: 2155263 | Estudiante: Pezo | Constantes: D = 3, P = 6, K = 2.
"""

import csv
import unicodedata
from pathlib import Path
from typing import Final
from generadores_u3 import lineas_ventas

CODIGO_UNIVERSITARIO: Final[int] = 2155263
RUTA_CSV: Final[Path] = Path(__file__).with_name("ventas.csv")
RUTA_REPORTE: Final[Path] = Path(__file__).with_name("reporte_ventas.txt")


def normalizar(texto: str) -> str:
    """Devuelve texto en minúsculas y sin marcas diacríticas (tildes) para ordenar."""
    descompuesto = unicodedata.normalize("NFD", texto.lower())
    return "".join(ch for ch in descompuesto if unicodedata.category(ch) != "Mn")


def escribir_csv_origen(ruta: Path, lineas: list[str]) -> None:
    """Escribe las líneas generadas en ventas.csv usando UTF-8."""
    with ruta.open("w", encoding="utf-8", newline="") as archivo:
        for linea in lineas:
            archivo.write(linea + "\n")


def procesar_ventas(ruta: Path) -> tuple[int, list[int], dict[str, float]]:
    """Lee ventas.csv, valida cada fila y acumula el total por categoría."""
    filas_validas = 0
    lineas_invalidas: list[int] = []
    totales_categoria: dict[str, float] = {}

    with ruta.open("r", encoding="utf-8", newline="") as archivo:
        lector = csv.reader(archivo)
        for num_linea, fila in enumerate(lector, start=1):
            if num_linea == 1:
                continue  # Saltar cabecera
            if len(fila) != 5:
                lineas_invalidas.append(num_linea)
                continue

            _, _, categoria, cant_txt, precio_txt = [campo.strip() for campo in fila]
            try:
                cantidad = int(cant_txt)
                precio = float(precio_txt)
            except ValueError:
                lineas_invalidas.append(num_linea)
                continue

            if not categoria or cantidad <= 0 or precio <= 0:
                lineas_invalidas.append(num_linea)
                continue

            filas_validas += 1
            totales_categoria[categoria] = (
                totales_categoria.get(categoria, 0.0) + cantidad * precio
            )

    totales_redondeados = {
        cat: round(monto, 2) for cat, monto in totales_categoria.items()
    }
    return filas_validas, lineas_invalidas, totales_redondeados


def escribir_reporte(
    ruta: Path,
    filas_validas: int,
    lineas_invalidas: list[int],
    totales: dict[str, float],
) -> None:
    """Genera reporte_ventas.txt alineado con f-strings y categorías ordenadas sin tildes."""
    categorias_ordenadas = sorted(totales.keys(), key=normalizar)
    invalidas_str = ", ".join(str(n) for n in lineas_invalidas) if lineas_invalidas else "Ninguna"

    lineas_salida = [
        "=" * 54,
        f"{'REPORTE DE VENTAS POR CATEGORÍA':^54}",
        "=" * 54,
        f"Filas válidas procesadas : {filas_validas}",
        f"Líneas inválidas (núm.)  : {invalidas_str}",
        "-" * 54,
        f"{'CATEGORÍA':<28}{'TOTAL VENDIDO (S/)':>26}",
        "-" * 54,
    ]

    total_general = 0.0
    for cat in categorias_ordenadas:
        monto = totales[cat]
        total_general += monto
        lineas_salida.append(f"{cat:<28}{monto:>26,.2f}")

    lineas_salida.extend(
        [
            "-" * 54,
            f"{'TOTAL GENERAL':<28}{round(total_general, 2):>26,.2f}",
            "=" * 54,
        ]
    )

    contenido = "\n".join(lineas_salida) + "\n"
    with ruta.open("w", encoding="utf-8") as archivo:
        archivo.write(contenido)
    print(contenido)


def main() -> None:
    """Orquesta la generación del CSV, validación y emisión del reporte."""
    escribir_csv_origen(RUTA_CSV, lineas_ventas(CODIGO_UNIVERSITARIO))
    validas, invalidas, totales = procesar_ventas(RUTA_CSV)
    escribir_reporte(RUTA_REPORTE, validas, invalidas, totales)


if __name__ == "__main__":
    main()