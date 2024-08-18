import csv
import os
from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import ttk, messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz
from PIL import Image, ImageTk

root = Tk()
root.title("Weather Forcaster")
root.geometry("900x500+300+200")
root.resizable(False, False)
search_history = []  # List to store search history
data_window = None
api_key = "" # Add Your Open Weather Map API Key

# Function to save weather data to CSV
def save_weather_to_csv(city, weather_data):
    file_exists = os.path.isfile('weather_data.csv')
    with open('weather_data.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["City", "Temperature (°C)", "Humidity", "Pressure (hPa)", "Wind Speed (m/s)", "Description", "DateTime"])
        writer.writerow([
            city,
            int(weather_data['main']['temp']-273.15),
            weather_data['main']['humidity'],
            weather_data['main']['pressure'],
            weather_data['wind']['speed'],
            weather_data['weather'][0]['description'],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])
    messagebox.showinfo("Info", "Weather data stored successfully!")

def getWeather():
    city = textfield.get()

    geolocator = Nominatim(user_agent="Weather_Forecaster")
    location = geolocator.geocode(city)
    obj = TimezoneFinder()
    timezone = obj.certain_timezone_at(lat=location.latitude, lng=location.longitude)

    home = pytz.timezone(timezone)
    local_time = datetime.now(home)
    current_time = local_time.strftime("%I:%M %p")
    clock.config(text=current_time)
    name.config(text="Current Weather")

    # Weather
    api = f"https://api.openweathermap.org/data/2.5/weather?lat={location.latitude}&lon={location.longitude}&appid={api_key}"

    json_data = requests.get(api).json()
    condition = json_data['weather'][0]['main']
    description = json_data['weather'][0]['description']
    temp = int(json_data['main']['temp']-273.15)
    pressure = json_data['main']['pressure']
    humidity = json_data['main']['humidity']
    wind = json_data['wind']['speed']

    # Hide suggestion box
    suggestion_list.place_forget()

    # Update UI
    t.config(text=(temp,"°C"))
    c.config(text=(condition,"|","Feels", "Like", temp, "°C"))
    w.config(text=(wind, "m/s"))
    h.config(text=humidity)
    d.config(text=description)
    p.config(text=(pressure, "hPa"))

    # Save weather data to CSV
    save_button.config(state="normal")
    save_button.config(command=lambda: save_weather_to_csv(city, json_data))

    # Update search history
    if city not in search_history:
        search_history.append(city)

def show_saved_data():
    global data_window
    
    # Close the previous data window if it exists
    if data_window is not None:
        data_window.destroy()

    try:
        with open('weather_data.csv', newline='') as file:
            reader = csv.reader(file)
            data_window = Toplevel(root)
            data_window.title("Saved Locations Data")
            data_window.geometry("1050x400")

            # List to store checkbox variables
            checkbox_vars = []
            rows = list(reader)

            # Display the heading row without a checkbox
            for j, heading in enumerate(rows[0]):
                heading_label = Label(data_window, text=heading, width=15, fg='black', font=('Arial', 10, 'bold'))
                heading_label.grid(row=0, column=j+1)

            # Display the data rows with checkboxes
            for i, row in enumerate(rows[1:], start=1):
                var = IntVar()  # Create an IntVar for each row
                checkbox_vars.append(var)
                
                cb = Checkbutton(data_window, variable=var)
                cb.grid(row=i, column=0)

                for j, value in enumerate(row):
                    label = Label(data_window, text=value, width=20, fg='blue')
                    label.grid(row=i, column=j+1)

            # Add "Delete Selected" button
            delete_button = Button(data_window, text="Delete Selected", command=lambda: delete_selected_rows(checkbox_vars, rows, data_window))
            delete_button.grid(row=len(rows), columnspan=10, pady=10)

    except FileNotFoundError:
        messagebox.showerror("Error", "No data saved yet.")

def delete_selected_rows(checkbox_vars, rows, data_window):
    # Indices of rows to keep
    rows_to_keep = [0] + [i+1 for i, var in enumerate(checkbox_vars) if not var.get()]

    if len(rows_to_keep) == len(rows):
        messagebox.showinfo("Info", "No rows selected for deletion.")
        return

    # Keep only the rows that were not selected
    rows = [rows[i] for i in rows_to_keep]

    # Write the updated data back to the CSV file
    with open('weather_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    messagebox.showinfo("Info", "Selected locations deleted successfully!")
    
    # Refresh the saved locations window
    for widget in data_window.winfo_children():
        widget.destroy()  # Clear the existing widgets
    show_saved_data()  # Reload the saved data window
    
# Collapsing Menu
def toggle_menu():
    if menu_frame.winfo_viewable():
        menu_frame.place_forget()
    else:
        menu_frame.place(x=0, y=0, width=200, height=500)
        menu_frame.lift()

# Resize and use the hamburger icon
def load_resized_image(image_path, size):
    image = Image.open(image_path)
    image = image.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(image)


# Fetch Location suggestions
def fetch_location_suggestions(query):
    try:
        api_url = f"http://api.openweathermap.org/geo/1.0/direct?q={query}&limit=5&appid={api_key}"
        response = requests.get(api_url)
        suggestions = response.json()

        # Check if the response is a list (which it should be if successful)
        if isinstance(suggestions, list):
            # Format the suggestions
            return [f"{item['name']}, {item.get('state', '')}, {item['country']}" for item in suggestions]
        else:
            # If the response is not a list, return an empty list or handle the error
            print("Unexpected API response format:", suggestions)
            return []
    except Exception as e:
        print("Error fetching location suggestions:", e)
        return []

    
def update_suggestions(event):
    query = textfield.get()
    if len(query) > 2:  # Show suggestions only after 3 characters are typed
        suggestions = fetch_location_suggestions(query)
        if suggestions:
            suggestion_list.delete(0, tk.END)
            for suggestion in suggestions:
                suggestion_list.insert(tk.END, suggestion)
            suggestion_list.place(x=50, y=100, width=350, height=150)  # Show the suggestion box
            suggestion_list.lift()
        else:
            suggestion_list.place_forget()  # Hide the suggestion box if there are no suggestions
    else:
        suggestion_list.place_forget()

# Handle selection from the suggestion list
def on_suggestion_select(event):
    try:
        # Check if a selection is made
        selection = suggestion_list.curselection()
        if selection:
            selected_city = suggestion_list.get(selection)
            textfield.delete(0, tk.END)
            textfield.insert(0, selected_city)
        suggestion_list.place_forget()  # Hide the suggestion list after selection
    except Exception as e:
        print("Error in on_suggestion_select:", e)

def show_search_history():
    history_window = Toplevel(root)
    history_window.title("Search History")
    history_window.geometry("400x300")

    if search_history:
        for i, city in enumerate(search_history):
            city_button = Button(history_window, text=city, font=("arial", 12), bg="#1ab5ef", fg="white", 
                                 command=lambda c=city: [textfield.delete(0, tk.END), textfield.insert(0, c), history_window.destroy()])
            city_button.pack(fill=X, pady=5)
    else:
        Label(history_window, text="No search history yet.", font=("arial", 12), bg="#333333", fg="white").pack(pady=50)



# Menu
menu_frame = Frame(root, bg="#333333")
menu_frame.place_forget()

saved_data_button = Button(menu_frame, text="Saved Locations", font=("arial", 15, "bold"), bg="#1ab5ef", fg="white", command=show_saved_data)
saved_data_button.pack(fill=X)

hamburger_icon = load_resized_image("assets/hamburger_icon.png", (40, 40))
hamburger_button = Button(root, image=hamburger_icon, borderwidth=0, cursor="hand2", command=toggle_menu)
hamburger_button.place(x=850, y=20)

# Search History Button in the Menu
history_button = Button(menu_frame, text="Search History", font=("arial", 15, "bold"), bg="#1ab5ef", fg="white", command=show_search_history)
history_button.pack(fill=X)

# Save Button
save_button = Button(root, text="Store Weather", state="disabled", font=("arial", 12, "bold"), bg="#1ab5ef", fg="white")
save_button.place(x=700, y=35)

# Search Box
Search_image = PhotoImage(file="assets/search.png")
myimage = Label(image=Search_image)
myimage.place(x=20, y=20)

textfield = tk.Entry(root, justify="center", width=17, font=("poppins", 25, "bold"), bg="#404040", border=0, fg="white")
textfield.place(x=50, y=40)
textfield.focus()

Search_icon = PhotoImage(file="assets/search_icon.png")
myimage_icon = Button(image=Search_icon, borderwidth=0, cursor="hand2", bg="#404040", command=getWeather)
myimage_icon.place(x=400, y=34)

## Create a Listbox for displaying suggestions
suggestion_list = tk.Listbox(root, bg="#404040", fg="white", font=("poppins", 15))
suggestion_list.place_forget()

textfield.bind("<KeyRelease>", update_suggestions)
suggestion_list.bind("<<ListboxSelect>>", on_suggestion_select)

# Logo
logo_image = PhotoImage(file="assets/logo.png")
logo = Label(image=logo_image)
logo.place(x=150, y=100)

# Bottom Box
Frame_image = PhotoImage(file="assets/box.png")
frame_myimage = Label(image=Frame_image)
frame_myimage.pack(padx=5, pady=5, side=BOTTOM)

# Time
name = Label(root, font=("arial", 15, "bold"))
name.place(x=30, y=100)
clock = Label(root, font=("Helvetica", 20))
clock.place(x=30, y=130)

# Label
label1 = Label(root, text="Wind", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
label1.place(x=120, y=400)

label2 = Label(root, text="Humidity", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
label2.place(x=250, y=400)

label3 = Label(root, text="Description", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
label3.place(x=430, y=400)

label4 = Label(root, text="pressure", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
label4.place(x=650, y=400)

t = Label(font=("arial", 70, "bold"), fg="#ee666d")
t.place(x=450, y=150)
c = Label(font=("ariel", 15, "bold"))
c.place(x=400, y=250)

w = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
w.place(x=120, y=430)
h = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
h.place(x=280, y=430)
d = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
d.place(x=430, y=430)
p = Label(text="...", font=("arial", 20, "bold"), bg="#1ab5ef")
p.place(x=650, y=430)

root.mainloop()