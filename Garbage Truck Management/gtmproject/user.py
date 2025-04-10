import subprocess
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from tkinter import filedialog
from PIL import ImageTk, Image
import tkinter.font as tkFont
from datetime import datetime


root = Tk()
root.title("R3-Waste Management")
root.iconbitmap("gtmproject//assets//GTM.ico")
root.geometry("925x525+200+90")
root.resizable(height=False, width=False)
current_date = datetime.now().date()


f = open("cred.txt","r")
f.seek(0,0)
usr_cred=f.read()

try:
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="gtm"
    )
    cursor = con.cursor()
    print("connection secure")
    

    cursor.execute(f"SELECT * FROM user WHERE uid = '{usr_cred}' ")
    user = cursor.fetchone()
except:
    print("error occured")
print(user)


mainframe = tk.Frame(root, bg="white", highlightbackground="black", highlightthickness=1)
mainframe.place(relx=0.27, rely=0.15, relwidth=0.73, relheight=0.85)
# options
opframe = tk.Frame(root, bg="#8DB6CD")
opframe.configure(height=525, width=250)
opframe.pack(side=tk.LEFT)
# header
header = tk.Frame(root, bg="#737373", highlightbackground="black", highlightthickness=1)
header.place(relx=0.27, rely=0, relwidth=0.9, relheight=0.15)
headertext = tk.Label(header, text="R3-Waste Management", bg="#737373", fg="#8DB6CD",
                      font=("Comic Sans MS", 24, "bold"))
headertext.place(relx=0.2, rely=0.14)


# indicators
def indicator(lb, page, user):
    hid_indcator()
    lb.config(bg="#737373")
    delete_page()
    page(user)


# destroying pages
def delete_page():
    for frame in mainframe.winfo_children():
        frame.destroy()


def hid_indcator():
    bin_ind.config(bg="#8DB6CD")
    rep_ind.config(bg="#8DB6CD")
    log_ind.config(bg="#8DB6CD")


def bin_page(user):
    bin_frame = tk.Frame(mainframe, bg="white")
    bin_frame.place(relwidth=1, relheight=1)
    

    def send_bin_data():
            
        def send_data():
            print()
            fillbins = fillbins_entry.get()
            bluebins = bluebins_entry.get()

            if fillbins.isdigit():
                try:
                    query = "Update User set green_bins=%s,blue_bin=%s,last_reported=%s,no_of_bins=%s where uid=%s;"
                    cursor.execute(query, (fillbins,bluebins,current_date,str(int(fillbins)+int(bluebins)), user[0]))

                    bin_data_query = f"update bin_data set green_bins={fillbins},blue_bins={bluebins},no_of_bin={int(fillbins)+int(bluebins)},last_reported='{current_date}' where st_id='{user[2]}';"
                    cursor.execute(bin_data_query)

                    con.commit()
                    messagebox.showinfo("Success", "Data sended successfully!")
                except mysql.connector.Error:
                    messagebox.showerror("Error", "Error connecting to MySQL database!")
            else:
                messagebox.showerror("Error", "Please enter valid data!")
        
        blue_frame = tk.Frame(bin_frame,bg="#8DB6CD")
        blue_frame.place(relheight=0.5,relwidth=1)
       
        font = tkFont.Font(family="Times", size=20)
        uid=user[0]
        user_id=Label(blue_frame,text="USER ID :"+uid,font=font,bg="#8DB6CD")
        user_id.place(relx=0.1, rely=0.2)
        name = user[1]
        uname = Label(blue_frame, text="NAME :" + name, font=font,bg="#8DB6CD")
        uname.place(relx=0.1, rely=0.4)
        street = user[7]
        street_label = Label(blue_frame, text="STREET NAME :  " + street, font=font,bg="#8DB6CD")
        street_label.place(relx=0.1, rely=0.6)

        fill_lbl = tk.Label(bin_frame, text="Degradable:", font=font, bg="#737373", fg="black")
        fill_lbl.place(relx=0.03, rely=0.7)

        fillbins_entry = tk.Entry(bin_frame, width=5, font=font,background="#d3d3d3")
        fillbins_entry.place(relx=0.24, rely=0.7,relwidth=0.2)

        blue_lbl = tk.Label(bin_frame, text="Non-Degradable:", font=font, bg="#737373", fg="black")
        blue_lbl.place(relx=0.47, rely=0.7)

        bluebins_entry = tk.Entry(bin_frame, width=5, font=font,background="#d3d3d3")
        bluebins_entry.place(relx=0.76, rely=0.7,relwidth=0.2)

        # sendbutton
        send_btn = tk.Button(bin_frame, text="SUBMIT ", font=("Arial", 14,), bg="#737373", command=send_data)
        send_btn.place(relx=0.4, rely=0.85)
    send_bin_data()

    #notification
    def notification_open():
        print()
        notifications = []

        def notification_close():
            notification_frame.destroy()
            not_button.config(command=notification_open)
            not_button.place(relx=0.8, rely=0.1, relheight=0.1, relwidth=0.07)

        # Frame to hold the notification content
        notification_frame = tk.Frame(bin_frame)
        notification_frame.place(relx=0.5,relheight=1,relwidth=0.5)
        not_button.place(relx=0.43, rely=0.2, relheight=0.1, relwidth=0.07)
        try:
            q=f"select notification from notification where u_id='{user[0]}';"
            cursor.execute(q)
            t=cursor.fetchall()
            print(t)
            for i in t:
                for j in i:
                    tex=j
                    label=tk.Label(notification_frame,text=tex)
                    label.pack()
        except:
            label=tk.Label(notification_frame,text="no notification")
            label.pack()
        not_button.config(command=notification_close)
    not_button=tk.Button(bin_frame,text="📧",font=("Arial",30),bg="#d3d3d3",command=lambda: notification_open())
    not_button.place(relx=0.8,rely=0.1, relheight=0.1, relwidth=0.07)

