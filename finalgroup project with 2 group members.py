try:
    import canary as c
except:
    print("where is the canary")



HOURS = ("11","12","01","02","03","04","05","06","07","08","09") #the hours we are open for
LISTOFBURGERS =("Basic burger", "cheeseburger", "baken burger","bacon burger", "veggie burger", "chef special", "fries", "drink", "Spam spam spam burger", "4 dimensional burger")#this is just for the names of the burgers,
BURGERPRICES = [5, 5.75, 12.99, 15.99, 7.99, 15.30, 4.99, 3.99, 19.84, 79.99]
ALL= 0 #If your program doesn't trash global variables, 1 will use Previous entries in calculations, 0 will not
AUTOPRICE = True  #should the price be calculated by the order using BURGERPRICES
MENUAUTO = True #do you want the menu to show every time? yes? really?
closegate= "-1" #what input should be used to move on to the next step

try:
    import random
    BURGERPRICES[5] = round(random.random()*20+5, 2)
except Exception:
    print('darn, no random')


class orderData:
    '''stores the data in the a good way'''
    def __init__(self):
#        self._handler = []
        self._order = {}
        self._allorders = []
    def closeorder(self): # Storing dictionaries in a list
        self._order['id'] = len(self._allorders)
        self._allorders.append(self._order)
        self._order = {}
    def add(self, typ, x):
        self._order[typ] = x
    def showall(self):
        return self._allorders
    def get(self, typ): #The powerhouse of this class
        ''' gets a list of a Particular key'''
        handler = []
        for i in self._allorders:
            z = i.get(typ, [])
            if type(z) == list:
                handler.extend(z)
            else: handler.append(z)
        return handler
    def mirge(self,x):
        if len(x)> 0:
            for i in x:
                i['id'] = len(self._allorders)
                self._allorders.append(i)
    def caulcPrice(self,sorse, targit = 'bill'):
        total = 0
        x = countstuff(self._order.get(sorse, []), LISTOFBURGERS)
        y = list(zip(x.keys(), x.values(), BURGERPRICES))
        for i in y:
            total += i[1] * i[2]
        self._order[targit] = round(total,2)
        return round(total,2)






def collectData(): #note, I kind of made this program in the persptive of an enployee using it to take a customers order.
    data3 = orderData()
    close = "0"
    closemessige = "what time did the customer order or type "+closegate+' to wrap up the program: '
    close = input(closemessige)

    while close.lower() != closegate.lower():
        data3.add('time',str(collectTime(close)))
        menu(MENUAUTO)
        data3.add('burger',collectBurger(input("type the ids of the burger they ordered, type -2 if you don't know the ids, type {} when done: ".format(closegate))))
        data3.add('name',input("what is the customer's name: "))
        if AUTOPRICE: data3.caulcPrice('burger')
        else: data3.add('bill',float(collectBill(input("what is the customer's bill: "))))
        data3.closeorder()
        close = input(closemessige)
    return data3

def collectTime(inputTime):

    error = 1
    while error != 0:
        inputTime = inputTime.upper()  # we don't want am or pm, good thing it's only 11 hours
        if inputTime.find("AM") >= 1:
            inputTime = inputTime.replace("AM",'')
        if inputTime.find("PM") >= 1:
            inputTime = inputTime.replace("PM",'')
        if inputTime.find(" ") >= 1:
            inputTime = inputTime.replace(" ",'')

        if len(inputTime) == 3:  # if the user input 315 ithis these lines chance it to 03:15
            inputTime = "0" + inputTime
        elif len(inputTime) == 4 and  inputTime.find(":") == 1:
            inputTime = "0" + inputTime
        if inputTime.find(":") == -1:     # I may not need this but I don't think I can use insert with just a string
            inputTime = list(inputTime)
            inputTime.insert(2, ":")
        else: inputTime = list(inputTime)
        error = 0
        if len(inputTime) != 5: # an error chech to see if the time inputed is a valid time
            error += 1
            print("not the right amount of numbers")
        elif ''.join(inputTime[0:2]) not in HOURS: # a check to see if the hours are valid
            error += 1
            print("we are not open during that time")
        elif inputTime[3] not in list(map(str,range(0,6))):
            error += 1
            print("that time does not exist")
        elif inputTime[4] not in list(map(str, range(0,10))):
            error += 1
            print("I don't know how, but the last digit is wrong",)
        if error != 0:
            inputTime = input("try again: ")

    inputTime = ''.join(inputTime)   # turning the list back into a string
    return inputTime

def menu(auto=True):
    if auto :
        print("the burger id and burgers are")
        print("-" * 10)
        for x in range(0,len(LISTOFBURGERS)):  #Displays a list of the burgers we have
            print(x, LISTOFBURGERS[x], ('$'+str(BURGERPRICES[x]) if AUTOPRICE else ''))
        print("-" * 10)
    return

def collectBurger(burgerChoice = "0"):
    burgerChoices = []
    while burgerChoice != closegate: #this is the exit cheack
        while burgerChoice not in map(str,list(range(len(LISTOFBURGERS)))) and burgerChoice not in LISTOFBURGERS and burgerChoice != closegate:   #makes sure the input is valid
            if '-2' != burgerChoice and closegate != burgerChoice:
                print('that was not an option, here is the manu again')
            menu()
            burgerChoice = input("what is the burger you want? or type -2 if you are done ordering")
        if burgerChoice in map(str,list(range(len(LISTOFBURGERS)))):
            burgerChoice = LISTOFBURGERS[int(burgerChoice)]
        burgerChoices.append(burgerChoice)
        burgerChoice = input("another burger? if not type {}?: ".format(closegate))
    return burgerChoices

