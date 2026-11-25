"""Build interdepartmental target with stable and labour-analysis covariates."""
from pathlib import Path
import duckdb

root=Path(__file__).resolve().parents[1]
src=(root/'data'/'Persona_CPV-2024.csv').as_posix(); out=(root/'data'/'derived'/'talento_interdepartamental_extendido').as_posix()
if Path(out).exists(): raise FileExistsError(out)
cols='idep,iprov,imun,i00,p25_sexo,p26_edad,p28_cn,p29_ci,p32_pueblo_per,p341_idiomat_cod,p42_discap,dep_nac_cod,dep_res5_cod,dep_res_cod,p41a_nivel_act,aestudio,ocu_1d_19,act_eco_2d_19,condact_19,ft_19,p50_semp,p52_mov,dep_lab_cod'
text={'idep','iprov','imun','i00'}
casts=[f'trim({c}) AS {c}' if c in text else f'TRY_CAST({c} AS {"DOUBLE" if c=="aestudio" else "INTEGER"}) AS {c}' for c in cols.split(',')]
q=f"""WITH raw AS (SELECT * FROM read_csv('{src}',delim=';',header=true,all_varchar=true)), typed AS (SELECT {', '.join(casts)} FROM raw)
SELECT *, p41a_nivel_act BETWEEN 9 AND 13 AND p26_edad>=19 AS is_talent,
CASE WHEN p41a_nivel_act BETWEEN 9 AND 13 AND p26_edad>=19 AND dep_res5_cod BETWEEN 1 AND 9 AND dep_res_cod BETWEEN 1 AND 9 THEN CAST(dep_res5_cod<>dep_res_cod AS INTEGER) END AS migration_target FROM typed"""
con=duckdb.connect(); con.execute("SET memory_limit='4GB'"); con.execute("SET threads=4"); con.execute(f"COPY ({q}) TO '{out}' (FORMAT PARQUET,COMPRESSION ZSTD,PARTITION_BY (idep))"); print(con.execute(f"SELECT count(*) FILTER (WHERE migration_target IS NOT NULL), count(*) FILTER (WHERE migration_target=1) FROM parquet_scan('{out}/**/*.parquet',hive_partitioning=true)").fetchall())
