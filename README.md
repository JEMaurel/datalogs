📊 Log Analysis with DuckDB (Data Engineering Practice)

Este proyecto consiste en el análisis de logs de una API utilizando DuckDB y SQL analítico, con el objetivo de extraer métricas operativas, detectar problemas de performance y generar recomendaciones accionables para el equipo de desarrollo.

El trabajo simula un escenario real de observabilidad, combinando exploración de datos, agregaciones, window functions y análisis temporal.

🗂️ Dataset

Se trabaja sobre logs de acceso de una API en formato JSON (logs_access_logs.json), con información como:

Timestamp de la request

Endpoint

Código de estado HTTP

Tiempo de respuesta

Usuario

IP, user agent, etc.

Ejemplo de campos principales:

timestamp

endpoint

status_code

response_time_ms

user_id

🛠️ Tecnologías utilizadas

Python 3

DuckDB

SQL Analítico

Pandas (vía fetchdf())

🚀 Ejecución del proyecto

Clonar el repositorio:

git clone <url-del-repo>
cd datalogs


Instalar dependencias:

pip install duckdb pandas


Ejecutar el script principal:

python duki.py


El script carga los datos desde JSON, crea las tablas en DuckDB y ejecuta todas las queries de análisis.

📈 Análisis realizados
1. Exploración inicial

Total de requests

Período cubierto

Usuarios únicos

Endpoints únicos

2. Endpoints más usados

Identificación de los endpoints con mayor volumen de tráfico.

3. Análisis de errores (status ≥ 500)

Endpoints con más errores

Usuarios afectados

Tiempo promedio de respuesta en errores

4. Performance por endpoint

Se analizan métricas clave:

Promedio

p50 (mediana)

p95

Máximo

Se prioriza p95 como métrica principal, siguiendo buenas prácticas de SLO.

5. Tendencia horaria

Requests por hora

Latencia promedio

Errores por franja horaria

6. Window Functions (Ranking)

Top 3 requests más lentas por endpoint usando ROW_NUMBER().

7. Comparación día a día

Análisis de variación diaria utilizando LAG():

Diferencia absoluta

Cambio porcentual

🧠 Hallazgos principales

El tráfico está distribuido de forma pareja entre endpoints.

Algunos endpoints presentan errores con latencias extremadamente altas, lo cual indica fallas no controladas.

El promedio no es representativo; el p95 es la métrica más confiable.

Se detectan picos de latencia en horarios específicos sin aumento de tráfico.

✅ Recomendaciones

Optimizar endpoints con errores lentos (/api/products, /api/checkout).

Monitorear p95 y p99 como métricas clave de performance.

Revisar procesos internos que impactan la latencia en horarios específicos.

📌 Objetivo del proyecto

Este proyecto tiene fines educativos y prácticos, orientados a:

Data Engineering

Observabilidad

SQL avanzado

Análisis de logs en entornos productivos