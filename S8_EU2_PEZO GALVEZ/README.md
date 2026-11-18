# Examen Domiciliario EU2 · Analizador del Registro de Notas

- **Asignatura:** Lenguaje de Programación I (10018) — Ciclo IV (Semestre 2026-II)
- **Institución:** Facultad de Ingeniería de Sistemas e Informática — UNAP (Iquitos)
- **Estudiante:** Pezo Galvez
- **Código universitario:** `2155263` (`D = 3`, `P = 6`, `K = 2`)

## 1. Descripción general
Este proyecto procesa el registro académico de un aula determinista de 30 estudiantes (`generar_aula(2155263)`), cada uno con 6 evaluaciones (`ME1`, `ME2`, `ME3`, `PC1`, `PC2`, `EU`, donde `-1` representa *No Se Presentó* — NSP), implementando manualmente los algoritmos de ordenamiento, búsqueda, divide y vencerás y estadística descriptiva sin depender de `sort`, `sorted`, `min`, `max`, `sum`, `statistics`, `bisect`, `numpy` ni `pandas` en el módulo principal.

## 2. Estructura del proyecto
```text
S8_EU2_Pezo/
├── analizador.py   # Lógica de procesamiento, algoritmos propios y emisión de reporte
├── pruebas.py      # Batería de pruebas unitarias con assert (6 bloques de verificación)
└── README.md       # Documentación técnica del proyecto