#reportfunction
def rep_page(user):
    print()
    def upload_image():
        file_path = filedialog.askopenfilename()
        if file_path:
            global save_path
            image = Image.open(file_path)
            save_path = "Issues_Images/" + file_path.split("/")[-1]
            print(save_path)
            image.save(save_path)
            print(f"Image saved to {save_path}")

    def report_func():
        issue_type = valbox.get()
        if not issue_type:
            messagebox.showerror("Error", "Please select an issue type!")
        else:
            cursor.execute("SELECT I_ID FROM Issues ORDER BY I_ID DESC LIMIT 1")
            result = cursor.fetchone()
            if result:
                last_id = result[0]
                next_id_num = int(last_id[1:]) + 1
            else:
                next_id_num = 1
            next_id = f"I{next_id_num:03d}"
            address1=rep_entry.get()
            if not address1:
                address1=user[3]
            try:
                if save_path:
                    sql_query = f"insert into Issues values('{next_id}', '{address1} ', '{user[0]} ','{save_path}',CURDATE() , 0 , null,'{issue_type}'  );"
            except NameError:
                sql_query = f"insert into Issues(I_ID,address,UID,R_date,resolved,res_date,issue_name) values('{next_id}', '{user[3]} ' , '{user[0]} ',CURDATE(), 0 , null,'{issue_type}');"
            cursor.execute(sql_query)
            con.commit()
            messagebox.showinfo("Success", f"Issue reported successfully with ID: {next_id}")
    rep_frame = tk.Frame(mainframe, bg="white")
    rep_lb = tk.Label(rep_frame, text="Report Issue", font=("Arial", 16), bg="white")
    rep_lb.place(relx=0.4, rely=0.15, anchor="center")
    item = ["Animal carcass", "Sewage leak ", "Water overflow", "Garbage in the road", "Mosquito breeding",
            "Other Issues"]
    valbox = ttk.Combobox(rep_frame, values=item, state="readonly")
    valbox.place(relx=0.3, rely=0.25)
    Img_button = tk.Button(rep_frame, text="IMAGE", command=lambda: upload_image())
    Img_button.place(relx=0.63, rely=0.25, relheight=0.05)
    rep_entry = tk.Entry(rep_frame, width=40)
    rep_entry.place(relx=0.22, rely=0.35, relheight=0.1)
    rep_btn = tk.Button(rep_frame, text="Report", font=("Arial", 14), bg="#737373", command=lambda: report_func())
    rep_btn.place(relx=0.34, rely=0.55)
    rep_frame.place(relwidth=1, relheight=1)
#logoutfunction
def log_page(user):
    
    log_frame = tk.Frame(mainframe, bg="white")
    log_lb = tk.Label(log_frame, text="Logging Out, Are You Sure? ", font=("Arial", 16), bg="white")
    log_lb.place(relx=0.5, rely=0.35, anchor="center")
    yes_btn = tk.Button(log_frame, text="YES", font=("Arial", 14), bg="#737373",command=yes_func)
    yes_btn.place(relx=0.4, rely=0.50, anchor="center")
    no_btn = tk.Button(log_frame, text="NO", font=("Arial", 14), bg="#737373",command=no_func)
    no_btn.place(relx=0.55, rely=0.50, relwidth=0.08, anchor="center")
    log_frame.place(relwidth=1, relheight=1)
def yes_func():
    root.destroy()
    import gtm
def no_func():
    delete_page()
    mainframe.config(bg="white")
    hid_indcator()
#menu
menu_text = tk.Label(opframe, text="MENU", bg="#8DB6CD", fg="black", font=("Comic Sans MS", 16, "bold"))
menu_text.place(relx=0.16, rely=0.25)
# binpage
bin_pge = tk.Button(opframe, text="No.of Bin", bg="#8DB6CD", fg="black", font=("Arial", 16), bd=0,
                    command=lambda: indicator(bin_ind, bin_page, user))
bin_pge.place(relx=0.1, rely=0.4, relwidth=0.70, relheight=0.08)
bin_ind = tk.Label(opframe, text=" ", bg="#8DB6CD")
bin_ind.place(relx=0.05, rely=0.4, relwidth=0.05, relheight=0.08)
# reportpage
rep_pge = tk.Button(opframe, text="Report Issue", bg="#8DB6CD", fg="black", font=("Arial", 16), bd=0,
                    command=lambda: indicator(rep_ind, rep_page, user))
rep_pge.place(relx=0.16, rely=0.5, relwidth=0.70, relheight=0.08)
rep_ind = tk.Label(opframe, text=" ", bg="#8DB6CD")
rep_ind.place(relx=0.05, rely=0.5, relwidth=0.05, relheight=0.08)
# logoutpage
logout_pge = tk.Button(opframe, text="Logout", bg="#8DB6CD", fg="black", font=("Arial", 16), bd=0,
                       command=lambda: indicator(log_ind, log_page, user))
logout_pge.place(relx=0.10, rely=0.6, relwidth=0.70, relheight=0.08)
log_ind = tk.Label(opframe, text=" ", bg="#8DB6CD")
log_ind.place(relx=0.05, rely=0.6, relwidth=0.05, relheight=0.08)

root.mainloop()