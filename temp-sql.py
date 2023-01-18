import mysql.connector
from mysql.connector import Error

# pip3 install mysql-connector-python==8.0.29
# pip3 install mysql


#Her forbinder vi til MySQL-databasen som kører med XAMPP på default-porten 3306
def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

connection = create_connection("localhost", "root", "", "pass-db")

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


#Tabel med alle login
create_users_table = """
CREATE TABLE IF NOT EXISTS logins (
  id INT AUTO_INCREMENT, 
  name TEXT NOT NULL, 
  user TEXT, 
  pass TEXT, 
  PRIMARY KEY (id)
) ENGINE = InnoDB
"""
execute_query(connection, create_users_table)

