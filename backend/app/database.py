# import psycopg2
# from psycopg2.extras import RealDictCursor
# from app.config import settings

# try:
#     conn = psycopg2.connect(
#         host=settings.database_hostname,
#         port=settings.database_port,
#         dbname=settings.database_name,
#         user=settings.database_username,
#         password=settings.database_password,
#         cursor_factory=RealDictCursor
#     )
#     cursor = conn.cursor()
#     print("✅ Database connected successfully!")
# except Exception as e:
#     print(f"❌ Database connection failed: {e}")
#     exit()
