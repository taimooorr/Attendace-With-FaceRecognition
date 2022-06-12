import datetime
from turtle import goto
import cv2
import sys
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk,ImageDraw, ImageFont
import face_recognition
import pandas as pd

cap = cv2.VideoCapture(0)
capWidth = cap.get(3)
capHeight = cap.get(4)
success, frame = cap.read()
cancel = False
def Capture(event = 0):
    for i in range(10):
        return_value,image=cap.read()
        print(return_value,image.shape)
        cv2.imwrite('PicTaken/photo'+str(i)+'.jpg',image)

    global cancel, button, button1, button2
    cancel = True

    button.place_forget()
    buttonA.place_forget()
    button1 = Button(mainWindow, text="Go for Recognition", command=FaceRecognition)
    button2 = Button(mainWindow, text="Try Again", command=resume)
    button1.place(anchor=CENTER, relx=0.2, rely=0.95, width=150, height=40)
    button2.place(anchor=CENTER, relx=0.8, rely=0.95, width=150, height=40)
    button1.focus()
#Face Recognition Modules



def FaceRecognition(event = 0):
    uk=face_recognition.load_image_file('PicTaken/photo5.jpg')
    fnt=ImageFont.truetype('Pillow/Tests/fonts/calibri',60)
    ef= pd.read_csv('mycsv.csv')
    stuNo=list(ef['Roll Number'])
    Fname=list(ef['First Name'])
    Lname=list(ef['Last Name'])
    plocation=list(ef['Photo Location'])
    n=len(stuNo)
    stu=[]
    stu_encode=[]
    for i in range(n):
        stu.append(face_recognition.load_image_file(plocation[i],'RGB'))
        stu_encode.append(face_recognition.face_encodings(stu[i])[0])
    def identity_student(photo):
        try:
            uk_encode=face_recognition.face_encodings(photo)[0]
        except IndexError as e:
            messagebox.showinfo("Failed Encoding ","TryAgain! Please.")
            goto = resume(event=1)
        found = face_recognition.compare_faces(stu_encode,uk_encode,tolerance=0.5)
        print(found)
        index=-1
        try:
            for i in range(n):
                if found[i]:
                    index=i
            return(index)
        except IndexError:
            messagebox.showinfo("Something WentWrong ","TryAgain! Please.")
            goto = resume(event=1)
    stu_index = identity_student(uk)
    if(stu_index !=-1):
        x=str(datetime.datetime.now())
        sno=str(stuNo[stu_index])
        f=Fname[stu_index]
        l=Lname[stu_index]
        ar="\n"+sno+" "+f+" "+l+" "+x
        f=open("Attendace.txt","a")
        f.write(ar)
        f.close()
        messagebox.showinfo("Recognized","Apki Attendace Lag Gai Hai")
    pil_uk=Image.fromarray(uk)
    draw=ImageDraw.Draw(pil_uk)
    fnt=ImageFont.truetype('Pillow/Tests/fonts/calibri',30)
    if stu_index== -1:
        name="Face Not Recognized"
    else:
        name=Fname[stu_index]+" "+Lname[stu_index]+ " Reg# :" +sno
    x=100
    y=uk.shape[0]-120
    draw.text((x,y),name,font=fnt,fill=(255,0,0))
    pil_uk.show()
    resume(event=1)



#Resume Function IF Pic is Taken Wrongly  or When Recognition Models Run then it is called in end FOR Next user
def resume(event = 0):
    global button1, button2, button, lmain, cancel
    cancel = False

    button1.place_forget()
    button2.place_forget()

    mainWindow.bind('<Return>', Capture)
    button.place(bordermode=INSIDE, relx=0.5, rely=0.95, anchor=CENTER, width=90, height=40)
    buttonA.place(bordermode=INSIDE, relx=0.91, rely=0.12, anchor=CENTER, width=100, height=40)
    lmain.after(10, show_frame)
#Attendace Record in new Window#

def AttendanceRecord():
    mainWindow.withdraw()
    AttendanceRecord.newWindow = Toplevel(mainWindow)
    AttendanceRecord.newWindow.title("Attendance Record")
    AttendanceRecord.newWindow.geometry("950x750")
    AttendanceRecord.newWindow.resizable(width=False,height=False)
    Label(AttendanceRecord.newWindow,text ="Attendance Record").pack()
    tf = Text(AttendanceRecord.newWindow,width=600,height=600,font=('Calibri',20))
    tf.pack(pady=20)
    text_file = open("Attendace.txt",'r')
    Record =text_file.read()
    tf.insert(END,tf)
    text_file.close()
    buttonA = Button(AttendanceRecord.newWindow, text="Back",command= back)
    buttonA.place(bordermode=INSIDE, relx=0.91, rely=0.12, anchor=CENTER, width=100, height=40)

def back():
    AttendanceRecord.newWindow.destroy()
    mainWindow.deiconify()




#Main Windows and TakePicture Button

mainWindow = Tk()
mainWindow.title('Attendace With Face Recognition')
mainWindow.resizable(width=False, height=False)
mainWindow.bind('<Escape>', lambda e: mainWindow.quit())


#Main Windows Button
lmain = Label(mainWindow, compound=CENTER, anchor=CENTER, relief=RAISED)
button = Button(mainWindow, text="Take Picture", command=Capture)
buttonA = Button(mainWindow, text="Attendace Record", command=AttendanceRecord)
lmain.pack()
button.place(bordermode=INSIDE, relx=0.5, rely=0.95, anchor=CENTER, width=90, height=40)
buttonA.place(bordermode=INSIDE, relx=0.91, rely=0.12, anchor=CENTER, width=100, height=40)



def show_frame():
    global cancel, prevImg, button
    _, frame = cap.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

    prevImg = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=prevImg)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    if not cancel:
        lmain.after(10, show_frame)
show_frame()
mainWindow.mainloop()