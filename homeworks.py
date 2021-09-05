#Author: Jack Scallan
#Updated 10/05/21


def prompt():
    response = input("Would you like to view, add, or delete homework, or quit? (v/a/d/q): ")

    while response.lower() not in ("v", "a", "d", "q", "view", "add", "delete", "quit"):
        response = input("Would you like to view, add, or delete homework, or quit? (v/a/d/q): ")

    if response.lower() in ("v", "view"):
        view()
    elif response.lower() in ("a", "add"):
        add()
    elif response.lower() in ("d", "delete"):
        delete()
    else:
        quit()


def getRows():
    numRows = 0
    with open("homeworks.txt", "r") as textFile:
        for row in textFile:
            numRows += 1
    return numRows


def sort(list1):

    low = []
    equal = []
    high = []

    if len(list1) > 1:
        pivot = list1[0][4:9]
        for item in list1:
            if item[4:9] < pivot:
                low.append(item)
            elif item[4:9] == pivot:
                equal.append(item)
            elif item[4:9] > pivot:
                high.append(item)
        return sort(low) + equal + sort(high)
    else:
        return list1


def organizeByDate():
    homeworks = []
    with open("homeworks.txt", "r") as textFile:
        for row in textFile:
            homeworks.append(row)

    if len(homeworks) <= 1:
        return

    homeworks = sort(homeworks)


    with open("homeworks.txt", "w") as newFile:
        count = 0
        for item in homeworks:
            newFile.write(str(count) + item[1:])
            count += 1


def view():
    with open("homeworks.txt", "r") as textFile:
        numRows = 0
        for row in textFile:
            print(row)
            numRows += 1

        if numRows == 0:
            print("You have no homeworks :)")


def add():
    numRows = getRows()

    while True:
        homework = input("Enter the name of your homework: ")
        dueDate = input("Enter the due date (MM/DD): ")
        while (dueDate[2] != "/") or (not dueDate[:2].isnumeric()) or (not dueDate[3:].isnumeric()):
            print("That is not a valid date!")
            dueDate = input("Enter the due date (MM/DD): ")
        className = input("Enter the class it is for: ")

        numRows += 1
        row = '   '.join([str(numRows), dueDate, homework, className])

        with open("homeworks.txt", "a") as textFile:
            textFile.write(row)
            textFile.write("\n")

        print("Added: ", row)

        addAnother = input("Would you like to add another homework? (y/n): ")
        if len(addAnother) > 0 and addAnother.lower()[0] != "y": #If user doesn't type yes
            break

    organizeByDate()

    prompt()



def delete():
    view()
    lineToDelete = input("Which homework would you like to remove? (give number): ")
    deletedLine = ""  #Saving variable for printing later
    with open("homeworks.txt", "r") as textFile:
        lines = textFile.readlines()
        deletedLine = lines[int(lineToDelete) - 1]
        del lines[int(lineToDelete) - 1]


    rowNumber = 1
    with open("homeworks.txt", "w") as textFile:
        for line in lines:
            if int(line[0]) != rowNumber:
                line = ''.join([str(rowNumber), line[1:]])

            textFile.write(line)
            rowNumber += 1

    print("Removed: ", deletedLine)

    view()




if __name__ == "__main__":
    prompt()
