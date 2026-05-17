import os, csv, time
from datetime import datetime
from API import add_to_google_calendar
from UI import questions, Answers

folder = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(folder, "data.csv")
save_file = os.path.join(folder, "save.txt")

def GetFromDB(country,gender):
    with open(data_file, "r") as f:
        file = csv.DictReader(f)
        for row in file:
            if row["country"] == country:
            # Determine which column to pull based on gender
                if gender == "f":
                    return float(row['female'])
                elif gender == "m":
                    return float(row['male'])
                else:
                    print("non gender provided (using country average)")
                    return float(row['both'])
        #after going through the whole file
        print("country not in list")
        return 73.5 #assign average global life expectancy

def CalculateBMI(weight,height):
    height = height/100 #convert to meters
    return weight/height**2

def DateofBirth(date):
    try:
        dt = datetime.strptime(date, "%d/%m/%Y")
        return int(dt.timestamp())
    except ValueError:
        return None

def Exersie(value):
    if value == "none":
        return 0
    elif value == "moderate":
        return 3
    elif value == "active":
        return 6.9
    else:
        return 0

def Outlook(value):
    if value == "pessimistic":
        return -2
    elif value == "optimistic":
        return 2
    else:
        return 0
    
def Diet(value):
    if value == "poor":
        return -10
    elif value == "average":
        return 0
    elif value == "good":
        return 10
    else:
        return 0

def check_and_load():
    #checks if database file exists
    try:
        with open(data_file, "r") as f:
            pass #file exists
    except FileNotFoundError:
        print(f"Database file not found.")
        quit()

    # Checks if the save file exists, if not it creates it
    if os.path.exists(save_file):
        with open(save_file, "r") as file:
            file_size =  os.stat(save_file).st_size
            if file_size == 0: #file is empty
                print("file is empty")
                file.close() #close file
                os.remove(save_file) #delete file
                check_and_load() #try again
            else:
                #save time in variable
                UNIX_LE = int(file.read().strip())
                print(f"File found. Loaded UNIX_LE: {UNIX_LE}")
            
    else:
        #no file found, ask questions then save in file
        print("No save file found. Starting questions...")
        # run UI from UI.py to get answers
        answers = questions() # get answers from questions in UI
        UNIX_LE = calculations(answers)
        with open(save_file, "w") as file: #create file
            file.write(str(UNIX_LE)) #save UNIX life expecatcy to file
    return UNIX_LE

def calculations(var: Answers):
    BMI = CalculateBMI(var.weight,var.height)
    DOB = DateofBirth(var.birthday)
    lifeExpectancy = GetFromDB(var.country,var.gender)
    lifeExpectancy += Exersie(var.exercise)
    lifeExpectancy += Diet(var.diet)
    lifeExpectancy += Outlook(var.outlook)

    if var.smoke == "y":
        lifeExpectancy -= 10
    if var.alcohol == "y":
        lifeExpectancy -= 4.5
    if var.stress == "y":
        lifeExpectancy -= 2.8

    if var.sleep < 0 or var.sleep >= 24:
        print("invalid sleep input")
        lifeExpectancy += 0
    elif var.sleep <= 4 or var.sleep >= 9:
        lifeExpectancy -= 2
    else:
        lifeExpectancy += 2
    
    if BMI< 18.5:
        # print("BMI: underweight")
        lifeExpectancy -= 4
    elif BMI < 25:
        # print("BMI: healthy")
        lifeExpectancy -= 0
    elif BMI < 30:
        # print("BMI: overweight")
        lifeExpectancy -= 4
    else:
        # print("BMI: obese")
        lifeExpectancy -= 14
    
    #convert to UNIX time
    lifeExpectancy *= 31536000 #convert years to seconds
    return round(DOB+lifeExpectancy) #return date of death in UNIX time

TARGET = check_and_load()
add_to_google_calendar(TARGET)

while True:
    current_time = int(time.time()) # Get current Unix time
    seconds_left = TARGET - current_time
    
    years = seconds_left // 31536000 # seconds in a year
    months = (seconds_left % 31536000) // 2592000 #seconds in 30 days
    days = (seconds_left % 2592000) // 86400 #seconds in an day
    hours = (seconds_left % 86400) // 3600 #seconds in an hour
    minutes = (seconds_left % 3600) // 60 #seconds in a min
    seconds = seconds_left % 60
    
    DaysRemaining = (seconds_left//86400)

    os.system('cls') # Clear terminal
    print(f"TIME REMAINING: {years}y {months}m {days}d {hours}h {minutes}m {seconds}s")
    
    #print(f"SECONDS REMAINING: {seconds_left}")
    #print(f"DAYS REMAINING: {DaysRemaining}")
    #print(f"WEEEKS REMAINING: {DaysRemaining//7}")
    
    time.sleep(1)
