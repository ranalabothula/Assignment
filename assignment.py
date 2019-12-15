# importing csv module
import csv
import re
import io
# import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# csv file name
filename = "jobs_data.csv"

# schema initial
schemanormal = dict()
schema = dict()
schema = {}
schemanormal = {'Job Category': 8, 'Preferred Skills': 17, 'Salary Frequency': 12, 'Salary Range To': 11,
          'Minimum Qual Requirements': 16}
#print(schemanormal)

# initializing the data into rows table
fields = []
rows = []

# reading csv file
with open(filename, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile,delimiter=',',quotechar='"')
    #To skip the header
    fields = list(next(csvreader))
    i = 0;
    for field in fields:
        schema[field] = i
        i = i+1
    # extracting each data row one by one
    for row in csvreader:
        rows.append(row)
        #print(row)

#data clean up
for row in rows:
    #for x in row:

    #print(str(row).replace(r"[^a-zA-Z\d\_]+", ""))
    row = re.sub('[^A-Za-z0-9.&, ]+','',str(row))
    #print(row)

# newrows = []
# for row in rows:
#     # parsing each column of a row
#     newrow = row[8]
#     for col in desired_columns:
#         newrow = newrow+"~"+row[col]
#     newrows.append(newrow)
#print(newrows[10])

#Identify the required variables - 'Salary Range To',''
def getCategoriesWithHighPay(rows):
    global Q3
    listOfSalaries = []
    for row in rows:
        #print(row[schema["Salary Range To"]])
        listOfSalaries.append(float(row[schema["Salary Range To"]]))

    Q3 = getQ3(listOfSalaries , len(rows))
    #print(Q3);

    categoriesWithHighPay = []
    for row in rows:
        if (float(row[schema["Salary Range To"]]) >= Q3) :
            categoriesWithHighPay.append(row)

    return categoriesWithHighPay

# Function to give index of the median
def median(a, l, r):
    n = r - l + 1
    n = (n + 1) // 2 - 1
    return n + l

# Function to calculate IQR
def getQ3(a, n):

    a.sort()
    # Index of median of entire data
    mid_index = median(a, 0, n)

    # Median of second half
    Q3 = a[median(a, mid_index + 1, n)]
    #print(Q3)
    return Q3;

def normalizeSalaries(rows):

    salValue = float(0.0)
    for row in rows:
        if (str(row[schemanormal['Salary Frequency']]) == 'Hourly') :
            salValue = float(row[schemanormal['Salary Range To']]) * 2008
            #print(salValue)
            row[schemanormal['Salary Range To']] = salValue
        else:
            if (str(row[schemanormal['Salary Frequency']]) == 'Daily'):
                salValue = float(row[schemanormal['Salary Range To']]) * 251
                #print(salValue)
                row[schemanormal['Salary Range To']] = salValue
        #print(row[schemanormal['Salary Range To']])
    return rows


# def lemmatize(skillsWithHighPay):
#     skillsSet = set()
#     wholeWords = ""
#     stop_words = set(stopwords.words('english'))
#     for skill in skillsWithHighPay:
#         skill = re.sub('[^A-Za-z0-9 ]+', '', str(skill))
#         wholeWords = wholeWords + '\n' + skill
#     wholeWordsSplit = wholeWords.split('\n',1)
#     for word in wholeWordsSplit:
#         if not word in stop_words:
#             skillsSet.add(word)
#
#     return skillsSet

def getSkillsWithHighPay(rawCategoriesWithHighPay):
    skillsWithHighPay = set()
    splitSkills = []
    for row in rawCategoriesWithHighPay:
        skillInTable = row[schemanormal["Preferred Skills"]]
        if (str(skillInTable).__contains__(";")) :
            splitSkills = str(skillInTable).split(';')
        elif(str(skillInTable).__contains__("o\s")):
                splitSkills = re.split('o\s', str(skillInTable))
        else:
            if (re.match("(?:^\w{1}[.0-1])",skillInTable)):
                #print(skillInTable)
                splitSkills = re.split('\d.',str(skillInTable))
                #print(splitSkills)
        for skill in splitSkills:
            stripSkill = re.sub(r'^\.','',skill)
            # if(stripSkill.startswith("PREFERRED SKILLS")):
            #     stripSkill = stripSkill[len("PREFERRED SKILLS"):]
            skillsWithHighPay.add(stripSkill.strip())

    return skillsWithHighPay


def getCleanedData(rows):
    newRows = []
    for row1 in rows:
        # for x in row:
        # print(str(row).replace(r"[^a-zA-Z\d\_]+", ""))
        cleanRow = []
        for key in row1:
            cleanRow.append(re.sub(r"[^A-Za-z0-9,.&\s]", "", str(key)))
        newRows.append(cleanRow)
    # for newRow in newRows:
    #     print(newRow)
    return newRows


def removeSkillsInLowPay(allSkillsWithHighPay,salNormalizedRows,maxSalary):
    removableSkills = set()
    for row in salNormalizedRows:
        if (float(row[schemanormal["Salary Range To"]]) < float(maxSalary)) :
            for skill in allSkillsWithHighPay:
                if (row[schemanormal["Preferred Skills"]].__contains__(skill)) :
                    removableSkills.add(skill)
    for skill in removableSkills:
        allSkillsWithHighPay.remove(skill)
            # if any(ext in row[schemanormal["Preferred Skills"]] for ext in allSkillsWithHighPay):
            #     #print("removing "+row[schemanormal["Preferred Skills"]])
            #     allSkillsWithHighPay.remove(row[schemanormal["Preferred Skills"]])
    return allSkillsWithHighPay


def getJobCategoriesWithHighPaySkills(finalSkillsWithHighPay,salNormalizedRows):
    setOfJobCategories = set()
    for row in salNormalizedRows:
        for skill in finalSkillsWithHighPay:
            if (row[schemanormal["Preferred Skills"]].__contains__(skill)) :
                setOfJobCategories.add(row[schemanormal["Job Category"]])
        # if any(ext in row[schemanormal["Job Category"]] for ext in finalSkillsWithHighPay):
        #     setOfJobCategories.add(row[schemanormal["Job Category"]])
    return setOfJobCategories

if __name__ == '__main__':
    global Q3
    cleanData = getCleanedData(rows)
    salNormalizedRows = normalizeSalaries(cleanData)
    rawCategoriesWithHighPay = getCategoriesWithHighPay(salNormalizedRows)
    #print(Q3)
    #print(rawCategoriesWithHighPay.__len__())
    allSkillsWithHighPay = getSkillsWithHighPay(rawCategoriesWithHighPay)
    # for skill in allSkillsWithHighPay:
    #     print(skill)
    #problem 1
    finalSkillsWithHighPay = removeSkillsInLowPay(allSkillsWithHighPay,salNormalizedRows,Q3)
    # for skill in finalSkillsWithHighPay:
    #     print(skill)
    #problem 2
    jobCategoriesWithHighPaySkills = getJobCategoriesWithHighPaySkills(finalSkillsWithHighPay,salNormalizedRows)
    print(jobCategoriesWithHighPaySkills)
