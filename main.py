import transact

#printing the heading of the document
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("                                                                         Welcome to Idumenta Costume Rental app                                                          ")
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

#Prompt user for renting or returning
def promptUser():
    ''' prints the prompt menu of the application, returns None'''
    print("\n")
    print("Select a desired option\n")
    print("(1)  | |  Press 1 to rent a costume\n")
    print("(2)  | |  Press 2 to return a costume\n")
    print("(3)  | |  Press 3 to exit\n")

def exitApp():
    '''Displays thank you message after exit of the application, returns None'''
    print("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("                                                  Thanks for using the application. Have a good day!!")
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
continueLoop = True

while continueLoop == True:
    promptUser()
    try:
        userInput = int(input("Choose an option: "))
        if userInput == 1:
            transact.rentCostume()

        elif userInput == 2:
            transact.returnCostume()

        elif userInput == 3:
            exitApp()
            continueLoop = False

        else:
            print("Enter a valid option")
            
    except ValueError :
        print("Please input an option") 

