from tkinter import *
import datetime
from PIL import ImageTk, Image, ImageOps
import cv2
from threading import *
import time

root = Tk()
root.title('WhiteBlue Application')
root.geometry('{}x{}'.format(800, 480))

image = Image.open("/home/gnaneshwar/Downloads/app/images/logo.jpeg")
image = image.resize((150, 40), Image.ANTIALIAS)
img1 = ImageTk.PhotoImage(image)

image_rc = Image.open("/home/gnaneshwar/Downloads/app/images/red.png")
image_rc = image_rc.resize((30, 30), Image.ANTIALIAS)
img_rc = ImageTk.PhotoImage(image_rc)

image_gc = Image.open("/home/gnaneshwar/Downloads/app/images/green.png")
image_gc = image_gc.resize((30, 30), Image.ANTIALIAS)
img_gc = ImageTk.PhotoImage(image_gc)

image_d = Image.open("/home/gnaneshwar/Downloads/app/images/download.png")
image_d = image_d.resize((80, 80), Image.ANTIALIAS)
img_d = ImageTk.PhotoImage(image_d)

cap = cv2.VideoCapture(0)

def update(det, emp):
    if det == True:
        img_color.imgtk = img_gc
        img_color.configure(image=img_gc)

        emp_id = emp[0]
        emp_name = emp[1]
        entry_time = emp[2]
        txt = "Emp ID: "+str(emp_id)+"\nEmp Name: "+emp_name+"\nCheck In: "+entry_time
    
        emp_details.configure(text= txt)
        status.configure(text="Door is Open!\nProceed to Enter.", fg='#080', font= ('Aerial', 12, 'bold'))
    else:
        img_color.imgtk = img_gc
        img_color.configure(image=img_rc)
    
        emp_id = ""
        emp_name = ""
        entry_time = ""
        txt = "Emp ID: "+str(emp_id)+"\nEmp Name: "+emp_name+"\nCheck In: "+entry_time
    
        emp_details.configure(text= txt)
        status.configure(text="Unable to recognize. Please contact helpline - \n+91 11111 00000", fg='#f00', font= ('Aerial', 12))

def detect_face(img):
    face_cascade = cv2.CascadeClassifier('data/lbpcascade_frontalface.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5);
    if (len(faces) == 0):
        return False
    
    (x, y, w, h) = faces[0]
    #time.sleep(5)
    cv2.imwrite('new.png',img[y:y+w, x:x+h])
    return True

key = True    
def ex1():    
    time.sleep(2)
    while True: 
        global key
        c = datetime.datetime.now()
        k = c.strftime("%d-%B-%Y %A %-H:%M:%-S")
        e = [56,"Vela",k]
        if key == True:
            global frame
            var = detect_face(frame)
            if var == True:
                update(var,e)
                img = Image.open("/home/gnaneshwar/Desktop/tkinter_opencv/new.png")
                image_tk = img.resize((80, 80), Image.ANTIALIAS)
                img_tk = ImageTk.PhotoImage(image_tk)
                detect.imgtk = img_tk
                detect.configure(image=img_tk)
            else:
                update(var,e)
                img = Image.open("/home/gnaneshwar/Downloads/app/images/download.png")
                image_tk = img.resize((80, 80), Image.ANTIALIAS)
                img_tk = ImageTk.PhotoImage(image_tk)
                detect.imgtk = img_tk
                detect.configure(image=img_tk)
        else:
            break
        

def video_stream():
    c = datetime.datetime.now()
    k = c.strftime("%d-%B-%Y %A %-H:%M:%-S")
    time1.configure(text=k)
    global frame
    _, frame = cap.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    image = img.resize((400, 330), Image.ANTIALIAS)
    image = ImageOps.mirror(image)
    imgtk = ImageTk.PhotoImage(image)
    
    live_video.imgtk = imgtk
    live_video.configure(image=imgtk)
    live_video.after(10, video_stream) 

t1 = Thread(target = video_stream)
t2 = Thread(target = ex1)

def video_thread():   
    t1.start()

def detect_thread():
    t2.start()   
	
top_frame = Frame(root, bg='white')
center = Frame(root, bg='white')
bottom = Frame(root, bg='white', relief=RIDGE,borderwidth=2)

root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

top_frame.grid(row=0, sticky="nsew")
center.grid(row=1, sticky="nsew")
bottom.grid(row=3, sticky="nsew")

top_frame.grid_rowconfigure(0, weight=1)
top_frame.grid_columnconfigure(1, weight=1)

top_left = Frame(top_frame, bg='white', width=200, height=50)
top_mid = Frame(top_frame, bg='white', width=400, height=50)
top_right = Frame(top_frame, bg='white', width=200, height=50)

logo = Label(top_mid, image = img1,borderwidth=0)
logo.pack(fill=None, expand=True)

time1 = Label(top_right, text = "Time", bg='white', borderwidth=0)
time1.pack(fill=None, expand=True, padx=5, pady=5)

top_left.grid(row=0, column=0, sticky="ns")
top_mid.grid(row=0, column=1, sticky="nesw")
top_right.grid(row=0, column=2, sticky="nsew")

center.grid_rowconfigure(0, weight=1)
center.grid_columnconfigure(1, weight=1)

ctr_left = Frame(center, bg='white', width=200, height=330)
ctr_mid = Frame(center, bg='white', width=400, height=330)
ctr_right = Frame(center, bg='white', width=200, height=330)

live_video = Label(ctr_mid)
live_video.pack(fill=None, expand=True,padx=5, pady=5)

ctr_left.grid(row=0, column=0, sticky="ns")
ctr_mid.grid(row=0, column=1, sticky="nsew")
ctr_right.grid(row=0, column=2, sticky="ns")

bottom.grid_rowconfigure(0, weight=1)
bottom.grid_columnconfigure(2, weight=1)
bottom.grid_columnconfigure(3, weight=1)

#borderwidth=1, relief=RIDGE
btm_left = Frame(bottom, bg='white', width=130, height=130)
btm_mid1 = Frame(bottom, bg='white', width=130, height=130)
btm_mid2 = Frame(bottom, bg='white', width=200, height=130)
btm_right = Frame(bottom, bg='white', width=200, height=130)

detect = Label(btm_left, image = img_d,borderwidth=0)
detect.pack(fill=None, expand=True, padx=30, pady=5)

img_color = Label(btm_mid1, image = img_rc,borderwidth=0)
img_color.pack(fill=None, expand=True, padx=30, pady=5)

emp_details= Label(btm_mid2, justify="left", wraplength=230, bg='white',text= "Emp ID: \nEmp Name: \nCheck In: ", font= ('Aerial', 10))
emp_details.pack(fill=BOTH, expand=True)

status= Label(btm_right, justify="left", wraplength=230, bg='white',text= "Unable to recognise the face, please contact the admin", font= ('Aerial', 10))
status.pack(fill=BOTH, expand=True)

btm_left.grid(row=0, column=0, sticky="nsew")
btm_mid1.grid(row=0, column=1, sticky="nsew")
btm_mid2.grid(row=0, column=2, sticky="nsew")
btm_right.grid(row=0, column=3, sticky="nsew")

def on_closing():
    global key
    key = False
    cap.release()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

video_thread()
detect_thread()
root.mainloop()
