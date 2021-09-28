# Homework-Organizer
This python program allows the user to easily enter their homeworks, and then takes that data and organizes it in a readily available excel sheet and PDF file, ordered by due date.

**HOW TO USE:**
1. Download source file, and move to an easily accessible location.
2. Open terminal and change to proper directory in terminal window where file is located.
3. Run the program: `python3 homeworks.py`

---

## How it works:
Built in python, this program requests for the input of the user (prompting for the homeworks they want to enter), and creates a readable PDF file. First, the homework inputs are recorded onto a csv file. Then, using the Pandas library, the csv file is exported onto an excel file. Next, once again using the pandas library, we read from this excel sheet and then format it using an HTML/CSS file. Finally, utilizing pdfkit and wkhtmltopdf, the file is then exported to a PDF. Then, a user can choose to send an email of their homeworks due at any time.

---

## REQUIREMENTS (installations required):
- Program works the best on LINUX operating systems.
- User must have Python installed
- User needs to install: openpyxl, pandas, pandas xlrd pdfkit, wkhtmltopdf, boto3
  - openpyxl: `pip install openpyxl`
  - pandas: `pip install pandas`
  - pdfkit: `pip install pandas xlrd pdfkit`
  - wkhtmltopdf: https://wkhtmltopdf.org/downloads.html
  - boto3: `pip install boto3`

## FOR SENDING AN EMAIL (OPTIONAL)
1. Create an AWS account.
2. Verify an email.
3. Create an access key and type `aws configure` in terminal. Enter in information.
4. Modify the email in the email-info/email-info.txt file.

### Example:
**Adding and Viewing Files:**
<img src="http://g.recordit.co/7s5Jn5s5eG.gif" width="1000" alt="example-gif"/>

**Deleting and Viewing Files:**
<img src="http://g.recordit.co/Xvsb5Dv8XG.gif" width="1000" alt="example-gif"/>

**Screenshot of a Sent Email:**
<img width="1017" alt="Screen Shot 2021-09-28 at 4 41 08 PM" src="https://user-images.githubusercontent.com/54595949/135162876-5f9d82be-7151-4384-8d62-b35608d025ae.png">
