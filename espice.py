# importing libraries
import datetime
from tkinter import *
import tkinter.messagebox as mb
from tkinter import ttk
import sqlite3

# Creating the universal font variables
headlabelfont = ("Noto Sans CJK TC", 15, 'bold')
labelfont = ('Garamond', 14)
entryfont = ('Garamond', 12)

# Connecting to the Database where all information will be stored
connector = sqlite3.connect('SchoolManagement.db')
cursor = connector.cursor()
connector.execute(
"CREATE TABLE IF NOT EXISTS SCHOOL_MANAGEMENT (STUDENT_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, NAME TEXT, EMAIL TEXT, PHONE_NO TEXT, GENDER TEXT, ADD_NUMBER TEXT, CLASS TEXT, SECTION TEXT)"
)
connector.execute(
"CREATE TABLE IF NOT EXISTS AWARDS_HISTORY (HISTORY_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, NAME TEXT,  COMP_NAME TEXT, COMP_TYPE TEXT,YEAR TEXT, PRIZE TEXT, ADD_NUMBER TEXT)"
)

# Creating the functions
def reset_fields():
   global name_strvar, email_strvar, contact_strvar, gender_strvar, dob,class_strvar,section_strvar
   for i in ['name_strvar', 'email_strvar', 'contact_strvar', 'gender_strvar','class_strvar','section_strvar']:
       exec(f"{i}.set('')")
def reset_form():
   global tree
   tree.delete(*tree.get_children())
   global awardtree
   awardtree.delete(*awardtree.get_children())
   reset_fields()
def display_records():
   tree.delete(*tree.get_children())
   curr = connector.execute('SELECT * FROM SCHOOL_MANAGEMENT')
   data = curr.fetchall()
   for records in data:
       tree.insert('', END, values=records)

#def display_records_awards():
def add_record():
   global name_strvar, email_strvar, contact_strvar, gender_strvar, dob,class_strvar,section_strvar
   name = name_strvar.get()
   email = email_strvar.get()
   contact = contact_strvar.get()
   gender = gender_strvar.get()
   DOB = dob.get()
   class1 = class_strvar.get()
   section = section_strvar.get()
   if not name or not email or not contact or not gender or not DOB or not class1 or not section:
       mb.showerror('Error!', "Please fill all the missing fields!!")
   else:
       try:
           connector.execute(
           'INSERT INTO SCHOOL_MANAGEMENT (NAME, EMAIL, PHONE_NO, GENDER, ADD_NUMBER,CLASS,SECTION) VALUES (?,?,?,?,?,?,?)', (name, email, contact, gender, DOB, class1,section)
           )
           connector.commit()
           mb.showinfo('Record added', f"Record of {name} was successfully added")
           reset_fields()
           display_records()
       except mysql.connector.Error as err:
           print(err)
           mb.showerror('Wrong type', 'The type of the values entered is not accurate. Pls note that the contact field can only contain numbers')
def remove_record():
   if not tree.selection():
       mb.showerror('Error!', 'Please select an item from the database')
   else:
       current_item = tree.focus()
       values = tree.item(current_item)
       selection = values["values"]
       tree.delete(current_item)
       connector.execute('DELETE FROM SCHOOL_MANAGEMENT WHERE STUDENT_ID=%d' % selection[0])
       connector.commit()
       mb.showinfo('Done', 'The record you wanted deleted was successfully deleted.')
       display_records()
def view_record():
   global name_strvar, email_strvar, contact_strvar, gender_strvar, dob, class_strvar,section_strvar
   current_item = tree.focus()
   values = tree.item(current_item)
   selection = values["values"]
   name_strvar.set(selection[1]); email_strvar.set(selection[2])
   contact_strvar.set(selection[3]); gender_strvar.set(selection[4])
   dob.set(selection[5]); stream_strvar.set(selection[6])
   class_strvar.set(selection[8]);section_strvar.set(selection[9])
