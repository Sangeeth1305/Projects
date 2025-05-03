import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
import pickle
import random
import string
import mysql.connector as mysql
from customtkinter import CTkImage
from PIL import Image

#basic config
root=tk.Tk()
root.title("ZeroKey")
root.geometry("450x550+450+80")
root.resizable(False,False)
root.overrideredirect(True)
root.configure(bg="#1e1e1e")

#mysql connection
try:
    db = mysql.connect(
        host="localhost",
        user="",
        password="",
        database=""
    )
    cursor = db.cursor()
except:
    print("Connection Failed")

#homeframe
homeframe=tk.Frame(root)
homeframe.place(relheight=1, relwidth=1)  
#loginframe
loginframe=tk.Frame(homeframe)
loginframe.place(relheight=1, relwidth=1)
#splashframe
splashframe=tk.Frame(homeframe)
splashframe.place(relheight=1, relwidth=1)

homeimg = CTkImage(Image.open("assets/home.png"), size=(32, 32))
gearimg = CTkImage(Image.open("assets/gear.png"), size=(32, 32))
searchimg = CTkImage(Image.open("assets/search.png"), size=(32, 32))
searchimg1 = CTkImage(Image.open("assets/search.png"), size=(20, 20))

#login/register info
try:
    bfile1=open("pass.dat","rb")
    lst=pickle.load(bfile1)
    user=lst[0]
    pwd=lst[1]
except EOFError:    
    bfile1.close()
    user=""
    pwd=""

#generator config
def generator():
    genframe=tk.Frame(homeframe)
    genframe.place(relheight=0.9, relwidth=1)
    genframe.configure(bg="#879BA7")
    noinplabel=ctk.CTkLabel(genframe, text="Enter a number", font=("Arial", 16,"bold")
                            , bg_color="#879BA7",text_color="black")
    noinplabel.place(rely=0.2, relx=0.36)
    inputnopass = tk.Entry(genframe)
    inputnopass.place(rely=0.27, relx=0.36)
    passgenlabel=ctk.CTkLabel(genframe, text="Password",font=("Arial", 16,"bold")
                              , bg_color="#879BA7",text_color="black")
    passgenlabel.place(rely=0.35, relx=0.41)
    outputgenpass = tk.Entry(genframe, width=30)
    outputgenpass.place(rely=0.4, relx=0.29)
    def random_gen():
        try:
            length = int(inputnopass.get())
            characters = string.ascii_letters + string.digits
            random_text = ''.join(random.choices(characters, k=length))
            outputgenpass.delete(0, tk.END)
            outputgenpass.insert(0, random_text)
        except ValueError:
            outputgenpass.insert(0, "Enter a Integer")
    genbtn=ctk.CTkButton(genframe, text="Generate",font=("Arial", 12,"bold"),text_color="black"
                         ,fg_color="#777777",width=100,hover_color="#777777",command=random_gen)
    genbtn.place(rely=0.6, relx=0.37)
    def copy_func():
        text = outputgenpass.get()
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()
    copybtn = ctk.CTkButton(genframe, text="Copy",text_color="black",fg_color="#777777",hover_color="#777777"
                        ,font=("Arial",12,"bold"),command=copy_func)
    copybtn.place(rely=0.5, relx=0.38,relwidth=0.2)

