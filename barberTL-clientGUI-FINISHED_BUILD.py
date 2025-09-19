# Εισαγωγή βιβλιοθηκών για GUI, Calendar και Ημερομηνίας
import mysql.connector
import tkinter as tk
import datetime
from tkinter import messagebox
from tkcalendar import *
from datetime import datetime, timedelta

# Σύνδεση με MySQL Server και χρήση της σωστής βάσης δεδομένων
mydb = mysql.connector.connect(
  host = "localhost",
  user = "root",
  password = "",
  database = "barberDB",
  port = 3306
)

# Συνάρτηση για εκχώρηση ραντεβού Client
def insertClient(name, phone, date, time):
    mycursor = mydb.cursor()
    sql = "INSERT INTO customers (cname, cphonum, cdate, ctime) VALUES (%s, %s, %s, %s)"
    val = (name, phone, date, time)
    # ΛΕίτουργία MySQL εντολής
    mycursor.execute(sql, val)
    mydb.commit()
    # Ενημέρωση επιτηχής εκχώρησης ραντεβού
    messagebox.showinfo(title="Success!", message="Appointment saved!")

def selectClient(name, phone):
    mycursor = mydb.cursor()
    # Έλεγχος σωστής ολοκλήρωσης παραμέτρων
    try:
        if name and phone:
            sql = "SELECT * FROM customers WHERE cname = (%s) AND cphonum = (%s)"
            # ΛΕίτουργία MySQL εντολής
            mycursor.execute(sql, (name, (phone)))
            myresult = mycursor.fetchall()
            if myresult:
                row = myresult[0]
                display_text = (f"Name: {row[0]}\n"
                   f"Phone: {row[1]}\n"
                   f"Date: {row[2]}\n"
                   f"Time: {row[3]}")
                messagebox.showinfo(title="Appointment Details", message=display_text)
            else:
                messagebox.showinfo(title="Not Found", message="No matching appointment found")
                return myresult
        else:
            messagebox.showinfo(title="Error", message="Please ensure that you have filled the Name and Phone boxes correctly.")
            return None
    except mysql.connector.Error as err:
        messagebox.showerror(title="Database Error", message=str(err))
        return None

def deleteClient(name, phone):
    # Έλεγχος σωστής ολοκλήρωσης παραμέτρων
    try:
        confirm = messagebox.askyesno(title="Confirm", message="Delete this appointment?")
        if not confirm:
            return False
        
        mycursor = mydb.cursor()
        sql = "DELETE FROM customers WHERE cname = %s AND cphonum = %s"
        val = (name, phone)
        # ΛΕίτουργία MySQL εντολής
        mycursor.execute(sql, val)
        mydb.commit()
        
        if mycursor.rowcount > 0:
            messagebox.showinfo(title="Success", message="Appointment deleted successfully!")
            return True
        else:
            messagebox.showinfo(title="Not Found", message="No matching appointment found")
            return False
    except mysql.connector.Error as err:
        messagebox.showerror(title="Database Error", message=str(err))
        return False

def updateClient(name, phone, date, time):
    # Έλεγχος σωστής ολοκλήρωσης παραμέτρων
    try:
        mycursor = mydb.cursor()
        sql = "UPDATE customers SET cdate = %s, ctime = %s WHERE cname = %s AND cphonum = %s"
        val = (date, time, name, phone)
        # ΛΕίτουργία MySQL εντολής
        mycursor.execute(sql, val)
        mydb.commit()
        
        if mycursor.rowcount > 0:
            messagebox.showinfo(title="Success", message="Appointment updated successfully!")
            return True
        else:
            messagebox.showinfo(title="Not Found", message="No matching appointment found")
            return False
    except mysql.connector.Error as err:
        messagebox.showerror(title="Database Error", message=str(err))
        return False

def seeClient(date):
    # Έλεγχος σωστής ολοκλήρωσης παραμέτρων
    try:
        mycursor = mydb.cursor()
        sql = "SELECT * FROM customers where cdate = %s"
        # ΛΕίτουργία MySQL εντολής
        mycursor.execute(sql, (date, ))
        myresult = mycursor.fetchall()
        if myresult: 
            for row in myresult:
                display_text = (f"Name: {row[0]}\n"
                f"Phone: {row[1]}\n"
                f"Date: {row[2]}\n"
                f"Time: {row[3]}")
            messagebox.showinfo(title="Appointments", message=display_text)
        else:
            messagebox.showinfo(title="Appointments", message="There are no Appointments for the selected date.")
    except mysql.connector.Error as err:
        messagebox.showerror(title="Database Error", message=str(err))
        return False

