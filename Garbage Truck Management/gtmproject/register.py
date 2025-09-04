import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import mysql.connector
import subprocess

root = tk.Tk()
root.title("Garbage Truck Management")
root.iconbitmap("gtmproject//assets//GTM.ico")
root.geometry("600x450+200+90")
root.configure(bg="#53d858")
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
mainframe.place(relheight=1,relwidth=1)
mainframe.pack()
#image&textforloginpage
pht = Image.open("gtmproject//assets//b2.jpg")
bgimg = pht.resize((600, 450))
bgimg = ImageTk.PhotoImage(bgimg)
imglabel = tk.Canvas(mainframe, width=600, height=450, bg="white")
imglabel.create_image(0, 0, anchor='nw', image=bgimg)
imglabel.create_text(300, 80, text="REGISTER", font=("Comic Sans MS", 14, "bold"), fill="black")
imglabel.pack()
#addresslabel$entry
lbadd=tk.Label(mainframe, text="Address:", bg="#98FB98", font=("Arial", 10, "bold"))
lbadd.place(relx=0.27, rely=0.41)
addreg = tk.Entry(mainframe, width=30)
addreg.place(relx=0.4, rely=0.41)
#usernamelabel&entry
#global userreg
lbuser=tk.Label(mainframe, text="Username:", bg="#98FB98", font=("Arial", 10, "bold"))
lbuser.place(relx=0.27, rely=0.25)
userreg = tk.Entry(mainframe, width=30)
userreg.place(relx=0.4, rely=0.25)
#passwordlabel&entry
#global passreg
lbpass = tk.Label(mainframe, text="Password:", bg="#98FB98", font=("Arial", 10, "bold"))
lbpass.place(relx=0.27, rely=0.33)
passreg = tk.Entry(mainframe, show="*", width=30)
passreg.place(relx=0.4, rely=0.33)
#listbox
street=["Anna nagar", "Raja nagar","Thinnappa nagar","Tamil nagar","ADD STREET"]
strbox = ttk.Combobox(mainframe, values=street, state="writeonly")
strbox.place(relx=0.4, rely=0.49,relwidth=0.31)
#register function
def register():
    conn = connect_db()
    cursor = conn.cursor()
    #streetid
    cursor.execute("SELECT st_id FROM user ORDER BY st_id DESC LIMIT 1")
    result = cursor.fetchone()
    if result:
        slast_id = result[0]
        snext_id_num = int(slast_id[2:]) + 1
    else:
        snext_id_num = 1
    snext_id = f"st{snext_id_num:02d}"
    #userid
    cursor.execute("SELECT uid FROM user ORDER BY uid DESC LIMIT 1")
    result = cursor.fetchone()
    if result:
        last_id = result[0]
        next_id_num = int(last_id[2:]) + 1
    else:
        next_id_num = 1
    next_id = f"US{next_id_num:03d}"
    #user_password
    address=addreg.get()
    username = userreg.get()
    password = passreg.get()
    street_name = strbox.get()
    if not username or not password or not street_name:
        messagebox.showerror("Input Error", "All fields must be filled out.")
        return
    regquery="insert into user(uid,uname,st_id,address,pwd,streetname) values(%s,%s, %s, %s,%s,%s);"
    cursor.execute(regquery,(next_id,username,snext_id,address,password,street_name))
    conn.commit()
    conn.close()
    f=open("cred.txt","w")
    f.write(next_id)
    f.close()
    messagebox.showinfo("Registration", "User registered successfully!")
    root.destroy()
    import user
# register button
regisbtn = tk.Button(mainframe, text="REGISTER",  bg="#737373", fg="black", font=("Arial", 14),command=register)
regisbtn.place(relx=0.4, rely=0.6)
root.mainloop()