#homemenucofing
def passmenu():
    passmenuframe=tk.Frame(homeframe)
    passmenuframe.place(relheight=0.9, relwidth=1)
    passmenuframe.configure(bg="#879BA7")
    passwordlabel=ctk.CTkLabel(passmenuframe, text="Passwords", font=("Arial", 16,"bold"),
                                bg_color="#879BA7",text_color="black")
    passwordlabel.place(rely=0.125, relx=0.4)
    def show_passwords():
        pwdscroll = ctk.CTkScrollbar(passmenuframe, orientation="vertical",bg_color="#879BA7")
        pwdscroll.place(relx=0.93, rely=0.22, relheight=0.7)
        treepass = ttk.Treeview(passmenuframe, columns=("Domain", "Username", "Password")
                                , show="headings",yscrollcommand=pwdscroll.set)
        treepass.place(relx=0.05, rely=0.23, relwidth=0.88, relheight=0.69)
        pwdscroll.configure(command=treepass.yview)
        treeconfig = ttk.Style()
        treeconfig.theme_use("default")
        treeconfig.configure("Treeview",
                background="#dbe5eb",
                foreground="black",
                rowheight=25,
                fieldbackground="#dbe5eb")
        treeconfig.configure("Treeview.Heading", 
                background="#879BA7", 
                foreground="black", 
                font=("Arial", 12, "bold"))
        treepass.heading("Domain", text="Domain")
        treepass.heading("Username", text="Username")
        treepass.heading("Password", text="Password")
        treepass.column("Domain", width=100, anchor="center")
        treepass.column("Username", width=150, anchor="center")
        treepass.column("Password", width=150, anchor="center")
        cursor.execute("SELECT * FROM vault")
        records = cursor.fetchall()
        for record in records:
            treepass.insert("",tk.END, values=record)
        def click_copy(event):
            clickedpass = treepass.focus()
            if clickedpass:
                values = treepass.item(clickedpass, "values")
                password = values[2] 
                root.clipboard_clear()
                root.clipboard_append(password)
                root.update()
                messagebox.showinfo("Copied", "Password copied to clipboard!")
        treepass.bind("<Double-1>", click_copy)
    show_passwords()

#searchconfig
def searchfunc():
    def searchdetails():
        for row in searchtree.get_children():
            searchtree.delete(row)
        domain_name = searchentry.get()
        query = "SELECT * FROM vault WHERE domain LIKE %s"
        cursor.execute(query, ('%' + domain_name + '%',))
        results = cursor.fetchall()
        for record in results:
            searchtree.insert("", tk.END, values=record)
    searchframe=tk.Frame(homeframe)
    searchframe.place(relheight=0.9, relwidth=1)
    searchframe.configure(bg="#879BA7")
    searchlabel=ctk.CTkLabel(searchframe, text="Search Passwords", font=("Arial", 16,"bold"),
                                bg_color="#879BA7",text_color="black")
    searchlabel.place(rely=0.075, relx=0.35) 
    searchentry=ctk.CTkEntry(searchframe, width=200, placeholder_text="Enter Domain Name")
    searchentry.place(rely=0.15, relx=0.1,relwidth=0.7) 
    searchbtn=ctk.CTkButton(searchframe, image=searchimg1 ,text_color="#777777",fg_color="#777777"
                            ,hover_color="#777777",command=searchdetails)
    searchbtn.place(rely=0.15, relx=0.8,relwidth=0.1)
    searchscroll = ctk.CTkScrollbar(searchframe, orientation="vertical", bg_color="#879BA7")
    searchscroll.place(relx=0.93, rely=0.24, relheight=0.65)
    searchtree = ttk.Treeview(searchframe, columns=("Domain", "Username", "Password"),
                        show="headings", yscrollcommand=searchscroll.set)
    searchtree.place(relx=0.05, rely=0.24, relwidth=0.88, relheight=0.64)
    searchscroll.configure(command=searchtree.yview)
    treeconfig = ttk.Style()
    treeconfig.theme_use("default")
    treeconfig.configure("Treeview",
                background="#dbe5eb",
                foreground="black",
                rowheight=25,
                fieldbackground="#dbe5eb")
    treeconfig.configure("Treeview.Heading", 
                background="#879BA7", 
                foreground="black", 
                font=("Arial", 12, "bold"))
    searchtree.heading("Domain", text="Domain")
    searchtree.heading("Username", text="Username")
    searchtree.heading("Password", text="Password")
    searchtree.column("Domain", width=100,anchor="center")
    searchtree.column("Username",width=150, anchor="center")
    searchtree.column("Password",width=150, anchor="center")
    def update_record():
        selected = searchtree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a record to update.")
            return
        values = searchtree.item(selected, "values")
        update_win = tk.Toplevel(root)
        update_win.title("Update Record")
        update_win.geometry("300x200+450+80")
        update_win.configure(bg="#1e1e1e")
        tk.Label(update_win, text="Domain:", bg="#1e1e1e", fg="white").pack()
        domain_ent = tk.Entry(update_win)
        domain_ent.insert(0, values[0])
        domain_ent.pack()
        tk.Label(update_win, text="Username:", bg="#1e1e1e", fg="white").pack()
        user_ent = tk.Entry(update_win)
        user_ent.insert(0, values[1])
        user_ent.pack()
        tk.Label(update_win, text="Password:", bg="#1e1e1e", fg="white").pack()
        pass_ent = tk.Entry(update_win)
        pass_ent.insert(0, values[2])
        pass_ent.pack()
        def save_updates():
            updated_domain = domain_ent.get()
            updated_user = user_ent.get()
            updated_pass = pass_ent.get()
            cursor.execute("UPDATE vault SET domain=%s, user=%s, password=%s WHERE domain=%s AND user=%s AND password=%s",
                           (updated_domain, updated_user, updated_pass, values[0], values[1], values[2]))
            db.commit()
            update_win.destroy()
            searchdetails()
        tk.Button(update_win, text="Save", command=save_updates).pack(pady=10)
    updatebtn = ctk.CTkButton(searchframe, text="Update", text_color="black", fg_color="#777777",
                               hover_color="#666666", font=("Arial", 12, "bold"), command=update_record)
    updatebtn.place(rely=0.9, relx=0.15)
    def deletedetails():
        selected = searchtree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a record to delete.")
            return
        values = searchtree.item(selected, "values")
        confirm = messagebox.askyesno("Confirm Delete", f"Delete record for {values[0]}?")
        if confirm:
            cursor.execute("DELETE FROM vault WHERE domain=%s AND user=%s AND password=%s",
                           (values[0], values[1], values[2]))
            db.commit()
            searchdetails()
    delete_btn = ctk.CTkButton(searchframe, text="Delete", text_color="black", fg_color="#777777",
                               hover_color="#666666", font=("Arial", 12, "bold"), command=deletedetails)
    delete_btn.place(rely=0.9, relx=0.55)

