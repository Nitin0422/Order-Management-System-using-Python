import copy
import datetime


rentBasket = {}
rentedCostumes = {}
returnBasket = {}


def getFileContent():
    ''' Reads the file and returns lines, returns a list'''
    file = open("costume.txt", "r")
    content = file.readlines()
    file.close()
    return content

def getMenuItems(fileContent):
    ''''Fills file data in to dictionary, returns a dictionary'''
    menuItems = {}
    for index in range(len(fileContent)):
        menuItems[index + 1] = fileContent[index].replace("\n", "").split(",")
    return menuItems

def checkStock(menuItems):
    '''Checks atleast one quantity is nonzero, returns Boolean'''
    nullCheck = 0

    for key in menuItems.keys():
        item = menuItems.get(key)
        quantity = int(item[3])
        if quantity == 0:
            nullCheck = nullCheck + 1
    
    if nullCheck == (len(menuItems)):
        return False
    else:
        return True

def rentCostume():
    ''' rents the costume when called with help of other functions, returns None'''
    print("\n")
    if checkStock(menuItems) == True:
        printMenuItems()
        serialNumber = getSerialNumber(menuItems)
        validateQuantity(serialNumber)
        
    else:
        print("\n++++++++++++++++++++++++++++++++++++")
        print("            Store is out of costumes        ")
        print("++++++++++++++++++++++++++++++++++++")

def printMenuItems():
    '''prints the elements of the dictionary, returns None'''
    global menuItems
    print("-----------------------------------------------------------------------------------------------------------------------------------")
    print("Costume ID", "\t", "Costume Name", "\t\t", "Brand", "\t\t", "Price", "\t\t", "Quantity" )
    print("-----------------------------------------------------------------------------------------------------------------------------------")
    for key, value in menuItems.items():
        print(key, "\t\t", value[0], "\t\t", value[1], "\t\t", value[2], "\t\t", value[3])
    print("--------------------------------------------------------------------------------------------------------------------------------------------------------")

def getSerialNumber(menuItems):
    '''Validates the costume ID to be rented or returned, Returns Int value as sn'''
    SN = 0
    iterate = True
    while iterate == True:
        try:
            SN = int(input("Enter a serial number: "))
        except ValueError:
            print("Enter a valid number")
        if SN > 0 and SN <= 5:
            rentItem = menuItems.get(SN) #extracts the row of the respective costume to be rented through serial number
            quantity = int(rentItem[3])#extracts the quantity of costume and type casts to int'''
            if quantity == 0:
                print("Out of stock")
            else:
                iterate = False
        else:
            print("\nEnter a valid serial number!\n")
    return SN
                
            

def validateQuantity(serialNumber):
    '''validates quantity entered and calls other functions to print invoice, returns None'''
    global menuItems
    exceptionCatched = False
    userInput = 0
    
    try:
        userInput = int(input("\nEnter quantity of costume to be rented: "))
    except:
        print("Enter a number!!!")
        exceptionCatched = True
        validateQuantity(serialNumber) #recursion
        
    if exceptionCatched == False:
            rentItem = menuItems.get(serialNumber) #extracts the row of the respective costume to be rented through serial number
            quantity = int(rentItem[3]) #extracts the quantity of costume and type casts to int
            
            if userInput >0 and userInput <= quantity:
                menuItems[serialNumber][3] = str(int(menuItems[serialNumber][3]) - userInput)      
                updateFile()
                addToRentBasket(rentItem, userInput, serialNumber)
                addMoreItems()
            
            else:
                print("Please input valid quantity!!")
                validateQuantity(serialNumber) #recursion

def updateFile():
    '''updates the text file with new data, returns None'''
    global menuItems
    file = open("costume.txt", "w")
    for value in menuItems.values():
        newData = value[0] + "," + value[1] + ","  + value[2] + "," + value[3] + "\n"
        file.write(newData)
    file.close()

