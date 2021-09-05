# Homework-Organizer
This python program allows the user to easily enter their homeworks, and then takes that data and creates a readily available excel sheet and PDF file.

**HOW TO USE:**
1. Download source file, and move to an easily accessible location.
2. Open terminal and change to proper directory in terminal window where file is located.
3. Run the program: `python3 homeworks.py`

---

### How it works:
Built in python, this program requests for the input of the user (prompting for the homeworks they want to enter), and creates a readable PDF file. First, the homework inputs are recorded onto a csv file. Then, using the Pandas library, the csv file is exported onto an excel file. Next, once again using the pandas library, we read from this excel sheet and then format it using an HTML/CSS file. Finally, utilizing pdfkit and wkhtmltopdf, the file is then exported to a PDF.

---

## REQUIREMENTS (installations required):
- Program works the best on LINUX operating systems.
- User must have Python installed
- User needs to install: openpyxl, pandas, pandas xlrd pdfkit, 

- openpyxl: `pip install openpyxl`
- pandas: `pip install pandas`
- pdfkit: `pip install pandas xlrd pdfkit`
- wkhtmltopdf: https://wkhtmltopdf.org/downloads.html

**Example:**
<img src="http://g.recordit.co/7s5Jn5s5eG.gif" width="1000" alt="example-gif"/>
