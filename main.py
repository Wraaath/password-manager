import PySimpleGUI as sg
import mysql.connector
from mysql.connector import Error
from turtle import width
from tkinter.font import BOLD, ITALIC


# -- Requirements
# pip3 install mysql-connector-python==8.0.29
# pip3 install mysql
# pip3 install PySimpleGUI
# pip3 install turtle





# Her forbinder vi til MySQL-databasen som kører med XAMPP på default-porten 3306
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

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


# Table med felterne til dine logins
create_login_table = """
CREATE TABLE IF NOT EXISTS logins (
  id INT AUTO_INCREMENT, 
  Website TEXT NOT NULL, 
  Username TEXT, 
  Password TEXT, 
  PRIMARY KEY (id)
) ENGINE = InnoDB
"""
execute_query(connection, create_login_table)


#-------------------------------- Visuals --------------------------------
import PySimpleGUI as sg
from tkinter.font import BOLD, ITALIC

sg.theme("BrownBlue")

hidden = False

def error(manager_window):
    manager_window["-NO_PICK-"].update("")

def fetch_data(connection):
    select_users = "SELECT * FROM logins"
    data = execute_read_query(connection, select_users)
    return data

def manager_function(website, username, password, connection):
    global hidden
    headings = ['ID', 'Website', 'Username', 'Password']
    data = fetch_data(connection)

    login_layout = [
        [sg.Push(), sg.Text("My Password Manager", font=("", 20, BOLD)), sg.Push()],
        [sg.Button("Create new password"), sg.Push(), sg.Button("Hide/Show")],
        [sg.Table(values=data, headings=headings, justification="c", key="-TABLE-", enable_events=True, expand_x=True, expand_y=True, font=("", 13))],
        [sg.Button("Close"), sg.Button("Delete Passwords")],
        [sg.Text("", key="-NO_PICK-", text_color="red", font=("", 12, BOLD))], [sg.Text("", key="-different_passwords-")],
        
    ]
    
    manager_window = sg.Window("Password Manager.exe", login_layout, size=(600,600))
    while True:
        event, values = manager_window.read()

        if event == "Close" or event == sg.WIN_CLOSED:
            break 
        elif event == "Create new password":
            manager_window.close()
            create_function()
        elif event == "Update":
            manager_window["-list1-"].update("Website: " + website + "\n" + "Username: " + username + "\n" + "Password: " + password)
        if event == "Delete Passwords":
            try:
                error(manager_window)
                row = values["-TABLE-"]
                row = row[0]
                print("index", row)
                number_ID = data[row]
                print("numberid", number_ID)
                nummer = str(number_ID[0])
                print("nummer", nummer)
                delete_logins = "DELETE FROM logins WHERE id = "+nummer+""
                print("boop", delete_logins)
                execute_query(connection, delete_logins)
                data = fetch_data(connection)
                manager_window["-TABLE-"].update(data)
            except IndexError:
                manager_window["-NO_PICK-"].update("You need to pick a password to delete!")
        elif event == "Hide/Show":
            if hidden:
                data2 = []
                print(data)
                for i, row in enumerate(data1):
                    row = list(row)
                    data2.append(row)
                    print(row)
                    print(data[i][3])
                    print(row[3])
                    row[3] = data[i][3]
                hidden = False
                manager_window["-TABLE-"].update(values=data2)

            if not hidden:
                data1 = []
                for row in data:
                    row = list(row)
                    data1.append(row)
                    row[3] = "******"
                hidden = True
                manager_window["-TABLE-"].update(values=data1)
                
        

    manager_window.close()
    return 

def create_function():

    create_layout = [
        [sg.Text("Create new details", font=("", 20, BOLD))],
        [sg.Text("\n" "Name on website")],[sg.Input("", key="-website-")], 
        [sg.Text("Username / Email")], [sg.Input("", key="-username-")],
        [sg.Text("Password")],[sg.Input("", key="-password-", password_char="*")],
        [sg.Button("Create"), sg.Button("Back")]
    ]

    create_window = sg.Window("Password Manager.exe", create_layout, size=(300,250))

    while True:
        event, values = create_window.read()
        print(event)

        if event == sg.WIN_CLOSED:
            break
        elif event == "Back":
            create_window.close()
            manager_function(None, None, None, connection) 
        elif event =="Create":
            website = values["-website-"]
            username = values["-username-"]
            password = values["-password-"]
            create_users = """
            INSERT INTO
              `logins` (`Website`, `Username`, `Password`)
            VALUES
              ('"""+website+"""', '"""+username+"""', '"""+password+"""');
            """
            execute_query(connection, create_users)
            create_window.close()
            manager_function(website, username, password, connection)

            
    create_window.close()

# Caller programmet
manager_function(None, None, None, connection)