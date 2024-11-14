import tkinter as tk
from logging import warning, debug

import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap

import getData


def search():
    city = city_entry.get()
    result = getData.get_weather_data(city)
    if result is None:
        messagebox.showinfo("Error", "Please enter a valid city")
        return
    #if city is found, unpack weather information
    city, temperature, description, country, icon_url, image= result
    location_label.config(text=f"{city}, {country}")

    # update the weather icon
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon

    # update temperature and description labels
    temperature_label.configure(text=f"Temperature: {temperature}°C")
    description_label.configure(text=f"Description: {description}")


root = ttkbootstrap.Window(themename="morph")
root.title("Weather App")
root.geometry("600x600")

#Enter the city name
city_entry = tk.Entry(root, font="Helvetica 12 bold")
city_entry.pack(pady=10, padx=10)

#Button to search for city-specific weather information
search_button = tk.Button(root, text="Search", command=search) # command argument runs the method "search"
search_button.pack(pady=10, padx=10)

#Label Widget to show city & country name
location_label = tk.Label(root, font="Helvetica, 25")
location_label.pack(pady=20)

#Label Widget to show weather icon
icon_label = tk.Label(root)
icon_label.pack()

#Label Widget to show temperature
temperature_label = tk.Label(root, font="Helvetica, 20 bold")
temperature_label.pack()

#Label Widget to show weather description
description_label = tk.Label(root, font="Helvetica, 20 bold")
description_label.pack()

#start the window
root.mainloop()