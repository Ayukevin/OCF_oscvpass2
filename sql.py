import mysql.connector
import pandas as pd
import setting

conn = mysql.connector.connect( **setting.my_sql_setting )
cursor = conn.cursor()

cursor.execute("USE mydatabase;")
cursor.execute("SELECT * FROM users;")

