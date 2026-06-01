import duckdb as db

con = db.connect("db/lakehouse.duckdb")

con.execute("""
    CREATE OR REPLACE VIEW silver_trips AS
    SELECT * FROM read_parquet('dados/silver/yellow_tripdata_2024-01.parquet')
""")

con.execute("""
COPY (
    SELECT
        pickup_borough,
        pickup_zone,
        COUNT(*)                        AS total_viagens,
        ROUND(SUM(total_amount), 2)     AS receita_total,
        ROUND(AVG(total_amount), 2)     AS ticket_medio,
        ROUND(AVG(trip_distance), 2)    AS distancia_media
    FROM silver_trips
    GROUP BY 1, 2
    ORDER BY total_viagens DESC
) TO 'dados/gold/viagens_por_bairro.parquet' (FORMAT PARQUET) 

""")

con.execute("""COPY (
    SELECT
        EXTRACT('hour' FROM tpep_pickup_datetime)::INT  AS hora,
        COUNT(*)                                        AS total_viagens,
        ROUND(AVG(total_amount), 2)                     AS ticket_medio,
        ROUND(AVG(trip_duration_minutes), 1)            AS duracao_media_min
    FROM silver_trips
    GROUP BY 1
    ORDER BY 1
) TO 'dados/gold/viagens_por_hora.parquet' (FORMAT PARQUET) """)

