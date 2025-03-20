import psycopg2
conn = psycopg2.connect(
    dbname="local",
    user="postgres",
    password="Aswin2000",
    host="localhost",
    port="5432",
)