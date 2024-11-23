import tkinter as tk
from tkinter import ttk
import json
swaping = False
try:
    with open('censusDict.json', 'r') as file:
        testIfDict = json.load(file)
        if type(testIfDict) == dict:
            print('sure')
            data = testIfDict


except:
    data = {'NAME': 'county name', 'B01002_001E': 'Age above avg'}
dataAsString = ''
for i, e in data.items():
    dataAsString = dataAsString + i + ' : ' + e + '\n'

def writeToFile():
    with open('censusDict.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False)
    dataAsString = ''
    for i,e in data.items():
        dataAsString = dataAsString + i + ' : ' + e + '\n'
    print('saved', data)
    thedata['text']= dataAsString


def on_select(event):
    selected_item = combo_box.get()
    destinationtextfeld.delete(0, 'end')
    destinationtextfeld.insert(0, data[combo_box.get()])

def submit():
    data[e1.get()] = e2.get()
    combo_box.config(values=list(data.keys()))
    combo_box.set(list(data.keys())[-1])
    destinationtextfeld.delete(0, 'end')
    destinationtextfeld.insert(0, data[combo_box.get()])
    e1.delete(0,'end')
    e1.insert(0, e3.get())
    e2.delete(0, 'end')
    e2.insert(0, e4.get())
    writeToFile()

def copyTime():
    e1.delete(0,'end')
    e1.insert(0, e3.get())
    e2.delete(0, 'end')
    e2.insert(0, e4.get())

def newEntry():
    top.state(newstate='normal')
    top.attributes('-topmost', 'true')
    top.lift()



def deleteEntry():
    data.pop(combo_box.get())
    combo_box.config(values=list(data.keys()))
    combo_box.config(values=list(data.keys()))
    combo_box.set(list(data.keys())[-1])
    destinationtextfeld.delete(0, 'end')
    destinationtextfeld.insert(0, data[combo_box.get()])

def updateEntry():
    data[combo_box.get()]= destinationtextfeld.get()
    combo_box.config(values=list(data.keys()))
    writeToFile()

root = tk.Tk()
root.title("Steven's Dictionary builder")

thedata = tk.Label(root, text=dataAsString)
thedata.pack(pady=10, side='right')

deletebutton = tk.Button(root, text= 'new entry', command=newEntry)
deletebutton.pack(pady=10)

# Create a label
label = tk.Label(root, text="Selected Item: ")
label.pack(pady=10)

# Create a Combobox widget
combo_box = ttk.Combobox(root, values=list(data.keys()))
combo_box.pack(pady=5)

# Set default value
combo_box.set(list(data.keys())[0])

# Bind event to selection
combo_box.bind("<<ComboboxSelected>>", on_select)

top = tk.Toplevel(root)
tk.Label(top, text='census data name').grid(row=1)
tk.Label(top, text='column name').grid(row=2)
tk.Label(top, text='notepad').grid(row=0, column=2)
e1 = tk.Entry(top)
e2 = tk.Entry(top)
e3 = tk.Entry(top)
e4 = tk.Entry(top)
e1.grid(row=1, column=1)
e2.grid(row=2, column=1)
e3.grid(row=1, column=3)
e4.grid(row=2, column=3)
submitEntryButton = tk.Button(top, text='submit', command=submit)
submitEntryButton.grid(row=3, column=1)
closeEntryButton = tk.Button(top, text='close', command=lambda:top.state(newstate='withdrawn'))
closeEntryButton.grid(row=0, column=3)
copyEntryButton = tk.Button(top, text='<copy<', command=copyTime)
copyEntryButton.grid(row=1,column=2)
top.state(newstate='withdrawn')


destinationtextfeld = tk.Entry(root, textvariable=data[combo_box.get()])
destinationtextfeld.insert(0, data[combo_box.get()])
destinationtextfeld.pack()

updatebutton = tk.Button(root, text= 'update entry', command=updateEntry)
updatebutton.pack(pady=10)


deletebutton = tk.Button(root, text= 'delete entry', command=deleteEntry)
deletebutton.pack(pady=20)






root.mainloop()
