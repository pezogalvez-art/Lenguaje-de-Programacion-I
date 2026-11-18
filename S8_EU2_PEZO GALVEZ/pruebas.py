"""Pruebas unitarias con assert para el módulo analizador.py (EU2).

Código universitario: 2155263 | Estudiante: Pezo | Constantes: D = 3, P = 6, K = 2.
"""

import statistics
import analizador


def test_promedio_dc() -> None:
    """Verifica el cálculo ponderado de unidad, manejo de NSP y validación de longitud."""
    # Caso normal: (14*0.04 + 15*0.04 + 16*0.04 + 12*0.19 + 14*0.19 + 15*0.25) / 0.75 = 13.99
    assert analizador.promedio_dc([14, 15, 16, 12, 14, 15]) == 13.99

    # Caso con un NSP (-1 cuenta como 0): 9.93 / 0.75 = 13.24
    assert analizador.promedio_dc([-1, 15, 16, 12, 14, 15]) == 13.24

    # Caso límite: todos NSP
    assert analizador.promedio_dc([-1, -1, -1, -1, -1, -1]) == 0.0

    # Caso de error: longitud distinta de 6
    try:
        analizador.promedio_dc([15, 16, 17])
        assert False, "Debió lanzar ValueError con menos de 6 notas"
    except ValueError:
        pass


def test_mergesort_y_ranking() -> None:
    """Verifica casos borde de mergesort, estabilidad y coincidencia con sorted()."""
    # Casos borde: vacía y un elemento
    assert analizador.mergesort([], lambda x: x) == []
    assert analizador.mergesort([42], lambda x: x) == [42]

    # Caso borde: empates (verifica estabilidad conservando identidad de objetos)
    p1 = {"id": 1, "nota": 15}
    p2 = {"id": 2, "nota": 15}
    p3 = {"id": 3, "nota": 18}
    p4 = {"id": 4, "nota": 15}
    ordenado_empates = analizador.mergesort([p1, p2, p3, p4], lambda d: d["nota"])
    assert ordenado_empates == [p1, p2, p4, p3]
    assert ordenado_empates[0] is p1
    assert ordenado_empates[1] is p2
    assert ordenado_empates[2] is p4

    # Verificación del ranking del aula contra sorted() con la misma clave
    aula = analizador.generar_aula(analizador.CODIGO_UNIVERSITARIO)
    copia_antes = [est.copy() for est in aula]
    ranking = analizador.obtener_ranking(aula)

    assert aula == copia_antes, "obtener_ranking no debe mutar la lista aula original"
    esperado = sorted(
        aula,
        key=lambda est: (
            -analizador.promedio_dc(est["notas"]),
            analizador.normalizar(est["nombre"]).lower(),
        ),
    )
    assert ranking == esperado, "El ranking de mergesort no coincide con sorted()"


def test_aprobados_y_nsp() -> None:
    """Verifica el conteo recursivo de aprobados por divide y vencerás y total de NSP."""
    # Umbral exacto 10.5
    lista_umbral = [10.49, 10.50, 20.0, 0.0, 10.5]
    assert analizador.contar_aprobados(lista_umbral, 0, len(lista_umbral) - 1) == 3

    # Casos borde de rango
    assert analizador.contar_aprobados([], 0, -1) == 0
    assert analizador.contar_aprobados([11.0], 0, 0) == 1
    assert analizador.contar_aprobados([10.4], 0, 0) == 0

    # Verificación sobre el aula real contra conteo de referencia
    aula = analizador.generar_aula(analizador.CODIGO_UNIVERSITARIO)
    proms = [analizador.promedio_dc(est["notas"]) for est in aula]
    aprobados_dc = analizador.contar_aprobados(proms, 0, len(proms) - 1)
    aprobados_ref = sum(1 for p in proms if p >= 10.5)
    assert aprobados_dc == aprobados_ref

    nsp_ref = sum(1 for est in aula for n in est["notas"] if n == -1)
    assert analizador.contar_nsp(aula) == nsp_ref


def test_busqueda_por_codigo() -> None:
    """Verifica que buscar_por_codigo encuentra a los 30 estudiantes y devuelve None si no existe."""
    aula = analizador.generar_aula(analizador.CODIGO_UNIVERSITARIO)
    aula_ordenada = analizador.ordenar_por_codigo(aula)

    # Debe encontrar a cada uno de los 30 estudiantes
    for est in aula:
        encontrado = analizador.buscar_por_codigo(aula_ordenada, est["codigo"])
        assert encontrado is not None
        assert encontrado == est

    # Códigos inexistentes (menor que el primero, intermedio y mayor que el último)
    assert analizador.buscar_por_codigo(aula_ordenada, 100000) is None
    assert analizador.buscar_por_codigo(aula_ordenada, 555555) is None
    assert analizador.buscar_por_codigo(aula_ordenada, 999999) is None
    assert analizador.buscar_por_codigo([], 515654) is None


def test_estadisticas_evaluaciones() -> None:
    """Verifica los estadísticos por columna excluyendo NSP (-1)."""
    aula = analizador.generar_aula(analizador.CODIGO_UNIVERSITARIO)
    stats = analizador.estadisticas_evaluaciones(aula)
    assert len(stats) == 6

    for col_idx, st in enumerate(stats):
        validas = [
            float(est["notas"][col_idx])
            for est in aula
            if est["notas"][col_idx] != -1
        ]
        assert st["rindieron"] == len(validas)
        assert st["media"] == round(sum(validas) / len(validas), 2)
        assert st["minimo"] == round(min(validas), 2)
        assert st["maximo"] == round(max(validas), 2)
        assert st["desviacion"] == round(statistics.pstdev(validas), 2)


def test_generar_usuarios() -> None:
    """Verifica formato de usuarios, tildes/Ñ y sufijos numéricos ante colisiones."""
    # Ejemplo exacto del enunciado + colisiones forzadas
    aula_demo = [
        {"codigo": 598257, "nombre": "Milagros Chávez Ñahui", "notas": [15] * 6},
        {"codigo": 112257, "nombre": "Mateo Chávez Quispe", "notas": [15] * 6},
        {"codigo": 998857, "nombre": "Mónica Chávez Pérez", "notas": [15] * 6},
        {"codigo": 445509, "nombre": "Óscar Ñahui López", "notas": [15] * 6},
    ]
    usuarios_demo = analizador.generar_usuarios(aula_demo)
    assert usuarios_demo == ["mchavez57", "mchavez572", "mchavez573", "onahui09"]

    # Verificación sobre los 30 estudiantes del aula: misma longitud y sin repetidos
    aula = analizador.generar_aula(analizador.CODIGO_UNIVERSITARIO)
    usuarios_aula = analizador.generar_usuarios(aula)
    assert len(usuarios_aula) == len(aula)
    assert len(set(usuarios_aula)) == len(usuarios_aula), "Existen usuarios duplicados"


def main() -> None:
    """Ejecuta todas las baterías de pruebas unitarias."""
    test_promedio_dc()
    test_mergesort_y_ranking()
    test_aprobados_y_nsp()
    test_busqueda_por_codigo()
    test_estadisticas_evaluaciones()
    test_generar_usuarios()
    print("Todas las pruebas de pruebas.py pasaron exitosamente (6/6 bloques OK).")


if __name__ == "__main__":
    main()