def addToRentBasket(rentItem, userInput, serialnumber):
    '''Adds data elements to rentbasket, returns None'''
    orderedItem = copy.deepcopy(rentItem)
    strPrice = orderedItem[2].replace("$", "")
    price = float(strPrice)
    charge = price * userInput
    orderedItem[3] = str(userInput)
    orderedItem.append(("$" + str(charge)))
    rentBasket[serialnumber] = orderedItem

def addMoreItems():
    '''Asks user to rent more items, returns None'''
    userInput = input("Do you want to rent more costumes ?? Enter \'Y\' for yes and \'N\' for no ")
    if userInput.upper() == 'Y':
        if checkStock(menuItems) == True:
            rentCostume()
        else:
            print("\n++++++++++++++++++++++++++++++++++++")
            print("            Store is out of costumes        ")
            print("++++++++++++++++++++++++++++++++++++")
            printRentInvoice()

    elif userInput.upper() == 'N':
        printRentInvoice()

    else:
        print("\nEnter \'Y\' or \'N\' ")
        addMoreItems()

def printRentInvoice():
    '''Asks user name and phone number and calls function to generate bill, returns None'''
    global rentedCostumes
    try:
        customerName = input("Enter Customer name: ")
        phoneNumber = int(input("Enter Phone Number: "))
        print("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("                                                                       Invoice Details                                                                           ")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("\nCustomer Name:  ", customerName)
        print("Phone Number:  ", phoneNumber)
        dateTime = datetime.datetime.now() 
        print("Date time of borrow: ", dateTime)
        printRentBasket()
        createRentTextInvoice(customerName, phoneNumber)

        if len(rentedCostumes) == 0:
            rentedCostumes.update(rentBasket)
        else:
            newList = []
            oldList = []
            for oldEntry in rentedCostumes.keys():
                oldList = rentedCostumes.get(oldEntry)
                for newEntry in rentBasket.keys():
                    newList = rentBasket.get(newEntry)
                    if oldEntry == newEntry:
                        newList[3] = int(newList[3]) + int(oldList[3])
                        rentBasket[newEntry] = newList
                    else:
                        rentBasket[newEntry] = newList
            rentedCostumes.update(rentBasket)
        rentBasket.clear()
       
    except ValueError:
        print("Enter phone number in integer value")
        printRentInvoice()    

def printRentBasket():
    '''prints elements of dictionary rentBasket, returns None'''
    print("-------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("Costume ID", "\t", "Costume Name", "\t\t", "Brand", "\t\t", "Price", "\t\t", "Quantity", "\t\t", "Amount" )
    print("-------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    grossAmount = 0
    for key, value in rentBasket.items():
        print(" ",key, "\t\t", value[0], "\t\t", value[1], "\t\t", value[2], "\t\t", value[3], "\t\t", value[4])
        grossAmount = grossAmount + float(value[4].replace("$", ""))
    print("--------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("\n---------------------------------------------------------------------------------------------------------------------    Total Amount =   ", "$", grossAmount)

def getDateTime():
    '''calculates current date and time, returns date and time as int'''
    year = str(datetime.datetime.now().year)
    month = str(datetime.datetime.now().month)
    day = str(datetime.datetime.now().day)
    hour = str(datetime.datetime.now().hour)
    minute = str(datetime.datetime.now().minute)
    second = str(datetime.datetime.now().minute)
    DateTime = year+month+day+hour+minute+second
    return DateTime

def createRentTextInvoice(customerName, phoneNumber):
    '''Creates text file for rent invoice, returns None'''
    global rentBasket
    rentFile = open(getDateTime()+"_"+customerName+"rent_invoice.txt", "w")

    rentFile.write("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    rentFile.write("\t\t\t\tInvoice Details \n")
    rentFile.write("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n")

    rentFile.write("Customer Name: ")
    rentFile.write(customerName)
    rentFile.write("\n\n")
    rentFile.write("Customer Phone: ")
    rentFile.write(str(phoneNumber))
    rentFile.write("\n")

    rentFile.write("\n\nITEMS RENTED: ")

    rentFile.write("\n----------------------------------------------------------------------------------------------------------------------------------------------------\n")
    rentFile.write("Costume ID \t Costume Name \t\t Brand \t\t Price \t\t Quantity \t\t Amount\n")
    rentFile.write("-------------------------------------------------------------------------------------------------------------------------------------------------------\n")

    grossAmount = 0
    for key, value in rentBasket.items():
        item = str(key) + "\t" + value[0] + "\t\t" + value[1] + "\t\t" + value[2] + "\t\t" + value[3] +  "\t\t\t" + value[4]
        rentFile.write(item)
        rentFile.write("\n\n")    
        grossAmount = grossAmount + float(value[4].replace("$", ""))
    rentFile.write("-------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    rentFile.write("\n----------------------------------------------------------------------------------------------------------------------------  Total Amount =   ")
    rentFile.write(("$" + str(grossAmount)))
    rentFile.close()


def returnCostume():
    ''' Returns the costume when called, returns None'''
    if checkStock(rentedCostumes) == True:
        printRentedCostumes()
        serialNumber = getSerialNumber(rentedCostumes)
        validateReturnQuantity(serialNumber)
    else:
        print(" All rented costumes has already been returned!!")
        
def printRentedCostumes():
    '''Prints the elements of dictionary rentedCostumes.'''
    global rentedCostumes
    print("\n------------------------------------------------------------------------------------------------------------------------------------------------")
    print("Costume ID", "\t", "Costume Name", "\t\t", "Brand", "\t\t", "Price", "\t\t", "Quantity" )
    print("------------------------------------------------------------------------------------------------------------------------------------------------")
    for key, value in rentedCostumes.items():
        print("  ", key, "\t\t", value[0], "\t\t", value[1], "\t\t", value[2], "\t\t", value[3])
    print("--------------------------------------------------------------------------------------------------------------------------------------------------------")


def validateReturnQuantity(serialNumber):
    '''Validates quantity to return costumes and calls other fucntions for furthur process, returns None'''
    global rentedCostumes
    userInput = 0
    try:
        userInput = int(input("Enter the quantity of costumes to be returned: "))
        days = int(input("Enter the number of days costume has been rented for: "))
    except ValueError:
        print("\nEnter valid input !!!")
        validateReturnQuantity(serialNumber)

    returnItem = rentedCostumes.get(serialNumber)  #extracts the row of the respective costume to be rented through serial number
    quantity = int(returnItem[3])  #extracts the quantity of costume and type casts to int
    
    if userInput <= quantity:
        rentedCostumes[serialNumber][3] = str(int(rentedCostumes[serialNumber][3]) - userInput)
        updateFileWhileReturn(returnItem, userInput, serialNumber)
        addToReturnBasket(returnItem, userInput, days, serialNumber)
        returnMoreItems()
      
    else:
        print("Enter valid quantity !!!")
        validateReturnQuantity(serialNumber) #recursion

def  updateFileWhileReturn(returnItem, userInput, serialNumber):
    '''Updates the original file after costume has been returned, returns None'''
    for value in menuItems.values():
        if value[0] == returnItem[0]:
            menuItems[serialNumber][3] = str(int(menuItems[serialNumber][3]) + userInput) 
    file = open("costume.txt", "w")
    for value in menuItems.values():
        newData = value[0] + "," + value[1] + ","  + value[2] + "," + value[3] + "\n"
        file.write(newData)
    file.close()

def addToReturnBasket(returnItem, userInput, days, serialNumber):
    '''Adds elements to returnBasket dicitonary, returns None'''
    requestedItem = copy.deepcopy(returnItem)
    strPrice = requestedItem[2]
    price = float(strPrice.replace("$", ""))
    charge = price * userInput
    requestedItem[3] = str(userInput)
    requestedItem.pop()
    requestedItem.append(("$" + str(charge)))
    fine = 0
    if (days-5) > 0:
        fine = (days-5) * 3
    requestedItem.append(str(fine))
    returnBasket[serialNumber] = requestedItem

    
def returnMoreItems():
    '''Prompts user to add more items, returns None'''
    userInput = input("Do you want to return more costumes ?? Enter \'Y\' for yes and \'N\' for no ")
    if userInput.upper() == 'Y':
        if checkStock(rentedCostumes) == True:
            returnCostume()
        else:
            print(" All rented costumes has already been returned!!")
            printReturnInvoice()

    elif userInput.upper() == 'N':
        printReturnInvoice()

    else:
        print("\nEnter \'Y\' or \'N\' ")
        returnMoreItems()

def  printReturnInvoice():
    '''Prompts user for name and phone and prints invoice, returns None'''
    global returnBasket
    try:
        customerName = input("Enter Customer name: ")
        phoneNumber = int(input("Enter Phone Number: "))
        print("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("                                                                       Invoice Details                                                                           ")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("\nCustomer Name:  ", customerName)
        print("Phone Number:  ", phoneNumber)
        dateTime = datetime.datetime.now() 
        print("Date time of borrow: ", dateTime)
        printReturnBasket()
        createReturnTextInvoice(customerName, phoneNumber)
        returnBasket.clear()
       
    except:
        print("Enter phone number in integer value")
        printReturnInvoice()

def printReturnBasket():
    ''''Prints the elements present  in the returnBasket dicitonary, returns None'''
    global returnBasket
    print("---------------------------------------------------------------------------------------------------------------------------------------------------")
    print("Costume ID", "\t", "Costume Name", "\t\t", "Brand", "\t\t", "Price", "\t\t", "Quantity", "\t\t", "Amount" )
    print("-----------------------------------------------------------------------------------------------------------------------------------------------------")
    grossAmount = 0
    grossFine = 0
    for key, value in returnBasket.items():
        print(key, "\t\t", value[0], "\t\t", value[1], "\t\t", value[2], "\t\t", value[3], "\t\t", value[4])
        grossAmount = grossAmount + float(value[4].replace("$", ""))
        grossFine = grossFine + float(value[5])
    print("--------------------------------------------------------------------------------------------------------------------------------------------------------")
    totalAmount = grossAmount + grossFine
    print("\n--------------------------------------------------------------------------------------------    Total Amount before fine =   ", "$", grossAmount)
    print("\n--------------------------------------------------------------------------------------------    Total Fine =   ", "$", grossFine)
    print("\n--------------------------------------------------------------------------------------------    Total Amount after fine =   ", "$", totalAmount)
    
def createReturnTextInvoice(customerName, phoneNumber):
    '''Creates and writes in a txt file the return invoice, returns None'''
    global returnBasket
    returnFile = open(getDateTime()+"_"+customerName+"return_invoice.txt", "w")

    returnFile.write("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    returnFile.write("\t\t\t\tInvoice Details \n")
    returnFile.write("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n")

    returnFile.write("Customer Name: ")
    returnFile.write(customerName)
    returnFile.write("\n\n")
    returnFile.write("Customer Phone: ")
    returnFile.write(str(phoneNumber))
    returnFile.write("\n")

    returnFile.write("\n\nITEMS RENTED: ")

    returnFile.write("\n--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    returnFile.write("Costume ID \t Costume Name \t\t Brand \t\t Price \t\t Quantity \t\t Amount\n")
    returnFile.write("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")

    grossAmount = 0
    grossFine = 0
    for key, value in returnBasket.items():
        item = str(key) + "\t\t" + value[0] + "\t\t" + value[1] + "\t\t" + value[2] + "\t\t" + value[3] +  "\t\t\t" + value[4]
        returnFile.write(item)
        returnFile.write("\n\n")    
        grossAmount = grossAmount + float(value[4].replace("$", ""))
        grossFine = grossFine + float(value[5])
    returnFile.write("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    totalAmount = grossAmount + grossFine
    returnFile.write("\n--------------------------------------------------------------------------------------------    Total Amount before fine =   ")
    returnFile.write(("$" + str(grossAmount)))
    returnFile.write("\n--------------------------------------------------------------------------------------------    Total Fine =    ")
    returnFile.write(("$" + str(grossFine)))
    returnFile.write("\n--------------------------------------------------------------------------------------------    Total Amount after fine =   ")
    returnFile.write(("$" + str(totalAmount)))
    returnFile.close()

    
fileContent = getFileContent()
menuItems = getMenuItems(fileContent)













