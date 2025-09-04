import tkinter as tk
from tkinter import *
from tkinter import ttk,messagebox
from PIL import ImageTk, Image
import mysql.connector
import subprocess

root = tk.Tk()
root.title("Garbage Truck Management")
root.iconbitmap("gtmproject//assets//GTM.ico")
root.geometry("600x450+200+90")
root.configure(bg="#8DB6CD")

#mysqlconnection
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database=""
)
#mainframe
mainframe = tk.Frame(root)
#loginframe
loginframe = tk.Frame(root)
#loginfunction
def login(select_role):
    username = entryuser.get()
    password = entrypass.get()
    conn = connect_db()
    cursor = conn.cursor()
    if select_role == "ADMIN":
        cursor.execute("SELECT * FROM admin WHERE ad_name = %s AND pwd = %s", (username, password))
        ad = cursor.fetchone()
        if ad:
            messagebox.showinfo("Login Success","Welcome, Admin!")
            loginframe.destroy()
            root.destroy()
            import admin
        else:
            messagebox.showerror("Login Failed", "Invalid Admin credentials")
    elif select_role == "USER":
        cursor.execute("SELECT * FROM user WHERE uname = %s AND pwd = %s", (username, password))
        userv = cursor.fetchone()
        f=open("cred.txt","w")
        f.write(userv[0])
        f.close()
        if userv:
            messagebox.showinfo("Login Success","Welcome, User!")
            loginframe.destroy()
            root.destroy()
            import user
        else:
            messagebox.showerror("Login Failed", "Invalid User credentials")
    conn.close()
def back_func():
    loginframe.destroy()
    root.destroy()
    import gtm
#loginpage
def show_login(select_role):
    #clearmainframe
    mainframe.destroy()
    #imageforloginpage
    global bgimg
    pht = Image.open("gtmproject//assets//b2.jpg")
    bgimg = pht.resize((643, 450))
    bgimg = ImageTk.PhotoImage(bgimg)
    imglabel = tk.Canvas(loginframe, width=600, height=450,bg="white")
    imglabel.create_image(0, 0, anchor='nw', image=bgimg)
    imglabel.create_text(310, 100, text="LOG IN", font=("Comic Sans MS", 14, "bold"), fill="black")
    imglabel.pack()
    #backbtn
    back_btn = tk.Button(loginframe, text="Back",bg="#737373",
    font=("Arial", 12),command=back_func)
    back_btn.place(relx=0.3, rely=0.5)
    #usernamelabel&entry
    global entryuser
    lbuser=tk.Label(loginframe, text="Username:", bg="#98FB98",font=("Arial", 10, "bold"))
    lbuser.place(relx=0.27, rely=0.3)
    entryuser = tk.Entry(loginframe, width=30)
    entryuser.place(relx=0.4, rely=0.3)
    #passwordlabel&entry
    global entrypass
    lbpass = tk.Label(loginframe,text="Password:",bg="#98FB98",
    font=("Arial", 10, "bold"))
    lbpass.place(relx=0.27, rely=0.39)
    entrypass = tk.Entry(loginframe, show="*", width=30)
    entrypass.place(relx=0.4, rely=0.39)
    # Login button
    loginbtn = tk.Button(loginframe,text="Login",command=lambda:login(select_role),bg="#737373",fg="black",font=("Arial", 14))
    loginbtn.place(relx=0.45, rely=0.5)
    loginframe.pack()
#rolecheck
def openlogin():
    select_role = lstbox.get()
    if select_role in ["USER", "ADMIN"]:
        show_login(select_role)
    else:
        errorlbl.config(text="Please select a role before proceeding.")
def reg_func():
    root.destroy()
    import register
pht = Image.open("gtmproject//assets//b2.jpg")
bgimg = pht.resize((643,450))
bgimg = ImageTk.PhotoImage(bgimg)
imglabel = tk.Canvas(mainframe, width=600, height=450,bg="green")
imglabel.create_image(0, 0, anchor='nw', image=bgimg)
imglabel.create_text(310, 100, text="Garbage Truck Management",font=("Comic Sans MS", 14, "bold"), fill="black")
imglabel.pack()
#Roleselection
roles=["USER", "ADMIN"]
lstbox = ttk.Combobox(mainframe, values=roles, state="readonly")
lstbox.place(relx=0.37, rely=0.45)
#log inbutton
logbtn = tk.Button(mainframe, text="LOG IN", bg="#737373",fg="black", font=("Arial", 14), command=openlogin)
logbtn.place(relx=0.3, rely=0.6)
#Registerbutton
regbtn = tk.Button(mainframe, text="REGISTER", bg="#737373",fg="black", font=("Arial", 14),command=reg_func)
regbtn.place(relx=0.5, rely=0.6)
#errormessagelabel
errorlbl=tk.Label(mainframe, text="All fields are mandatory",fg="red", bg="black")
errorlbl.place(relx=0.5, rely=0.75, anchor='center')
mainframe.pack()
root.mainloop()