"""Examen domiciliario EU2 - Analizador del registro de notas.

Código universitario: 2155263 | Estudiante: Pezo | Constantes: D = 3, P = 6, K = 2.
"""

import math
import random
import unicodedata
from typing import Any, Callable, Final

CODIGO_UNIVERSITARIO: Final[int] = 2155263
PESOS_SILABO: Final[tuple[float, ...]] = (0.04, 0.04, 0.04, 0.19, 0.19, 0.25)
PESO_TOTAL_UNIDAD: Final[float] = 0.75
NOTA_APROBATORIA: Final[float] = 10.5
NOMBRES_EVALUACIONES: Final[tuple[str, ...]] = ("ME1", "ME2", "ME3", "PC1", "PC2", "EU")

Estudiante = dict[str, Any]
EstadisticaColumna = dict[str, float | int]


def normalizar(texto: str) -> str:
    """Elimina tildes y diacríticos manteniendo caracteres base (Ñ -> N)."""
    descompuesto = unicodedata.normalize("NFD", texto)
    return "".join(
        ch for ch in descompuesto if unicodedata.category(ch) != "Mn"
    )


def generar_aula(tu_codigo: int) -> list[Estudiante]:
    """Genera un aula determinista de 30 estudiantes a partir del código universitario."""
    rng = random.Random(tu_codigo)
    nombres = (
        "Milagros", "Carlos", "Lucía", "José", "María",
        "Diego", "Sofía", "Andrés", "Valeria", "Sebastián",
        "Camila", "Mateo", "Fernanda", "Gabriel", "Daniela",
        "Alejandro", "Paula", "Javier", "Natalia", "Rodrigo",
        "Renata", "Álvaro", "Ximena", "Óscar", "Andrea",
        "Héctor", "Claudia", "Fabián", "Mónica", "Raúl",
    )
    apellidos = (
        "Chávez", "Ñahui", "Pezo", "Arévalo", "Quispe",
        "Gutiérrez", "Fernández", "Pérez", "López", "Sánchez",
        "Ramírez", "Vásquez", "Torres", "Díaz", "Méndez",
        "Cárdenas", "Ríos", "Huamán", "Flores", "Castillo",
        "Salazar", "Rojas", "Navarro", "Paredes", "Delgado",
        "Ortega", "Jiménez", "Núñez", "Silva", "Mendoza",
    )

    codigos_usados: set[int] = set()
    aula: list[Estudiante] = []

    for i in range(30):
        codigo = rng.randint(100000, 999999)
        while codigo in codigos_usados:
            codigo = rng.randint(100000, 999999)
        codigos_usados.add(codigo)

        nom = nombres[i % len(nombres)]
        ap1 = apellidos[(i * 3 + rng.randint(0, 4)) % len(apellidos)]
        ap2 = apellidos[(i * 7 + rng.randint(1, 5)) % len(apellidos)]
        nombre_completo = f"{nom} {ap1} {ap2}"

        notas: list[float] = []
        for _ in range(6):
            if rng.random() < 0.08:  # ~8% de inasistencias (NSP = -1)
                notas.append(-1.0)
            else:
                notas.append(rng.randint(12, 40) / 2.0)

        aula.append({
            "codigo": codigo,
            "nombre": nombre_completo,
            "notas": notas,
        })

    return aula


def promedio_dc(notas: list[float]) -> float:
    """Calcula el promedio ponderado de unidad (NSP = -1 cuenta como 0).

    Args:
        notas: Lista de 6 calificaciones en orden ME1, ME2, ME3, PC1, PC2, EU.

    Returns:
        Promedio ponderado dividido entre 0.75 y redondeado a 2 decimales.

    Raises:
        ValueError: Si la lista no tiene exactamente 6 notas.
    """
    if len(notas) != len(PESOS_SILABO):
        raise ValueError("Se requieren exactamente 6 notas por estudiante")

    acumulado = 0.0
    for i in range(len(notas)):
        valor = 0.0 if notas[i] == -1 else float(notas[i])
        acumulado += valor * PESOS_SILABO[i]

    return round(acumulado / PESO_TOTAL_UNIDAD, 2)


def _merge(
    izq: list[Any],
    der: list[Any],
    clave: Callable[[Any], Any],
) -> list[Any]:
    """Mezcla dos listas ordenadas manteniendo estabilidad (<= favorece izquierda)."""
    resultado: list[Any] = []
    i = 0
    j = 0
    len_izq = len(izq)
    len_der = len(der)

    while i < len_izq and j < len_der:
        if clave(izq[i]) <= clave(der[j]):
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1

    while i < len_izq:
        resultado.append(izq[i])
        i += 1

    while j < len_der:
        resultado.append(der[j])
        j += 1

    return resultado