def add_award_record(prizeyear_strvar,compname_strvar,award_strvar,category_strvar):
   global name_strvar, email_strvar, contact_strvar, gender_strvar, dob, class_strvar,section_strvar
   current_item = tree.focus()
   values = tree.item(current_item)
   selection = values["values"]
   name= selection[1]
   studentid =  selection[3]
   dob = selection[5]
   if not name:
       mb.showerror('Error!', "Please fill all the missing fields!!")
   else:
       try:
           connector.execute(
           'INSERT INTO AWARDS_HISTORY (ADD_NUMBER, NAME, COMP_NAME, COMP_TYPE,YEAR, PRIZE) VALUES (?,?,?,?,?,?)', (dob, name, compname_strvar,      category_strvar,prizeyear_strvar,award_strvar)
           )
           connector.commit()
           mb.showinfo('Record added', f"Record of {name} was successfully added")
           reset_fields()
           display_records()
       except mysql.connector.Error as err:
           print(err)
           mb.showerror('Wrong type', 'The type of the values entered is not accurate. Pls note that the contact field can only contain numbers')

def dashboard():
  curr = connector.execute('SELECT COUNT(*) FROM SCHOOL_MANAGEMENT')
  data = curr.fetchall()
  for i in range(len(data)):
     totalPeopleCount = str(data[i][0])
     
  curr = connector.execute('SELECT COUNT(*) FROM AWARDS_HISTORY WHERE PRIZE NOT IN ("Participation")')
  data = curr.fetchall()
  for i in range(len(data)):
     totalAwardsCount = str(data[i][0])
     
  curr = connector.execute('SELECT DISTINCT (NAME) FROM AWARDS_HISTORY WHERE PRIZE IN ("First") Order by YEAR DESC')
  data = curr.fetchall()
  for i in range(len(data)):
     studentPerformerName = str(data[i][0])
     
  newDashboard= Toplevel(main)
  newDashboard.title("Dashboard for Teacher")
  newDashboard.geometry("1366x768")
  newDashboard.state('zoomed')
  p1 = PhotoImage(file = 'espice_logo.png')
  newDashboard.iconphoto(False, p1)
  #Label(newDashboard, font=headlabelfont, bg='blue',text="Dashboard for Espice Club").pack(side=TOP, fill=X)
  # ==============================================================================
 # ================== HEADER ====================================================
 # =============================================================================
  newDashboard.header = Frame(newDashboard, bg='#009df4')
  newDashboard.header.place(x=200, y=0, width=1200, height=60)
  newDashboard.logout_text = Button(newDashboard.header, text="Logout", bg='#32cf8e', font=("", 13, "bold"), bd=0, fg='white', cursor='hand2', activebackground='#32cf8e')
  newDashboard.logout_text.place(x=950, y=15)
 # ==============================================================================
 # ================== SIDEBAR ===================================================
 # ==============================================================================
  newDashboard.sidebar = Frame(newDashboard, bg='#ffffff')
  newDashboard.sidebar.place(x=0, y=0, width=200, height=450)
 # logo
  newDashboard.logoImage = PhotoImage(file='admin.png')
  newDashboard.logo = Label(newDashboard.sidebar, image=newDashboard.logoImage, bg='#ffffff')
  newDashboard.logo.place(x=30, y=150)
  newDashboard.espice_logoImage = PhotoImage(file='elogo.png')
  newDashboard.espice_logo = Label(newDashboard.sidebar, image=newDashboard.espice_logoImage)
  newDashboard.espice_logo.place(x=30, y=280)

   # Name of brand/person
  newDashboard.brandName = Label(newDashboard.sidebar, text='Admin', bg='#ffffff', font=("", 15, "bold"))
  newDashboard.brandName.place(x=80, y=320)    
