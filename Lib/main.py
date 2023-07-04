import pandas as pd
from tkinter import *
import datetime

data = pd.read_csv('C:/Users/The user/Desktop/python/FinalProject/attendance.csv')
date = None
buttons = []

def is_present(i):
    ''' מקבל אינדקס של תלמידה ומעדכן שהיא נוכחת '''
    # אם זה התלמידה הראשונה יוצרים עמודה בשם התאריך
    if not list(data.columns).__contains__(e.get()):
        global date
        date = e.get()
        data[date] = False
        data.drop('Unnamed: 0', axis=1, inplace=True)
    if data.loc[i, date] == True:
        data.loc[i, date] = False
        buttons[i].config(bg='white')
    else:
        data.loc[i, date] = True
        buttons[i].config(bg='pink')

def save_to_file():
    ''' שמירת הנתונים לקובץ CSV '''
    data.to_csv('C:/Users/The user/Desktop/python/FinalProject/attendance.csv')

def add_students_window():
    ''' פתיחת חלון להוספת תלמידים '''
    window = Toplevel()
    window.geometry("300x300+400+100")
    Label(window, text= 'הכניסי שם תלמידה:').pack()
    e = Entry(window, width=20)
    e.pack()

    Button(window, width=15, height=3, text='שמירת התלמידה', background='#ff6699',command=lambda: save_student(e.get())).pack()

def save_student(name):
    ''' שמירת התלמידה החדשה '''
    data.loc[data.shape[0], 'name'] = name
    if list(data.columns).__contains__('Unnamed: 0'):
        data.drop('Unnamed: 0', axis=1, inplace=True)
    save_to_file()
    exit()

def open_attendance_window():
    ''' פתיחת חלון נוכחות '''
    window = Toplevel()
    window.geometry("300x300+300+200")
    Label(window, text=  'תאריכי נוכחות,בחרי תאריך'  ,width=  30).pack()
    # כפתורים לפי תאריך
    for i in range(2, len(data.columns)):
        b = Button(window, text=data.columns[i], width=15, height=3, background="white", activebackground="red",
                   command=lambda d=data.columns[i]: show_attendance_date(d))
        b.pack()
    Button(window, text='אחוזי נוכחות לכל תלמידה', width=20, height=3, background="#ff4d80",
           command=open_student_attendance_window).pack()

def show_attendance_date(d):
    ''' פתיחת חלון נוכחות לפי תאריך '''
    window = Toplevel()
    window.geometry("300x400+300+100")
    for name, present in zip(data['name'], data[d]):
        if present == True or present == False:
            Label(window, text=f'name: {name} --- present: {present}').pack()

def open_student_attendance_window():
    ''' פתיחת חלון נוכחות לפי תלמידות '''
    window = Toplevel()
    window.geometry("300x300+400+100")
    window.title('אחוזי נוכחות')
    for i in range(len(data['name'])):
        p = calc_present_student(i)
        Label(window, text=f'Student: {data["name"][i]} אחוזי נוכחות : {p}').pack()

def calc_present_student(i):
    '''הפונקציה מקבלת אינדקס תלמידה ומחזירה חישוב אחוזי נוכחות לתלמידה '''
    count_present = 0
    count_all = 0
    for j in range(2, data.shape[1]):
        if data.iloc[i, j] == True:
            count_present += 1
            count_all += 1
        elif data.iloc[i, j] == False:
            count_all += 1
    return count_present / count_all

root = Tk()
root.title('נוכחות כיתה')
root.geometry("500x500+400+100")

Label(root, text='הכנסי תאריך').pack()
e = Entry(root, width=30)
e.insert(0, str(datetime.date.today().strftime('%d/%m/%Y')))
e.pack()
Label(root, text='רשימת הלמידות בכיתה, לחצו על התלמידה כדי לסמן או לבטל נוכחות').pack()
for i in range(len(data['name'])):
    b = Button(root, text=data['name'][i], width=8, height=3, background="white", activebackground="red",
               command=lambda x=i: is_present(x))
    b.pack()
    buttons.append(b)
Button(root, text='שמירה', width=8, height=3, background='#ff6699', command=save_to_file).pack()
Button(root, text='הוספת תלמידות', width=15, height=2,background='#ff4d80', command=add_students_window).pack()
Button(root, text='בדיקת נוכחות', width=15, height=2,background='#ff4d80', command=open_attendance_window).pack()

root.mainloop()