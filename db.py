import pymysql as mq

from tkinter import messagebox


# Replace these with your actual database credentials
host = "localhost"
user = "root"
password = ""
db_name = "my_test"
# connecting with database if database exist


def create_database (host,user,password,db_name):
    try:
        con = mq.connect(host=host, user=user, password=password)
        my_cur = con.cursor()
        my_cur.execute("create database'"+db_name)
    except mq.Error as e:
         messagebox.showinfo("error", e)



con = mq.connect(host=host, user=user, password=password, database=db_name)
my_cur = con.cursor()



def create_table(tb_name,name,number,qty,description,amount):

# code will create table
    try:

       table = "CREATE TABLE '"+tb_name+"' (sno INT PRIMARY KEY AUTO_INCREMENT, time TIMESTAMP, '"+name+"'name VARCHAR(20), '"+number+"' INT, '"+qty+"' INT, '"+description+"'TEXT, '"+amount+"' INT)"
       my_cur.execute(table)

    except mq.Error as e:
        messagebox.showinfo("error", e)
      
 
def insert (a, b, c, d, e):

    try:
      ins = "INSERT INTO customers (name, number, qty, description, amount) VALUES (%s, %s, %s, %s, %s)"
      cust = (a, b, c, d,e)
      my_cur.execute(ins, cust)
      con.commit()
      #messagebox.showinfo("info","data inserted ")
      #print("Data inserted")
    except mq.Error as e:
        messagebox.showinfo("error", e)

def get_all():
    try:
        my_cur.execute("SELECT * FROM customers")
        result = my_cur.fetchall()
        return result
    except mq.Error as e:
        messagebox.showinfo("error", e)







