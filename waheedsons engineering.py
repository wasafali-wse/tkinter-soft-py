# importing some necessory modules 

#from statistics import mode
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from docxtpl import *
import time 
import os
import pymysql as mq
import json
import socket as s
from datetime import datetime
# creating class for real time diplay 
# class ti : 

#     def __init__ (self):
#         now = time.time()
#         formatted_time = time.strftime("%d-%m-%Y %H:%M:%S:%p", time.localtime(now))
#         self.time_var = tk.StringVar(value=formatted_time)  # Use a StringVar to hold the time
#         t_l = ttk.Label(d_opt,textvariable=self.time_var,width=30,font=("helvetica",16))
#         t_l.grid(row=0,column=0,sticky="w")
#         self.update_time()  # Call the method to start updating time

#     def update_time(self):
#         current_time = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
#         self.time_var.set(current_time)  # Update the time_var
#         d_opt.after(1000, self.update_time)  # Call update_time again after 1000 ms (1 second)   

# creating method for light theme 
def light ():
    try:
         
         # Import the tcl file
         root.tk.call("source", "utility/forest-light.tcl")
         # Set the theme with the theme_use method
         style.theme_use("forest-light")
    except Exception as error:
        tex.delete(0.0,tk.END)
        tex.insert(tk.END,str(error))

#creating method for dark theme

def dark ():
    try:
       
       # Import the tcl file
       root.tk.call("source", "utility/forest-dark.tcl")

       # Set the theme with the theme_use method
       
       style.theme_use("forest-dark")
    except Exception as error:
         tex.delete(0.0,tk.END)
         tex.insert(tk.END,str(error))
    pass
# method for switching between themes
def change ():
    if mode_var.get():
        dark()
        tex.delete(0.0,tk.END)
        tex.insert(tk.END,"true")
    else:
        #print ("false")
        light()
        tex.delete(0.0,tk.END)
        tex.insert(tk.END,"false")
  
        
# creating database table 
def create_table():
# code will create table
    con = mq.connect(host=host, user=user, password=password, database=database)
    
    my_cur = con.cursor()
    
    try:

       table = "CREATE TABLE Customers_List (Sno INT PRIMARY KEY AUTO_INCREMENT, Time TIMESTAMP NOT NULL, Name VARCHAR(20), Contact BIGINT, Qty INT, description TEXT, rate INT,Amount INT, T_Amount INT, discount INT,balance VARCHAR(10),delivery VARCHAR(10),status VARCHAR(10))"
       my_cur.execute(table)
       messagebox.showinfo("success","table created successfully")
    except mq.Error as e:
        messagebox.showinfo("error", e)
       # print (e)

