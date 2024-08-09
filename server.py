import socket
import json
from docxtpl import DocxTemplate
import os
import pymysql as mq 
import win32api
import win32print
import time as tm



with open("utility/server_config.json", "r") as file:
    data = json.load(file)
path =data ["output"]["path"]
host = data["database"]["host"]
user = data["database"]["user"]
database = data["database"]["database"]
password = data["database"]["password"]
portr = data["database"]["soc_port"]
printer = data ["printer"]["ip"]
label_printer = data["label_printer"]["ip"]
path = data["output"]["path"]
port =int(portr)
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hosta = socket.gethostname()
soc.bind((hosta, port))
soc.listen(10)
# with open("wse_config.json", "r") as f:
#     data = json.load(f)
# hostc = data["database"]["host"] 
# user = data["database"]["user"]
# database = data["database"]["database"]
# password = data["database"]["password"]
# port = data["database"]["port"]



try:

    while True:
        print(f"Server is Listening to port {port} ................")
        client_socket, addr = soc.accept()
        data = client_socket.recv(1024).decode("utf-8")
        client_data = json.loads(data)
        try:
            con = mq.connect(host=host, user=user, password=password, database=database)
            my_cur = con.cursor()
        except mq.Error as e:
            print(e)

        if client_data.get("command", "") == "generate":
            my_cur.execute("SELECT * FROM Customers_list ORDER BY Sno DESC LIMIT 1")
            last = my_cur.fetchone()
            
            if last:
                sno, time, name, contact, qty, description, rate, amount, tamount, discount, balance, delivery, status = last
                #os.chdir("D:/pythonProject/soft")
                doc = DocxTemplate("utility/WSE invoice.docx")
                doc.render({"sno": sno, "time_now": time, "name": name, "contact": contact, "qt": qty,
                             "description": description, "r": rate, "amt": amount, "t_amt": tamount, "d_amt": discount,
                             "b_amt": balance, "d_time": delivery, "status": status})

                b = str(name)
                c = str(sno)

                #"C:/Users/wasaf/OneDrive/Desktop/WSE_INVOICES.docx/new_invoice '" + b + "' '" + c + "' .docx"
                doc.save(f"{path}/new_invoice '{b}' '{c}'.docx")
                #file = "C:/Users/wasaf/OneDrive/Desktop/WSE_INVOICES.docx/new_invoice '" + b + "' '" + c + "' .docx"
                file = f"{path}/new_invoice '{b}' '{c}'.docx"
                try :

                    if os.path.exists(file):
                        win32api.ShellExecute(0,"print",file,printer,".",win32print.OpenPrinter(printer))
                        mes = f" invoice generated successfully name {b} sno {c}"
                        client_socket.send(mes.encode("utf-8"))
                        print (f" last generated invoice name {0},sno {1}").format(b,c)
                    else :
                    
                        er = "error occured while printng"
                        client_socket.send(er.encode("utf-8"))
                except Exception as e :
                    er = str(e)
                    client_socket.send(er.encode("utf-8"))     
            else:
                mes = "No new records found in the database."

                client_socket.send(mes.encode("utf-8"))
    #this section is for printing serial vise            
        elif client_data.get("command", "") == "serial":
    #    else:
            print("Received data from client:", client_data)
            sno = client_data.get("sno","")
            sn_o = str(sno)
            my_cur.execute(f"Select * FROM Customers_list WHERE Sno ={sn_o}")
            slip = my_cur.fetchone()
            if slip:
                sno, time, name, contact, qty, description, rate, amount, tamount, discount, balance, delivery, status = slip
                doc = DocxTemplate("utility/WSE invoice.docx")
                doc.render({"sno": sno, "time_now": time, "name": name, "contact": contact, "qt": qty,
                             "description": description, "r": rate, "amt": amount, "t_amt": tamount, "d_amt": discount,
                             "b_amt": balance, "d_time": delivery, "status": status})
                b = str(name)
                c = str(sno)

                #"C:/Users/wasaf/OneDrive/Desktop/WSE_INVOICES.docx/new_invoice '" + b + "' '" + c + "' .docx"
                doc.save(f"{path}/new_invoice '{b}' '{c}'.docx")
                #file = "C:/Users/wasaf/OneDrive/Desktop/WSE_INVOICES.docx/new_invoice '" + b + "' '" + c + "' .docx"
                file = f"{path}/new_invoice '{b}' '{c}'.docx"
                try :

                    if os.path.exists(file):
                        win32api.ShellExecute(0,"print",file,printer,".",win32print.OpenPrinter(printer))
                        mes = f" invoice generated successfully name {b} sno {c}"
                        client_socket.send(mes.encode("utf-8"))
                        print (f"last invoice generated name {b} sno {c}")
                    else :
                    
                        er = "error occured while printng"
                        client_socket.send(er.encode("utf-8"))
                        print(er)
                except Exception as e :
                    er = str(e)
                    client_socket.send(er.encode("utf-8"))  
                    print(er)   
            else:
                mes = "No new records found in the database."

                client_socket.send(mes.encode("utf-8"))
                print(mes)
            mes = "Invalid command. Please use 'sno' command."
            client_socket.send(mes.encode("utf-8"))
            print(mes)