#menu
def menu():
    def save_pass():
        domain = domainentry.get()
        username = userentry.get()
        password = passentry.get()
        if domain and username and password:
            cursor.execute("INSERT INTO vault(domain, user, password) VALUES (%s, %s, %s)"
                           , (domain, username, password))
            db.commit()
            domainentry.delete(0, tk.END)
            userentry.delete(0, tk.END)
            passentry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Please fill in all fields.")
    menuframe=tk.Frame(homeframe)
    menuframe.place(relheight=0.1, relwidth=1,rely=0.9)
    menuframe.configure(bg="#879BA7")
    homebtn=ctk.CTkButton(menuframe, image=homeimg,text="",fg_color="#879BA7",hover_color="#879BA7",command=passmenu)
    homebtn.place(relx=0.35,rely=0.1)
    genbtn=ctk.CTkButton(menuframe, image=gearimg,text="",fg_color="#879BA7",hover_color="#879BA7",command=generator)
    genbtn.place(relx=0.06,rely=0.1)
    srhbtn=ctk.CTkButton(menuframe,image=searchimg,text="",fg_color="#879BA7",hover_color="#879BA7",command=searchfunc)
    srhbtn.place(relx=0.65,rely=0.1)
    menuscreenframe=tk.Frame(homeframe)
    menuscreenframe.place(relheight=0.9, relwidth=1)
    menuscreenframe.configure(bg="#879BA7")
    addlabel=ctk.CTkLabel(menuscreenframe, text="Add Your Credentials", font=("Arial", 16,"bold")
                            , bg_color="#879BA7",text_color="black")
    addlabel.place(rely=0.2, relx=0.33)
    domainlabel=ctk.CTkLabel(menuscreenframe, text="Domain:", font=("Arial",12,"bold")
                             , bg_color="#879BA7",text_color="black")
    domainlabel.place(rely=0.3, relx=0.2)
    domainentry = tk.Entry(menuscreenframe, width=30)
    domainentry.place(rely=0.3, relx=0.35)
    userlabel=ctk.CTkLabel(menuscreenframe, text="Username:", font=("Arial",12,"bold")
                           , bg_color="#879BA7",text_color="black")   
    userlabel.place(rely=0.4, relx=0.2)
    userentry = tk.Entry(menuscreenframe, width=30)
    userentry.place(rely=0.4, relx=0.35)
    passlabel=ctk.CTkLabel(menuscreenframe, text="Password:", font=("Arial",12,"bold")
                           , bg_color="#879BA7",text_color="black")
    passlabel.place(rely=0.5, relx=0.2)
    passentry = tk.Entry(menuscreenframe, width=30,show="*")     
    passentry.place(rely=0.5, relx=0.35)
    addbtn=ctk.CTkButton(menuscreenframe, text="Add",font=("Arial",12,"bold"),text_color="black"
                         ,fg_color="#777777",hover_color="#777777",command=save_pass)
    addbtn.place(rely=0.6, relx=0.37)
                             
