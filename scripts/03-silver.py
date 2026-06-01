import duckdb as db

con = db.connect("db/lakehouse.duckdb")


con.execute("""
    CREATE OR REPLACE VIEW bronze_trips AS
    SELECT * FROM read_parquet('dados/bronze/yellow_tripdata_2024-01.parquet')
""")

con.execute("""
    CREATE OR REPLACE VIEW bronze_zones AS
    SELECT * FROM read_csv_auto('dados/bronze/taxi_zones.csv')
""")

con.execute("""

COPY (SELECT
                t.VendorID,
                t.tpep_pickup_datetime,
                t.tpep_dropoff_datetime,
                t.passenger_count,
                t.trip_distance,
                t.RatecodeID,
                t.store_and_fwd_flag,
                t.PULocationID,
                t.DOLocationID,
                t.payment_type,
                t.fare_amount,
                t.extra,
                t.mta_tax,
                t.tip_amount,
                t.tolls_amount,
                t.improvement_surcharge,
                t.total_amount,
                t.congestion_surcharge,
                t.Airport_fee,
                pu.Borough  AS pickup_borough,
                pu.Zone     AS pickup_zone,
                do_.Borough AS dropoff_borough,
                do_.Zone    AS dropoff_zone,
                DATEDIFF('minute', t.tpep_pickup_datetime, t.tpep_dropoff_datetime) AS trip_duration_minutes
                        
                FROM bronze_trips t
                    LEFT JOIN bronze_zones pu
                    ON t.PULocationID = pu.LocationID
                    LEFT JOIN bronze_zones do_
                    ON t.DOLocationID = do_.LocationID
                    
                WHERE t.total_amount > 0 
                    AND t.total_amount IS NOT NULL 
                    AND  t.trip_distance > 0
                    AND t.passenger_count > 0
                    AND t.tpep_pickup_datetime IS NOT NULL
                    AND t.tpep_pickup_datetime >= '2024-01-01'
                    AND t.tpep_pickup_datetime < '2024-02-01'
                    AND DATEDIFF('minute', t.tpep_pickup_datetime, t.tpep_dropoff_datetime)  > 0
                    AND DATEDIFF('minute', t.tpep_pickup_datetime, t.tpep_dropoff_datetime)  < 180

              ) TO 'dados/silver/yellow_tripdata_2024-01.parquet' ( FORMAT PARQUET) """)