"""Pruebas unitarias e integrales para el Examen Domiciliario EU3 (Kardex).

Aquí sí se permiten list, sorted, sum y weakref para verificar nuestros resultados.
"""

from pathlib import Path
import tempfile
import weakref

from estructuras import Historial, ListaInventario, Producto
from kardex import (
    calcular_valor_total,
    cargar_inventario,
    ejecutar_ciclo_kardex,
    obtener_top_3_por_valor,
    procesar_movimientos,
    verificar_sin_fugas_50_iteraciones,
)


def probar_producto_y_slots() -> None:
    p = Producto("P001", "Prueba", "General", 12.5, 4, 2)
    assert p.valor() == 50.0
    assert not hasattr(p, "__dict__"), "Producto debe usar __slots__ sin __dict__"
    try:
        p.atributo_inexistente = 123  # type: ignore[attr-defined]
        assert False, "Debió lanzar AttributeError al asignar un atributo inexistente"
    except AttributeError:
        pass


def probar_lista_inventario_y_weakref() -> None:
    inv = ListaInventario()
    p3 = Producto("P003", "C", "Cat", 10.0, 5, 2)
    p1 = Producto("P001", "A", "Cat", 20.0, 3, 2)
    p2 = Producto("P002", "B", "Cat", 15.0, 4, 2)

    ref_p2 = weakref.ref(p2)
    inv.insertar_ordenado(p3)
    inv.insertar_ordenado(p1)
    inv.insertar_ordenado(p2)
    del p2

    assert [p.codigo for p in inv] == ["P001", "P002", "P003"]
    assert inv.buscar("P002") is not None
    assert inv.buscar("P999") is None
    assert ref_p2() is not None, "El nodo en ListaInventario mantiene vivo a P002"

    assert inv.eliminar("P002") is True
    assert inv.eliminar("P002") is False
    assert ref_p2() is None, "Al eliminar el nodo sin otras referencias, el Producto debe morir"


def probar_historial_dinamico() -> None:
    hist = Historial(capacidad_inicial=2)
    for i in range(1, 6):
        hist.agregar((i + 1, "01", "ENTRADA", "P101", i, 10 + i))
    assert len(hist) == 5
    assert hist.capacidad == 8
    assert hist[0] == (2, "01", "ENTRADA", "P101", 1, 11)
    assert hist[-1] == (6, "01", "ENTRADA", "P101", 5, 15)


def probar_validacion_y_top3() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        carpeta = Path(tmp)
        f_cat = carpeta / "cat.csv"
        f_mov = carpeta / "mov.csv"

        f_cat.write_text(
            "codigo,nombre,categoria,precio,stock_inicial,stock_minimo\n"
            "P02,Prod B,Cat,10.0,10,5\n"
            "P01,Prod A,Cat,10.0,10,5\n"
            "P03,Prod C,Cat,50.0,3,5\n"
            "P04,Prod D,Cat,5.0,2,5\n",
            encoding="utf-8",
        )
        f_mov.write_text(
            "dia,tipo,codigo,cantidad\n"
            "01,ENTRADA,P03,1\n"      # P03 pasa a stock 4 -> valor 200.0
            "02,SALIDA,P03,10\n"      # Rechazo: stock insuficiente
            "03,OTRO,P01,2\n"         # Rechazo: dato inválido
            "04,SALIDA,P99,1\n",      # Rechazo: dato inválido
            encoding="utf-8",
        )

        inv, err_cat = cargar_inventario(f_cat)
        assert len(err_cat) == 0
        hist, rechazos = procesar_movimientos(f_mov, inv)
        assert len(hist) == 1
        assert list(rechazos) == [
            (3, "stock insuficiente", "solicitado 10, disponible 4 (P03)"),
            (4, "dato inválido", "03,OTRO,P01,2"),
            (5, "dato inválido", "código inexistente 'P99'"),
        ]

        # Empate entre P01 (100.0) y P02 (100.0): debe ir primero P01 por código ascendente
        t1, t2, t3 = obtener_top_3_por_valor(inv)
        assert [t1.codigo, t2.codigo, t3.codigo] == ["P03", "P01", "P02"]


def probar_integracion_y_memoria() -> None:
    inv, hist, rechazos, _ = ejecutar_ciclo_kardex()
    esperado_total = round(sum(p.stock * p.precio for p in inv), 2)
    assert calcular_valor_total(inv) == esperado_total

    orden_esperado = sorted(
        list(inv), key=lambda p: (-round(p.stock * p.precio, 6), p.codigo)
    )[:3]
    t1, t2, t3 = obtener_top_3_por_valor(inv)
    assert [t1.codigo, t2.codigo, t3.codigo] == [p.codigo for p in orden_esperado]
    assert len(hist) > 0 and len(rechazos) == 5

    mem_ini, mem_fin = verificar_sin_fugas_50_iteraciones()
    assert abs(mem_fin - mem_ini) < 8192, f"Posible fuga detectada: {mem_ini} -> {mem_fin}"


def main() -> None:
    probar_producto_y_slots()
    probar_lista_inventario_y_weakref()
    probar_historial_dinamico()
    probar_validacion_y_top3()
    probar_integracion_y_memoria()
    print("Todas las pruebas unitarias e integrales de EU3 pasaron correctamente (OK).")


if __name__ == "__main__":
    main()