# creating home screen  
def Home_screen ():
    # method for preview text widget
    def preview ():
        new = str(f"name     {str(entr_name.get())}\ncontact    {str(entr_contact.get())}\nqty     {str(entr_qty.get())}\nrate      {entr_rate.get()}\ndesc {str(entr_description.get())}\nAmount    {str(entr_amount.get())}\nT Amount     {str(entr_t_amount.get())}\nBalance   {entr_discount.get()}\nDiscount     {str(entr_balance.get())}\ndelivery   {entr_delivery.get()}\nstatus   {str(selected_status.get())} ")
        tex_1.delete(0.0,tk.END)
        tex_1.insert(tk.END,str(new))
        #print (str (new))
    # method for inserting data into table     
    def inserts():
    # sno ,time ,name ,contact ,qty ,description ,rate ,amount ,t amount ,balance ,discount ,delivery ,status 
      name_t = entr_name.get()
      contact_t = "+92"+entr_contact.get()
      qty_t = entr_qty.get()
      description_t = entr_description.get()
      rate_t = entr_rate.get()
      amount_t = entr_amount.get()
      T_amount_t= entr_t_amount.get()
      balance_t = entr_balance.get()
      discount_t =  entr_discount.get()
      delivery_t = entr_delivery.get()
      status_t = selected_status.get()
    
      try:
        ins = "INSERT INTO Customers_list(Name,Contact,Qty,description,rate,Amount,T_Amount,discount,balance,delivery,status)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        t = (name_t,contact_t,qty_t,description_t,rate_t,amount_t,T_amount_t,balance_t,discount_t,delivery_t,status_t)
        my_cur.execute(ins,t)
        con.commit()
        tex.delete(0.0,tk.END)
        tex.insert(tk.END,"Data Inserted ")
      except mq.Error as e:
        tex.delete(0.0,tk.END)
        tex.insert(tk.END,e) 
    # method for getting data from table      
    def get_data():
      try:
        # Clear the Treeview widget before inserting new data
        for item in tree_view.get_children():
            tree_view.delete(item)

        my_cur.execute("SELECT * FROM Customers_list order by Sno DESC LIMIT 100")
        my_result = my_cur.fetchall()

        for index, item in enumerate(my_result, start=1):
            # Append the index to the item identifier to make it unique
            item_id = f"item_{index}"

            tree_view.insert('', tk.END, item_id, values=item)

        tex.delete(0.0, tk.END)
        tex.insert(tk.END, "Data Gotten")
      except Exception as e:
        tex.delete(0.0, tk.END)
        tex.insert(tk.END, f"Error {e}")
    # method for generating slip with word template    
    def generate_slip(port):
        while True:
            try:
                for x in range(1):
                    my_cur.execute("SELECT * FROM Customers_list ORDER BY Sno DESC LIMIT 1")
                    last = my_cur.fetchone()
                so = s.socket(s.AF_INET, s.SOCK_STREAM)
                host = s.gethostname()
                porta = int(port)
                so.connect((host, porta))
                cm = "generate"
                data = json.dumps({"command": cm})
                so.send(data.encode("utf-8"))

                massage = so.recv(1024).decode("utf-8")
                tex.delete(0.0, tk.END)
                tex.insert(tk.END, f" NOTE: {massage} !")
                so.close()
                print(last)
                break
                
            except Exception as e:
                tex.delete(0.0, tk.END)
                tex.insert(tk.END, f"Error  {e}")

        
    #creating fram 
    Home_f = ttk.LabelFrame(root,width=1255,height=605,text="  HOME SCREEN  ")
    #Home_f.place(x=260,y=105)
    Home_f.grid(row=2,column=0,sticky="n")
    #frame fro treeview
    tree_fram = ttk.LabelFrame(Home_f,height=220,width=1245)
    tree_fram.place(x=5,y=5)
    #scrllo bar for treeview
    y_scrol = ttk.Scrollbar(tree_fram,)
    y_scrol.place(x=1230,y=0,relheight=1,relwidth=0.01)
    # creating  treeview 
    cols = ("Sno","Time","Name","Contacts","Qty","DESCRIPTION","RATE","AMOUNT","Total Amount","Discount","Balance","Delivery","Status")
    tree_view = ttk.Treeview(tree_fram,columns=cols,height=7,yscrollcommand=y_scrol.set,show=["headings"])
    #tree_view.column("",width=0)
    for name in cols:
       
       tree_view.heading(name,text=name)
    tree_view.column("Sno",width=40)         #40
    tree_view.column("Time",width=125)       #150
    tree_view.column("Name",width=140)       #140
    tree_view.column("Contacts",width=110)   #120
    tree_view.column("Qty",width=25)         #40
    tree_view.column("DESCRIPTION",width=320)#180
    tree_view.column("RATE",width=60)        #60
    tree_view.column("AMOUNT",width=60)      #80
    tree_view.column("Total Amount",width=60)#80
    tree_view.column("Discount",width=60)    #80
    tree_view.column("Balance",width=60)     #80
    tree_view.column("Delivery",width=60)    #80
    tree_view.column("Status",width=60)      #80
    
    tree_view.place(x=5,y=0)
    
    y_scrol.config(command=tree_view.yview)# tree view is completd now 
    # cut button methods
    def cut_1 ():
        entr_name.delete(0,tk.END)
    def cut_2 ():
        entr_contact.delete(0,tk.END)
    def cut_3 ():
        entr_qty.delete(0,tk.END)
    def cut_4 ():
        entr_description.delete(0,tk.END)
    def cut_5 ():
        entr_rate.delete(0,tk.END)
    def cut_6 ():
        entr_amount.delete(0,tk.END)
    def cut_7 ():
        entr_t_amount.delete(0,tk.END)
    def cut_8 ():
        entr_balance.delete(0,tk.END)
    def cut_9 ():
        entr_discount.delete(0,tk.END)
    def cut_10 ():
        entr_delivery.delete(0,tk.END)
    def cut_all ():
        cut_1()
        cut_2()
        cut_3()
        cut_4()
        cut_5()
        cut_6()
        cut_7()
        cut_8()
        cut_9()
        cut_10()
    def all ():
        inserts()
        get_data()
        cut_all()
        pass
            
    #  prewritten buttons
    but_f = ttk.Frame(Home_f,height=120,width=640)
    but_f.place(x=20,y=225)
    my_button_name = ["CHARGER","China","Pak","10A","20A","30A","40A","tubular",
                      "Ups","inverex","fronus","homage","NS ","Apollo","NRE","growatt",
                      "720w","1440w","1.2kw/kva","2.2kw","3.2kw","5.2kw","8kw","10kw",
                      "Inverter","500w","1000w","1500w","2000w","AC/DC","W/O Solar","Stabilizer"] 
    # first step declaring method for prewritten buttons
    def _1 ():
        entr_description.insert(tk.END,"Charger ")
    def _2 ():
        entr_description.insert(tk.END,"China ")
    def _3 ():
        entr_description.insert(tk.END,"Pak ")
    def _4 ():
        entr_description.insert(tk.END,"10A ")
    def _5 ():
        entr_description.insert(tk.END,"20A ")
    def _6 ():
        entr_description.insert(tk.END,"30A ")
    def _7 ():
        entr_description.insert(tk.END,"40A  ")
    def _8 ():
        entr_description.insert(tk.END,"tubular ")
    def _9 ():
        entr_description.insert(tk.END,"Ups ")
    def _10 ():
        entr_description.insert(tk.END,"inverex ")
    def _11():
        entr_description.insert(tk.END,"fronus ")
    def _12 ():
        entr_description.insert(tk.END,"homage ")
    def _13 ():
        entr_description.insert(tk.END,"NS ")
    def _14 ():
        entr_description.insert(tk.END,"Apollo ")
    def _15 ():
        entr_description.insert(tk.END,"NRE ")
    def _16 ():
        entr_description.insert(tk.END,"Growatt ")
    def _17 ():
        entr_description.insert(tk.END,"720w ")
    def _18 ():
        entr_description.insert(tk.END,"1440w ")
    def _19 ():
        entr_description.insert(tk.END,"1.2kw/1.4kva ")
    def _20 ():
        entr_description.insert(tk.END,"2.2kw ")
    def _21 ():
        entr_description.insert(tk.END,"3.2kw  ")
    def _22 ():
        entr_description.insert(tk.END,"5.2kw ")
    def _23 ():
        entr_description.insert(tk.END,"8kw ")
    def _24 ():
        entr_description.insert(tk.END,"10kw ")
    def _25 ():
        entr_description.insert(tk.END,"inverter ")
    def _26 ():
        entr_description.insert(tk.END,"500w ")
    def _27 ():
        entr_description.insert(tk.END,"1000w ")
    def _28 ():
        entr_description.insert(tk.END,"1500w ")
    def _29 ():
        entr_description.insert(tk.END,"2000w ")
    def _30 ():
        entr_description.insert(tk.END,"AC/DC Fan ")
    def _31 ():
        entr_description.insert(tk.END,"without Solar ")
    def _32 ():
        entr_description.insert(tk.END,"Stabilizer ")

    # now creating buttons
    # first row
    button_1 = tk.Button(but_f, text=my_button_name[0], bg="light grey",fg ="black" ,height=1, width=10,command=_1)
    button_1.place(x=0, y=0, width=80, height=30)
    button_2 = tk.Button(but_f, text=my_button_name[1], bg="light grey",fg ="black" , height=1, width=10,command=_2)
    button_2.place(y=0, x=80, width=80, height=30)
    button_3 = tk.Button(but_f, text=my_button_name[2], bg="light grey",fg ="black" , height=1, width=10,command=_3)
    button_3.place(y=0, x=160, width=80, height=30)
    button_4= tk.Button(but_f, text=my_button_name[3], bg="light grey",fg ="black" , height=1, width=10,command=_4)
    button_4.place(y=0, x=240, width=80, height=30)
    button_5 = tk.Button(but_f, text=my_button_name[4], bg="light grey", height=1,fg ="black" , width=10,command=_5)
    button_5.place(y=0, x=320, width=80, height=30)
    button_6 = tk.Button(but_f, text=my_button_name[5], bg="light grey", height=1,fg ="black" , width=10,command=_6)
    button_6.place(y=0, x=400, width=80, height=30)
    button_7 = tk.Button(but_f, text=my_button_name[6], bg="light grey", height=1,fg ="black" , width=10,command=_7)
    button_7.place(y=0, x=480, width=80, height=30)
    button_8 = tk.Button(but_f, text=my_button_name[7], bg="light grey", height=1,fg ="black" , width=10,command=_8)
    button_8.place(y=0, x=560, width=80, height=30)
    # second row 
    button_9 = tk.Button(but_f, text=my_button_name[8], bg="light grey", height=1, fg ="black" ,width=10,command=_9)
    button_9.place(y=30, x=0, width=80, height=30)
    button_10 = tk.Button(but_f, text=my_button_name[9], bg="light grey", height=1,fg ="black" , width=10,command=_10)
    button_10.place(x=80, y=30, width=80, height=30)
    button_11 = tk.Button(but_f, text=my_button_name[10], bg="light grey", height=1,fg ="black" , width=10,command=_11)
    button_11.place(x=160, y=30, width=80, height=30)
    button_12 = tk.Button(but_f, text=my_button_name[11], bg="light grey", height=1,fg ="black" , width=10,command=_12)
    button_12.place(x=240, y=30, width=80, height=30)
    button_13 = tk.Button(but_f, text=my_button_name[12], bg="light grey", height=1,fg ="black" , width=10,command=_13)
    button_13.place(x=320, y=30, width=80, height=30)
    button_14 = tk.Button(but_f, text=my_button_name[13], bg="light grey", height=1,fg ="black" ,  width=10,command=_14)
    button_14.place(x=400, y=30, width=80, height=30)
    button_15 = tk.Button(but_f, text=my_button_name[14], bg="light grey", height=1,fg ="black" ,  width=10,command=_15)
    button_15.place(x=480, y=30, width=80, height=30)
    button_16 = tk.Button(but_f, text=my_button_name[15], bg="light grey", height=1,fg ="black" ,  width=10,command=_16)
    button_16.place(x=560, y=30, width=80, height=30)
    #third row
    button_17 = tk.Button(but_f, text=my_button_name[16], bg="light grey", height=1,fg ="black" ,  width=10,command=_17)
    button_17.place(x=0, y=60, width=80, height=30)
    button_18 = tk.Button(but_f, text=my_button_name[17], bg="light grey", height=1,fg ="black" ,  width=10,command=_18)
    button_18.place(x=80, y=60, width=80, height=30)
    button_19 = tk.Button(but_f, text=my_button_name[18], bg="light grey", height=1,fg ="black" ,  width=10,command=_19)
    button_19.place(x=160, y=60, width=80, height=30)
    button_20 = tk.Button(but_f, text=my_button_name[19], bg="light grey", height=1,fg ="black" ,  width=10,command=_20)
    button_20.place(x=240, y=60, width=80, height=30)
    button_21 = tk.Button(but_f, text=my_button_name[20], bg="light grey", height=1,fg ="black" ,  width=10,command=_21)
    button_21.place(x=320, y=60, width=80, height=30)
    button_22 = tk.Button(but_f, text=my_button_name[21], bg="light grey", height=1,fg ="black" ,  width=10,command=_22)
    button_22.place(x=400, y=60, width=80, height=30)
    button_23 = tk.Button(but_f, text=my_button_name[22], bg="light grey", height=1,fg ="black" ,  width=10,command=_23)
    button_23.place(x=480, y=60, width=80, height=30)
    button_24 = tk.Button(but_f, text=my_button_name[23], bg="light grey", height=1,fg ="black" ,  width=10,command=_24)
    button_24.place(x=560, y=60, width=80, height=30)
    # forth row
    button_25 = tk.Button(but_f, text=my_button_name[24], bg="light grey", height=1,fg ="black" ,  width=10,command=_25)
    button_25.place(x=0, y=90, width=80, height=30)
    button_26 = tk.Button(but_f, text=my_button_name[25], bg="light grey", height=1,fg ="black" ,  width=10,command=_26)
    button_26.place(x=80, y=90, width=80, height=30)
    button_27 = tk.Button(but_f, text=my_button_name[26], bg="light grey", height=1, fg ="black" , width=10,command=_27)
    button_27.place(x=160, y=90, width=80, height=30)
    button_28 = tk.Button(but_f, text=my_button_name[27], bg="light grey", height=1,fg ="black" ,  width=10,command=_28)
    button_28.place(x=240, y=90, width=80, height=30)
    button_29 = tk.Button(but_f, text=my_button_name[28], bg="light grey", height=1,fg ="black" ,  width=10,command=_29)
    button_29.place(x=320, y=90, width=80, height=30)
    button_30 = tk.Button(but_f, text=my_button_name[29], bg="light grey", height=1, fg ="black" , width=10,command=_30)
    button_30.place(x=400, y=90, width=80, height=30)
    button_31= tk.Button(but_f, text=my_button_name[30], bg="light grey", height=1,fg ="black" ,  width=10,command=_31)
    button_31.place(x=480, y=90, width=80, height=30)
    button_32= tk.Button(but_f, text=my_button_name[31], bg="light grey", height=1,fg ="black" ,  width=10,command=_32)
    button_32.place(x=560, y=90, width=80, height=30)
   
        
    # now creating labels 
    a = tk.Label(Home_f,width=16,text="NAME",font=("helvetica",12),bg="#5fb700",fg="white",height=1)
    a.place(x=10,y=370)
    b = tk.Label(Home_f,width=16,text="CONTACT",font=("helvetica",12),bg="#5fb700",fg="white",height=1)
    b.place(x=10,y=410)
    c = tk.Label(Home_f,width=16,text="QTY",font=("helvetica",12),bg="#5fb700",fg="white",height=1)
    c.place(x=10,y=450)
    d = tk.Label(Home_f,width=16,text="DESCRIPTION",font=("helvetica",12),bg="#5fb700",fg="white",height=1)
    d.place(x=10,y=490)
    e = tk.Label(Home_f,width=16,text="RATE",font=("helvetica",12),bg="#5fb700",fg="white",height=1)
    e.place(x=10,y=530)
    f = tk.Label(Home_f,width=16,text="AMOUNT",font=("helvetica",12),bg="#5fb700",fg="white",height=1)
    f.place(x=500,y=370)
    h = tk.Label(Home_f,width=16,text="TOTAL AMOUNT",font=("helvetica",12),bg="#5fb700",fg="white",height=1)
    h.place(x=500,y=410)
    i = tk.Label(Home_f,width=16,text="BALANCE",font=("helvetica",12),bg="#5fb700",fg="white",height=1)
    i.place(x=500,y=450)
    j = tk.Label(Home_f,width=16,text="DISCOUNT",font=("helvetica",12),bg="#5fb700",fg="white",height=1)
    j.place(x=500,y=490)
    k = tk.Label(Home_f,width=16,text="DELIVERY",font=("helvetica",12),bg="#5fb700",fg="white",height=1)
    k.place(x=500,y=530)
    
    l1 = tk.Frame(Home_f,bg="grey",width=5,height=240)
    l1.place(x=485,y=355)
    l2 = tk.Frame(Home_f,bg="grey",width=5,height=380)
    l2.place(x=980,y=220)
    l3 = tk.Frame(Home_f,bg="grey",width=980,height=5)
    l3.place(x=0,y=355)
    #creating entries
    entr_name = ttk.Entry(Home_f,font=("helvetica",12))
    entr_name.place(x=205,y=365)
    entr_contact = ttk.Entry(Home_f,font=("helvetica",12))
    entr_contact.place(x=205,y=405)
    entr_qty = ttk.Entry(Home_f,font=("helvetica",12))
    entr_qty.place(x=205,y=445)
    entr_description = ttk.Entry(Home_f,font=("helvetica",12))
    entr_description.place(x=205,y=485)
    entr_rate = ttk.Entry(Home_f,font=("helvetica",12))
    entr_rate.place(x=205,y=525)
    entr_amount = ttk.Entry(Home_f,font=("helvetica",12))
    entr_amount.place(x=695,y=365)
    entr_t_amount = ttk.Entry(Home_f,font=("helvetica",12))
    entr_t_amount.place(x=695,y=405)
    entr_discount= ttk.Entry(Home_f,font=("helvetica",12))
    entr_discount.place(x=695,y=445)
    entr_balance = ttk.Entry(Home_f,font=("helvetica",12))
    entr_balance.place(x=695,y=485) 
    entr_delivery = ttk.Entry(Home_f,font=("helvetica",12))
    entr_delivery.place(x=695,y=525)
    
    #creating cut buttons for entries
    submit_but = ttk.Button(Home_f,width=10,text="SAVE",command=all)
    submit_but.place(x=670,y=265)
    generate_but = ttk.Button(Home_f,width=10,text="PRINT",command=lambda: generate_slip(port))
    generate_but.place(x=870,y=265)
    preview_but = ttk.Button(Home_f,width=10,text="CHECK",command=preview)
    preview_but.place(x=670,y=305)
    cutall_but = ttk.Button(Home_f,width=10,text="CLEAR ALL",command=cut_all)
    cutall_but.place(x=770,y=265)
    get_but = ttk.Button(Home_f,width=10,text="GET LIST",command=get_data)
    get_but.place(x=770,y=305)
    cut_1_b= tk.Button (Home_f,width=3,fg="white",height=1,bg="red",activebackground="blue",font=("helvetica",12),text="CUT",command=cut_1)
    cut_1_b.place(x=442,y=367)
    cut_2_b = tk.Button (Home_f,width=3,fg="white",height=1,bg="red",activebackground="blue",font=("helvetica",12),text="CUT",command=cut_2)
    cut_2_b.place(x=442,y=407) 
    cut_3_b = tk.Button (Home_f,width=3,fg="white",height=1,bg="red",activebackground="blue",font=("helvetica",12),text="CUT",command=cut_3)
    cut_3_b.place(x=442,y=447) 
    cut_4_b = tk.Button (Home_f,width=3,fg="white",height=1,bg="red",activebackground="blue",font=("helvetica",12),text="CUT",command=cut_4)
    cut_4_b.place(x=442,y=487) 
    cut_5_b = tk.Button (Home_f,width=3,fg="white",height=1,bg="red",activebackground="blue",font=("helvetica",12),text="CUT",command=cut_5)
    cut_5_b.place(x=442,y=527) 
    cut_6_b = tk.Button (Home_f,width=3,fg="white",height=1,bg="red",activebackground="blue",font=("helvetica",12),text="CUT",command=cut_6)
    cut_6_b.place(x=932,y=367) 
    cut_7_b = tk.Button (Home_f,width=3,fg="white",height=1,bg="red",activebackground="blue",font=("helvetica",12),text="CUT",command=cut_7)
    cut_7_b.place(x=932,y=407) 
    cut_8_b = tk.Button (Home_f,width=3,fg="white",height=1,bg="red",activebackground="blue",font=("helvetica",12),text="CUT",command=cut_9)
    cut_8_b.place(x=932,y=447) 
    cut_9_b = tk.Button (Home_f,width=3,fg="white",height=1,bg="red",activebackground="blue",font=("helvetica",12),text="CUT",command=cut_8)
    cut_9_b.place(x=932,y=487) 
    cut_10_b = tk.Button (Home_f,width=3,fg="white",height=1,bg="red",activebackground="blue",font=("helvetica",12),text="CUT",command=cut_10)
    cut_10_b.place(x=932,y=527)  
    # creating radio button
    selected_status = tk.StringVar()

    # Create radio buttons and associate them with the selected_status variable
    new_radio = ttk.Radiobutton(Home_f, text="NEW", variable=selected_status, value="new")
    change_radio = ttk.Radiobutton(Home_f, text="CHANGE", variable=selected_status, value="change")
    repair_radio = ttk.Radiobutton(Home_f, text="REPAIR", variable=selected_status, value="repairing")

    # Pack the radio buttons into the window
    new_radio.place(x=700,y=225)
    change_radio.place(x=760,y=225)
    repair_radio.place(x=850,y=225)
    # now creating text preview 
    tex_1 = tk.Text(Home_f,width=27,height=19,bg="light grey",font=("ariel",12),fg ="black"  )
    tex_1.place(x=1000,y=225)
    but_1.config(bg="light green")
    but_2.config(bg="light grey")
    but_3.config(bg="light grey")
    but_4.config(bg="light grey")
    but_5.config(bg="light grey")
    # home screen is completed
    return Home_screen


