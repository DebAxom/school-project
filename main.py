import os
import readline
import pandas as pd
import mysql.connector as sql
import matplotlib.pyplot as plt
from simple_term_menu import TerminalMenu

db = sql.connect(host="127.0.0.1",port="3306",
user="root",password="JoiAiAxom")
cursor = db.cursor()

cursor.execute("create database gunv;")
curose.execute("use gunv;")
try: cursor.execute("drop table shootings;")
except : pass

cursor.execute('''create table if not exists shootings 
    (slno INTEGER PRIMARY KEY, casename varchar(50), 
    location varchar(50), fatalities int, injured int, 
    total_victims int, place varchar(50) , age int, race 
    varchar(10), gender varchar(1), type varchar(10), 
    year int(4));''')

df = pd.read_csv(r"shootings.csv")

def convertToSQL_Table():
    for x,y in df.iterrows():
        data = tuple(y)
        cursor.execute(f'''insert into shootings (casename, 
        location, fatalities, injured, total_victims, 
        place, age, race, gender, type, year) values
        ("{data[0]}","{data[1]}",{data[2]},{data[3]},{data[4]},
        "{data[5]}",{data[6]},"{data[7]}","{data[8]}","{data[9]}",
        {data[10]});'''w)
        db.commit()

convertToSQL_Table()

def convertToCSV():
    cursor.execute('''select casename, location, fatalities, 
    injured, total_victims, place, age, race, 
    gender, type, year from shootings;''')
    newdf = pd.DataFrame(cursor.fetchall(),
    columns=['casename', 'location', 'fatalities', 
    'injured', 'total_victims', 'place', 'age', 
    'race', 'gender', 'type', 'year'])
    newdf.to_csv("edited-data.csv", index=False)

def editMenu():
    print("Choose Action :")
    options = ["Add Data", "Delete Row", "Edit Data"]

    terminal_menu = TerminalMenu(options,
    menu_highlight_style=("fg_yellow",))
    index = terminal_menu.show()

    if index == None : return
    if index == 0: AddData()
    if index == 1: DeleteRow()
    if index == 2: EditData()

def AddData():
    casename = input("Enter Casename : ")
    print('\033[1A' + '\033[K', end='')
    location = input("Enter Location : ")
    print('\033[1A' + '\033[K', end='')
    fatalities = input("Enter no of fatalities : ")
    print('\033[1A' + '\033[K', end='')
    injured = input("Enter no of injured : ")
    print('\033[1A' + '\033[K', end='')
    total_victims = input("Enter total no of victims : ")
    print('\033[1A' + '\033[K', end='')
    place = input("Enter place : ")
    print('\033[1A' + '\033[K', end='')
    age = input("Enter age of shooter : ")
    print('\033[1A' + '\033[K', end='')
    race = input("Enter race of shooter : ")
    print('\033[1A' + '\033[K', end='')
    gender = input("Enter gender : ")
    print('\033[1A' + '\033[K', end='')
    types = input("Enter type of shooting: ")
    print('\033[1A' + '\033[K', end='')
    year = input("Enter year : ")
    print('\033[1A' + '\033[K', end='')
    cursor.execute(f'''insert into shootings (casename, location, 
    fatalities, injured, total_victims, place, age, race, gender, 
    type, year) values("{casename}","{location}",{fatalities},{injured},
    {total_victims},"{place}",{age},"{race}","{gender}","{types}",{year});''')
    db.commit()

def EditData():
    id = input("Enter the slno : ")
    print("Select the field you want to update : ")
    options = ["casename", "location", "fatalities", "injured", 
    "total_victims", "place", "age", "race", 
    "gender", "type", "year"]
    terminal_menu = TerminalMenu(options,menu_highlight_style=("fg_yellow",))
    index = terminal_menu.show()
    value = input(f"Enter new Value for {options[index]} : ")
    if index == 2 or index == 3 or index == 4 or index == 6 or index == 10 :
        cursor.execute(f'''update table shootings set {options[index]} = {value} where slno = {id};''')
        db.commit()
        return
    cursor.execute(f'''update shootings set {options[index]} = "{value}" where slno = {id};''')
    db.commit()

def DeleteRow():
    id = int(input("Enter Row number : "))
    cursor.execute(f"delete from shootings where slno = {id};")
    db.commit()

