from datetime import datetime
import string, random
import sqlite3,os
if os.path.isfile('sqlite.db'):
    conn=sqlite3.connect("sqlite.db")
    cur=conn.cursor()
else:
    conn=sqlite3.connect("sqlite.db")
    cur=conn.cursor()
    cur.execute('''
            Create table if not exists Account(
                AccId varchar(20)PRIMARY KEY,
                FirstName VARCHAR(20) NOT NULL, LastName VARCHAR(35),DOB DATE NOT NULL,
                Balance MONEY NOT NULL, Card_No VARCHAR(20) NOT NULL UNIQUE, Pin CHAR(12) NOT NULL)

    ''')
    cur.execute('''INSERT INTO Account values(1001,'Pranjal','Goyal',"2001-10-11",1000,"125356278654","1234")''')
    cur.execute('''INSERT INTO Account values(1002,'Neha','Jain',"1998-11-01",1200,"154328629874","4321")''')
    cur.execute('''INSERT INTO Account values(1003,'Anusha','Mittal',"2000-11-07",2000,"652987153076","7777")''')
    # print("one row inserted")
# print(cur.execute('''SELECT Balance FROM Account;''').fetchall())
    cur.execute('''
            Create table if not exists Transactions(
                Transaction_ID VARCHAR(15) PRIMARY KEY,Description TEXT NOT NULL,Senders_card VARCHAR(20),
                Receivers_card VARCHAR(20),Senders VARCHAR(20),Receiver VARCHAR(20),
                Amount MONEY,Transaction_Date DATE NOT NULL,Transaction_Time TIME NOT NULL)
    ''')

# print(cur.execute('''SELECT * FROM Transactions;''').fetchall())
    # print("Transaction table created successfully.")



print("WELCOME TO MY ATM \n\n")
def menu():
    print("\n \nChoose the task from the menu \n","-"*5,"1.  Pin Change \n","-"*5,"2.  Money Transfer \n","-"*5,"3.  Withdraw Money \n","-"*5,"4.  Print Statement \n","-"*5,"5.  Transaction Log \n","-"*5,"6.  Exit")
    task=input("Enter number for the task: ")
    if(not task.isdigit()):
        print("please enter the digit from the above menu")
        return menu()
    elif(task=="1"):
        PinChange()
    elif(task=="2"):
        MoneyTransfer()
    elif(task=="3"):
        # print("corrext3")
        Withdraw()
    elif(task=="4"):
       PrintStatement()
    elif(task=="5"):
        TransactionLog()
    elif(task=="6"):
        print("Thank you for visiting.")
    else:
        print("Invalid Number Entered")

a_num=input("Enter your Card Number: ")

send=0
sender=""
receive=0

def PinChange():
    new_pin=input("Please Enter Your New Pin: ")
    if(not new_pin.isdigit()):
        print("Please Enter Digit Only")
    elif len(new_pin)>4 or len(new_pin)<4:
        print("Please Enter 4 Digits Only")
    else:
        cur.execute("UPDATE Account set Pin=? where Card_No=?",(new_pin,a_num))
        conn.commit()
        print("Your Pin Is Changed")
        menu()



def MoneyTransfer():
    b_num=input("Enter The Card Number You Want To Transfer The Money: ")
    a=cur.execute(f''' 
                    SELECT Balance FROM Account where Card_No is '{a_num}'
    ''')
    for c in a:
        global send
        send=c[0]
    # print(send)
    b=cur.execute(f''' 
                    SELECT Balance,FirstName FROM Account where Card_No is '{b_num}'
    ''')
    
    check=True
    for d in b:
        check=False
        global receive
        receive=d[0]
        receiver=d[1]
        # print(receiver)
        amt=input("Enter The Amount You want To Transfer: ")
        if(int(amt)>send):
            print("insufficient amount")
        else:
            sender_bal=send-int(amt)
            rec_bal=receive+int(amt)
            cur.execute("UPDATE Account set Balance =? where Card_No=?",(sender_bal,a_num))
            cur.execute("UPDATE Account set Balance =? where Card_No=?",(rec_bal,b_num))
            conn.commit()
        p=cur.execute(f''' 
                        SELECT Balance,FirstName FROM Account where Card_No is '{a_num}'
        ''')
        for x in p:
            print("Balance left in your account: ",x[0])
            global sender
            sender=x[1]
            # print(sender)
        now=datetime.now()
        time=now.strftime("%H:%M:%S")
        date=now.strftime("%d-%m-%Y")
        # charst=list(set(string.digits+ e))
        t_id=''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) 
        # print(t_id)  
        des=sender+" sent to "+receiver
        # print(des) 
        cur.execute(f'''
                    INSERT INTO Transactions VALUES('{t_id}','{des}','{a_num}','{b_num}','{sender}','{receiver}','{amt}','{date}','{time}')
        ''')
        conn.commit()
        menu()
    if check:
        print("invalid account")
    

def Withdraw():
    amount=input("Enter The Amount You Want To Withdraw: ")
    query="""SELECT Balance from Account where Card_No= ?"""
    cur.execute(query, (a_num,))
    records =cur.fetchall()
    if(not amount.isdigit):
        print("please enter the correct amount.")
        return Withdraw()
    else:
        for a in records:
            if(a[0]<int(amount)):
                print("Insufficient Amount")
            else:
                bal=a[0]-int(amount)
                cur.execute("UPDATE Account set Balance =? where Card_No=?",(bal,a_num))
                conn.commit()
                print("Balance left in your account:",bal)
                menu()
                
def PrintStatement():
    a=cur.execute(f''' 
                    SELECT * FROM Account where Card_No is '{a_num}'
    ''')
    for x in a:
        fp=open("statement.txt","w")
        text="First Name: ",x[1],"\nSecond Name: ",x[2],"\nDate Of Birth: ",x[3],"\nCard Number: ",x[5],"\nBalance: ",str(x[4])
        fp.writelines(text)
        fp.close
    fp=open("statement.txt","r")
    state=fp.read()
    print(state)
    fp.close()
    menu()


def TransactionLog():
    query=cur.execute(f'''
                        Select * FROM Transactions WHERE Senders_card ='{a_num}' or Receivers_card= '{a_num}'
    ''')
    data=query.fetchall()
    f=open("Transactions.txt","w+",encoding='utf-8')
    for i in data:
        for j in range(len(i)):
            f.write(str(i[j]))
            f.write("\t\t\t")
        f.write("\n")
    f.close()
    print("Transaction file is created")
    menu()


def Authenticate():
    query="""SELECT Card_No, Pin from Account where Card_No= ?"""
    cur.execute(query, (a_num,))
    records =cur.fetchall()
    if(not a_num.isdigit()):
        print("Card Number should contain numbers only...")

    elif(len(a_num)>12 or len(a_num)<12):
        print("Card Number must be of 12 Length..")
        # return Authenticate()
    else:
        check=True
        for a in records:
            check=False
                # pin_check()
            trial=1
            while trial<=3:
                trial+=1
                pin=input("Enter Your Pin Number: ")
                if(not pin.isdigit()):
                    print("PIN should contain positive numbers only...")
                    # return False
                elif(len(pin)>4 or len(pin)<4):
                    print("PIN must be of 4 Length.. Try Again..")
                    # return False
                else:
                    if pin == a[1]:
                        menu()
                        break
                        # print("correct")
                    else:
                        print("Invalid Pin Please Enter Again")
        if check:
            print("The Card Number Does Not Exists")

Authenticate()

cur.close()
conn.commit()
conn.close()