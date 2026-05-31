import duckdb as db 


con = db.connect()

con.execute("""
    CREATE VIEW trips AS
    SELECT * FROM read_parquet('dados/bronze/yellow_tripdata_2024-01.parquet')
""")

con.execute("""
    CREATE VIEW zones AS
    SELECT * FROM read_csv_auto('dados/bronze/taxi_zones.csv')
""") 

numero_linhas = con.execute("""SELECT COUNT(*) FROM trips""").fetchdf()

colunas = con.execute("""SELECT * FROM trips LIMIT 1""").fetchdf()

zonas = con.execute("""SELECT * FROM zones LIMIT 5""").fetchdf()

estatisticas = con.execute("""SELECT *,
                                CASE 
                                    WHEN total_amount < 0 THEN total_amount ELSE NULL
                                END AS total_amount_negativo,
                                
                           FROM trips""").fetchdf()
estatisticas_minmax = con.execute("""
    SELECT 
    SUM(total_amount) / COUNT(*) AS media_total_amount,
        MIN(total_amount) AS min_total_amount,
        MAX(total_amount) AS max_total_amount
    FROM trips
""").fetchdf()

datas = con.execute(""" SELECT MIN(tpep_pickup_datetime) AS data_inicial,
                                MAX(tpep_pickup_datetime) AS data_final
                        FROM trips""").fetchdf()

print(numero_linhas)
print('-----------------------------')
print(colunas)
print('-----------------------------')
print(zonas)
print('-----------------------------')
print(estatisticas)
print('-----------------------------')
print(datas)
print('-----------------------------')
print(estatisticas_minmax)