def collectBill(thereBill):
    thereBill2 = ""
    error = 1
    while error == 1:
        error = 0
        if thereBill[0] == "$":        # if a $ is added, remove it
            thereBill = thereBill.replace('$','')

        try:
            thereBill = round(float(thereBill),2)
        except Exception:
            print('that was not the proper format, you should have put ###.##')
            error = 1

        if error == 1:
            thereBill = input("try again")

    return float(thereBill)


def q6and7(time, bill):
    sumPerHour = [0]*len(HOURS)
    time2 = []
    for i in time: #get reid of them Minutes
        i =list(i)
        i.pop(2)
        i.pop(2)
        i.pop(2)
        i =''.join(i)
    #    print(i)
        time2.append(i)
    busy = countstuff(time2,HOURS)

    for i in range(0,len(time2)): # Nothing more fun than involving three lists in a single line of code
        sumPerHour[HOURS.index(time2[i])] += bill[i]
    return busy, sumPerHour

def countstuff(inp, con): #this thing counts how many people should up per hour
    output = {}
    for i in con:
        output[i] = (inp.count(i))
    return output


def countstuff2(inp, con): #no longer being used
    output = {}
    for i in con:
        output[i] = (inp.count(con.index(i)))
    return output


def combind(data): # this create a list of list, to group the people and there orders, no longer being used
    output = []
    for i in range(len(list(data.values())[0])):
        order = {"id": i}
        for x in data.keys():
            order[x] = (data[x][i])
        output.append(order)
    return output


def combindlist(data):  # same thing, just using list instade of dicatnarys, also no longer being used
    output = []
    for i in range(len(list(data.values())[0])):
        order = []
        order.append(i)
        for x in data.keys():
            order.append(data[x][i])
        output.append(order)
    return output


def second_to_last_lowest_bill(name_list, bill_list):
    client_info = list(zip(name_list, bill_list))  # Combine name and bill information
    sorted_info = sorted(client_info, key=lambda x: x[1])  # Sort the client_info list based on bills in ascending order
    second_to_last_client = sorted_info[1][0]
    return second_to_last_client

def busiest_hour(time_list): # Count the occurrences of each time in the time_list
    hour_counts = {}
    for time in time_list:
        hour = time.split(':')[0]
        hour_counts[hour] = hour_counts.get(hour, 0) + 1
    busiest_hour = max(hour_counts, key=hour_counts.get) #Find the busiest hour
    return busiest_hour, hour_counts[busiest_hour]

def best_hour(time_list, bill_list):
    time_and_bill = list(zip(time_list, bill_list))  # Create a dictionary to store total sales for each hour
    hour_sales = {}
    for time, bill in time_and_bill:
        hour = time.split(':')[0]
        hour_sales[hour] = hour_sales.get(hour, 0) + bill
    best_hour = max(hour_sales, key=hour_sales.get) # Find the best hour in terms of sales
    return best_hour, hour_sales[best_hour]

def main(data, data2 =()):

    if type(data) == list:
        handle = data
        data = orderData()
        try:
            data.mirge(handle)
        except Exception:
            print('please pass the orderData class, the output from the orderData class, or call the collectData funtion')
            return handle

    if type(data) != orderData:
        print('please pass the orderData class, the output from the orderData class, or call the collectData funtion')
        return data

    if ALL == 1:
        try:
            data.mirge(data2)
        except Exception:
            print('the extra data is bad')

    print('-'*20)
    if len(data.get('name')) < 10: #question 1
        print("there is no 10th customer")
    else: print("the 10th customer is :",data.get('name')[9])

    if len(data.get('name')) > 0: #question 2
        print('the person with the longest name is '+sorted(data.get('name'), key=lambda item: len(item), reverse=True)[0])
    else: print('the person with the longest name is no one, the is no one, there never was anyone.')

    topburgers = sorted(countstuff(data.get('burger'), LISTOFBURGERS).items(), key=lambda item: item[1], reverse=True) #question 3
    print('the top three most selling burgers are ', list(map(lambda x: x[0], topburgers))[:3])

    topclients = sorted(data.showall(), key=lambda x: x['bill'], reverse=True) #question 4
    print("the top", min(3, len(topclients)),"customers are", list(map(lambda x: x['name'], topclients))[:min(3, len(topclients))])

    try: print('the person with the second to lowest bill is', second_to_last_lowest_bill(data.get('name'),data.get('bill')))
    except Exception:
        print('the secod_to_last_lowst_bill funtion crashed in some way, running backup code')
        if len(data.showall()) >= 2: #question 5
            print('the person with the second to lowest bill is', sorted(data.showall(), key=lambda x: x["bill"])[1]['name'])
        else: print('there is one person or no persons that order, I can check but meh')

    busy, sumPerHour = q6and7(data.get("time"),data.get("bill"))

    try:
        print("our busiest hour is {} with {} people in that hour".format(*busiest_hour(data.get('time'))))
    except Exception:
        print('busiest_hour funtion failed, running backup code')
        print("our busiest hour is " + str(int(sorted(busy.items(), key=lambda item: item[1], reverse=True)[0][0])) + " o'clock") #question 6

    try:print("our best hour is {} with the amount of money we made is {}".format(*best_hour(data.get('time'),data.get('bill'))))
    except Exception:
        print('the best_hour funtion has crashed running backup code')
        print("our best hour is " +str(int(HOURS[sumPerHour.index(max(sumPerHour))]))+ " o'clock") #question 7

    print("the amount of money we have made is: $"+ str(round(sum(data.get("bill")),2))) #question 8

    if ALL == 0:
        try:
            data.mirge(data2)
        except Exception:
            print('the extra data is bad')
    return data.showall()


if 'data' not in locals():
    data = []

data = main(collectData(),data)

input('going to close the code now')