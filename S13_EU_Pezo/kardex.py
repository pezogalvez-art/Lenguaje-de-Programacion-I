"""Módulo principal del sistema Kardex de bodega (EU3).

Código universitario: 2155263 | Estudiante: Pezo | Constantes: D = 3, P = 6, K = 2.
Restricciones cumplidas: sin list/dict como contenedores principales, sin sort,
sorted, min, max, sum ni pandas.
"""

import csv
import gc
from pathlib import Path
import tracemalloc
from typing import Final

from estructuras import Historial, ListaInventario, ListaRechazos, Producto
from generadores_u3 import catalogo_bodega, movimientos_bodega

CODIGO_UNIVERSITARIO: Final[int] = 2155263
DIR_BASE: Final[Path] = Path(__file__).resolve().parent
RUTA_CATALOGO: Final[Path] = DIR_BASE / "catalogo.csv"
RUTA_MOVIMIENTOS: Final[Path] = DIR_BASE / "movimientos.csv"
RUTA_REPORTE: Final[Path] = DIR_BASE / "kardex_reporte.txt"
RUTA_ACTUALIZADO: Final[Path] = DIR_BASE / "catalogo_actualizado.csv"


def generar_archivos_entrada(
    ruta_cat: Path = RUTA_CATALOGO,
    ruta_mov: Path = RUTA_MOVIMIENTOS,
    tu_codigo: int = CODIGO_UNIVERSITARIO,
) -> None:
    """Escribe catalogo.csv y movimientos.csv con cabecera en UTF-8."""
    with ruta_cat.open("w", encoding="utf-8", newline="") as f_cat:
        escritor = csv.writer(f_cat)
        escritor.writerow(
            ["codigo", "nombre", "categoria", "precio", "stock_inicial", "stock_minimo"]
        )
        for fila in catalogo_bodega(tu_codigo):
            escritor.writerow(fila)

    with ruta_mov.open("w", encoding="utf-8", newline="") as f_mov:
        f_mov.write("dia,tipo,codigo,cantidad\n")
        for linea in movimientos_bodega(tu_codigo):
            f_mov.write(linea.strip() + "\n")


def cargar_inventario(ruta_cat: Path) -> tuple[ListaInventario, ListaRechazos]:
    """Carga catalogo.csv en una ListaInventario ordenada validando cada fila."""
    inventario = ListaInventario()
    errores_catalogo = ListaRechazos()

    with ruta_cat.open("r", encoding="utf-8", newline="") as f_cat:
        lector = csv.reader(f_cat)
        for num_linea, fila in enumerate(lector, start=1):
            if num_linea == 1:
                continue  # Cabecera
            if len(fila) != 6:
                errores_catalogo.agregar(num_linea, "dato inválido", "cantidad de columnas != 6")
                continue

            codigo = fila[0].strip()
            nombre = fila[1].strip()
            categoria = fila[2].strip()
            try:
                precio = float(fila[3].strip())
                stock_ini = int(fila[4].strip())
                stock_min = int(fila[5].strip())
            except ValueError:
                errores_catalogo.agregar(num_linea, "dato inválido", "tipos numéricos inválidos")
                continue

            if not codigo or not nombre or not categoria or precio <= 0 or stock_ini < 0 or stock_min < 0:
                errores_catalogo.agregar(num_linea, "dato inválido", "valores fuera de dominio")
                continue

            try:
                inventario.insertar_ordenado(
                    Producto(codigo, nombre, categoria, precio, stock_ini, stock_min)
                )
            except ValueError as err:
                errores_catalogo.agregar(num_linea, "dato inválido", str(err))

    return inventario, errores_catalogo