# =============================================================================
# ============= BODY ==========================================================
# =============================================================================
  newDashboard.heading = Label(newDashboard, text='Dashboard', font=("", 15, "bold"), fg='#0064d3', bg='#eff5f6')
  newDashboard.heading.place(x=210, y=70)

  # body frame 1
  newDashboard.bodyFrame1 = Frame(newDashboard, bg='#ffffff')
  newDashboard.bodyFrame1.place(x=228, y=110, width=650, height=350)

   # body frame 2
  newDashboard.bodyFrame2 = Frame(newDashboard, bg='#009aa5')
  newDashboard.bodyFrame2.place(x=40, y=495, width=250, height=200)

    # body frame 3
  newDashboard.bodyFrame3 = Frame(newDashboard, bg='#e21f26')
  newDashboard.bodyFrame3.place(x=320, y=495, width=250, height=200)

    # body frame 4
  newDashboard.bodyFrame4 = Frame(newDashboard, bg='#ffcb1f' )
  newDashboard.bodyFrame4.place(x=600, y=495, width=250, height=200)
    
   # body frame 5
  newDashboard.bodyFrame5 = Frame(newDashboard)
  newDashboard.bodyFrame5.place(x=930, y=110, width=500, height=400)
  newDashboard.earningsIcon_image = PhotoImage(file='AwardCategory.png')
  newDashboard.earningsIcon = Label(newDashboard.bodyFrame5, image=newDashboard.earningsIcon_image)
  newDashboard.earningsIcon.place(x=0, y=0)
    # body frame 6
  newDashboard.bodyFrame6 = Frame(newDashboard)
  newDashboard.bodyFrame6.place(x=930, y=400, width=500, height=400)
  newDashboard.schoolIcon_image = PhotoImage(file='AwardsSchool.png')
  newDashboard.schoolIcon = Label(newDashboard.bodyFrame6, image=newDashboard.schoolIcon_image)
  newDashboard.schoolIcon.place(x=0, y=0)
# =============================================================================
# ============= BODY ==========================================================
# =============================================================================
  Label(newDashboard.bodyFrame1, font=headlabelfont, bg='blue',text="Yearly Report of Achievement").pack(side=TOP, fill=X)
  awardtree = ttk.Treeview(newDashboard.bodyFrame1, height=100, selectmode=BROWSE,
                   columns=("Name", "Competition", "Category","Year","Prize","Admission Number"))
  X_scroller = Scrollbar(awardtree, orient=HORIZONTAL, command=awardtree.xview)
  Y_scroller = Scrollbar(awardtree, orient=VERTICAL, command=awardtree.yview)
  X_scroller.pack(side=BOTTOM, fill=X)
  Y_scroller.pack(side=RIGHT, fill=Y)
  awardtree.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)
  awardtree.heading('Name', text='Name', anchor=CENTER)
  awardtree.heading('Competition', text='Competition', anchor=CENTER)
  awardtree.heading('Category', text='Category', anchor=CENTER)
  awardtree.heading('Prize', text='Prize', anchor=CENTER)
  awardtree.heading('Year', text='Year', anchor=CENTER)
  awardtree.heading('Admission Number', text='Admission Number', anchor=CENTER)
  awardtree.column('#0', width=30, stretch=NO, anchor=CENTER)
  awardtree.column('#1', width=100, stretch=NO, anchor=CENTER)
  awardtree.column('#2', width=200, stretch=NO, anchor=CENTER)
  awardtree.column('#3', width=100, stretch=NO, anchor=CENTER)
  awardtree.column('#4', width=50, stretch=NO, anchor=CENTER)
  awardtree.column('#5', width=50, stretch=NO, anchor=CENTER)
  awardtree.place(y=30, relwidth=1, relheight=0.9, relx=0)
  awardtree.delete(*awardtree.get_children())
  curr = connector.execute('SELECT NAME,  COMP_NAME, COMP_TYPE,YEAR, PRIZE , ADD_NUMBER  FROM AWARDS_HISTORY WHERE PRIZE NOT IN ("Participation") Order by YEAR DESC ,                     prize ASC')
  data = curr.fetchall()
  for records in data:
       awardtree.insert('', END, values=records)

