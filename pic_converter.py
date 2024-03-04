import os
import shutil
from PIL import Image, ExifTags
from pillow_heif import register_heif_opener
from multiprocessing import Process, cpu_count, Pool
from tkinter import Tk
from tkinter.filedialog import askdirectory
register_heif_opener()
#path = "C:/Users/scpul/OneDrive/Documents/transfer/moms photos possestd 2"




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


#path = "C:/Users/scpul/OneDrive/Desktop/DCIM"
#destination = "C:/Users/scpul/OneDrive/Desktop/test2/"




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


    if entry[0].split('.')[1] == 'HEIC':
        image = Image.open(entry[0])
        image.convert('RGB').save(entry[1] + os.path.basename(entry[0]).split('.')[0] +'.jpg')
        image.close()
        shutil.copystat(entry[0], entry[1] + os.path.basename(entry[0]).split('.')[0] +'.jpg')
    else:shutil.copy2(entry[0], entry[1])
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

def main():
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


def howToFile():
    lookforfilesmk2(path)
    destination = r"C:\Users\scpul\OneDrive\Desktop\my phone photos"
    for entry in AllFiles:
        if not destination.endswith('/'):
            destination = destination + '/'
        if entry.split('.')[1] == 'HEIC':
            name, extension = entry.split('.')
            print(entry)
            print(destination + name[name.rindex('\\')+1:]+ '.jpg')
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