def procesar_movimientos(
    ruta_mov: Path,
    inventario: ListaInventario,
) -> tuple[Historial, ListaRechazos]:
    """Procesa movimientos.csv en orden registrando aplicados y rechazos con su motivo."""
    historial = Historial()
    rechazos = ListaRechazos()

    with ruta_mov.open("r", encoding="utf-8", newline="") as f_mov:
        lector = csv.reader(f_mov)
        for num_linea, fila in enumerate(lector, start=1):
            if num_linea == 1:
                continue  # Cabecera
            if len(fila) != 4:
                rechazos.agregar(num_linea, "dato inválido", ",".join(fila))
                continue

            dia = fila[0].strip()
            tipo = fila[1].strip().upper()
            codigo = fila[2].strip()
            cant_txt = fila[3].strip()

            try:
                cantidad = int(cant_txt)
            except ValueError:
                rechazos.agregar(num_linea, "dato inválido", f"cantidad no entera '{cant_txt}'")
                continue

            if tipo not in ("ENTRADA", "SALIDA") or cantidad <= 0 or not dia:
                rechazos.agregar(num_linea, "dato inválido", f"{dia},{tipo},{codigo},{cantidad}")
                continue

            producto = inventario.buscar(codigo)
            if producto is None:
                rechazos.agregar(num_linea, "dato inválido", f"código inexistente '{codigo}'")
                continue

            if tipo == "ENTRADA":
                producto.stock += cantidad
                historial.agregar((num_linea, dia, tipo, codigo, cantidad, producto.stock))
            else:
                if cantidad > producto.stock:
                    rechazos.agregar(
                        num_linea,
                        "stock insuficiente",
                        f"solicitado {cantidad}, disponible {producto.stock} ({codigo})",
                    )
                else:
                    producto.stock -= cantidad
                    historial.agregar((num_linea, dia, tipo, codigo, cantidad, producto.stock))

    return historial, rechazos


def calcular_valor_total(inventario: ListaInventario) -> float:
    """Calcula el valor total del inventario redondeado a 2 decimales sin usar sum()."""
    total = 0.0
    for prod in inventario:
        total += prod.valor()
    return round(total, 2)


def obtener_top_3_por_valor(inventario: ListaInventario) -> tuple[Producto | None, Producto | None, Producto | None]:
    """Obtiene el Top 3 por valor (stock * precio) descendente y código ascendente sin sort()."""
    top1: Producto | None = None
    top2: Producto | None = None
    top3: Producto | None = None

    def _va_antes(a: Producto, b: Producto) -> bool:
        va = round(a.valor(), 6)
        vb = round(b.valor(), 6)
        if va != vb:
            return va > vb
        return a.codigo < b.codigo

    for prod in inventario:
        if top1 is None or _va_antes(prod, top1):
            top3 = top2
            top2 = top1
            top1 = prod
        elif top2 is None or _va_antes(prod, top2):
            top3 = top2
            top2 = prod
        elif top3 is None or _va_antes(prod, top3):
            top3 = prod

    return top1, top2, top3