def viewMenu():
    print("Choose Action :")
    options = ["No of people killed by criminals of each race", 
    "No of Shootings by Place", "No of Shootings by Year", 
    "Mass vs Spree", "Find cases by location", "List all Data"]

    terminal_menu = TerminalMenu(options,menu_highlight_style=("fg_yellow",))
    index = terminal_menu.show()

    if index == None : return
    if index == 0: CriminalsEthnicity()
    if index == 1: ShootingsByPlace()
    if index == 2: ShootingsByYear()
    if index == 3: MassVsSpree()
    if index == 4: FindCasesByLocation()
    if index == 5: 
        cursor.execute("select * from shootings;")
        data = cursor.fetchall()
        print(pd.DataFrame(data).to_string(index=False))

def FindCasesByLocation():
    location = input("Enter the Location : ")
    cursor.execute(f"select casename, location, fatalities, injured, total_victims, 
    place, age, race, gender, type, year from shootings where location like '%{location}%';")
    data = cursor.fetchall()
    print(pd.DataFrame(data,columns=['casename', 'location', 'fatalities', 'injured', '
    total_victims', 'place', 'age', 'race', 'gender', 'type', 'year']).to_string(index=False))

def MassVsSpree():
    x1 = []
    y1 = []
    x2 = []
    y2 = []

    cursor.execute("select year, count(*) from shootings group by year having type='Mass';")
    data1 = cursor.fetchall()
    cursor.execute("select year, count(*) from shootings group by year having type='Spree';")
    data2 = cursor.fetchall()

    for i in data1: 
        x1.append(i[0])
        y1.append(i[1])
    for i in data2: 
        x2.append(i[0])
        y2.append(i[1])
    
    plt.xlabel = "Year"
    plt.ylabel = "Frequency"
    plt.plot(x1,y1,label="Mass",linestyle="-")
    plt.plot(x2,y2,label="Spree",linestyle="--")
    plt.legend()
    plt.show()

def CriminalsEthnicity():
    x = []
    y = []
    cursor.execute("select race, sum(total_victims) as total from shootings group by race;")
    data = cursor.fetchall()
    for i in data: 
        x.append(i[0])
        y.append(i[1])
    plt.barh(x,y)
    plt.title("Number of people killed by people of each race")
    plt.xlabel("No of victims killed by the race")
    plt.ylabel("Race of the criminal")
    plt.show()

def ShootingsByPlace():
    x = []
    y = []
    cursor.execute("select place, count(*) as total from shootings group by place;")
    data = cursor.fetchall()
    for i in data: 
        x.append(i[0])
        y.append(i[1])
    plt.barh(x,y)
    plt.title("Shootings by place")
    plt.xlabel("No of shootings")
    plt.ylabel("Place")
    plt.show()

def ShootingsByYear():
    x = []
    y = []
    cursor.execute("select Year, count(*) as total from shootings group by year;")
    data = cursor.fetchall()
    for i in data: 
        x.append(i[0])
        y.append(i[1])
    plt.bar(x,y)
    plt.title("Number of Shootings per year")
    plt.xlabel("Year")
    plt.ylabel("No of Shootings")
    plt.show()

def clear():
    os.system("clear")
    return

def help():
    print('''
    \033[33mFollowing are the commands you can type in this CLI :
    > view // To open the view menu
    > edit // To open the edit menu
    > print // To get the edited data in csv format
    > clear // To clear the terminal
    > exit // To close this application
    ''')

if __name__ == "__main__":

    commandsList = {
        'edit' : editMenu,
        'view' : viewMenu,
        'help' : help,
        'clear' : clear,
        'print' : convertToCSV,
        'default' : lambda : print('\033[31mType a Valid command')
    }

    print(''' 
    \033[1;37mWelcome to the world of Crime !
    \033[0;37mThis CLI based application will help you analyze data of some selected gun violence case in tge USA.

    \033[33mFollowing are the commands you can type in this CLI :
    > view // To open the view menu
    > edit // To open the edit menu
    > print // To get the edited data in csv format
    > clear // To clear the terminal
    > exit // To close this application
    > help // To open the help menu

    ''')

    while True:
        cm = input("\033[1;34mλ \033[0;37m")
        if cm=="exit" : break
        try: commandsList.get(cm)()
        except Exception as e:
            commandsList.get('default')()