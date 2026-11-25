# Dataset de migración interna — Censo Bolivia 2024

Este repositorio contiene el script que transforma el CSV de personas del CPV 2024 en Parquet particionado por departamento y el ZIP de datos utilizado en Colab.

## ZIP para Colab

Descarga `data/exports/cochabamba_santa_cruz_parquets.zip` y súbelo al notebook. Contiene nueve particiones Parquet y abarca los datos nacionales, incluidos los registros con y sin talento; no está limitado geográficamente al corredor. El notebook aplica sus propios filtros. Contiene microdatos e identificadores de vivienda de uso público.

## Reproducir los Parquet

Con Python 3 y DuckDB, coloca el CSV original en `data/Persona_CPV-2024.csv` y ejecuta:

```bash
pip install -r requirements.txt
python scripts/build_interdepartmental_extended.py
```

El proceso lee columnas seleccionadas con DuckDB, usa un límite de memoria de 4 GB y genera Parquet con compresión Zstandard en `data/derived/talento_interdepartamental_extendido/idep=XX/`. No sobrescribe un directorio de salida existente. La ejecución puede requerir espacio temporal y tarda según el equipo.

Para crear un ZIP equivalente, comprime la carpeta `data/derived/talento_interdepartamental_extendido` completa conservando sus subcarpetas `idep=XX`. `is_talent` indica nivel educativo 9–13 y edad de al menos 19 años; `migration_target` solo se define para personas con talento y departamentos válidos. El análisis del corredor puede construir su propia variable objetivo.

La variable `dep_nac_cod=0` mezcla nacidos en el exterior con falta de respuesta; para distinguirlos se requiere incorporar `p35_lugnac`, ausente en estos Parquet. El CSV original no está incluido.
