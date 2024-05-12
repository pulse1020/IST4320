import os
import shutil
import tkinter
import tkinter as tk
import threading

from PIL import Image, ExifTags
from pillow_heif import register_heif_opener
from multiprocessing import Process, cpu_count, Pool
from tkinter import Tk
from tkinter.filedialog import askdirectory
register_heif_opener()
# find main at line 150, half of this stuff is junk



#not used
def basicc():
    for entry in obj:
        name, extension = entry.path.split('.')
        if extension == 'HEIC':
            image = Image.open(entry.path)
            image.convert('RGB').save(name+'.jpg')
            os.remove(entry.path)
        elif extension == 'AAE':
            os.remove(entry.path)
        x += 1
        print(str(round((x/total)*100,2))+'%')
        return

def test():
    for entry in obj:
        print(entry.name)

def lookforfiles(path2, dest):
    obj = os.scandir(path2)
    for entry in obj:
        if entry.is_file():
            name, extension = entry.name.split('.')
            if extension == 'HEIC':
                image = Image.open(entry.path)
                image.convert('RGB').save(dest+ name + '.jpg')
            elif extension == 'AAE':
                pass
            else: shutil.copy2(entry.path, dest)
        elif entry.is_dir():
            lookforfiles(entry.path, dest)
    whenDone += 1
    print(str(round((whenDone / total) * 100, 2)) + '%')

def MoveAndConvert(entry):

    destination = "C:/Users/scpul/OneDrive/Desktop/test2/"
    if destination.endswith('/') == False:
        destination = destination + '/'
    if entry.name.split('.')[1] == 'HEIC':
        name, extension = entry.name.split('.')
        image = Image.open(entry.path)
        image.convert('RGB').save(destination + entry + '.jpg')
    else :shutil.copy(entry.path, destination)
    return entry.name







def lookforfilesmk2(path2, files = []):
    obj = os.scandir(path2)

    for entry in obj:
        if entry.is_file() and entry.name.split('.')[1] != 'AAE':
            #AllFiles.append(entry.path)
            files.append(entry.path)
        elif entry.is_dir():
            lookforfilesmk2(entry.path, files)
    obj.close()


    return files



def MoveAndConvertMk2(entry):
    try:
        if entry[0].split('.')[1] == 'HEIC':
            image = Image.open(entry[0])
            image.convert('RGB').save(entry[1]  + os.path.basename(entry[0]).split('.')[0] + entry[2]+ '.jpg')
            image.close()
            shutil.copystat(entry[0], entry[1] + os.path.basename(entry[0]).split('.')[0] + entry[2]+ '.jpg')
        else:
            x, y = os.path.basename(entry[0]).split('.')
            shutil.copy2(entry[0], entry[1] + x + entry[2] + '.'+ y)

    except:
        print('oh no')
        print(entry[1] + entry[2] +  os.path.basename(entry[0]))
    return entry[0]


def getinfo():
    path = askdirectory(title="Select Source", initialdir='C:/Users/scpul/OneDrive/Desktop/')
    destination = askdirectory(title="Select destination",initialdir='C:/Users/scpul/OneDrive/Desktop/')
    if not destination.endswith('/'):
        destination = destination + '/'
    return path, destination


def noDupes(stuff: list, destan: str) -> list:
    num = 0
#    print('stuff len' ,len(stuff))
#    whatinthe = os.scandir(destan)
    whatinthe = []
#   (\[).*(\])

    lookforfilesmk2(destan, whatinthe)
    dam = map(lambda x: os.path.basename(x).split('.')[0],whatinthe)
    okay = set(dam)
#    print(len(okay))
    for x in range(len(stuff)-1,-1,-1):
#        print(os.path.basename(thing).split('.')[0])
        if os.path.basename(stuff[x]).split('.')[0] in okay:
            #stuff.remove(x)
            stuff.pop(x)
            num += 1
    print('number of dups', num)
#    print(okay)
#    whatinthe.close()
    del whatinthe, dam, okay
    return stuff

def main2():
    sourse, dest = getinfo()

    willitwork = []
    lookforfilesmk2(sourse, willitwork)
    print('the number of files that was detected is', len(willitwork))
    noDupes(willitwork, dest)
    package = zip(willitwork, [dest]*len(willitwork))
 #   print('the number of files we need to move is', len(needstobemoved))
    print('the number of files that was detected is', len(willitwork))
    whenDone = 0
    with Pool() as pool:
        proess = pool.imap(MoveAndConvertMk2, package)
        for x in proess:
            whenDone +=1
            print(str(round(whenDone / len(willitwork) * 100, 2)) + '%', x)