#login verification
def verifylogin():
    username = userentry.get()
    password = passentry.get()
    if username == user and password == pwd:
        loginframe.destroy()
        menu()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

#registercred
def storereg():
    usernew = userentryreg.get()
    passnew = passentryreg.get()
    bfile=open("pass.dat","wb")
    infolst=[usernew,passnew]
    pickle.dump(infolst,bfile)  
    bfile.close()
    root.destroy()
    import Password
    
#register
def createreg():
    #registerframe
    global regframe
    regframe=tk.Frame(homeframe)
    regframe.place(relheight=1,relwidth=1)
    loginframe.destroy()
    regframe.configure(bg="#1e1e1e")
    regtext=ctk.CTkLabel(regframe, text="ZeroKey🔐", font=("Impact", 18), bg_color="#1e1e1e") 
    regtext.place(rely=0.25,relx=0.4)
    userinp = ctk.CTkLabel(regframe, text="Username:", font=("Arial", 12), bg_color="#1e1e1e")
    userinp.place(rely=0.35, relx=0.2)
    global userentryreg
    userentryreg = ctk.CTkEntry(regframe, width=200, placeholder_text="Enter your username")
    userentryreg.place(rely=0.35, relx=0.4)
    passinplabel = ctk.CTkLabel(regframe, text="Password:", font=("Arial", 12), bg_color="#1e1e1e")
    passinplabel.place(rely=0.45, relx=0.2)
    global passentryreg
    passentryreg = ctk.CTkEntry(regframe, width=200, show="*", placeholder_text="Enter your password")
    passentryreg.place(rely=0.45, relx=0.4)
    regbutton = ctk.CTkButton(regframe, text="Register",width=100,command=storereg)
    regbutton.place(rely=0.55, relx=0.4)

#login
def loginscreen():
    loginframe.configure(bg="#1e1e1e")
    logintext=ctk.CTkLabel(loginframe, text="ZeroKey🔐", font=("Impact", 18), bg_color="#1e1e1e") 
    logintext.place(rely=0.25,relx=0.4)
    userlabel = ctk.CTkLabel(loginframe, text="Username:", font=("Arial", 12), bg_color="#1e1e1e")
    userlabel.place(rely=0.35, relx=0.2)
    global userentry
    userentry = ctk.CTkEntry(loginframe, width=200, placeholder_text="Enter your username")
    userentry.place(rely=0.35, relx=0.4)
    passlabel = ctk.CTkLabel(loginframe, text="Password:", font=("Arial", 12), bg_color="#1e1e1e")
    passlabel.place(rely=0.45, relx=0.2)
    global passentry
    passentry = ctk.CTkEntry(loginframe, width=200, show="*", placeholder_text="Enter your password")
    passentry.place(rely=0.45, relx=0.4)
    loginbutton = ctk.CTkButton(loginframe, text="Login",width=100,command=verifylogin)
    loginbutton.place(rely=0.55, relx=0.4)

#login/register intiate
def checkverify():
    if user=="" and pwd=="":
        createreg()
    else:
        loginscreen()

#loadingscreen
def splashscreen():
    splashframe.configure(bg="#1e1e1e")
    splashtext=ctk.CTkLabel(splashframe, text="ZeroKey🔐", font=("Impact", 18), bg_color="#1e1e1e") 
    splashtext.place(rely=0.25,relx=0.4)
    splashmess=ctk.CTkLabel(splashframe,text="Your Digital Vault",font=("Impact",18),bg_color="#1e1e1e")
    splashmess.place(rely=0.55,relx=0.35) 
    progressbar = ctk.CTkProgressBar(splashframe, width=250,)
    progressbar.place(rely=0.45,relx=0.225)
    progressbar.set(0.2)
    progressbar.after(1000, lambda: progressbar.set(0.5))
    progressbar.after(3000, lambda: progressbar.set(0.8))
    progressbar.after(4500, lambda: progressbar.set(1.0))
    def close_splash():
        splashframe.destroy()
        checkverify()
    splashframe.after(5000, close_splash)
splashscreen()

root.mainloop()  

#create database password;
#create a table vault with domain, user, password
#CREATE TABLE vault (domain VARCHAR(255), user VARCHAR(255), password VARCHAR(255));