def mergesort(datos: list[Any], clave: Callable[[Any], Any]) -> list[Any]:
    """Ordena una lista de forma recursiva y estable según la función clave.

    Args:
        datos: Lista de elementos a ordenar (no se modifica).
        clave: Función que extrae la clave comparable de cada elemento.

    Returns:
        Nueva lista ordenada ascendentemente por clave.
    """
    n = len(datos)
    if n <= 1:
        return datos[:]

    mitad = n // 2
    izquierda = mergesort(datos[:mitad], clave)
    derecha = mergesort(datos[mitad:], clave)
    return _merge(izquierda, derecha, clave)


def obtener_ranking(aula: list[Estudiante]) -> list[Estudiante]:
    """Devuelve una copia del aula ordenada por promedio descendente y nombre ascendente."""
    return mergesort(
        aula,
        lambda est: (-promedio_dc(est["notas"]), normalizar(est["nombre"]).lower()),
    )


def ordenar_por_codigo(aula: list[Estudiante]) -> list[Estudiante]:
    """Devuelve una copia del aula ordenada ascendentemente por código."""
    return mergesort(aula, lambda est: est["codigo"])


def contar_aprobados(promedios: list[float], lo: int, hi: int) -> int:
    """Cuenta recursivamente por divide y vencerás cuántos promedios son >= 10.5.

    Args:
        promedios: Lista de promedios finales.
        lo: Índice inicial inclusivo del subrango.
        hi: Índice final inclusivo del subrango.

    Returns:
        Cantidad de promedios aprobatorios en el rango [lo, hi].
    """
    if lo > hi:
        return 0
    if lo == hi:
        return 1 if promedios[lo] >= NOTA_APROBATORIA else 0

    mitad = (lo + hi) // 2
    return contar_aprobados(promedios, lo, mitad) + contar_aprobados(
        promedios, mitad + 1, hi
    )


def contar_nsp(aula: list[Estudiante]) -> int:
    """Cuenta el total de evaluaciones con NSP (-1) en todo el aula."""
    total_nsp = 0
    for est in aula:
        for nota in est["notas"]:
            if nota == -1:
                total_nsp += 1
    return total_nsp


def buscar_por_codigo(
    aula_ordenada: list[Estudiante], codigo: int
) -> Estudiante | None:
    """Busca un estudiante por código mediante búsqueda binaria iterativa.

    Args:
        aula_ordenada: Lista de estudiantes ordenada ascendentemente por código.
        codigo: Código entero de 6 dígitos a localizar.

    Returns:
        El diccionario del estudiante si existe, o None si no se encuentra.
    """
    lo = 0
    hi = len(aula_ordenada) - 1

    while lo <= hi:
        m = (lo + hi) // 2
        cod_actual = aula_ordenada[m]["codigo"]
        if cod_actual == codigo:
            return aula_ordenada[m]
        if cod_actual < codigo:
            lo = m + 1
        else:
            hi = m - 1

    return None


def construir_matriz_notas(aula: list[Estudiante]) -> list[list[float]]:
    """Construye la matriz de notas (n x 6) sin compartir referencias entre filas."""
    return [est["notas"][:] for est in aula]


def estadisticas_evaluaciones(aula: list[Estudiante]) -> list[EstadisticaColumna]:
    """Calcula estadísticas por columna (ME1..EU) excluyendo los NSP (-1).

    Args:
        aula: Lista de diccionarios de estudiantes.

    Returns:
        Lista de 6 diccionarios con evaluacion, media, minimo, maximo, desviacion y rindieron.
    """
    matriz = construir_matriz_notas(aula)
    num_filas = len(matriz)
    num_cols = len(NOMBRES_EVALUACIONES)
    resultados: list[EstadisticaColumna] = []

    for col in range(num_cols):
        validas: list[float] = []
        for fila in range(num_filas):
            nota = matriz[fila][col]
            if nota != -1:
                validas.append(float(nota))

        rindieron = len(validas)
        if rindieron == 0:
            resultados.append({
                "evaluacion": NOMBRES_EVALUACIONES[col],
                "media": 0.0,
                "minimo": 0.0,
                "maximo": 0.0,
                "desviacion": 0.0,
                "rindieron": 0,
            })
            continue

        suma_val = 0.0
        minimo_val = validas[0]
        maximo_val = validas[0]
        for val in validas:
            suma_val += val
            if val < minimo_val:
                minimo_val = val
            if val > maximo_val:
                maximo_val = val

        media = suma_val / rindieron

        suma_cuadrados = 0.0
        for val in validas:
            diff = val - media
            suma_cuadrados += diff * diff
        desviacion = math.sqrt(suma_cuadrados / rindieron)

        resultados.append({
            "evaluacion": NOMBRES_EVALUACIONES[col],
            "media": round(media, 2),
            "minimo": round(minimo_val, 2),
            "maximo": round(maximo_val, 2),
            "desviacion": round(desviacion, 2),
            "rindieron": rindieron,
        })

    return resultados


