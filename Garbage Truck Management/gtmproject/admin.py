try:

    from tkinter import *
    from tkinter import ttk
    from tkinter import messagebox
    import tkinter as tk
    from PIL import ImageTk, Image
    import mysql.connector as mysql
    from datetime import datetime
    import subprocess
except:
    print("package not found")

# Get the current date
current_date = datetime.now().date()

try:
    con = mysql.connect(
        host="localhost",
        user="root",
        password="root",
        database="gtm"
    )
    cursor=con.cursor()
except:
    print("mysql error")
q3 = "select sum(no_of_bins) from user order by st_id  ;"
cursor.execute(q3)
t = cursor.fetchall()
print(t)
root = Tk()
root.title("R3-Waste Management")
root.geometry("925x525+200+90")
root.resizable(0, 0)
root.configure(bg="#d3d6d2")
root.iconbitmap("gtmproject//assets//GTM.ico")

def adminscreen():
    style = ttk.Style()
    style.theme_use('default')
    main_frame = Frame(root, background="white", highlightbackground="black", highlightthickness=2)
    main_frame.place(x=279, y=68, relheight=0.9, relwidth=0.7)
    header = Frame(root, bg="#737373")
    header.place(relx=0.3, rely=0, relwidth=0.7, relheight=0.13)
    headertext = tk.Label(header, text="R3-Waste Management", bg="#737373", fg="#50C878",
                      font=("Comic Sans MS", 24, "bold"))
    headertext.place(relx=0.2, rely=0.14)
    sidebar = Frame(root, bg="#50C878",highlightbackground="black", highlightthickness=2)
    sidebar.place(relx=0, rely=0, relwidth=0.31, relheight=1)
    def hide_indicator():
        tree_indicate.config(bg="#50C878")
        Vi_indicate.config(bg="#50C878")
        Bu2_indicate.config(bg="#50C878")
    def delete_frames():
        for frame in main_frame.winfo_children():
            frame.destroy()
    def indicate(lb, page):
        delete_frames()
        hide_indicator()
        # indicator active color
        lb.config(background="#737373")
        page()
    # TREE VIEW CONFIGURE
    def tree_view():
        try:
            q2 = "select st_id,no_of_bin,L_date,green_bins,blue_bins from bin_data order by no_of_bin desc;"
            cursor.execute(q2)
            t2 = cursor.fetchall()
        except:
            print("database error")
        style.configure("TreeView",
                        background="#d3d6d2",
                        foreground='black',
                        fieldbackground='#d3d3d3',
                        rowheight=60)
        style.configure("Treeview.Heading", background="white", foreground="Black")
        # SELECTED COLOUR CHANGE
        style.map("TreeView",
                  background=[('selected', '#347083')])
        # CREATING FRAME FOR TREE VIEW TO SCROLL
        t_frame = Frame(main_frame)
        t_frame.place(relwidth=1, relheight=0.9)
        # scroll bar
        t_scroll = Scrollbar(t_frame)
        t_scroll.pack(side=RIGHT, fill=Y)
        # tree view creation , placing it in treeview frame
        global treeview
        treeview = ttk.Treeview(t_frame, yscrollcommand=t_scroll.set, selectmode="extended")
        # configuring scroll bar
        t_scroll.config(command=treeview.yview)
        root.resizable(False, False)
        def on_Double_Click(event):
            def ok_button_function():
                item = treeview.selection()
                for i in item:
                    details=treeview.item(i,"values")
                    st_ID = details[0]
                    q = f"select uid from user where st_id='{st_ID}';"
                    cur_date = datetime.now().date()
                    cursor.execute(q)
                    t = cursor.fetchall()
                    for i in t:
                        q2 = f"insert into notification values('{i[0]}','Our team of collectors are coming to your street  from 9.30','{cur_date}');"
                        cursor.execute(q2)
                    q3 = f"update user set last_reported=null where st_id='{st_ID}';"
                    cursor.execute(q3)
                    con.commit()
                    print(t)
                    print(st_ID)
                    query = f"update  bin_data set l_date='{cur_date}' where st_id='{st_ID}' ;"
                    cursor.execute(query)
                    '''waste_collection_query=f"insert into waste_collection values('{st_ID}','{cur_date}',{details[1]},{details[2]},{details[3]});"
                    cursor.execute(waste_collection_query)'''
                    con.commit()
                top_window.destroy()
            global top_window
            top_window = Toplevel()
            top_window.geometry("500x600")
            button = Button(top_window, text="are you logging in?", command=ok_button_function)
            button.pack()
        treeview['columns'] = ("str_ID", "Nob", "green_bin", "blue_bin", "lst_date", "diff_date")
        # format columns
        treeview.column("#0", width=10, stretch=NO)
        treeview.column("str_ID", anchor=W, width=50)
        treeview.column("Nob", anchor=W, width=50)
        treeview.column("green_bin", anchor=W, width=50)
        treeview.column("blue_bin", anchor=W, width=50)
        treeview.column("lst_date", anchor=CENTER, width=80)
        treeview.column("diff_date", anchor=W, width=100)
        # headings
        treeview.heading("#0", text="", anchor=W)
        treeview.heading("str_ID", text="Str_ID", anchor=W)
        treeview.heading("Nob", text="No_of_bins", anchor=W)
        treeview.heading("green_bin", text="degradable wastes", anchor=W)
        treeview.heading("blue_bin", text="non-degradable wastes", anchor=W)
        treeview.heading("lst_date", text="last_collected_date", anchor=CENTER)
        treeview.heading("diff_date", text="collected_Since", anchor=W)
        # sample data
        data = []
        for i in t2:
            data.append(list(i))
        count = 1
        # iterating treeview
        for i in data:
            if i[2]==None:
                i.append("0"+ " day")
            else:
                date_diff = current_date - i[2]
                i.append(str(date_diff.days) + " days")
            treeview.insert(parent="", index=END, iid=count, text="", values=(i[0], i[1], i[3], i[4], i[2], i[5]))
            count += 1
        treeview.bind('<Double-1>', on_Double_Click)
        # to stop tree view from resizing
        treeview.bind('<Motion>', 'break')
        treeview.place(relx=0, rely=0, relwidth=1, relheight=1)
    def ViewIssues():
        WLabel_frame = Frame(main_frame, bg="red")
        WLabel_frame.config(height=10, width=50)
        WLabel_frame.place(relheight=0.1,relwidth=1)
        wquery=f"SELECT * FROM issues WHERE RES_DATE IS NULL ORDER BY R_DATE ASC LIMIT 1;"
        cursor.execute(wquery)
        wq=cursor.fetchall()
        Is_d=wq[0]
        is_1=Is_d[0]
        is_2 = Is_d[4].strftime("%Y-%m-%d")
        WLabel = Label(WLabel_frame, text='WARNING!-Issue number ' + is_1 + ' is due by ' + is_2,bg="red")
        WLabel.place(x=190, y=15)
        disabled_cells = set()
        def data_button_func():
            dataroot = Toplevel(root)
            dataroot.geometry("1025x450+200+70")
            # CREATING FRAME FOR TREE VIEW TO SCROLL
            t_frame = Frame(dataroot)
            t_frame.pack()
            # scroll bar
            t_scroll = Scrollbar(t_frame)
            t_scroll.pack(side=RIGHT, fill=Y)
            # tree view creation , placing it in dataview frame
            global dataview
            dataview = ttk.Treeview(t_frame, yscrollcommand=t_scroll.set, selectmode="extended")
            # dataview.configure()
            # configuring scroll bar
            t_scroll.config(command=dataview.yview)
            dataview.pack()
            root.resizable(False, False)
            def on_Double_Click(event):
                # it is not working for second time if two issues with same usr id exists
                item_id = dataview.identify_row(event.y)
                column_id = dataview.identify_column(event.x)
                column = int(column_id.strip('#')) - 1  # Columns are 1-indexed in identify_column
                values = dataview.item(item_id, "values")
                i_Id = values[0]
                print(i_Id)
                cursor.execute(f"select image from issues where I_Id='{i_Id}'")
                t = cursor.fetchone()
                print(t)
                print(i_Id, " :", column_id)
                if (item_id, column) in disabled_cells:
                    return
                elif (item_id, column) not in disabled_cells:
                    try:
                        if column == 5:
                            ph = PhotoImage(file=t[0])
                            photoroot = Toplevel()
                            photoroot.geometry("500x600")
                            label1 = Label(photoroot, image=ph)
                            label1.pack()
                            photoroot.mainloop()
                            disabled_cells.add((item_id, column))
                    except:
                        photoroot = Toplevel()
                        photoroot.geometry("200x50")
                        label1 = Label(photoroot, text="no image")
                        label1.pack()
                    i_Id=""
            dataview['columns'] = ("Complaint_ID", "Complaint_Type", "Uid", "Address", "Complaint_date", "IMAGE")
            # format columns
            dataview.column("#0", width=10, stretch=NO)
            dataview.column("Complaint_ID", anchor=W, width=50)
            dataview.column("Complaint_Type", anchor=W, width=300)
            dataview.column("Uid", anchor=W, width=50)
            dataview.column("Address", anchor=CENTER, width=400)
            dataview.column("Complaint_date", anchor=W, width=150)
            dataview.column("IMAGE", anchor=W, width=100)
            # headings
            dataview.heading("#0", text="", anchor=W)
            dataview.heading("Complaint_ID", text="COMPLAINT_ID", anchor=W)
            dataview.heading("Complaint_Type", text="COMPLAINT_TYPE", anchor=W)
            dataview.heading("Uid", text="User ID", anchor=W)
            dataview.heading("Address", text="ADDRESS", anchor=CENTER)
            dataview.heading("Complaint_date", text="COMPLAINT_DATE", anchor=W)
            dataview.heading("IMAGE", text="IMAGE", anchor=W)
            # sample data
            try:
                q2 = "select * from issues ;"
                cursor.execute(q2)
                t2 = cursor.fetchall()
            except:
                print("database error")
            count = 1
            # iterating treeview
            for i in t2:
                dataview.insert(parent="", index=END, iid=count, text="",
                                values=(i[0], i[7], i[2], i[1], i[4], "image"))
                count += 1
            dataview.bind('<Double-1>', on_Double_Click)
            dataroot.mainloop()
        data_button = Button(main_frame, text="DATA",
                             bg="White",
                             activebackground='#ffffff',
                             font=("Arial", 9, "bold"),
                             bd=0,
                             cursor='hand1',
                             command=lambda: data_button_func()
                             )
        data_button.place(x=300, y=250)
        # add two text inputs for issue code and date.date should be listbox for currdate and custom.
        def go_button_function():
            Issue_code = issue_no_entry.get()
            curr_date = datetime.now().date()
            print()
            q = f"update issues set res_date='{curr_date}' where I_id='{Issue_code}'; "
            cursor.execute(q)
            con.commit()
            cursor.execute(f"select Uid from issues where I_Id='{Issue_code}'")
            t = cursor.fetchone()
            print(t)
            q2 = f"insert into notification values('{t[0]}', 'Your issue reported resolved','{curr_date}')"
            cursor.execute(q2)
            con.commit()
        global issue_no_entry
        text_box_frame = Frame(main_frame, bg="#50C878",highlightbackground="black",highlightthickness=1)
        text_box_frame.config(height=70)
        issue_no_entry = Entry(text_box_frame)
        issue_no_entry.place(x=120, y=20)
        Sdate = StringVar()
        Label(text_box_frame, text="Issue no:", bg="#50C878").place(x=45, y=20)
        date_entry = Entry(text_box_frame, textvariable=Sdate)
        date_entry.place(x=350, y=20)
        Label(text_box_frame, text="Date:", bg="#50C878").place(x=290, y=20)
        go_button = Button(text_box_frame, text="GO", command=go_button_function)
        text_box_frame.place(rely=0.82,relwidth=1)
        go_button.place(x=550, y=20)
    def log_page():
        log_frame = tk.Frame(main_frame, bg="white")
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
        delete_frames()
        main_frame.config(bg="white")
        hide_indicator()
    menu_options = Label(sidebar,
                         text="Menu",
                         bg="#50C878",
                         fg="Black",
                         font=("Arial", 16,"bold"),
                         
                         )
    menu_options.place(x=30, y=150, anchor="w")
    # view issue button
    global tree, Vi, Bu2
    #logs
    tree = Button(sidebar, text="LOGS",
                  bg="#50C878",
                  font=("Arial", 9, "bold"),
                  bd=0,
                  cursor='hand2',
                  activebackground='#ffffff',
                  command=lambda: indicate(tree_indicate, tree_view))
    tree_indicate = Label(sidebar, text='', bg='#50C878')
    tree.place(x=30, y=250, anchor="w")
    tree_indicate.place(x=3, y=250, anchor="w")
    #viewisssues
    Vi = Button(sidebar, text="VIEW ISSUES",
                bg="#50C878",
                font=("Arial", 9, "bold"),
                bd=0,
                cursor='hand2',
                activebackground='#ffffff',
                command=lambda: indicate(Vi_indicate, ViewIssues))
    Vi_indicate = Label(sidebar, text='', bg='#50C878')
    Vi.place(x=30, y=300, anchor="w")
    Vi_indicate.place(x=3, y=300, anchor="w")
    #logout
    Bu2 = Button(sidebar, text="LOG OUT",
                 bg="#50C878",
                 font=("Arial", 9, "bold"),
                 bd=0,
                 cursor='hand2',
                 activebackground='#ffffff',
                 command=lambda: indicate(Bu2_indicate, log_page))
    # Button inactive color violet
    Bu2_indicate = Label(sidebar, text='', bg='#50C878')
    Bu2_indicate.place(x=3, y=350, anchor="w")
    Bu2.place(x=30, y=350, anchor="w")
adminscreen()
root.mainloop()