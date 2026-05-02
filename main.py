import os, csv, time
from datetime import datetime
from API import add_to_google_calendar

folder = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(folder, "data.csv")
save_file = os.path.join(folder, "save.txt")

def checkforDBfile():
    try:
        with open(data_file, "r") as f:
            return
    except FileNotFoundError:
        print(f"Database file not found.")
        quit()

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
        UNIX_LE = questions()
        with open(save_file, "w") as file: #create file
            file.write(str(UNIX_LE)) #save UNIX life expecatcy to file
    return UNIX_LE

def questions():
    checkforDBfile()
    weight = int(input("how much do you weigh? (kg) "))
    height = int(input("how tall are you? (cm) "))

    while True:
        birthDay = input("when were you born? [d/mm/yyyy] ")
        DOB = DateofBirth(birthDay)
        if DOB is not None:
            break # continue as normal
        print("Invalid date")

    gender = input("what was is your gender? (m/f) ").strip().lower()
    country = input("what country are you from? ").strip().title()
    smoke = input("do you smoke? (y/n) ").strip().lower()
    alcohol = input("do you drink alcohol? (y/n) ").strip().lower()
    stress = input("are you often stressed? (y/n) ").strip().lower()
    exersise = input("how much do you exersies?\n - none\n - moderate (1-3 times a week)\n - active(4-7 times a week)\n").strip().lower()
    diet = input("what is your diet?\n - poor\n - average\n - good\n").strip().lower()
    outlook = input("what is your outlook on life\n - pessimistic\n - neutral\n - optimistic").strip().lower()
    sleep = int(input("how many hours do you sleep at night? "))
    BMI = CalculateBMI(weight,height)

    #calculation
    lifeExpectancy = GetFromDB(country,gender)
    lifeExpectancy += Exersie(exersise)
    lifeExpectancy += Diet(diet)
    lifeExpectancy += Outlook(outlook)

    if smoke == "y":
        lifeExpectancy -= 10
    if alcohol == "y":
        lifeExpectancy -= 4.5
    if stress == "y":
        lifeExpectancy -= 2.8

    if sleep < 0 or sleep >= 24:
        print("invalid sleep input")
        lifeExpectancy += 0
    elif sleep <= 4 or sleep >= 9:
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