def main():
    mainbox = tk.Tk()
    source = tk.StringVar()
    destination= tk.StringVar()
    willitwork = []
    colltion = False
    def getinput(): #this is called when you push the sourse button
        inputtextfeld.delete(0,'end')
        source= askdirectory(title="Select Source")
        inputtextfeld.insert(0, source)
        inputtextfeld.configure(width=len(source))
        willitwork.clear()


    def getdestination():
        destination= askdirectory(title="Select destination")
        destinationtextfeld.delete(0,'end')
        if not destination.endswith('/'):
            destination = destination + '/'
        destinationtextfeld.insert(0, destination)
        destinationtextfeld.configure(width=len(destination))
        willitwork.clear()

    def conflict_test():

        willitwork_set = set()
        nonlocal colltion
        for f in willitwork:
            willitwork_set.add(os.path.basename(f))
        if len(willitwork) != len(willitwork_set):
            colltion = True
            filesfound.config(text=f'same name files found adding Folder path to name.\n this will Deactivate the ignore same files at source. \n files found: {len(willitwork)}')
        else: colltion = False
        del willitwork_set
        return


    def find():
        source = inputtextfeld.get()
        destination = destinationtextfeld.get()
        willitwork.clear()
        lookforfilesmk2(source, willitwork)
        noDupes(willitwork, destination)
        if not destination.endswith('/'):
            destinationtextfeld.insert("end", "/")
            filesfound.config(text=f'Please do not remove the last /.\n files found: {len(willitwork)}')
        else: filesfound.config(text=f'files found: {len(willitwork)}')
        conflict_test()
        return willitwork

    def package():
        for i in willitwork:
            if colltion:
                x = str(' [' + os.path.abspath(i)\
                        .replace(inputtextfeld.get()\
                            .replace('/','\\'), '')\
                        .replace(os.path.basename(i),'')\
                        .replace('\\','-')+'] ')
            else: x = ''
            yield i, str(destinationtextfeld.get()), x


    def go_time():
        progress.pack()
        print('prossesing')
        #package = zip(willitwork, [str(destinationtextfeld.get())] * len(willitwork))
        #   print('the number of files we need to move is', len(needstobemoved))
        print('the number of files that was detected is', len(willitwork))
        whenDone = 0
        with Pool() as pool:
            proess = pool.imap(MoveAndConvertMk2, package())
            for x in proess:
                whenDone += 1
                progress.configure(text=f'{str(round(whenDone / len(willitwork) * 100, 2))} %')
                print(x)

    def submit():
        time.sleep(5)  # put your stuff here

    def help():
        top =tk.Toplevel(mainbox)
        top_label = tk.Label(top, text='this is a program that will copy most* of '
                                       'the files in a folder tree (source) and place it in a single folder (destionation).\n\n'
                                       'once you select the top of the folder tree (source) and the destionation foulder,\n '
                                       'the set buttion will scan the two directories and find what files need to be copied. \n\n'
                                       'if there is files in the destionation, the program will not bother copting files with the same name. \n'
                                       'unless  there is two or files with the same name in the source folder tree.\n'
                                       'if that is the case, then the program will add the destionation to the name of each file. \n'
                                       'this will disable the feature that will stop the files from being copyed if they exist in the destionation.\n\n'
                                       '*.AAE files will not be copied and .HEIC pictures will be converted to .jpg')
        top_label.pack()

    def start_submit_thread(event):
        global submit_thread
        submit_thread = threading.Thread(target=go_time)
        submit_thread.daemon = True
        #progressbar.start()
        submit_thread.start()
        mainbox.after(20, check_submit_thread)

    def check_submit_thread():
        if submit_thread.is_alive():
            mainbox.after(20, check_submit_thread)
        #else:
        #    progressbar.stop()

    goButton = tk.Button(mainbox, text="help", command=help)
    goButton.pack()

    inputButton = tk.Button(mainbox, text="source", command=getinput)
    inputButton.pack()

    listpathbox = tk.Checkbutton(mainbox)
#    listpathbox.pack(side='right')

    inputtextfeld = tkinter.Entry(mainbox, textvariable= source)
    inputtextfeld.pack()

    destinationButton = tk.Button(mainbox, text="destination", command=getdestination)
    destinationButton.pack()

    destinationtextfeld = tkinter.Entry(mainbox, textvariable= destination)
    destinationtextfeld.pack()

    setButton = tk.Button(mainbox, text="set", command=find, state='disabled')
    setButton.pack()

    filesfound = tk.Label(mainbox, text="push set after select selecting actual folders")
    filesfound.pack()

    goButton = tk.Button(mainbox, text="go", command=lambda:start_submit_thread(None), state='disabled')
    goButton.pack()

    progress = tk.Label(mainbox, text='test')

    def update():
        if os.path.isdir(inputtextfeld.get()) and os.path.isdir(destinationtextfeld.get()):
            setButton.configure(state='normal')
        else: setButton.configure(state='disabled')

        if len(willitwork) > 0 and setButton['state'] == 'normal':
            goButton.configure(state='normal')
        else:
            goButton.configure(state='disabled')
            filesfound.configure(text = "push set after select selecting actual folders")
        setButton.after(1000, update)

    update()
    mainbox.mainloop()


def howToFile():
    lookforfilesmk2(path)
    destination = r"C:\Users\scpul\OneDrive\Desktop\my phone photos"
    for entry in AllFiles:
        if not destination.endswith('/'):
            destination = destination + '/'
        if entry.split('.')[1] == 'HEIC':
            name, extension = entry.split('.')
            print(entry)
            print(destination + name[name.rindex('\\')+1:] + '.jpg')
    print(os.path.basename(AllFiles[1]))

def howToFile2():
    lookforfilesmk2(path)
    print(path, destination)
    print(AllFiles[1])
    print(os.path.basename(AllFiles[1]).split('.')[0])

def howToFile3():
    test = os.scandir('C:/Users/scpul/OneDrive/Desktop/my phone photos')
    print(type(test))
    test2 = map(lambda x:x.name.split('.')[0],test)
    test.close()
    print(set(test2))


if __name__ == '__main__':
    main()


    #print(reee, list(reee))