# Body Frame 2
  newDashboard.total_people = Label(newDashboard.bodyFrame2, text=totalPeopleCount, bg='#009aa5', font=("", 25, "bold"))
  newDashboard.total_people.place(x=100, y=100)
  newDashboard.totalPeopleImage = PhotoImage(file='left-icon.png')
  newDashboard.totalPeople = Label(newDashboard.bodyFrame2, image=newDashboard.totalPeopleImage, bg='#009aa5')
  newDashboard.totalPeople.place(x=180, y=0)
  newDashboard.totalPeople_label = Label(newDashboard.bodyFrame2, text="Total Students", bg='#009aa5', font=("", 12, "bold"),fg='white')
  newDashboard.totalPeople_label.place(x=5, y=5)
 
# Body Frame 3
  newDashboard.people_award = Label(newDashboard.bodyFrame3, text=totalAwardsCount, bg='#e21f26', font=("", 25, "bold"))
  newDashboard.people_award.place(x=100, y=100)
  newDashboard.LeftImage = PhotoImage(file='earn3.png')
  newDashboard.Left = Label(newDashboard.bodyFrame3, image=newDashboard.LeftImage, bg='#e21f26')
  newDashboard.Left.place(x=180, y=0)
  newDashboard.people_award = Label(newDashboard.bodyFrame3, text="Total Awards", bg='#e21f26', font=("", 12, "bold"), fg='white')
  newDashboard.people_award.place(x=5, y=5)
    
# Body Frame 4
  newDashboard.best_student = Label(newDashboard.bodyFrame4, text=studentPerformerName, bg='#ffcb1f', font=("", 25, "bold"))
  newDashboard.best_student.place(x=10, y=100)
  newDashboard.studentImage = PhotoImage(file='award.png')
  newDashboard.student = Label(newDashboard.bodyFrame4, image=newDashboard.studentImage, bg='#ffcb1f')
  newDashboard.student.place(x=180, y=10)
  newDashboard.best_student_label = Label(newDashboard.bodyFrame4, text="Student Performer", bg='#ffcb1f', font=("", 12, "bold"),fg='white')
  newDashboard.best_student_label.place(x=5, y=5)

