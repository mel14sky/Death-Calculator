# SQ4011 - Programming Project
## Death Calculator ⏳💀

[https://github.com/mel14sky/Death-Calculator](https://github.com/mel14sky/Death-Calculator)

| Morgan Lasky | 25198100@live.harper.ac.uk | mel14sky |
| --- | --- | --- |
| Jac Crofts | 25251000@live.harper.ac.uk | jac_dormer |

This python application calculates your estimated life expectancy based on demographic and lifestyle factors, then displays a live countdown to your date of death, it will add this event to your Google Calendar as a modern memento mori.

The idea of this morbid death clock is to inspire you to "carpe diem" and make the most of the little time you have. Life is short, and it's up to you, to give it meaning. I hope this Death Calculator inspires you to live the rest of your life to fullest doing the things you enjoy, and spending time with the people you love.

---

## Project Structure

- **main.py** imports data from data.csv containing average life expectancy based on country of birth and biological sex. It then calculates life expectancy from the answers taken from UI.py and adds this to the user's date of birth to find the date of death. This is converted to UNIX time. Before running UI.py a subroutine is also used to check if there is a save file. This will mean that the next time the user opens the program they won't need to re-answer all the questions, and the countdown will start straight away.

- **UI.py** creates the user interface and asks user questions like Do you smoke? And which country where you born in? These are saved in class which main.py will pull to calculate the date of death.

- **API.py** calls the google calendar API and adds the calculated date to the user's google calendar providing the "credentials.json" exists

- **data.csv** - The database containing life expectancy in different countries

- **credentials.json** - contains Google API OAuth credentials

- **save.txt** - code will generate a save file to store your UNIX timestamp

- **token.json** - code will generate this to store the active Google login

---

## Video Demo

# link to video goes here

---

## Set Up

- `pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib`

- download your API key and store it credentials.json

- If you want to restart the questions again simply delete the save.txt file

### To download your key:

- Go to [https://console.cloud.google.com/](https://console.cloud.google.com/) then click create a new project

- API & Services > Credentials > Create credentials > OAuth Client IDs

- Select Web App then click create

- Download the file and rename to "credentials.json" and put it in the project folder

- Go to audience and ensure the publishing status is set to in production.

<summary>set publishing status</summary> 
<img src="../image1.png" width="512">

---

## Task Breakdown

| **Task** | **Member** |
| --- | --- |
| Research factors that affect health the most | Jac |
| Find a database of life expectancy for different countries | Morgan |
| Write questions based on research to user to determine health | Morgan |
| main.py - Calculate date of death and add to user date of birth | Morgan |
| main.py - Create countdown clock from current time to date of death | Morgan |
| main.py - Create save file to store UNIX time for reopening the program | Morgan |
| main.py - Read in data from CSV file to get initial life expectancy | Morgan |
| Data validation for and error catching | Morgan |
| UI.py - Design UI | Jac |
| API.py - API call to add date to calendar | Morgan |
| Create video demonstration | Jac |
| Project description and Repo set up | Morgan |
