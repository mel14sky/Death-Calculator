import tkinter as tk
from tkinter import ttk
from datetime import date, datetime
import csv
import os
from dataclasses import dataclass

# --- 1. DEFINE YOUR DATA STRUCTURE ---
@dataclass
class Answers:
    birthday: str = ""
    height: int = 0
    weight: int = 0
    gender: str = ""
    country: str = ""
    smoke: str = ""
    alcohol: str = ""
    stress: str = ""
    exercise: str = ""
    diet: str = ""
    outlook: str = ""
    sleep: int = 0

# --- 2. MAIN UI FUNCTION ---
def questions():
    # Setup paths
    folder = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(folder, "data.csv")
    
    # Store the final result here
    final_data = None
    
    # Track current question index and temporarily store answers in a dictionary
    state = {
        "current": 0,
        "answers": {} 
    }

    # Define questions as: (Question, Field Name, Input Type)
    q_list = [
        ("What is your date of birth?", "birthday", "date"),
        ("How tall are you (cm)?", "height", "number"),
        ("How much do you weigh (kg)?", "weight", "number"),
        ("What is your gender?", "gender", ["Male", "Female"]),
        ("What country were you born in?", "country", "country"),
        ("Do you smoke?", "smoke", ["Yes", "No"]),
        ("Do you drink alcohol?", "alcohol", ["Yes", "No"]),
        ("Are you often stressed?", "stress", ["Yes", "No"]),
        ("How much do you exercise?", "exercise", ["None", "Moderate", "Active"]),
        ("What is your diet?", "diet", ["Poor", "Average", "Good"]),
        ("What is your outlook on life?", "outlook", ["Pessimistic", "Neutral", "Optimistic"]),
        ("How much sleep do you get?", "sleep", "number"),
    ]

    def get_countries():
        countries = []
        if os.path.exists(data_file):
            with open(data_file, "r") as f:
                file = csv.DictReader(f)
                for row in file:
                    countries.append(row["country"])
        else:
            # Fallback if CSV is missing
            countries = ["United States", "United Kingdom", "Canada", "Australia"] 
        return sorted(set(countries))

    # --- INITIALIZE TKINTER ROOT ---
    root = tk.Tk()
    root.title("Lifestyle Survey")
    root.geometry("900x700")
    
    style = ttk.Style(root)
    style.theme_use('clam')

    # --- UI ELEMENTS ---
    frame = tk.Frame(root, padx=40, pady=30)
    frame.pack(expand=True, fill="both")

    question_label = tk.Label(frame, font=("Arial", 20, "bold"), wraplength=700)
    question_label.pack(pady=20)

    progress = ttk.Progressbar(frame, length=700)
    progress.pack(pady=5)

    progress_label = tk.Label(frame)
    progress_label.pack()

    # Input widgets
    entry = ttk.Entry(frame, width=35, font=("Arial", 14))
    button_frame = tk.Frame(frame)
    
    date_var = tk.StringVar()
    date_entry = ttk.Entry(frame, textvariable=date_var, width=25, font=("Arial", 14))
    
    country_var = tk.StringVar()
    country_entry = ttk.Entry(frame, textvariable=country_var, width=35, font=("Arial", 14))
    country_listbox = tk.Listbox(frame, height=10)

    selected_button = None

    # --- HELPER FUNCTIONS ---
    def format_date(event=None):
        text = date_var.get()
        cleaned = "".join([c for c in text if c.isdigit() or c == "/"])
        if len(cleaned) == 2 and not cleaned.endswith("/"):
            cleaned += "/"
        elif len(cleaned) == 5 and not cleaned.endswith("/"):
            cleaned += "/"
        cleaned = cleaned[:10]
        if cleaned != text:
            date_var.set(cleaned)
            date_entry.icursor(len(cleaned))
        check_valid()

    def update_country_list(event=None):
        typed = country_var.get().lower().strip()
        country_listbox.delete(0, tk.END)
        for c in get_countries():
            if typed in c.lower():
                country_listbox.insert(tk.END, c)

    def select_country(event):
        if country_listbox.curselection():
            country_var.set(country_listbox.get(country_listbox.curselection()))
            check_valid()

    def animate_progress(target):
        current_val = progress['value']
        if abs(current_val - target) < 0.5:
            progress['value'] = target
            return
        progress['value'] += (target - current_val) / 10
        root.after(15, lambda: animate_progress(target))

    def check_valid(event=None):
        q, field, q_type = q_list[state["current"]]
        valid = False

        if q_type == "date":
            try:
                d = datetime.strptime(date_var.get(), "%d/%m/%Y").date()
                valid = d <= date.today()
            except ValueError:
                valid = False
        elif q_type == "number":
            valid = entry.get().isdigit()
        elif q_type == "country":
            valid = country_var.get().strip().title() in get_countries()
        elif isinstance(q_type, list):
            valid = field in state["answers"] and state["answers"][field] != ""

        next_btn.config(state="normal" if valid else "disabled")

    def select_answer(ans, btn):
        nonlocal selected_button
        q, field, q_type = q_list[state["current"]]
        
        state["answers"][field] = ans
        
        if selected_button:
            selected_button.config(bg="SystemButtonFace")
        btn.config(bg="lightblue")
        selected_button = btn
        check_valid()

    def show_question():
        nonlocal selected_button
        
        q, field, q_type = q_list[state["current"]]
        question_label.config(text=q)

        # Hide all inputs
        for w in (entry, button_frame, date_entry, country_entry, country_listbox):
            w.pack_forget()
        for w in button_frame.winfo_children():
            w.destroy()

        selected_button = None
        saved = state["answers"].get(field, "")

        # Show appropriate input
        if q_type == "date":
            date_entry.pack(pady=10)
            date_var.set(saved)
        elif q_type == "number":
            entry.pack(pady=10)
            entry.delete(0, tk.END)
            entry.insert(0, saved)
        elif q_type == "country":
            country_entry.pack()
            country_listbox.pack()
            update_country_list()
            country_var.set(saved)
        elif isinstance(q_type, list):
            button_frame.pack()
            for option in q_type:
                btn = tk.Button(button_frame, text=option, width=25, height=2, font=("Arial", 12))
                btn.config(command=lambda o=option, b=btn: select_answer(o, b))
                if saved == option:
                    btn.config(bg="lightblue")
                    selected_button = btn
                btn.pack(pady=5)

        animate_progress((state["current"] / len(q_list)) * 100)
        progress_label.config(text=f"{state['current']+1}/{len(q_list)}")
        check_valid()

    def go_next():
        q, field, q_type = q_list[state["current"]]
        
        # Save text entry inputs before moving forward
        if q_type == "date":
            state["answers"][field] = date_var.get()
        elif q_type == "number":
            state["answers"][field] = int(entry.get()) # Convert to int
        elif q_type == "country":
            state["answers"][field] = country_var.get().strip().title()

        state["current"] += 1
        
        if state["current"] >= len(q_list):
            save_and_close()
        else:
            show_question()

    def go_back():
        if state["current"] > 0:
            state["current"] -= 1
            show_question()

    def save_and_close():
        nonlocal final_data
        # Populate the dataclass with the dictionary we've been building
        final_data = Answers(**state["answers"])
        root.destroy()

    # --- BINDINGS ---
    date_entry.bind("<KeyRelease>", format_date)
    country_entry.bind("<KeyRelease>", update_country_list)
    country_listbox.bind("<<ListboxSelect>>", select_country)
    entry.bind("<KeyRelease>", check_valid)

    # --- NAVIGATION BUTTONS ---
    btn_frame = tk.Frame(frame)
    btn_frame.pack(pady=20)

    tk.Button(btn_frame, text="Back", command=go_back, font=("Arial", 12)).pack(side="left", padx=10)
    next_btn = tk.Button(btn_frame, text="Next", state="disabled", command=go_next, font=("Arial", 12))
    next_btn.pack(side="left", padx=10)

    # --- START UI LOOP ---
    show_question()
    
    # Code pauses here until root.destroy() is called
    root.mainloop() 
    
    # Return the populated dataclass to main.py
    return final_data

# Allow testing the UI standalone without main.py
if __name__ == "__main__":
    result = questions()
    print("UI Closed. Collected Data:", result)