def edit_record():
   global name_strvar, email_strvar, contact_strvar, gender_strvar, dob, class_strvar,section_strvar,award_strvar,prizeyear_strvar,compname_strvar,category_strvar
   current_item = tree.focus()
   values = tree.item(current_item)
   selection = values["values"]
   name_strvar.set(selection[1]); email_strvar.set(selection[2])
   contact_strvar.set(selection[3]); gender_strvar.set(selection[4])
   #dob.set(str(selection[5]))
   class_strvar.set(selection[6]);section_strvar.set(selection[7])
   new= Toplevel(main)
   new.title("Update Record for " +(selection[1]))
   new.geometry("600x400")
   p1 = PhotoImage(file = 'elogo.png')
   new.iconphoto(False, p1)
   Label(new, font=headlabelfont, bg='blue',text="Update Record for " + (selection[1]) ).pack(side=TOP, fill=X)
   new_left_frame = Frame(new, bg=lf_bg)
   new_left_frame.place(x=0, y=30, relheight=1, relwidth=1.0)
   Label(new_left_frame, text="Competition Name", font=labelfont, bg=lf_bg).grid(column = 10, row = 5, padx = 10, pady = 25)
   listbox = Listbox(new_left_frame, exportselection = False,width = 0)
   listbox.insert(1, "EXUN - DPS RK PURAM")
   listbox.insert(2, "Code Wars - DPS Vasant Kunj")
   listbox.insert(3, "WarP - DPS Mathura Road'")
   listbox.insert(4, "Synta - DPS Saket'")
   listbox.insert(5, "Core - DPS Dwarka")
   listbox.insert(6, "Tech Syndicate - Amity Gurugram")
   listbox.insert(7, "Minet - Mothers Internation School")
   listbox.grid(column=10, row=6)
   Label(new_left_frame, text=" Category", font=labelfont, bg=lf_bg).grid(column = 20, row = 5, padx = 10, pady = 25)
   categorybox = Listbox(new_left_frame, exportselection = False, width=0)
   categorybox.insert(1, "Hackathon")
   categorybox.insert(2, "Crossword")
   categorybox.insert(3, "Quiz")
   categorybox.insert(4, "Design")
   categorybox.insert(5, "Surprise")
   categorybox.insert(6, "Programming")
   categorybox.insert(7, "Movie")
   categorybox.grid(column=20, row=6)
   Label(new_left_frame, text=" Year", font=labelfont, bg=lf_bg).grid(column = 35, row = 5, padx = 10, pady = 25)
   Label(new_left_frame, text="Award", font=labelfont, bg=lf_bg).grid(column = 45, row = 5, padx = 10, pady = 25)
   yearchoosen = Listbox(new_left_frame, width=0, exportselection = False)
   yearchoosen.insert(1, "2022")
   yearchoosen.insert(2, "2023")
   yearchoosen.insert(3, "2024")
   yearchoosen.grid(column=35, row=6)
   awardchoosen = Listbox(new_left_frame, width=0, exportselection = False)
   awardchoosen.insert(1, "First")
   awardchoosen.insert(2, "Second")
   awardchoosen.insert(3, "Third")
   awardchoosen.insert(4, "Participation")
   awardchoosen.grid(column=45, row=6)
   def selected_item():
       for i in listbox.curselection():
            compname_strvar =str(listbox.get(i))
       for i in yearchoosen.curselection():
            prizeyear_strvar = yearchoosen.get(i)
       for i in awardchoosen.curselection():
            award_strvar = awardchoosen.get(i)
       for i in categorybox.curselection():
            category_strvar = categorybox.get(i)
       add_award_record(prizeyear_strvar,compname_strvar,award_strvar,category_strvar)
   Button(new_left_frame, text=' Add Record', font=labelfont,command=selected_item).grid(column = 20, row = 15, padx = 10, pady = 25)
 #  Button(new_left_frame, text=' Add Record', font=labelfont,command=add_award_record).grid(column = 20, row = 15, padx = 10, pady = 25)
def report_yearly():
   new2= Toplevel(main)
   new2.title("Yearly  Report")
   new2.geometry("700x400")
   p1 = PhotoImage(file = 'elogo.png')
   new2.iconphoto(False, p1)
   new2.resizable(0, 0)
   Label(new2, font=headlabelfont, bg='blue',text="Yearly Report of Achievement").pack(side=TOP, fill=X)
   OptionMenu(new2, class_strvar, '2022', '2023', '2024').place(x=45, rely=0.25, relwidth=0.5)
   Button(new2, text='Submit', font=labelfont, command=view_record, width=18).place(relx=0.025, rely=0.85)
   awardtree = ttk.Treeview(new2, height=100, selectmode=BROWSE,
                   columns=('HISTORY ID', "Name", "Competition", "Category","Year","Prize","Admission Number"))
   X_scroller = Scrollbar(awardtree, orient=HORIZONTAL, command=awardtree.xview)
   Y_scroller = Scrollbar(awardtree, orient=VERTICAL, command=awardtree.yview)
   X_scroller.pack(side=BOTTOM, fill=X)
   Y_scroller.pack(side=RIGHT, fill=Y)
   awardtree.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)
   awardtree.heading('HISTORY ID', text='ID', anchor=CENTER)
   awardtree.heading('Name', text='Name', anchor=CENTER)
   awardtree.heading('Competition', text='Competition', anchor=CENTER)
   awardtree.heading('Category', text='Category', anchor=CENTER)
   awardtree.heading('Prize', text='Prize', anchor=CENTER)
   awardtree.heading('Year', text='Year', anchor=CENTER)
   awardtree.heading('Admission Number', text='Admission Number', anchor=CENTER)
   awardtree.column('#0', width=0, stretch=NO)
   awardtree.column('#1', width=30, stretch=NO)
   awardtree.column('#2', width=100, stretch=NO)
   awardtree.column('#3', width=200, stretch=NO)
   awardtree.column('#4', width=100, stretch=NO)
   awardtree.column('#5', width=80, stretch=NO)
   awardtree.column('#6', width= 80, stretch=NO)
   awardtree.column('#7', width= 100, stretch=NO)
   awardtree.place(y=30, relwidth=1, relheight=0.9, relx=0)
   awardtree.delete(*awardtree.get_children())
   curr = connector.execute('SELECT * FROM AWARDS_HISTORY Order by YEAR DESC')
   data = curr.fetchall()
   for records in data:
       awardtree.insert('', END, values=records)
