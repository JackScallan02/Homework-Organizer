#Author: Jack Scallan
#Updated 10/03/21
import csv
import sys
import pandas as pd
import pdfkit
import os
import boto3
from botocore.exceptions import ClientError
import codecs


SENDER = ""
RECIPIENT = ""
try:
    with open("email-info/email-info.txt", "r") as f:
        i = 0
        for line in f:
            # print(line)
            if not line.isspace():
                i += 1
            if i == 1:
                SENDER = line[15:len(line) - 2]
            elif i == 2:
                RECIPIENT = line[18:len(line) - 2]
                break
except:
    pass

def prompt():
    response = input("Would you like to view, add, delete homework, send email, or quit? (v/a/d/e/q): ")

    while response.lower() not in ("v", "a", "d", "e", "q", "view", "add", "delete", "email", "quit"):
        response = input("Would you like to view, add, or delete homework, or quit? (v/a/d/q): ")

    if response.lower() in ("v", "view"):
        view(True)
    elif response.lower() in ("a", "add"):
        add()
    elif response.lower() in ("d", "delete"):
        delete()
    elif response.lower() in ("e", "email"):
        sendEmail()
    else:
        return


def sendData():
    with open("homeworks.csv", "r") as f:
        reader = csv.reader(f)
        out = []
        for row in reader:
            out.append(row[1:])

    with open("dataOut.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(['Due Date', 'Name', 'Class'])
        for i in range(len(out)):
            writer.writerow(out[i])


    dataOut = pd.read_csv("dataOut.csv")
    #To Excel
    dataOut.to_excel("homeworks.xlsx", index=False)

    #To HTML
    htmlOut = pd.read_excel("homeworks.xlsx")

    htmlOut.to_html("temp.html", table_id="my-table", columns=['Due Date', 'Name', 'Class'], col_space=100, index=False)

    text='''
<style>
    #my-table {
        border: 1px solid black;
        border-collapse: collapse;
        background-color: #c7f0ff;
    }
    #my-table td {
        background-color: white;
    }
    th {
        text-align: center;
    }
</style>
<center>
<h2>Homeworks</h2>
        '''

    with open("temp.html", "r+") as f:
        content = f.read()
        f.seek(0, 0)
        f.write(text.rstrip('\r\n') + '\n' + content)


    with open("temp.html", "a") as f:
        f.write("</center>")

    #To PDF
    pdfkit.from_file("temp.html", "homeworks.pdf")

    try:
        os.system("cp homeworks.pdf ~/Desktop")
    except:
        print("Failed to move file to desktop.")
        return

def sendEmail():
    if SENDER == "" or RECIPIENT == "":
        print("No email specified! Enter your email in email-info/email-info.txt")
        return

    AWS_REGION = "us-east-1"
    SUBJECT = "Your Homeworks"

    i = 0
    content = codecs.open("temp.html", "r")
    BODY_HTML = content.read()
    BODY_HTML = BODY_HTML[253:]

    htmlStr1 = '''
    <!DOCTYPE html>
<html>
<head>
    <style>
        #my-table {
            border: 1px solid black;
            border-collapse: collapse;
            background-color: #c7f0ff;
            color: black;
        }
        #my-table td {
            background-color: white;
        }
        th {
            text-align: center;
        }
        h2 {
            color: black;
        }
    </style>
 </head>
 <center>
    '''
    htmlStr2 = '''</html>'''


    BODY_HTML = htmlStr1 + BODY_HTML + htmlStr2

    BODY_TEXT = "Application doesn't support HTML"

    CHARSET = "UTF-8"
    client = boto3.client('ses',region_name=AWS_REGION)
    try:
        print("Sending email...")
    #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent!"),
        # print(response['MessageId'])



def getRows():
    numRows = 0
    with open("homeworks.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            numRows += 1
    return numRows


def sort(list1):

    low = []
    equal = []
    high = []

    if len(list1) > 1:
        pivot = list1[0][1]
        for item in list1:
            if item[1] < pivot:
                low.append(item)
            elif item[1] == pivot:
                equal.append(item)
            elif item[1] > pivot:
                high.append(item)
        return sort(low) + equal + sort(high)
    else:
        return list1


def organizeByDate():
    homeworks = []
    with open("homeworks.csv", "r") as f:
        reader = csv.reader(f)

        for row in reader:
            homeworks.append(row)

    if len(homeworks) <= 1:
        return

    homeworks = sort(homeworks)

    with open("homeworks.csv", "w") as f:
        count = 1
        for i in range(0, len(homeworks)):
            homeworks[i][0] = str(count)
            writer = csv.writer(f)
            writer.writerow(homeworks[i])

            count += 1

    sendData()


def view(openPDF):
    with open("homeworks.csv", "r") as f:
        numRows = 0
        reader = csv.reader(f)

        for row in reader:
            print(row[0], " Due Date: ", row[1], " Name: ", row[2], " Class: ", row[3])
            numRows += 1

        if numRows == 0:
            print("You have no homework :)")
            return

        if openPDF:
            os.system("open homeworks.pdf")


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

        with open("homeworks.csv", "a") as f:
            writer = csv.writer(f)
            writer.writerow([str(numRows), dueDate, homework, className])

        print("Homework Added!")

        addAnother = input("Would you like to add another homework? (y/n): ")
        if len(addAnother) > 0 and addAnother.lower()[0] != "y": #If user doesn't type yes
            break

    organizeByDate()

    prompt()



def delete():
    numHomeworks = 0
    with open("homeworks.csv", "r") as f:
        for line in f:
            numHomeworks += 1
    if numHomeworks == 0:
        print("You have no homework!")
        prompt()
        return

    view(False)
    lineToDelete = input("Which homework would you like to remove? (give number): ")
    while not lineToDelete.isnumeric():
        print("Invalid! Give a number.")
        lineToDelete = input("Which homework would you like to remove? (give number): ")

    deletedLine = ""  #Saving variable for printing later

    with open("homeworks.csv", "r") as f:
        reader = csv.reader(f)
        lines = []
        count = 1
        for line in reader:
            if count != int(lineToDelete):
                lines.append(line)
            else:
                deletedLine = line
            count += 1


    rowNumber = 1
    with open("homeworks.csv", "w") as f:
        writer = csv.writer(f)
        count = 1
        for i in range(0, len(lines)):
            lines[i][0] = count
            writer.writerow(lines[i])
            count += 1

    print("Removed: ", deletedLine[2])

    print("Remaining homeworks: \n")
    view(False)
    print()

    sendData()

    prompt()




if __name__ == "__main__":

    prompt()