def ADD_screen ():
    def search_from (event):
        for it in tree_view_1.get_children():
            tree_view_1.delete(it)
        try:

            quer = str(entr_ser.get())
            ser = (
            "SELECT * FROM Customers_list WHERE  Time LIKE '%"
            + quer
            + "%' OR Name LIKE '%"
            + quer
            + "%' OR Contact LIKE '%"
            + quer
            + "%' OR Qty LIKE '%"
            + quer
            + "%' OR description LIKE '%"
            + quer
            + "%' OR rate LIKE '%"
            + quer
            + "%' OR Amount LIKE '%"
            + quer
            + "%' OR T_Amount LIKE '%"
            + quer
            + "%' OR discount LIKE '%"
            + quer
            + "%' OR balance LIKE '%"
            + quer
            + "%' OR delivery LIKE '%"
            + quer
            + "%'ORDER BY Sno DESC"
        )
            my_cur.execute(ser)
            data = my_cur.fetchall()
            for index,item in enumerate(data,start=1) :
                item_id = f"item_{index}"
                tree_view_1.insert('', tk.END, item_id, values=item)
            tex.delete(0.0,tk.END)
            tex.insert(tk.END," NOTE:DATA brought successfully !")
        except Exception as e:
            tex.delete(0.0, tk.END)
            tex.insert(tk.END, f"Error {e}")
    def search_sno (event):
        for ite in tree_view_1.get_children():
            tree_view_1.delete(ite)
        try:
            queri = entr_ser_sno.get()
            queri_1= str(queri)
            seri = ("SELECT * FROM Customers_list WHERE Sno = %s ORDER BY Sno ")
            my_cur.execute(seri,( queri_1,))
            got_sno = my_cur.fetchall()
            for index,item in enumerate(got_sno,start=1) :
                item_id = f"item_{index}"
                tree_view_1.insert('', tk.END, item_id, values=item)

            tex.delete(0.0,tk.END)
            tex.insert(tk.END,f" NOTE:DATA brought successfully !{queri}")
        except Exception as e:
            tex.delete(0.0, tk.END)
            tex.insert(tk.END, f"Error {e}")
    def search_by_amount(event):
        for ite in tree_view_1.get_children():
            tree_view_1.delete(ite)
        try:
            queri = str(entr_amountt.get())
            ser = "SELECT * FROM Customers_list WHERE T_Amount = %s ORDER BY Sno DESC"
            my_cur.execute(ser,(queri,))
            got_amount = my_cur.fetchall()
            for index,item in enumerate(got_amount,start=1) :
                item_id = f"item_{index}"
                tree_view_1.insert('', tk.END, item_id, values=item)

            tex.delete(0.0,tk.END)
            tex.insert(tk.END,f" NOTE:DATA brought successfully !{queri}")
        except Exception as e:
            tex.delete(0.0, tk.END)
            tex.insert(tk.END, f"Error {e}")

    def search_by_date(event):
    # Retrieve date components from the entry widgets
        day = entr_ser_date.get()
        month = entr_ser_mon.get()
        year = entr_ser_yr.get()

    # Construct a date string in the format YYYY-MM-DD
        date_string = f"{year}-{month.zfill(2)}-{day.zfill(2)}"

    # Clear the treeview widget
        for item in tree_view_1.get_children():
            tree_view_1.delete(item)

        try:
        # Create an SQL query to search by the constructed date string
            query = "SELECT * FROM Customers_list WHERE Time LIKE %s ORDER BY Sno DESC"
            my_cur.execute(query, ('%' + date_string + '%',))
            data = my_cur.fetchall()

            for index, item in enumerate(data, start=1):
                item_id = f"item_{index}"
                tree_view_1.insert('', tk.END, item_id, values=item)

            tex.delete(0.0, tk.END)
            tex.insert(tk.END, "NOTE:DATA brought successfully!")
        except Exception as e:
            tex.delete(0.0, tk.END)
            tex.insert(tk.END, f"Error: {e}")
    
    
    def generate_slip_rendom(port):
        while True:
            so = s.socket(s.AF_INET, s.SOCK_STREAM)
            host = s.gethostname()
            porta = int(port)
            so.connect((host, porta))   
            item_sno = str(entr_print.get())
            data = json.dumps({"command":"serial","sno":item_sno,}).encode('utf-8')
            so.send(data)
        
            
            massage =so.recv(1024).decode('utf-8')
            tex.delete(0.0,tk.END)
            tex.insert(tk.END, f" NOTE: {massage} !")
            so.close()
            print("this is serial no ",item_sno)
            break
             
    add_f = ttk.LabelFrame(root,width=1255,height=605,text="  SEARCH SCREEN  ")
    add_f.grid(row=2,column=0,sticky="n")
    #frame fro treeview
    tree_fram_1 = ttk.LabelFrame(add_f,height=285,width=1245)
    tree_fram_1.place(x=5,y=5)
    #scrllo bar for treeview
    y_scrol = ttk.Scrollbar(tree_fram_1,)
    y_scrol.place(x=1230,y=0,relheight=1,relwidth=0.01)
    # creating  treeview 
    cols = ("Sno","Time","Name","Contacts","Qty","DESCRIPTION","RATE","AMOUNT","Total Amount","Discount","Balance","Delivery","Status")
    tree_view_1 = ttk.Treeview(tree_fram_1,columns=cols,height=10,yscrollcommand=y_scrol.set,show=["headings"])
    #tree_view.column("",width=0)
    for name in cols:
       
       tree_view_1.heading(name,text=name)
    tree_view_1.column("Sno",width=40)
    tree_view_1.column("Time",width=125)
    tree_view_1.column("Name",width=140)
    tree_view_1.column("Contacts",width=110)
    tree_view_1.column("Qty",width=25)
    tree_view_1.column("DESCRIPTION",width=320)
    tree_view_1.column("RATE",width=60)
    tree_view_1.column("AMOUNT",width=60)
    tree_view_1.column("Total Amount",width=60)
    tree_view_1.column("Discount",width=60)
    tree_view_1.column("Balance",width=60)
    tree_view_1.column("Delivery",width=60)
    tree_view_1.column("Status",width=60)
    
    tree_view_1.place(x=5,y=0)
    
    y_scrol.config(command=tree_view_1.yview)# tree view is completd now 
    # creating tk label 
    l_1 = tk.Label(add_f,height=1,font=("ariel",16),text=" S E A R C H   B Y   A S   Y O U   W A N T ",bg="light grey",fg="black")
    l_1.place(x=0,y=295,relwidth=1)
    # creating search button 
    ser_but = ttk.Button(add_f,width=80,text=" C L I C K   M E   F O R   S E A R C H ",)
    ser_but.place(x=50 ,y=340)
     # creating search sno 
    #sno = entr_sno_print.get() 


    # creating search date 
    ser_but_date = ttk.Button(add_f,width=80,text=" C L I C K   M E   F O R   S E A R C H   D A T E ",)
    ser_but_date.place(x=640 ,y=460)
    
    # creating search date 
    ser_but_amount = ttk.Button(add_f,width=80,text=" C L I C K   M E   F O R   S E A R C H   A M O U N T ")
    ser_but_amount.place(x=640 ,y=340)

    # creating search entry
    entr_ser = ttk.Entry(add_f,width=47,font=("helvetica",16))
    entr_ser.place(x=50,y=400)
    entr_ser.bind("<Return>",search_from)

    # creating search entry amount5
    entr_amountt = ttk.Entry(add_f,width=47,font=("helvetica",16))
    entr_amountt.place(x=640,y=400)
    entr_amountt.bind("<Return>",search_by_amount)
    # creating search enrty sno
    entr_ser_sno = ttk.Entry(add_f,width=20,font=("helvetica",16))
    entr_ser_sno.place(x=50,y=520)
    entr_ser_sno.bind("<Return>",search_sno)
    #creating search print
    entr_print =ttk.Entry(add_f,width=20,font=("helvetica",16))
    entr_print.place(x=320,y=520)
        
    # creatin search enrty date 
    d = ttk.Label(add_f,text="Day 00",font=("calibri light",20)).place(x=650,y=520)
    m = ttk.Label(add_f,text="Mon 00",font=("calibri light",20)).place(x=840,y=520)
    y = ttk.Label(add_f,text="Year 00",font=("calibri light",20)).place(x=1020,y=520)
    entr_ser_date = ttk.Entry(add_f,width=6,font=("helvetica",16))
    entr_ser_date.place(x=740,y=520)
    entr_ser_date.bind("<Return>",search_by_date)
    entr_ser_mon = ttk.Entry(add_f,width=6,font=("helvetica",16))
    entr_ser_mon.place(x=930,y=520)
    entr_ser_mon.bind("<Return>",search_by_date)
    entr_ser_yr = ttk.Entry(add_f,width=6,font=("helvetica",16))
    entr_ser_yr.place(x=1110,y=520)
    a = ttk.Label(add_f,)
    ser_but_sno = ttk.Button(add_f,width=80,text=" C L I C K   M E   F O R   P R I N T   S N O",command=lambda:generate_slip_rendom(port))
    ser_but_sno.place(x=50 ,y=460)
    but_1.config(bg="light grey")
    but_2.config(bg="light green")
    but_3.config(bg="light grey")
    but_4.config(bg="light grey")
    but_5.config(bg="light grey")
    return ADD_screen