def report_record():
   global name_strvar, email_strvar, contact_strvar, gender_strvar, dob, stream_strvar,class_strvar,section_strvar
   current_item = tree.focus()
   values = tree.item(current_item)
   selection = values["values"]
   name_strvar.set(selection[1]); email_strvar.set(selection[2])
   contact_strvar.set(selection[3]); gender_strvar.set(selection[4])
   dob.set(selection[5])
   class_strvar.set(selection[7]);section_strvar.set(selection[8])

# Initializing the GUI window
main = Tk()
main.title('DPS Noida')
main.geometry('1000x600')
p1 = PhotoImage(file = 'DPSN_Logo.png')
main.iconphoto(False, p1)
main.resizable(0, 0)

# Creating the background and foreground color variables
lf_bg = 'MediumSpringGreen' # bg color for the left_frame
cf_bg = 'PaleGreen' # bg color for the center_frame

# Creating the StringVar or IntVar variables
name_strvar = StringVar()
class_strvar =StringVar()
email_strvar = StringVar()
contact_strvar = StringVar()
gender_strvar = StringVar()
section_strvar = StringVar()
compname_strvar = StringVar()
award_strvar = StringVar()
prizeyear_strvar = StringVar()
category_strvar =StringVar()
dob = StringVar()
awardtree = ttk.Treeview()

# Placing the components in the main window
p2=PhotoImage(file = 'elogo.png')
Label(main, font=headlabelfont, bg='blue',text="ESPICE CLUB STUDENT MANAGEMENT SYSTEM").pack(side=TOP, fill=X)

#Label.iconphoto(False, p2)
left_frame = Frame(main, bg=lf_bg)
left_frame.place(x=0, y=30, relheight=1, relwidth=0.2)
center_frame = Frame(main, bg="Gray35")
center_frame.place(relx=0.2, y=30, relheight=1, relwidth=0.6)
right_frame = Frame(main, bg=cf_bg)
right_frame.place(relx=0.8, y=30, relheight=1, relwidth=0.2)

