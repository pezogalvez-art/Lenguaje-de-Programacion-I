"""Proyecto PC06 - B2: Nodo y ListaEnlazada con __slots__ y verificación contra list.

Código universitario: 2155263 | Estudiante: Pezo | Constantes: D = 3, P = 6, K = 2.
"""

from typing import Any, Final, Iterator
from generadores_u3 import operaciones_lista

CODIGO_UNIVERSITARIO: Final[int] = 2155263


class Nodo:
    """Nodo de lista enlazada simple con __slots__ para minimizar huella de memoria."""

    __slots__ = ("dato", "siguiente")

    def __init__(self, dato: Any, siguiente: "Nodo | None" = None) -> None:
        self.dato = dato
        self.siguiente = siguiente


class ListaEnlazada:
    """Lista enlazada simple con manipulación directa de referencias."""

    __slots__ = ("cabeza", "_tamano")

    def __init__(self) -> None:
        self.cabeza: Nodo | None = None
        self._tamano: int = 0

    def __len__(self) -> int:
        return self._tamano

    def __iter__(self) -> Iterator[Any]:
        actual = self.cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    def insertar_inicio(self, x: Any) -> None:
        self.cabeza = Nodo(x, self.cabeza)
        self._tamano += 1

    def insertar_final(self, x: Any) -> None:
        nuevo = Nodo(x)
        if self.cabeza is None:
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo
        self._tamano += 1

    def insertar_en(self, indice: int, x: Any) -> None:
        if not 0 <= indice <= self._tamano:
            raise IndexError("Índice fuera de rango en insertar_en.")
        if indice == 0:
            self.insertar_inicio(x)
            return
        actual = self.cabeza
        for _ in range(indice - 1):
            assert actual is not None
            actual = actual.siguiente
        assert actual is not None
        actual.siguiente = Nodo(x, actual.siguiente)
        self._tamano += 1

    def eliminar(self, x: Any) -> bool:
        """Elimina la primera aparición de x; devuelve True si lo eliminó."""
        anterior: Nodo | None = None
        actual = self.cabeza
        while actual is not None:
            if actual.dato == x:
                if anterior is None:
                    self.cabeza = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente
                self._tamano -= 1
                return True
            anterior = actual
            actual = actual.siguiente
        return False

    def invertir(self) -> None:
        """Invierte los enlaces de la lista en el sitio en O(n) tiempo y O(1) espacio."""
        anterior: Nodo | None = None
        actual = self.cabeza
        while actual is not None:
            siguiente_temp = actual.siguiente
            actual.siguiente = anterior
            anterior = actual
            actual = siguiente_temp
        self.cabeza = anterior

    def medio(self) -> Any:
        """Devuelve el dato del nodo central en una pasada (el segundo si hay par)."""
        if self.cabeza is None:
            raise ValueError("La lista está vacía; no existe nodo medio.")
        lento = self.cabeza
        rapido = self.cabeza
        while rapido is not None and rapido.siguiente is not None:
            assert lento.siguiente is not None
            lento = lento.siguiente
            rapido = rapido.siguiente.siguiente
        return lento.dato

    def k_desde_final(self, k: int) -> Any:
        """Devuelve el k-ésimo elemento desde el final en una sola pasada (k=1 es el último)."""
        if k < 1 or self.cabeza is None:
            raise ValueError("k debe ser >= 1 y la lista no debe estar vacía.")
        adelantado: Nodo | None = self.cabeza
        for _ in range(k):
            if adelantado is None:
                raise IndexError("k supera la longitud de la lista.")
            adelantado = adelantado.siguiente

        rezagado = self.cabeza
        while adelantado is not None:
            assert rezagado.siguiente is not None
            rezagado = rezagado.siguiente
            adelantado = adelantado.siguiente
        return rezagado.dato

    def formatear(self) -> str:
        """Devuelve la representación 'a -> b -> ... -> None'."""
        partes: list[str] = []
        actual = self.cabeza
        while actual is not None:
            partes.append(str(actual.dato))
            actual = actual.siguiente
        partes.append("None")
        return " -> ".join(partes)


def simular_con_list(ops: list[tuple]) -> list[Any]:
    """Simula las operaciones en una list estándar únicamente para verificar con assert."""
    ref: list[Any] = []
    for op in ops:
        nombre = op[0]
        if nombre == "insertar_inicio":
            ref.insert(0, op[1])
        elif nombre == "insertar_final":
            ref.append(op[1])
        elif nombre == "insertar_en":
            ref.insert(op[1], op[2])
        elif nombre == "eliminar":
            if op[1] in ref:
                ref.remove(op[1])
        elif nombre == "invertir":
            ref.reverse()
    return ref


def main() -> None:
    """Aplica las operaciones personales a ListaEnlazada y verifica resultados."""
    ops = operaciones_lista(CODIGO_UNIVERSITARIO)
    lista = ListaEnlazada()

    for op in ops:
        nombre = op[0]
        if nombre == "insertar_inicio":
            lista.insertar_inicio(op[1])
        elif nombre == "insertar_final":
            lista.insertar_final(op[1])
        elif nombre == "insertar_en":
            lista.insertar_en(op[1], op[2])
        elif nombre == "eliminar":
            lista.eliminar(op[1])
        elif nombre == "invertir":
            lista.invertir()

    referencia = simular_con_list(ops)
    assert list(lista) == referencia, f"Discrepancia: {list(lista)} != {referencia}"
    assert lista.medio() == referencia[len(referencia) // 2]
    assert lista.k_desde_final(3) == referencia[-3]

    print("Lista final :", lista.formatear())
    print("Longitud    :", len(lista))
    print("Nodo medio  :", lista.medio())
    print("k=3 final   :", lista.k_desde_final(3))
    print("Verificación assert contra list: OK")


if __name__ == "__main__":
    main()