def History_screen ():
        # method for preview text widget
    def preview ():
        new = str(f"name     {str(entr_name.get())}\ncontact    {str(entr_contact.get())}\nqty     {str(entr_qty.get())}\nrate      {entr_rate.get()}\ndesc {str(entr_description.get())}\nAmount    {str(entr_amount.get())}\nT Amount     {str(entr_t_amount.get())}\nBalance   {entr_discount.get()}\nDiscount     {str(entr_balance.get())}\ndelivery   {entr_delivery.get()}\nstatus   {str(selected_status.get())} ")
        tex_1.delete(0.0,tk.END)
        tex_1.insert(tk.END,str(new))
        #print (str (new))
    # method for inserting data into table     
    def inserts():
    # sno ,time ,name ,contact ,qty ,description ,rate ,amount ,t amount ,balance ,discount ,delivery ,status 
      name_t = entr_name.get()
      contact_t = "+92"+entr_contact.get()
      qty_t = entr_qty.get()
      description_t = entr_description.get()
      rate_t = entr_rate.get()
      amount_t = entr_amount.get()
      T_amount_t= entr_t_amount.get()
      balance_t = entr_balance.get()
      discount_t =  entr_discount.get()
      delivery_t = entr_delivery.get()
      status_t = selected_status.get()
    
      try:
        ins = "INSERT INTO Customers_list(Name,Contact,Qty,description,rate,Amount,T_Amount,discount,balance,delivery,status)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        t = (name_t,contact_t,qty_t,description_t,rate_t,amount_t,T_amount_t,balance_t,discount_t,delivery_t,status_t)
        my_cur.execute(ins,t)
        con.commit()
        tex.delete(0.0,tk.END)
        tex.insert(tk.END,"Data Inserted ")
      except mq.Error as e:
        tex.delete(0.0,tk.END)
        tex.insert(tk.END,e) 
    # method for getting data from table      
    def get_data():
      try:
        # Clear the Treeview widget before inserting new data
        for item in tree_view.get_children():
            tree_view.delete(item)

        my_cur.execute("SELECT * FROM Customers_list order by Sno DESC LIMIT 100")
        my_result = my_cur.fetchall()

        for index, item in enumerate(my_result, start=1):
            # Append the index to the item identifier to make it unique
            item_id = f"item_{index}"

            tree_view.insert('', tk.END, item_id, values=item)

        tex.delete(0.0, tk.END)
        tex.insert(tk.END, "Data Gotten")
      except Exception as e:
        tex.delete(0.0, tk.END)
        tex.insert(tk.END, f"Error {e}")
    # method for generating slip with word template    
    def generate_slip(port):
        while True:
            try:
                for x in range(1):
                    my_cur.execute("SELECT * FROM Customers_list ORDER BY Sno DESC LIMIT 1")
                    last = my_cur.fetchone()
                so = s.socket(s.AF_INET, s.SOCK_STREAM)
                host = s.gethostname()
                porta = int(port)
                so.connect((host, porta))
                cm = "generate"
                data = json.dumps({"command": cm})
                so.send(data.encode("utf-8"))

                massage = so.recv(1024).decode("utf-8")
                tex.delete(0.0, tk.END)
                tex.insert(tk.END, f" NOTE: {massage} !")
                so.close()
                print(last)
                break
                
            except Exception as e:
                tex.delete(0.0, tk.END)
                tex.insert(tk.END, f"Error  {e}")
        #frame fro treeview
    tok_f = ttk.LabelFrame(root,width=1255,height=605,text="  TOKEN SCREEN  ")
    #Home_f.place(x=260,y=105)
    tok_f.grid(row=2,column=0,sticky="n")    
    tree_fram = ttk.LabelFrame(tok_f,height=220,width=1245)
    tree_fram.place(x=5,y=5)
    #scrllo bar for treeview
    y_scrol = ttk.Scrollbar(tree_fram,)
    y_scrol.place(x=1230,y=0,relheight=1,relwidth=0.01)
    # creating  treeview 
    cols = ("Sno","Time","Name","Contacts","Qty","DESCRIPTION","RATE","AMOUNT","Total Amount","Discount","Balance","Delivery","Status")
    tree_view = ttk.Treeview(tree_fram,columns=cols,height=7,yscrollcommand=y_scrol.set,show=["headings"])
    #tree_view.column("",width=0)
    for name in cols:
       
       tree_view.heading(name,text=name)
    tree_view.column("Sno",width=40)         #40
    tree_view.column("Time",width=125)       #150
    tree_view.column("Name",width=140)       #140
    tree_view.column("Contacts",width=110)   #120
    tree_view.column("Qty",width=25)         #40
    tree_view.column("DESCRIPTION",width=320)#180
    tree_view.column("RATE",width=60)        #60
    tree_view.column("AMOUNT",width=60)      #80
    tree_view.column("Total Amount",width=60)#80
    tree_view.column("Discount",width=60)    #80
    tree_view.column("Balance",width=60)     #80
    tree_view.column("Delivery",width=60)    #80
    tree_view.column("Status",width=60)      #80
    
    tree_view.place(x=5,y=0)
    
    y_scrol.config(command=tree_view.yview)# tree view is completd now    
        # now creating labels 
    a = tk.Label(tok_f,width=16,text="NAME",font=("helvetica",12),bg="#5fb700",fg="white",height=1)
    a.place(x=10,y=370)
    b = tk.Label(tok_f,width=16,text="CONTACT",font=("helvetica",12),bg="#5fb700",fg="white",height=1)
    b.place(x=10,y=410)
    c = tk.Label(tok_f,width=16,text="QTY",font=("helvetica",12),bg="#5fb700",fg="white",height=1)
    c.place(x=10,y=450)
    d = tk.Label(tok_f,width=16,text="DESCRIPTION",font=("helvetica",12),bg="#5fb700",fg="white",height=1)
    d.place(x=10,y=490)
    e = tk.Label(tok_f,width=16,text="RATE",font=("helvetica",12),bg="#5fb700",fg="white",height=1)
    e.place(x=10,y=530)
    f = tk.Label(tok_f,width=16,text="AMOUNT",font=("helvetica",12),bg="#5fb700",fg="white",height=1)
    f.place(x=500,y=370)
    h = tk.Label(tok_f,width=16,text="TOTAL AMOUNT",font=("helvetica",12),bg="#5fb700",fg="white",height=1)
    h.place(x=500,y=410)
    i = tk.Label(tok_f,width=16,text="BALANCE",font=("helvetica",12),bg="#5fb700",fg="white",height=1)
    i.place(x=500,y=450)
    j = tk.Label(tok_f,width=16,text="DISCOUNT",font=("helvetica",12),bg="#5fb700",fg="white",height=1)
    j.place(x=500,y=490)
    k = tk.Label(tok_f,width=16,text="DELIVERY",font=("helvetica",12),bg="#5fb700",fg="white",height=1)
    k.place(x=500,y=530)
    
    l1 = tk.Frame(tok_f,bg="grey",width=5,height=240)
    l1.place(x=485,y=355)
    l2 = tk.Frame(tok_f,bg="grey",width=5,height=380)
    l2.place(x=980,y=220)
    l3 = tk.Frame(tok_f,bg="grey",width=980,height=5)
    l3.place(x=0,y=355)
    #creating entries
    entr_name = ttk.Entry(tok_f,font=("helvetica",12))
    entr_name.place(x=205,y=365)
    entr_contact = ttk.Entry(tok_f,font=("helvetica",12))
    entr_contact.place(x=205,y=405)
    entr_qty = ttk.Entry(tok_f,font=("helvetica",12))
    entr_qty.place(x=205,y=445)
    entr_description = ttk.Entry(tok_f,font=("helvetica",12))
    entr_description.place(x=205,y=485)
    entr_rate = ttk.Entry(tok_f,font=("helvetica",12))
    entr_rate.place(x=205,y=525)
    entr_amount = ttk.Entry(tok_f,font=("helvetica",12))
    entr_amount.place(x=695,y=365)
    entr_t_amount = ttk.Entry(tok_f,font=("helvetica",12))
    entr_t_amount.place(x=695,y=405)
    entr_discount= ttk.Entry(tok_f,font=("helvetica",12))
    entr_discount.place(x=695,y=445)
    entr_balance = ttk.Entry(tok_f,font=("helvetica",12))
    entr_balance.place(x=695,y=485) 
    entr_delivery = ttk.Entry(tok_f,font=("helvetica",12))
    entr_delivery.place(x=695,y=525)
    
    #creating cut buttons for entries
    submit_but = ttk.Button(tok_f,width=10,text="SAVE",command=all)
    submit_but.place(x=670,y=265)
    generate_but = ttk.Button(tok_f,width=10,text="PRINT",command=lambda: generate_slip(port))
    generate_but.place(x=870,y=265)
    preview_but = ttk.Button(tok_f,width=10,text="CHECK",command=preview)
    preview_but.place(x=670,y=305)
   # cutall_but = ttk.Button(Home_f,width=10,text="CLEAR ALL",command=cut_all)
   # cutall_but.place(x=770,y=265)
    get_but = ttk.Button(tok_f,width=10,text="GET LIST",command=get_data)
    get_but.place(x=770,y=305)
    # cut_1_b= tk.Button (Home_f,width=3,fg="white",height=1,bg="red",activebackground="blue",font=("helvetica",12),text="CUT",command=cut_1)
    # cut_1_b.place(x=442,y=367)
    # cut_2_b = tk.Button (Home_f,width=3,fg="white",height=1,bg="red",activebackground="blue",font=("helvetica",12),text="CUT",command=cut_2)
    # cut_2_b.place(x=442,y=407) 
    # cut_3_b = tk.Button (Home_f,width=3,fg="white",height=1,bg="red",activebackground="blue",font=("helvetica",12),text="CUT",command=cut_3)
    # cut_3_b.place(x=442,y=447) 
    # cut_4_b = tk.Button (Home_f,width=3,fg="white",height=1,bg="red",activebackground="blue",font=("helvetica",12),text="CUT",command=cut_4)
    # cut_4_b.place(x=442,y=487) 
    # cut_5_b = tk.Button (Home_f,width=3,fg="white",height=1,bg="red",activebackground="blue",font=("helvetica",12),text="CUT",command=cut_5)
    # cut_5_b.place(x=442,y=527) 
    # cut_6_b = tk.Button (Home_f,width=3,fg="white",height=1,bg="red",activebackground="blue",font=("helvetica",12),text="CUT",command=cut_6)
    # cut_6_b.place(x=932,y=367) 
    # cut_7_b = tk.Button (Home_f,width=3,fg="white",height=1,bg="red",activebackground="blue",font=("helvetica",12),text="CUT",command=cut_7)
    # cut_7_b.place(x=932,y=407) 
    # cut_8_b = tk.Button (Home_f,width=3,fg="white",height=1,bg="red",activebackground="blue",font=("helvetica",12),text="CUT",command=cut_9)
    # cut_8_b.place(x=932,y=447) 
    # cut_9_b = tk.Button (Home_f,width=3,fg="white",height=1,bg="red",activebackground="blue",font=("helvetica",12),text="CUT",command=cut_8)
    # cut_9_b.place(x=932,y=487) 
    # cut_10_b = tk.Button (Home_f,width=3,fg="white",height=1,bg="red",activebackground="blue",font=("helvetica",12),text="CUT",command=cut_10)
    # cut_10_b.place(x=932,y=527)  
    # creating radio button
    selected_status = tk.StringVar()

    # Create radio buttons and associate them with the selected_status variable
    new_radio = ttk.Radiobutton(tok_f, text="NEW", variable=selected_status, value="new")
    change_radio = ttk.Radiobutton(tok_f, text="CHANGE", variable=selected_status, value="change")
    repair_radio = ttk.Radiobutton(tok_f, text="REPAIR", variable=selected_status, value="repairing")

    # Pack the radio buttons into the window
    new_radio.place(x=700,y=225)
    change_radio.place(x=760,y=225)
    repair_radio.place(x=850,y=225)
    # now creating text preview 
    tex_1 = tk.Text(tok_f,width=27,height=19,bg="light grey",font=("ariel",12),fg ="black"  )
    tex_1.place(x=1000,y=225)
    but_1.config(bg="light green")
    but_2.config(bg="light grey")
    but_3.config(bg="light grey")
    but_4.config(bg="light grey")
    but_5.config(bg="light grey")         

    # his_f = ttk.LabelFrame(root,width=1255,height=605,text="  TOKEN SCREEN  ")
    # his_f.grid(row=2,column=0,sticky="n")
    but_1.config(bg="light grey")
    but_2.config(bg="light grey")
    but_3.config(bg="light green")
    but_4.config(bg="light grey")
    but_5.config(bg="light grey")
    return History_screen


