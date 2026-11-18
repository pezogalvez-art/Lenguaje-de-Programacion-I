"""Proyecto PC06 - B1: ArregloDinamico sobre ctypes.py_object con centinela y weakref.

Código universitario: 2155263 | Estudiante: Pezo | Constantes: D = 3 (impar -> F = 2).
"""

import ctypes
import weakref
from typing import Any, Final, Iterator

D: Final[int] = 3
FACTOR_CRECIMIENTO: Final[float] = 1.5 if D % 2 == 0 else 2.0
_VACIO: Final[object] = object()


class _ObjetoRastreable:
    """Clase auxiliar para comprobar liberación de memoria con weakref."""

    def __init__(self, etiqueta: str) -> None:
        self.etiqueta = etiqueta


class ArregloDinamico:
    """Arreglo dinámico respaldado por un bloque crudo ctypes.py_object."""

    def __init__(self, capacidad_inicial: int = 1) -> None:
        if capacidad_inicial < 1:
            raise ValueError("La capacidad inicial debe ser al menos 1.")
        self._tamano: int = 0
        self._capacidad: int = capacidad_inicial
        self._datos = self._crear_bloque(self._capacidad)
        self.copias_totales: int = 0

    @staticmethod
    def _crear_bloque(capacidad: int) -> ctypes.Array:
        # El bloque nace con celdas NULL; el acceso siempre se valida contra self._tamano
        return (ctypes.py_object * capacidad)()

    def _redimensionar(self, nueva_capacidad: int) -> None:
        nuevo_bloque = self._crear_bloque(nueva_capacidad)
        for i in range(self._tamano):
            nuevo_bloque[i] = self._datos[i]
            self.copias_totales += 1
        self._datos = nuevo_bloque
        self._capacidad = nueva_capacidad

    def agregar(self, x: Any) -> None:
        """Inserta x al final, multiplicando capacidad por F al llenarse."""
        if self._tamano == self._capacidad:
            nueva_cap = max(self._capacidad + 1, int(self._capacidad * FACTOR_CRECIMIENTO))
            self._redimensionar(nueva_cap)
        self._datos[self._tamano] = x
        self._tamano += 1

    def insertar(self, i: int, x: Any) -> None:
        """Inserta x en la posición i (acepta índices negativos)."""
        if i < 0:
            i += self._tamano
        if not 0 <= i <= self._tamano:
            raise IndexError("Índice fuera de rango en insertar.")
        if self._tamano == self._capacidad:
            nueva_cap = max(self._capacidad + 1, int(self._capacidad * FACTOR_CRECIMIENTO))
            self._redimensionar(nueva_cap)
        for j in range(self._tamano, i, -1):
            self._datos[j] = self._datos[j - 1]
            self.copias_totales += 1
        self._datos[i] = x
        self._tamano += 1

    def quitar(self) -> Any:
        """Elimina y devuelve el último elemento, limpiando la celda con _VACIO."""
        if self._tamano == 0:
            raise IndexError("No se puede quitar de un arreglo dinámico vacío.")
        self._tamano -= 1
        valor = self._datos[self._tamano]
        self._datos[self._tamano] = _VACIO

        if 0 < self._tamano <= self._capacidad // 4 and self._capacidad > 1:
            nueva_cap = max(1, self._capacidad // 2)
            self._redimensionar(nueva_cap)
        return valor

    def __getitem__(self, i: int) -> Any:
        if i < 0:
            i += self._tamano
        if not 0 <= i < self._tamano:
            raise IndexError("Índice fuera de rango.")
        return self._datos[i]

    def __len__(self) -> int:
        return self._tamano

    def __iter__(self) -> Iterator[Any]:
        for i in range(self._tamano):
            yield self._datos[i]


def demostrar_liberacion_centinela_vs_none() -> None:
    """Demuestra con weakref que _VACIO libera el objeto quitado y None no."""
    # 1. Con _VACIO en ArregloDinamico: al quitarlo, _objects reemplaza la referencia y muere
    arr = ArregloDinamico(capacidad_inicial=2)
    obj1 = _ObjetoRastreable("con_centinela")
    ref1 = weakref.ref(obj1)
    arr.agregar(obj1)
    del obj1
    assert ref1() is not None, "El objeto debe seguir vivo dentro del arreglo"
    arr.quitar()
    assert ref1() is None, "Con _VACIO, el objeto quitado debe morir inmediatamente"

    # 2. Con None directo en ctypes.py_object: _objects retiene el objeto previo
    bloque_crudo = (ctypes.py_object * 2)()
    obj2 = _ObjetoRastreable("con_none")
    ref2 = weakref.ref(obj2)
    bloque_crudo[0] = obj2
    del obj2
    bloque_crudo[0] = None
    assert ref2() is not None, "Con None, ctypes.py_object._objects no suelta el objeto"
    del bloque_crudo
    assert ref2() is None


def main() -> None:
    """Ejecuta pruebas, demostración weakref y simulación de 1 000 inserciones."""
    demostrar_liberacion_centinela_vs_none()

    # Prueba funcional de métodos requeridos
    prueba = ArregloDinamico()
    for val in [10, 20, 30]:
        prueba.agregar(val)
    prueba.insertar(1, 15)
    assert list(prueba) == [10, 15, 20, 30]
    assert prueba[-1] == 30 and prueba[-4] == 10
    assert len(prueba) == 4
    assert prueba.quitar() == 30

    # Experimento de 1 000 inserciones desde capacidad 1
    sim = ArregloDinamico(capacidad_inicial=1)
    for k in range(1000):
        sim.agregar(k)

    print(f"Factor de crecimiento (D={D} impar): F = {FACTOR_CRECIMIENTO}")
    print("Demostración weakref (_VACIO libera / None retiene): OK")
    print(f"Tras 1 000 inserciones -> Tamaño: {len(sim)}, Capacidad final: {sim._capacidad}")
    print(f"Copias totales realizadas durante el crecimiento: {sim.copias_totales}")


if __name__ == "__main__":
    main()