def emitir_reporte_y_actualizado(
    inventario: ListaInventario,
    historial: Historial,
    rechazos: ListaRechazos,
    ruta_rep: Path = RUTA_REPORTE,
    ruta_act: Path = RUTA_ACTUALIZADO,
) -> str:
    """Escribe kardex_reporte.txt alineado y catalogo_actualizado.csv en UTF-8."""
    with ruta_act.open("w", encoding="utf-8", newline="") as f_act:
        escritor = csv.writer(f_act)
        escritor.writerow(
            ["codigo", "nombre", "categoria", "precio", "stock_final", "stock_minimo"]
        )
        for prod in inventario:
            escritor.writerow(
                [
                    prod.codigo,
                    prod.nombre,
                    prod.categoria,
                    f"{prod.precio:.2f}",
                    prod.stock,
                    prod.stock_minimo,
                ]
            )

    valor_total = calcular_valor_total(inventario)
    t1, t2, t3 = obtener_top_3_por_valor(inventario)

    bajos_txt = ""
    for prod in inventario:
        if prod.stock < prod.stock_minimo:
            bajos_txt = f"{bajos_txt}, {prod.codigo}" if bajos_txt else prod.codigo
    if not bajos_txt:
        bajos_txt = "Ninguno"

    with ruta_rep.open("w", encoding="utf-8") as f_rep:
        f_rep.write("=" * 72 + "\n")
        f_rep.write(f"{'REPORTE DE KARDEX MENSUAL - BODEGA IQUITOS':^72}\n")
        f_rep.write("=" * 72 + "\n")
        f_rep.write(f"Movimientos aplicados : {len(historial)}\n")
        f_rep.write(f"Movimientos rechazados: {len(rechazos)}\n")
        f_rep.write("-" * 72 + "\n")
        f_rep.write(
            f"{'CÓDIGO':<8}{'PRODUCTO':<26}{'CATEGORÍA':<14}{'STOCK':>8}{'VALOR (S/)':>16}\n"
        )
        f_rep.write("-" * 72 + "\n")
        for prod in inventario:
            f_rep.write(
                f"{prod.codigo:<8}{prod.nombre:<26}{prod.categoria:<14}"
                f"{prod.stock:>8}{prod.valor():>16,.2f}\n"
            )
        f_rep.write("-" * 72 + "\n")
        f_rep.write(f"{'VALOR TOTAL DEL INVENTARIO:':<56}{valor_total:>16,.2f}\n")
        f_rep.write(f"Productos bajo stock mínimo: {bajos_txt}\n")
        f_rep.write("-" * 72 + "\n")
        f_rep.write("TOP 3 PRODUCTOS POR VALOR EN INVENTARIO:\n")
        puesto = 1
        for candidato in (t1, t2, t3):
            if candidato is not None:
                f_rep.write(
                    f"  {puesto}. {candidato.codigo} - {candidato.nombre:<24} "
                    f"S/ {candidato.valor():>10,.2f}\n"
                )
                puesto += 1
        f_rep.write("-" * 72 + "\n")
        f_rep.write("LÍNEAS RECHAZADAS DE movimientos.csv:\n")
        if len(rechazos) == 0:
            f_rep.write("  Ninguna línea rechazada.\n")
        else:
            for num_linea, motivo, detalle in rechazos:
                f_rep.write(f"  Línea {num_linea:>2}: {motivo:<20} | {detalle}\n")
        f_rep.write("=" * 72 + "\n")

    with ruta_rep.open("r", encoding="utf-8") as f_lectura:
        return f_lectura.read()


def ejecutar_ciclo_kardex() -> tuple[ListaInventario, Historial, ListaRechazos, str]:
    """Ejecuta una corrida completa del sistema Kardex."""
    generar_archivos_entrada()
    inventario, errores_cat = cargar_inventario(RUTA_CATALOGO)
    assert len(errores_cat) == 0, "El catálogo generado no debe tener filas inválidas."
    historial, rechazos = procesar_movimientos(RUTA_MOVIMIENTOS, inventario)
    texto_reporte = emitir_reporte_y_actualizado(inventario, historial, rechazos)
    return inventario, historial, rechazos, texto_reporte


def verificar_sin_fugas_50_iteraciones() -> tuple[int, int]:
    """Ejecuta 50 ciclos completos y mide memoria neta entre iteración 1 y 50."""
    gc.collect()
    tracemalloc.start()

    mem_iter_1 = 0
    mem_iter_50 = 0
    for i in range(1, 51):
        inv, hist, rech, rep = ejecutar_ciclo_kardex()
        del inv, hist, rech, rep
        gc.collect()
        actual, _ = tracemalloc.get_traced_memory()
        if i == 1:
            mem_iter_1 = actual
        elif i == 50:
            mem_iter_50 = actual

    tracemalloc.stop()
    return mem_iter_1, mem_iter_50


def main() -> None:
    """Punto de entrada: ejecuta el Kardex y verifica estabilidad de memoria."""
    _, _, _, reporte = ejecutar_ciclo_kardex()
    print(reporte)

    mem_ini, mem_fin = verificar_sin_fugas_50_iteraciones()
    variacion = mem_fin - mem_ini
    print(
        f"Verificación tracemalloc (50 ciclos): inicio={mem_ini} B, "
        f"fin={mem_fin} B, diferencia={variacion:+d} B"
    )


if __name__ == "__main__":
    main()