def record_screen ():
    rec_f = ttk.LabelFrame(root,width=1255,height=605,text="  RECORD SCREEN  ")
    rec_f.grid(row=2,column=0,sticky="n")
    but_1.config(bg="light grey")
    but_2.config(bg="light grey")
    but_3.config(bg="light grey")
    but_4.config(bg="light green")
    but_5.config(bg="light grey")
    return record_screen


def setting_screen ():
    set_f = ttk.LabelFrame(root,width=1255,height=605,text="  SETTING SCREEN  ")
    set_f.grid(row=2,column=0,sticky="n")
    mode = ttk.Checkbutton(set_f,text=" MODE SELECTION ",variable=mode_var,style="Switch",command=change)
    mode.place(x=10,y=100)
    cre = ttk.Button(set_f,width=10,command=create_table,text="create table")
    cre.place(x=10,y=140)
    but_1.config(bg="light grey")
    but_2.config(bg="light grey")
    but_3.config(bg="light grey")
    but_4.config(bg="light grey")
    but_5.config(bg="light green")
    return setting_screen

#creating window 

root = tk.Tk()
root.title("Management Software for WAHEEDSONS ENGINEERING")
#root.winfo_screenwidth()
#root.winfo_screenheight()
#"1580x820"
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
#root.option_add("*tearOff", False) # This is always a good idea
root.iconbitmap("utility/WSE LOGO.ico.ico")
#root.wm_attributes("-alpha", 0.85)

