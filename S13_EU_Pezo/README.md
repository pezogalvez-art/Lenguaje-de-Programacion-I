# Examen Domiciliario EU3 — Sistema Kardex de Bodega (LP1 · UNAP)

* **Estudiante:** Pezo Galvez
* **Código universitario:** `2155263`
* **Constantes personales:** `D = 3`, `P = 6`, `K = 2`

## 1. Descripción del proyecto
Sistema de control de inventario mensual (*Kardex*) para una bodega en Iquitos desarrollado en Python 3.14 sin usar `list` ni `dict` como contenedores principales, ni las funciones prohibidas (`sort`, `sorted`, `min`, `max`, `sum`, `pandas`).

## 2. Estructura de archivos
* `generadores_u3.py`: generadores deterministas `catalogo_bodega(2155263)` y `movimientos_bodega(2155263)`.
* `estructuras.py`:
  * `Producto`: `@dataclass(slots=True, weakref_slot=True)` con método `valor()`.
  * `NodoInventario` y `ListaInventario`: lista enlazada simple ordenada ascendentemente por `codigo` (`insertar_ordenado`, `buscar`, `eliminar`, `__iter__`, `__len__`).
  * `Historial`: arreglo dinámico respaldado por `ctypes.py_object` con crecimiento $\times 2$ y limpieza de referencias mediante el centinela `_VACIO`.
  * `ListaRechazos`: lista enlazada con punteros `cabeza` y `cola` para registrar movimientos rechazados en $O(1)$.
* `kardex.py`: generación de `catalogo.csv` y `movimientos.csv` (UTF-8), validación de reglas de negocio, obtención del Top 3 por valor sin `sort`, emisión de `kardex_reporte.txt` y `catalogo_actualizado.csv`, y prueba de estabilidad de memoria con `tracemalloc` en 50 ciclos.
* `pruebas.py`: batería de pruebas unitarias e integrales con `assert` y `weakref`.

## 3. Ejecución
```bash
python kardex.py
python pruebas.py