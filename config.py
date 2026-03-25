import mysql.connector
 
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="dikshapatil@00",
        database="symptom_analyzer"
    )