# Placing components in the left frame
Label(left_frame, text='New Member', font=headlabelfont, bg='DarkGreen', fg='LightCyan').pack(side=TOP, fill=X)
Label(left_frame, text="Name", font=labelfont, bg=lf_bg).place(relx=0.2, rely=0.05)
Label(left_frame, text="Class", font=labelfont, bg=lf_bg).place(relx=0.2, rely=0.20)
Label(left_frame, text="Section", font=labelfont, bg=lf_bg).place(relx=0.2, rely=0.30)
Label(left_frame, text="Phone Number", font=labelfont, bg=lf_bg).place(relx=0.2, rely=0.40)
Label(left_frame, text="Admission Number", font=labelfont, bg=lf_bg).place(relx=0.2, rely=0.50)
Label(left_frame, text="Email Address", font=labelfont, bg=lf_bg).place(relx=0.2, rely=0.60)
Label(left_frame, text="Gender", font=labelfont, bg=lf_bg).place(relx=0.2, rely=0.70)
Entry(left_frame, width=19, textvariable=name_strvar, font=entryfont).place(x=20, rely=0.1)
Entry(left_frame, width=19, textvariable=contact_strvar, font=entryfont).place(x=20, rely=0.45)
Entry(left_frame, width=19, textvariable=dob, font=entryfont).place(x=20, rely=0.55)
Entry(left_frame, width=19, textvariable=email_strvar, font=entryfont).place(x=20, rely=0.65)
OptionMenu(left_frame, class_strvar, 'IX', 'X', 'XI', "XII").place(x=45, rely=0.25, relwidth=0.5)
OptionMenu(left_frame, section_strvar, 'A','B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',"J").place(x=45, rely=0.35, relwidth=0.5)
OptionMenu(left_frame, gender_strvar, 'Male', "Female").place(x=45, rely=0.78, relwidth=0.5)
Button(left_frame, text='Submit and Add Record', font=labelfont, command=add_record, width=18).place(relx=0.025, rely=0.85)

# Placing components in the right frame 
#Label(right_frame, text='Reports', font=headlabelfont, bg='DarkGreen', fg='LightCyan').pack(side=TOP, fill=X)
Button(right_frame, text='Dashboard', font=labelfont, command=dashboard, width=15).place(relx=0.1, rely=0.15)
Button(right_frame, text='Delete Record', font=labelfont, command=remove_record, width=15).place(relx=0.1, rely=0.25)
Button(right_frame, text='View Record', font=labelfont, command=view_record, width=15).place(relx=0.1, rely=0.35)
Button(right_frame, text='Reset Fields', font=labelfont, command=reset_fields, width=15).place(relx=0.1, rely=0.45)
Button(right_frame, text='Delete database', font=labelfont, command=reset_form, width=15).place(relx=0.1, rely=0.55)
Button(right_frame, text='Update Record', font=labelfont, command=edit_record, width=15).place(relx=0.1, rely=0.65)
#Button(right_frame, text='Yearly Report', font=labelfont, command=report_yearly, width=15).place(relx=0.1, rely=0.75)

# Placing components in the center frame
Label(center_frame, text='Student Records', font=headlabelfont, bg='red', fg='LightCyan').pack(side=TOP, fill=X)
tree = ttk.Treeview(center_frame, height=100, selectmode=BROWSE,
                   columns=('Student ID', "Name", "Email Address", "Contact Number", "Gender", "Admission Number","Class","Section"))
X_scroller = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
Y_scroller = Scrollbar(tree, orient=VERTICAL, command=tree.yview)
X_scroller.pack(side=BOTTOM, fill=X)
Y_scroller.pack(side=RIGHT, fill=Y)
tree.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)
tree.heading('Student ID', text='ID', anchor=CENTER)
tree.heading('Name', text='Name', anchor=CENTER)
tree.heading('Email Address', text='Email ID', anchor=CENTER)
tree.heading('Contact Number', text='Phone No', anchor=CENTER)
tree.heading('Gender', text='Gender', anchor=CENTER)
tree.heading('Admission Number', text='Admission Number', anchor=CENTER)
tree.heading('Class', text='Class', anchor=CENTER)
tree.heading('Section', text='Section', anchor=CENTER)
tree.column('#0', width=0, stretch=NO)
tree.column('#1', width=20, stretch=NO)
tree.column('#2', width=100, stretch=NO)
tree.column('#3', width=80, stretch=NO)
tree.column('#4', width=80, stretch=NO)
tree.column('#5', width=80, stretch=NO)
tree.column('#6', width=60, stretch=YES)
tree.column('#7', width= 60, stretch=NO)
tree.column('#8', width=60, stretch=NO)
tree.place(y=30, relwidth=1, relheight=0.9, relx=0)
display_records()

# Finalizing the GUI window
main.update()
main.mainloop()