def generar_usuarios(aula: list[Estudiante]) -> list[str]:
    """Genera usuarios institucionales únicos en el orden del aula.

    Formato: inicial del nombre + primer apellido + 2 últimos dígitos del código,
    en minúsculas y sin tildes (Ñ -> n). Repetidos reciben sufijo 2, 3, ...
    """
    conteo_base: dict[str, int] = {}
    usuarios: list[str] = []

    for est in aula:
        partes = normalizar(est["nombre"]).lower().split()
        inicial = partes[0][0]
        primer_apellido = partes[1]
        dos_digitos = f"{est['codigo'] % 100:02d}"
        base = f"{inicial}{primer_apellido}{dos_digitos}"

        if base not in conteo_base:
            conteo_base[base] = 1
            usuarios.append(base)
        else:
            conteo_base[base] += 1
            usuarios.append(f"{base}{conteo_base[base]}")

    return usuarios


def imprimir_reporte(
    aula: list[Estudiante],
    ranking: list[Estudiante],
    aprobados: int,
    total_nsp: int,
    estadisticas: list[EstadisticaColumna],
    usuarios: list[str],
) -> None:
    """Imprime el reporte completo de la unidad alineado con f-strings."""
    total_est = len(aula)
    print("=" * 72)
    print(f"{'REPORTE ACADÉMICO DE UNIDAD II - LP1 (UNAP)':^72}")
    print("=" * 72)

    print("\n1. TOP 5 DEL RANKING")
    print(f"{'PUESTO':<8}{'CÓDIGO':<10}{'ESTUDIANTE':<34}{'PROMEDIO':>10}")
    print("-" * 62)
    top_limite = 5 if len(ranking) >= 5 else len(ranking)
    for i in range(top_limite):
        est = ranking[i]
        prom = promedio_dc(est["notas"])
        print(f"{i + 1:<8}{est['codigo']:<10}{est['nombre']:<34}{prom:>10.2f}")

    if ranking:
        ultimo = ranking[-1]
        prom_ult = promedio_dc(ultimo["notas"])
        print("-" * 62)
        print(
            f"{len(ranking):<8}{ultimo['codigo']:<10}"
            f"{ultimo['nombre']:<34}{prom_ult:>10.2f}  (Último)"
        )

    print("\n2. RESUMEN GENERAL DEL AULA")
    print(f"  - Total de estudiantes : {total_est}")
    print(f"  - Aprobados (>= 10.5)  : {aprobados} de {total_est}")
    print(f"  - Total de NSP (-1)    : {total_nsp} evaluaciones")

    print("\n3. ESTADÍSTICAS POR EVALUACIÓN (SIN NSP)")
    print(
        f"{'EVAL':<8}{'MEDIA':>10}{'MÍNIMO':>10}"
        f"{'MÁXIMO':>10}{'DESV. EST.':>12}{'RINDIERON':>12}"
    )
    print("-" * 62)
    for st in estadisticas:
        print(
            f"{st['evaluacion']:<8}"
            f"{st['media']:>10.2f}"
            f"{st['minimo']:>10.2f}"
            f"{st['maximo']:>10.2f}"
            f"{st['desviacion']:>12.2f}"
            f"{st['rindieron']:>12}"
        )

    print("\n4. PRIMEROS 5 USUARIOS INSTITUCIONALES (EN ORDEN DEL AULA)")
    print(f"{'N°':<6}{'CÓDIGO':<10}{'ESTUDIANTE':<32}{'USUARIO':<18}")
    print("-" * 66)
    usr_limite = 5 if len(usuarios) >= 5 else len(usuarios)
    for i in range(usr_limite):
        est = aula[i]
        print(f"{i + 1:<6}{est['codigo']:<10}{est['nombre']:<32}{usuarios[i]:<18}")
    print("=" * 72)


def main() -> None:
    """Coordina la generación del aula, procesamiento y emisión del reporte."""
    aula = generar_aula(CODIGO_UNIVERSITARIO)
    ranking = obtener_ranking(aula)
    promedios_aula = [promedio_dc(est["notas"]) for est in aula]
    aprobados = contar_aprobados(promedios_aula, 0, len(promedios_aula) - 1)
    total_nsp = contar_nsp(aula)
    estadisticas = estadisticas_evaluaciones(aula)
    usuarios = generar_usuarios(aula)

    imprimir_reporte(aula, ranking, aprobados, total_nsp, estadisticas, usuarios)


if __name__ == "__main__":
    main()