def delClient(name, phone):
    # Έλεγχος σωστής ολοκλήρωσης παραμέτρων
    try:
        mycursor = mydb.cursor()
        sql = "DELETE FROM customers where cname = %s AND cphonum = %s"
        # ΛΕίτουργία MySQL εντολής
        mycursor.execute(sql, (name, phone))
        mydb.commit()
        if mycursor.rowcount > 0:
            messagebox.showinfo(title="Appointments", message="Appointment succesfully canceled.")
        else:
            messagebox.showerror(title="Appointments", message="There was no Appointment with that Name and Phone Number.")
    except mysql.connector.Error as err:
        messagebox.showerror(title="Database Error", message=str(err))
        return False
    
# Συνάρτηση εφαρμογής
def GUI():
    # Δημιοργία παραθύρου εφαρμογής
    win = tk.Tk()
    # Μέγεθος παραθύρου
    win.geometry('800x600')
    # Τίτλος παραθύρου
    win.title("Barber Appointment")

    # Συνάρτηση για επιστροφή στην αρχική
    def back():
        # Διαγραφή παραθύρου
        win.destroy()
        GUI()

    # Συνάρτηση για προβολή ραντεβού απο Barber
    def bar_app():
        # Διαγραφή προηγουμένων επιλογών
        for widget in win.winfo_children():
            widget.destroy()
        # Μεταβλητή με την σημερινή ημέρα 
        today = datetime.now()
        # Μεταβλητή και δημιοργία του ημερολογίου
        cal = Calendar(win, selectmode="day",  mindate=today, maxdate=today + timedelta(days=60), weekendbackground='white', weekendforeground='black',)
        cal.bind("<<CalendarSelected>>", sunday)
        cal.pack(pady=20)

        dlabel = tk.Label(win, text="")
        dlabel.pack()

        # Συνάρτηση για επιλογή ημέρας
        def grab_date():
            selected_date = cal.get_date()
            month, day, year = selected_date.split('/')
            if len(year) == 2:
                year = f"20{year}"
            formatted_date = f"{year}-{int(month):02d}-{int(day):02d}"
            dlabel.config(text=formatted_date)

        # Επιλογή ημερομηνιας
        datebtn = tk.Button(win, text = "Select Date", command = grab_date)
        datebtn.pack(pady = 20)
        
        # Συνάρτηση που καλεί την συνάρτηση με της εντολές της MySQL
        def on_submit():
            date = dlabel.cget("text")
            seeClient(date)

        # Κουμπία επιλογών
        tk.Button(win, text="See Appointments", command=on_submit).pack(pady=20)
        tk.Button(win, text="Back", command=back).pack(pady=10)

    # Συνάρτηση για ακύρωση ραντεβού απο Barber
    def bar_can():
        # Διαγραφή προηγουμένων επιλογών
        for widget in win.winfo_children():
            widget.destroy()
        # Πεδίο για το όνομα και του τηλεφώνου του Client
        tk.Label(win, text="Name:").pack()
        entry_name = tk.Entry(win)
        entry_name.pack()
        tk.Label(win, text="Phone Number:").pack()
        entry_phone = tk.Entry(win)
        entry_phone.pack()
        
        # Συνάρτηση που καλεί την συνάρτηση με της εντολές της MySQL
        def on_submit():
            # Ειδοποιήση με επιλογή συνέχειας 
            yesno = messagebox.askyesno("Appointments", "Are you sure you want to continue?")
            if yesno:
                name = entry_name.get().strip()
                phone = entry_phone.get().strip()
                if not name:
                    messagebox.showerror("Error", "Please enter the customer's name")
                    return
                if not phone:
                    messagebox.showerror("Error", "Please enter the customer's phone number")
                    return
                delClient(name, phone)
            else:
                bar_can()

        # Κουμπία επιλογών
        tk.Button(win, text="Delete Appointment", command=on_submit).pack(pady=10)
        tk.Button(win, text="Back", command=back).pack(pady=10)

    # Συνάρτηση για εφαρμογή του Barber
    def tried(myresult):
        # Έλεγχος σωστού Login Barber
        if myresult:
            for widget in win.winfo_children():
                widget.destroy()
            tk.Label(win, text="Welcome!").pack()
            tk.Button(win, text="Appointments", command=bar_app).pack(pady=20)
            tk.Button(win, text="Cancel Appointments", command=bar_can).pack(pady=20)
        else:
            messagebox.showinfo(title="Not Found", message="No matching Barber found!")
            login()

    # Εντολές MySQL για Login του Barber
    def barberLogin(name, phone, password):
        for widget in win.winfo_children():
            widget.destroy()
        mycursor = mydb.cursor()
        try:
            if name and password:
                sql = "SELECT * FROM barbers WHERE bname = %s AND pass = %s"
                mycursor.execute(sql, (name, password))
            elif phone and password:
                sql = "SELECT * FROM barbers WHERE bphonum = %s AND pass = %s"
                mycursor.execute(sql, (phone, password))
            else:
                messagebox.showinfo(title="Error", message="Please ensure that you have filled the Name or Phone and the Password boxes correctly.")
                return
            myresult = mycursor.fetchall()
            tried(myresult)
        except mysql.connector.Error as err:
            messagebox.showerror(title="Database Error", message=str(err))
            return None
    
    #  Φόρμα Login για Barber
    def login():
        for widget in win.winfo_children():
            widget.destroy()

        tk.Label(win, text="Name or Phone Number:").pack()
        namephone = tk.Entry(win)
        namephone.pack()

        tk.Label(win, text="Password: ").pack()
        password = tk.Entry(win)
        password.pack()

        def on_submit():
            user_input = namephone.get().strip()
            passw = password.get().strip()
            if not user_input or not passw:
                messagebox.showinfo(title="Error", message="Please fill all fields.")
                return
            if user_input.isdigit():
                phone = int(user_input)
                name = None
            else:
                name = user_input
                phone = None
            barberLogin(name, phone, passw)
        tk.Button(win, text="Login", command=on_submit).pack(pady=10)
        tk.Button(win, text="Back", command=back).pack(pady=10)
        
    def sunday(event):
        cal = event.widget
        try:
            selected_date_str = cal.get_date()
            if len(selected_date_str.split('/')[-1]) == 2:
                selected_date = datetime.strptime(selected_date_str, "%m/%d/%y")
            else:
                selected_date = datetime.strptime(selected_date_str, "%m/%d/%Y")
            if selected_date.weekday() == 6:
                messagebox.showerror("Closed", "We're closed on Sundays!")
                cal.selection_clear()
                return False
            return True
        except ValueError as e:
            messagebox.showerror("Error", f"Date error: {str(e)}")
            return False

    def clientLogin():
        for widget in win.winfo_children():
            widget.destroy()
        # Apt insert
        tk.Button(win, text="Make Appointment", command = ins).pack(pady=10)
        # Apt select
        tk.Button(win, text="View your Appointment", width = 20, command = sel).pack(pady=10)
        # Apt delete
        tk.Button(win, text="Delete your Appointment", width = 20, command = delt).pack(pady=10)
        # Apt update
        tk.Button(win, text="Update your Appointment", width = 20, command = upd).pack(pady=10)
        tk.Button(win, text="Back", width = 10, command=back).pack(pady=10)

    
    tk.Button(win, text="Barber Application", width= 20, command=login).pack(pady=10)
    tk.Button(win, text="Client Application", width = 20, command=clientLogin).pack(pady=10)

    def ins():
        # Καθαρισμός παραθύρου
        for widget in win.winfo_children():
            widget.destroy()

        # Ετικέτες και Πεδία
        tk.Label(win, text="Full Name: ").pack()
        entry_name = tk.Entry(win)
        entry_name.pack()

        tk.Label(win, text="Phone: ").pack()
        entry_phone = tk.Entry(win)
        entry_phone.pack()

        # Calendar with today's date
        today = datetime.now()
        cal = Calendar(win, selectmode="day",  mindate=today, maxdate=today + timedelta(days=60), weekendbackground='white', weekendforeground='black',)
        cal.bind("<<CalendarSelected>>", sunday)
        cal.pack(pady=20)

        dlabel = tk.Label(win, text="")
        dlabel.pack()

        def grab_date():
            selected_date = cal.get_date()
            month, day, year = selected_date.split('/')
            if len(year) == 2:
                year = f"20{year}"
            formatted_date = f"{year}-{int(month):02d}-{int(day):02d}"
            dlabel.config(text=formatted_date)

        # Επιλογή ημερομηνιας
        datebtn = tk.Button(win, text = "Select Date", command = grab_date)
        datebtn.pack(pady = 20)

        # Επιλογη ωρας
        tk.Label(win, text="Available Time: ").pack()
        timesel = tk.StringVar()
        selected_time_label = tk.Label(win, text="No Time Selected!")
        selected_time_label.pack(pady=5)
        
        time = ["8:00", "8:30", "9:00", "9:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30"]
        time_frame = tk.Frame(win)
        time_frame.pack()

        def selecttime(i):
            timesel.set(i)
            selected_time_label.config(text=f"Selected Time: {i}")

        for i in time:
            b = tk.Button(time_frame, text=i, command=lambda i=i: selecttime(i))
            b.pack(side='left', padx=5, pady=5)

        # Συνάρτηση που παίρνει τιμές και καλεί insert
        def on_submit():
            name = entry_name.get().strip()
            phone = entry_phone.get().strip()
            date = dlabel.cget("text")
            time = timesel.get()

            if not name:
                messagebox.showerror("Error", "Please enter your name")
                return
            if not phone:
                messagebox.showerror("Error", "Please enter your phone number")
                return
            if len(phone) < 10:
                messagebox.showerror("Error", "Please ensure your phone number is correct")
                return
            if not date or date == "No Date Selected!":
                messagebox.showerror("Error", "Please select a date.")
                return
            if not time:
                messagebox.showerror("Error", "Please select a time.")
                return
            
            insertClient(name, phone, date, time)

            win.destroy()
            GUI()

        tk.Button(win, text="Make Appointment", command=on_submit).pack(pady=10)

        tk.Button(win, text="Back", command = back).pack(pady=10)

    def sel():
        # Καθαρισμός παραθύρου
        for widget in win.winfo_children():
            widget.destroy()

        # Ετικέτες και Πεδία
        tk.Label(win, text="Full Name: ").pack()
        entry_name = tk.Entry(win)
        entry_name.pack()

        tk.Label(win, text="Phone: ").pack()
        entry_phone = tk.Entry(win)
        entry_phone.pack()

        # Συνάρτηση που παίρνει τιμές και καλεί select
        def on_submit():
            name = entry_name.get()
            phone = entry_phone.get()
            sel = selectClient(name, phone)

        tk.Button(win, text="View Appointment", command=on_submit).pack(pady=10)
        tk.Button(win, text="Back", command = back).pack(pady=10)
    
    def delt():
        # Καθαρισμός παραθύρου
        for widget in win.winfo_children():
            widget.destroy()

        # Ετικέτες και Πεδία
        tk.Label(win, text="Full Name: ").pack()
        entry_name = tk.Entry(win)
        entry_name.pack()

        tk.Label(win, text="Phone: ").pack()
        entry_phone = tk.Entry(win)
        entry_phone.pack()

        # Συνάρτηση που παίρνει τιμές και καλεί delete
        def on_submit():
            name = entry_name.get()
            phone = entry_phone.get()
            deleteClient(name, phone)

        tk.Button(win, text="Delete Appointment", command=on_submit).pack(pady=10)
        tk.Button(win, text="Back", command = back).pack(pady=10)

    def upd():
        # Καθαρισμός παραθύρου
        for widget in win.winfo_children():
            widget.destroy()

        # Ετικέτες και Πεδία
        tk.Label(win, text="Full Name: ").pack()
        entry_name = tk.Entry(win)
        entry_name.pack()

        tk.Label(win, text="Phone Number: ").pack()
        phone = tk.Entry(win)
        phone.pack()

        # Calendar with today's date
        today = datetime.now()
        cal = Calendar(win, selectmode="day",  mindate=today, maxdate=today + timedelta(days=60), weekendbackground='white', weekendforeground='black',)
        cal.bind("<<CalendarSelected>>", sunday)
        cal.pack(pady=20)

        dlabel = tk.Label(win, text="")
        dlabel.pack()

        def grab_date():
            selected_date = cal.get_date()
            month, day, year = selected_date.split('/')
            if len(year) == 2:
                year = f"20{year}"
            formatted_date = f"{year}-{int(month):02d}-{int(day):02d}"
            dlabel.config(text=formatted_date)

        # Επιλογή ημερομηνιας
        datebtn = tk.Button(win, text = "Select New Date", command = grab_date)
        datebtn.pack(pady = 20)

        # Επιλογη ωρας
        tk.Label(win, text="Sected New Time: ").pack()
        timesel = tk.StringVar()
        selected_time_label = tk.Label(win, text="No Time Selected!")
        selected_time_label.pack(pady=5)
        
        time = ["8:00", "8:30", "9:00", "9:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30"]
        time_frame = tk.Frame(win)
        time_frame.pack()

        def selecttime(i):
            timesel.set(i)
            selected_time_label.config(text=f"Selected New Time: {i}")

        for i in time:
            b = tk.Button(time_frame, text=i, command=lambda i=i: selecttime(i))
            b.pack(side='left', padx=5, pady=5)

        # Συνάρτηση που παίρνει τιμές και καλεί update
        def on_submit():
            name = entry_name.get().strip()
            name = phone.get().strip()
            date = dlabel.cget("text")
            time = timesel.get()

            if not name:
                messagebox.showerror("Error", "Please enter your name")
                return
            if not phone:
                messagebox.showerror("Error", "Please enter your phone number")
                return
            if not date or date == "No Date Selected!":
                messagebox.showerror("Error", "Please select a date.")
                return
            if not time:
                messagebox.showerror("Error", "Please select a time.")
                return
            updateClient(name, phone, date, time)
        
        tk.Button(win, text="Update Appointment", command=on_submit).pack(pady=10)
        tk.Button(win, text="Back", command = back).pack(pady=10)

    win.mainloop()

if __name__ == "__main__":
    GUI()