# Create a style
style = ttk.Style(root)
# now creating application
# creating global variable 
mode_var = tk.BooleanVar(value=True)
# Replace these with your actual database credentials
# host = "localhost"
# user = "root"
# password = "admin"
# db_name = "wasaf"
with open("utility/wse_config.json", "r") as f:
    data = json.load(f)
host = data["database"]["host"] 
user = data["database"]["user"]
database = data["database"]["database"]
password = data["database"]["password"]
port = data["database"]["soc_port"]

try:

# connecting with database if database exist
    con = mq.connect(host=host, user=user, password=password, database=database)
    my_cur = con.cursor()
except mq.Error as e:
    print(e)
for x in range (20):
    root.rowconfigure(x,weight=1)  
      
for y in range (10):
    root.columnconfigure(y,weight=1)
# # main name
# img = tk.PhotoImage(file="utility/WSE Name bg.png")
# wse = ttk.Label(root,image=img)
# wse.grid(row=0,sticky="n")
#option frame 
opt = ttk.LabelFrame(root,text="   MENU   ",width=root.winfo_screenwidth()//.6,height=20 )
opt.grid(row=0,column=0,sticky="n")
for z in range(12):
    opt.columnconfigure(z,weight=1)
# now creating frame for message display 
dis = ttk.LabelFrame(opt,width=230,height=390,text="")
dis.grid(row=0,column=12)
tex = tk.Text(dis,bg="light green",width=35,height=1,fg="black",font=("calibiri",10) )
tex.pack(side=tk.LEFT,fill=tk.BOTH,padx=5,pady=5)

#now creating extra fr 
dis_1 = ttk.LabelFrame(opt,width=228,height=50,text="Created By ...")
dis_1.grid(row=0,column=10)
name = ttk.Label(dis_1,text="WAHEEDSONS ENGINEERING").pack()
#time and date frame
# d_opt = ttk.LabelFrame(root,text="   DATE TIME  ",width=12,height=97)
# d_opt.grid (row=0,column=1,sticky="nw")

# buttons in frame 
but_1 = tk.Button(opt,text="HOME SCREEN ",width=20,bg = "light grey",command=Home_screen)
but_1.grid(row=0,column=0)

but_2 = tk.Button(opt,text="SEARCH SCREEN ",width=20,bg = "light grey",command=ADD_screen)
but_2.grid(row=0,column=2)

but_3 = tk.Button(opt,text="TOKEN SCREEN ",width=20,bg = "light grey",command=History_screen)
but_3.grid(row=0,column=4)

but_4 = tk.Button(opt,text="RECORD SCREEN ",width=20,bg = "light grey",command=record_screen)
but_4.grid(row=0,column=6)

but_5 = tk.Button(opt,text="SETTING SCREEN ",width=20,bg = "light grey",command=setting_screen)
but_5.grid(row=0,column=8)

#ti()
Home_screen()
light()
root.mainloop()
