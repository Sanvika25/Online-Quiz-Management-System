import sys
import random
import mysql.connector
from mysql.connector import Error

ADMIN_PASSWORD = 'admin@9876'
import warnings
warnings.filterwarnings("ignore")

def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host = host_name,
            user = user_name,
            passwd = user_password
        )
        print("Your server is running!!!")
    except Error as err:
        print(f"Error: '{err}'")
    return connection

pw = 'admin@9876'
db = 'quiz'

# Make connection
connection = create_server_connection("localhost", "root", pw)

# Database creation
def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database Created Successfully.")
    except Error as err:
        print(f"Error: '{err}'")
        
create_database_query = "Create database if not exists quiz"
create_database(connection, create_database_query)

# database connection
def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host = host_name,
            user = user_name,
            passwd = user_password,
            database = db_name
        )
        print("MySQL Database Connection Successful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection

# Execute sql queries
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query Executed Successful.")
    except Error as err:
        print(f"Error: '{err}'")

create_quiz_table = '''
create table if not exists question (
question_id int primary key,
question varchar(1000) not null,
option_1 varchar(100) not null,
option_2 varchar(100) not null,
option_3 varchar(100) not null,
option_4 varchar(100) not null,
answer varchar(100) not null
)
'''

connection = create_db_connection("localhost", "root", pw, db)
execute_query(connection, create_quiz_table)

create_user_table = '''
create table if not exists users(
user_id int primary key,
name varchar(50) not null,
score int not null
)
'''

connection = create_db_connection("localhost", "root", pw, db)
execute_query(connection, create_user_table)


def login():
    cursor = mydb.cursor()
    while True:
        user_id = input("Enter your user ID (numerical): ")
        if not user_id.isdigit():
            print("Please enter a numerical user ID.")
            continue
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user_record = cursor.fetchone()
        
        if user_record:
            username = input("Enter your username: ")
            if user_record[1] == username:
                print("Login successful!")
                return [user_id, username]
            else:
                print("Invalid username for this user ID.")
        else:
            print("User ID not found.")
            register_new_user = input("Would you like to register as a new user? (Y/N): ")
            if register_new_user.upper() == 'Y':
                username = input("Enter your username: ")
                cursor.execute("INSERT INTO users (user_id, name, score) VALUES (%s, %s, %s)", (user_id, username, 0))
                mydb.commit()
                print("Registration successful! You can now proceed.")
                return [user_id, username]
            else:
                return None
# Question section
def Question(user_id,user_name):
    if not is_admin():
        print("Access Denied! Only admin can add questions.")
        return
    key='Y'
    while key=='Y' or key=='y':
        print("Welcome to Question Portal")
        print("***********************")
        question=input("Enter the question: ")
        option_1=input("Enter the option 1: ")
        option_2=input("Enter the option 2: ")
        option_3=input("Enter the option 3: ")
        option_4=input("Enter the option 4: ")
        answer=0
        
        while answer==0:
            option=int(input("Which option is correct answer (1,2,3,4): "))
            if option==1:
                answer=option_1
            elif option==2:
                answer=option_2
            elif option==3:
                answer=option_3
            elif option==4:
                answer=option_4
            else:
                print("Please choose the correct option as answer")
                
        mycursor.execute("Select * from question")
        data=mycursor.fetchall()
        question_id=(mycursor.rowcount)+1
        mycursor.execute("Insert into question values (%s,%s,%s,%s,%s,%s,%s)",
                         (question_id,question,option_1,option_2,option_3,option_4,answer))
        mydb.commit()
        key=input("Question added successfully.. Do you want to add more (Y/N) ")
    Home(user_id,user_name)

def is_admin():
    admin_pw = input("Enter admin password: ")
    return admin_pw == ADMIN_PASSWORD

# Quiz section
def Quiz(user_id, user_name):
    print("Welcome to Quiz portal")
    print("***********************")
    mycursor.execute("SELECT * FROM question")
    data = mycursor.fetchall()
    total_question = mycursor.rowcount

    if total_question == 0:
        print("No questions available yet!")
        input("Press any key to continue: ")
        Home(user_id, user_name)
        return

    to_attempt = int(input(f"Enter the number of questions to attempt (max {total_question}):"))

    if to_attempt > total_question or to_attempt <= 0:
        print("Please enter a valid number of questions to attempt!")
        Quiz(user_id, user_name)
        return

    question_ids = [i for i in range(1, total_question + 1)]
    question_ids = random.sample(question_ids, to_attempt)
    print("Quiz has started")
    c = 1
    score = 0
    for i in range(0, len(question_ids)):
        mycursor.execute("Select * from question where question_id=%s",(question_ids[i],))
        ques = mycursor.fetchone()
        print("--------------------------------------------------------------------------------------------")
        print("Q.",c,": ",ques[1],"\nA.",ques[2],"\t\tB.",ques[3],"\nC.",ques[4],"\t\tD.",ques[5])
        print("--------------------------------------------------------------------------------------------")
        c += 1
        ans = None
        while ans == None:
            choice = input("Answer (A,B,C,D): ")
            if choice=='A' or choice=='a':
                ans = ques[2]
            elif choice=='B' or choice=='b':
                ans = ques[3]
            elif choice=='C' or choice=='c':
                ans = ques[4]
            elif choice=='D' or choice=='d':
                ans = ques[5]
            else:
                print("Kindly select A,B,C,D as option only")
        if ans == ques[6]:
            print("Correct")
            score = score + 1
        else:
            print("Incorrect.. Correct answer is: ",ques[6])
    print("Quiz has ended !! Your final score is: ",score)
    
    mycursor.execute("SELECT score FROM users WHERE user_id = %s", (user_id,))
    existing_score = mycursor.fetchone()[0]
    # Inserting quiz score into the database
    if score > existing_score:
        mycursor.execute("UPDATE users SET score = %s WHERE user_id = %s", (score, user_id))
        mydb.commit()
        print("Your score has been updated!")

    mydb.commit()
    input("Press any key to continue: ")
    Home(user_id,user_name)

# Create home page
def Home(user_id,user_name):
    opt = 1
    while opt != 3:
        print("Welcome to Quiz")
        print("********************")
        print("1. Enter Questions")
        print("2. Take Quiz")
        print("3. Exit")
        opt = int(input("Enter your choice: "))
        if opt == 1:
            Question(user_id,user_name)
        elif opt == 2:
            Quiz(user_id,user_name)
        elif opt == 3:
            print("Exiting the Quiz")
            mycursor.close()
            mydb.close()
            sys.exit()
        else:
            Home(user_id,user_name)

mydb = mysql.connector.connect(
    host= "localhost",
    user= "root",
    passwd="admin@9876",
    database= "quiz"
)
mycursor = mydb.cursor()

# Run the program
user_credentials = login()
if user_credentials:
    Home(user_credentials[0],user_credentials[1])  # Passing user_id to Home function