# this section is for token printing 
        elif  client_data.get("command", "") == "token":

            print("Received data from client:", client_data)
            sno = client_data.get("sno","")
            sn_o = str(sno)
            my_cur.execute(f"Select * FROM Token_list WHERE Sno ={sn_o}")
            token = my_cur.fetchone()
            if token:
                sno, time, name, contact, qty, description= token
                doc = DocxTemplate("utility/token.docx")
                doc.render({"sno": f"TK00{sno}", "time_now": time, "name": name, "contact": contact, "qt": qty,
                             "description": description,})
                b = str(name)
                c = str(sno)

                #"C:/Users/wasaf/OneDrive/Desktop/WSE_INVOICES.docx/new_invoice '" + b + "' '" + c + "' .docx"
                doc.save(f"{path}/new_token '{b}' '{c}'.docx")
                #file = "C:/Users/wasaf/OneDrive/Desktop/WSE_INVOICES.docx/new_invoice '" + b + "' '" + c + "' .docx"
                file = f"{path}/new_token '{b}' '{c}'.docx"
                try :

                    if os.path.exists(file):
                        win32api.ShellExecute(0,"print",file,printer,".",win32print.OpenPrinter(printer))
                        mes = f" token generated successfully name {b} sno {c}"
                        client_socket.send(mes.encode("utf-8"))
                        print (f"token generated name {b} sno {c}")
                    else :
                    
                        er = "error occured while printng"
                        client_socket.send(er.encode("utf-8"))
                        print(er)
                except Exception as e :
                    er = str(e)
                    client_socket.send(er.encode("utf-8"))  
                    print(er)   
            else:
                mes = "No new records found in the database."

                client_socket.send(mes.encode("utf-8"))
                print(mes)
            mes = "Invalid command. Please use 'sno' command."
            client_socket.send(mes.encode("utf-8"))
            print(mes)  
    # this section isfor label printing         
        else:
            print("Received data from client:", client_data)
            sno = client_data.get("sno","")
            sn_o = str(sno)
            my_cur.execute(f"Select * FROM Customers_list WHERE Sno ={sn_o}")
            slip = my_cur.fetchone()
            current_time = tm.strftime("%Y-%m-%d T%H:%M")
            if slip:
                sno, time, name, contact, qty, description, rate, amount, tamount, discount, balance, delivery, status = slip
                doc = DocxTemplate("utility/label.docx")
                doc.render({"sno": f"INV0{sno}", "time_now": current_time, "name": name, "status": status})
                b = str(name)
                c = str(sno)

                #"C:/Users/wasaf/OneDrive/Desktop/WSE_INVOICES.docx/new_invoice '" + b + "' '" + c + "' .docx"
                doc.save(f"{path}/new_invoice '{b}' '{c}'.docx")
                #file = "C:/Users/wasaf/OneDrive/Desktop/WSE_INVOICES.docx/new_invoice '" + b + "' '" + c + "' .docx"
                file = f"{path}/new_invoice '{b}' '{c}'.docx"
                try :

                    if os.path.exists(file):
                        win32api.ShellExecute(0,"print",file,printer,".",win32print.OpenPrinter(label_printer))
                        mes = f" invoice generated successfully name {b} sno {c}"
                        client_socket.send(mes.encode("utf-8"))
                        print (f"last invoice generated name {b} sno {c}")
                    else :
                    
                        er = "error occured while printng"
                        client_socket.send(er.encode("utf-8"))
                        print(er)
                except Exception as e :
                    er = str(e)
                    client_socket.send(er.encode("utf-8"))  
                    print(er)   
            else:
                mes = "No new records found in the database."

                client_socket.send(mes.encode("utf-8"))
                print(mes)
            mes = "Invalid command. Please use 'sno' command."
            client_socket.send(mes.encode("utf-8"))
            print(mes   )       
        client_socket.close()
except Exception as e:
    client_socket.send(e.encode("utf-8"))
    print(e)

soc.close()
