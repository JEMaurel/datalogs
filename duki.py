



import duckdb


con = duckdb.connect()

con.execute( """ CREATE TABLE logs AS 
SELECT * 
FROM read_json_auto('data/logs_access_logs.json')""")

print ("total filas : " , con.execute("select count(*) FROM logs").fetchone()[0])
print( '\n columnas;  ')
for col in con.execute("describe logs").fetchall():
    print(f" {col[0]}:{col[1]}")

print("\n primeras tres filas")
print(con.execute("SELECT * FROM logs LIMIT 3").fetchdf())

result = con.execute("""
      SELECT
          COUNT(*) AS total_requests,
          MIN(timestamp) AS primera_request,
          MAX(timestamp)AS ultima_request,
          COUNT(DISTINCT user_id) AS usuarios_unicos,
          COUNT(DISTINCT endpoint)AS endpoint_unicos
          FROM logs
          """ ).fetchdf()

print(result)

query_2 = con.execute("""
    SELECT 
    endpoint,
    COUNT(*) AS hits,
    ROUND(COUNT(*) * 100 /(SELECT COUNT(*) FROM logs),2) AS porcentaje
    FROM logs 
    GROUP BY endpoint
    ORDER BY hits DESC 
    LIMIT 10 """

).fetchdf()
print ("\n top endpoints mas usados : ")
print ( query_2)

query_3 = con.execute("""
    SELECT 
        endpoint,
        COUNT(*) AS total_errors,
        COUNT(DISTINCT user_id) AS usuarios_afectados,
        ROUND( AVG(response_time_ms),2) AS avg_response_time
    FROM logs 
    WHERE status_code > 500 
    GROUP BY endpoint 
    ORDER BY total_errors DESC
    LIMIT 10 """

).fetchdf()
print( "\n endpoints con mas errores =============================================================== ")
print(query_3)

query_4 = con.execute("""
    SELECT 
        endpoint,
        COUNT(*) AS requests,
        ROUND(AVG(response_time_ms),2) AS avg_time,
        ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY response_time_ms),2) AS p50,
        ROUND(PERCENTILE_CONT(0.95) WITHIN GROUP(ORDER BY response_time_ms),2) AS p95,
        MAX(response_time_ms) AS max_time
    FROM logs
    WHERE status_code <500 
    GROUP BY endpoint 
    HAVING COUNT(*)>5
    ORDER BY p95 DESC 
    LIMIT 10 """
).fetchdf()

print ("\n prformance por endpoint =========================================================")
print(query_4)

query_5 = con.execute("""
    SELECT 
        EXTRACT(HOUR FROM timestamp) AS hora ,
        COUNT(*) AS requests,
        ROUND(AVG(response_time_ms),2) AS avg_response_time,
        SUM( CASE 
                WHEN status_code >=500 THEN 1 ELSE 0 END) AS errors
    FROM logs
    GROUP BY hora
    ORDER BY hora """
).fetchdf()
print("\n tendencia horaria ================================================")
print(query_5 )

query_6 = con.execute("""
    WITH ranked AS (
        SELECT 
            endpoint,
            timestamp,
            response_time_ms,
            user_id,
            ROW_NUMBER()OVER(PARTITION BY endpoint ORDER BY response_time_ms DESC )AS rank
       FROM logs 
        WHERE status_code < 500

)
SELECT 
    endpoint,
    timestamp,
    response_time_ms,
    user_id,
    rank
FROM ranked
WHERE rank <= 3
ORDER BY endpoint,rank
""").fetchdf()
print("\n top 3 mas lentas por endpoint ================================")
print(query_6)

query_7 = con.execute("""
    WITH daily_stats AS (
        SELECT 
            DATE(timestamp) AS fecha,
            COUNT(*) AS requests,
            ROUND(AVG(response_time_ms),2) AS avg_time
        FROM logs
        GROUP BY DATE(timestamp)
    )
SELECT 
    fecha,
    requests,
    LAG(requests) OVER(ORDER BY fecha) AS requests_dia_anterior,
    requests - LAG(requests) over ( ORDER BY fecha) AS diferencia,

    ROUND(
    (requests - LAG(requests) OVER (ORDER BY fecha)) *100.0/ 
    LAG(requests) OVER (ORDER BY fecha),2 ) AS cambio_porcentual
    FROM daily_stats
    ORDER BY fecha """

).fetchdf()
print("\n comparaciones dia a dia de requests ")
print(query_7)