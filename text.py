from Tkinter import *
import tkFileDialog
#import os
import MySQLdb

master = Tk()
l=[]
#tkinter function to call for dialog box
def callback():
    path = tkFileDialog.askopenfilename()
    #print(path)
    l.append(path)
    e.insert(0,path)
#box attributes
w = Label(master, text="File Path:")
e = Entry(master,text="")
b = Button(master,text="Browse", command = callback)

w.pack(side=LEFT)
e.pack(side=LEFT)
b.pack(side=LEFT)

master.mainloop()
k=l[0]
#image is send in bit format 
{"Content-Type": "application/octet-stream"}
import requests 
#requests library for fetch json from the api 
image_path = k
#microsoft api for text recognition
vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/"
text_recognition_url = vision_base_url + "RecognizeText"
image_data = open(image_path, "rb").read()
headers    = {'Ocp-Apim-Subscription-Key': "dc4d49bb082846a4ac431016a11f99ae", 
              "Content-Type": "application/octet-stream" }
params     = {'handwriting':True}
#response from api
response   = requests.post(text_recognition_url, 
                           headers=headers, 
                           params=params, 
                           data=image_data)
response.raise_for_status()
operation_url = response.headers["Operation-Location"]
import time

analysis = {}
while not "recognitionResult" in analysis:
    response_final = requests.get(response.headers["Operation-Location"], headers=headers)
    analysis       = response_final.json()
    time.sleep(1)
#image is read in form of polygons
polygons = [(line["boundingBox"], line["text"]) for line in analysis["recognitionResult"]["lines"]]
list1=[]
#appends names into the list
for p in polygons:
    list1.append(p[1])
list2=[]
list3=[]
for i in list1:
    j=i.split(" ")
    list2.append(j[0])
    list3.append(j[1])

present=0
absent=0
listtotal=[]
listtotal1=[]
#loads attendance into the list
#counts attendance i.e prersent and absent
for i in list3:
    for j in range(0,len(i)):
        if(i[j]=='P' or i[j]=='p'):
            present=present+1
        else:
            absent=absent+1
    listtotal.append(present)
    listtotal1.append(absent)
    present=0
    absent=0
print listtotal
print listtotal1
total=[]
#calculates attendance
for i in range(0,len(listtotal)):
    total.append((listtotal[i] * 100 )/ (listtotal[i] + listtotal1[i]))
    

for i in total:
    print i
# Open database connection
db = MySQLdb.connect("localhost","root","","attendance" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to INSERT a record into the database.
for i in range(0,len(list2)):
    sql = """INSERT INTO STUDENTS(name,Percentage,Present,Absent)VALUES(""" + "'"  +  list2[i]  +   "',"  +  "'" +  str(total[i]) +  "'," + "'" + str(listtotal[i]) + "'," +  "'" + str(listtotal1[i]) + "'"  + ")"
    try:
       # Execute the SQL command
       cursor.execute(sql)
       # Commit your changes in the database
       db.commit()
    except:
       # Rollback in case there is any error
       db.rollback()

# disconnect from server
db.close()
print('Done')
