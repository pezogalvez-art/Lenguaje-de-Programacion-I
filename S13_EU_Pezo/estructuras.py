"""Estructuras de datos propias para el sistema Kardex (EU3).

Prohibido usar list o dict como contenedor principal, así como sort, sorted,
min, max, sum o pandas.
"""

import ctypes
from dataclasses import dataclass
from typing import Final, Iterator

_VACIO: Final[object] = object()


@dataclass(slots=True, weakref_slot=True)
class Producto:
    """Representa un producto del catálogo de la bodega con huella mínima (__slots__)."""

    codigo: str
    nombre: str
    categoria: str
    precio: float
    stock: int
    stock_minimo: int

    def valor(self) -> float:
        """Calcula el valor monetario actual del stock de este producto."""
        return self.stock * self.precio


class NodoInventario:
    """Nodo enlazado simple para almacenar un Producto ordenado por código."""

    __slots__ = ("producto", "siguiente")

    def __init__(self, producto: Producto, siguiente: "NodoInventario | None" = None) -> None:
        self.producto = producto
        self.siguiente = siguiente


class ListaInventario:
    """Lista enlazada simple ordenada ascendentemente por producto.codigo."""

    __slots__ = ("cabeza", "_tamano")

    def __init__(self) -> None:
        self.cabeza: NodoInventario | None = None
        self._tamano: int = 0

    def __len__(self) -> int:
        return self._tamano

    def __iter__(self) -> Iterator[Producto]:
        actual = self.cabeza
        while actual is not None:
            yield actual.producto
            actual = actual.siguiente

    def insertar_ordenado(self, producto: Producto) -> None:
        """Inserta un Producto manteniendo el orden ascendente por código."""
        if self.buscar(producto.codigo) is not None:
            raise ValueError(f"Código duplicado en catálogo: '{producto.codigo}'.")

        nuevo = NodoInventario(producto)
        if self.cabeza is None or producto.codigo < self.cabeza.producto.codigo:
            nuevo.siguiente = self.cabeza
            self.cabeza = nuevo
            self._tamano += 1
            return

        actual = self.cabeza
        while actual.siguiente is not None and actual.siguiente.producto.codigo < producto.codigo:
            actual = actual.siguiente

        nuevo.siguiente = actual.siguiente
        actual.siguiente = nuevo
        self._tamano += 1

    def buscar(self, codigo: str) -> Producto | None:
        """Busca un Producto por código; devuelve None si no existe."""
        actual = self.cabeza
        while actual is not None:
            if actual.producto.codigo == codigo:
                return actual.producto
            if actual.producto.codigo > codigo:
                return None
            actual = actual.siguiente
        return None

    def eliminar(self, codigo: str) -> bool:
        """Elimina el nodo con el código dado y devuelve True si existía."""
        anterior: NodoInventario | None = None
        actual = self.cabeza
        while actual is not None:
            if actual.producto.codigo == codigo:
                if anterior is None:
                    self.cabeza = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente
                actual.siguiente = None
                self._tamano -= 1
                return True
            if actual.producto.codigo > codigo:
                return False
            anterior = actual
            actual = actual.siguiente
        return False


class Historial:
    """Arreglo dinámico sobre ctypes.py_object (crecimiento x2 y centinela _VACIO)."""

    __slots__ = ("_tamano", "_capacidad", "_datos")

    def __init__(self, capacidad_inicial: int = 2) -> None:
        if capacidad_inicial < 1:
            raise ValueError("La capacidad inicial debe ser >= 1.")
        self._tamano: int = 0
        self._capacidad: int = capacidad_inicial
        self._datos = (ctypes.py_object * self._capacidad)()

    @property
    def capacidad(self) -> int:
        return self._capacidad

    def _redimensionar(self, nueva_capacidad: int) -> None:
        nuevo_bloque = (ctypes.py_object * nueva_capacidad)()
        for i in range(self._tamano):
            nuevo_bloque[i] = self._datos[i]
            self._datos[i] = _VACIO
        self._datos = nuevo_bloque
        self._capacidad = nueva_capacidad

    def agregar(self, registro: tuple[int, str, str, str, int, int]) -> None:
        """Agrega una tupla (linea, dia, tipo, codigo, cantidad, stock_resultante)."""
        if self._tamano == self._capacidad:
            self._redimensionar(self._capacidad * 2)
        self._datos[self._tamano] = registro
        self._tamano += 1

    def __getitem__(self, indice: int) -> tuple[int, str, str, str, int, int]:
        if indice < 0:
            indice += self._tamano
        if not 0 <= indice < self._tamano:
            raise IndexError("Índice fuera de rango en Historial.")
        return self._datos[indice]

    def __len__(self) -> int:
        return self._tamano

    def __iter__(self) -> Iterator[tuple[int, str, str, str, int, int]]:
        for i in range(self._tamano):
            yield self._datos[i]


class ListaRechazos:
    """Lista enlazada simple para registrar rechazos sin usar list ni dict."""

    __slots__ = ("cabeza", "cola", "_tamano")

    class _NodoRechazo:
        __slots__ = ("linea", "motivo", "detalle", "siguiente")

        def __init__(
            self,
            linea: int,
            motivo: str,
            detalle: str,
            siguiente: "ListaRechazos._NodoRechazo | None" = None,
        ) -> None:
            self.linea = linea
            self.motivo = motivo
            self.detalle = detalle
            self.siguiente = siguiente

    def __init__(self) -> None:
        self.cabeza: ListaRechazos._NodoRechazo | None = None
        self.cola: ListaRechazos._NodoRechazo | None = None
        self._tamano: int = 0

    def agregar(self, linea: int, motivo: str, detalle: str) -> None:
        nodo = ListaRechazos._NodoRechazo(linea, motivo, detalle)
        if self.cola is None:
            self.cabeza = nodo
            self.cola = nodo
        else:
            self.cola.siguiente = nodo
            self.cola = nodo
        self._tamano += 1

    def __len__(self) -> int:
        return self._tamano

    def __iter__(self) -> Iterator[tuple[int, str, str]]:
        actual = self.cabeza
        while actual is not None:
            yield (actual.linea, actual.motivo, actual.detalle)
            actual = actual.siguiente