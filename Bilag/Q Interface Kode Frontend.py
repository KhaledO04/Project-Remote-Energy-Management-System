import tkinter as tk 
import tkinter.font as tkFont # For Text Fonts
import requests # APT
import time #API timer
from time import strftime # For Clock
import FileHandle

#Første gang koden køres, skal man skrive de næste to sætninger i terminalen og kører dem
#python skal allerede være installeret
#pip install tk
#pip install requests


# Colors
bg_color = "#A6E3E9" 
header_color = "#00ADB5" 
Button_color = "#CBF1F5"
text_color = "black"

def DisplayNames(self, filename):
        list = FileHandle.GetAll(filename)
        names = []

        for i,_ in enumerate(list):
            names.append(list[i]["name"])
            
        for name in names:
            self.insert(tk.END, name)

class InterFase:
    def __init__(self, root):
        self.root = root  # Assign root to self.root

        # Set the title of the window to "HUB"
        self.root.title("HUB")
        # Set the size of the window to 800x480 pixels
        width = 800
        height = 480
        # Apply the calculated size and position to set the geometry of the window
        self.root.geometry(f'{width}x{height}')
        # Make the window non-resizable in width and height
        self.root.resizable(width=False, height=False)
        
        # Fonts
        ft10 = tkFont.Font(family='Times', size=10,weight='bold')
        ft20 = tkFont.Font(family='Times', size=20,weight='bold')
        ft38 = tkFont.Font(family='Times', size=38,weight='bold')
        ft13 = tkFont.Font(family='Times', size=13, weight='bold')

        root.config(bg=bg_color)

        #Header Text
        HUBHeder_Label = tk.Label(root, text="Welcome HUB", font=ft38, fg=text_color, bg=header_color, justify="center")
        HUBHeder_Label.place(x=0, y=0, width=800, height=100)

        # Labels - HUB - Main Menu
        # Clock Label (Need a Clock)
        Clock_Label = tk.Label(root, font=('Times', 40, "bold"), fg="#000000", bg=bg_color, justify="center")
        Clock_Label.place(x=260, y=225, width=280, height=100)
        # This function is used to display time on the label
        def display_time():
            string = strftime('%H:%M:%S')
            Clock_Label.config(text=string)
            Clock_Label.after(1000, display_time)
        # Styling the label widget so that clock will look more attractive
        display_time()
        
     
        # Weather Label 
        self.Weather_Label = tk.Label(root, text="", font=ft13, fg=text_color, bg=bg_color, justify="center")
        self.Weather_Label.place(x=280, y=320, width=240, height=100)
        # Call fetch_and_display_weather() function initially to display the weather
        self.fetch_and_display_weather()

        # El Price Label
        self.ELPrice_Label = tk.Label(root, text="", font=ft13, fg=text_color, bg=bg_color, justify="center")
        self.ELPrice_Label.place(x=250, y=140, width=300, height=100)
        # Call fetch_and_display_price() function initially to display the price
        self.fetch_and_display_price()

        # Buttons - HUB - Main Menu
        # Functions
        Functions_Button = tk.Button(root, text="Functions", font=ft20, fg=text_color, bg=Button_color, justify="center", activebackground=Button_color)
        Functions_Button.place(x=100, y=130, width=150, height=100)
        Functions_Button["command"] = self.open_functions  # Bind button command to the method in InterFase

        # Data
        Data_Button = tk.Button(root, text="Data", font=ft20, fg=text_color, bg=Button_color, justify="center", activebackground=Button_color)
        Data_Button.place(x=100, y=330, width=150, height=100)
        Data_Button["command"] = self.open_data  # Bind button command to the method in InterFase

        # Rooms
        Rooms_Button = tk.Button(root, text="Rooms", font=ft20, fg=text_color, bg=Button_color, justify="center", activebackground=Button_color)
        Rooms_Button.place(x=550, y=130, width=150, height=100)
        Rooms_Button["command"] = self.open_rooms  # Bind button command to the method in InterFase

        # Units
        Units_Button = tk.Button(root, text="Units", font=ft20, fg=text_color, bg=Button_color, justify="center", activebackground=Button_color)
        Units_Button.place(x=550, y=330, width=150, height=100)
        Units_Button["command"] = self.open_units  # Bind button command to the method in InterFase

        # Settings
        Settings_Button = tk.Button(root, text="⚙️ Settings", font=ft10, fg=text_color, bg=bg_color, justify="center", activebackground=bg_color)
        Settings_Button.place(x=670, y=40, width=80, height=25)
        Settings_Button["command"] = self.open_settings  # Bind button command to the method in InterFase

    def open_functions(self):
        # Open a new window for Functions
        functions_window = tk.Toplevel(self.root)
        # Create the FunctionsPage instance within the new window
        functions_page = FunctionsPage(functions_window)

    def open_data(self):
        # Open a new window for Data
        data_window = tk.Toplevel(self.root)
        # Create the DataPage instance within the new window
        data_page = DataPage(data_window)

    def open_rooms(self):
        # Open a new window for Rooms
        rooms_window = tk.Toplevel(self.root)
        # Create the RoomsPage instance within the new window
        rooms_page = RoomsPage(rooms_window)

    def open_units(self):
        # Open a new window for Units
        units_window = tk.Toplevel(self.root)
        # Create the UnitsPage instance within the new window
        units_page = UnitsPage(units_window)
    
    def open_settings(self):
        # Open a new window for Units
        settings_window = tk.Toplevel(self.root)
        # Create the UnitsPage instance within the new window
        settings_page = SettingsPage(settings_window)

    def fetch_and_display_weather(self):
        # Get weather data from API
        weather_data = requests.get("https://api.openweathermap.org/data/2.5/weather", params={'lat': 56.162937, 'lon': 10.203921, 'appid': '4d7dad712e7ed35a0f7bd672abbea9a3', 'units': 'metric'}).json()

        # Extract relevant weather information
        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']

        # Display weather information
        weather_info = f"Temperature: {temperature} °C\nDescription: {description}"
        self.Weather_Label.config(text=weather_info)

        # Schedule the function to run again after 3600 seconds (1 hour)
        self.root.after(3600 * 1000, self.fetch_and_display_weather)

    def fetch_and_display_price(self):
        # Definer API-endepunktet for Elspotprices
        url = "https://api.energidataservice.dk/dataset/Elspotprices"

        # Parametre for forespørgslen
        params = {
            'filter': '{"PriceArea": "DK1"}',
            'limit': 1  # Henter kun den seneste post
        }

        # Udfør HTTP GET-forespørgslen
        response = requests.get(url, params=params)

        # Tjek om forespørgslen var vellykket
        if response.status_code == 200:
            data = response.json()
            if 'records' in data and len(data['records']) > 0:
                latest_price_data = data['records'][0]  # Den seneste post for DK1
                # Konverter prisen til kWh og afrund til to decimaler
                price_per_kwh = round(float(latest_price_data['SpotPriceDKK']) / 1000, 2)
                price_status = f" Price status: {price_per_kwh} DKK/kWh "
            else:
                price_status = "Ingen data fundet"
        else:
            price_status = "Forespørgslen mislykkedes"

        # Update the label text with the price status
        self.ELPrice_Label.config(text=price_status)
        # Schedule the function to run again after 3600 seconds (1 hour)
        self.root.after(3600 * 1000, self.fetch_and_display_price)


class FunctionsPage:
    def __init__(self, root):
        # Initialize the FunctionsPage within the specified root window
        self.root = root
        # Set the title of the window to "HUB"
        self.root.title("Functions")    
        # Set the size of the window to 800x480 pixels
        width = 200
        height = 250
        # Get the screen width and height
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        # Calculate the position of the window to center it on the screen
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        # Apply the calculated size and position to set the geometry of the window
        self.root.geometry(alignstr)
        # Make the window non-resizable in width and height
        self.root.resizable(width=False, height=False)

        root.config(bg=bg_color)

        # Create a listbox widget within the root window
        self.listbox = tk.Listbox(root, bg=Button_color, fg=text_color)
        # Pack the listbox with some padding
        self.listbox.pack(pady=10)

        # Display names of functions in the list
        DisplayNames(self.listbox, "functions.txt")

        # Create an entry widget for user input
        self.entry = tk.Entry(root, width=30, bg=Button_color, fg=text_color,)
        # Pack the entry widget with some padding
        self.entry.pack(pady=5)
        # Create an "Add" button to add items to the listbox
        self.add_button = tk.Button(root, text="Add", command=self.add_item, fg=text_color, activebackground=header_color, bg=Button_color)
        # Pack the "Add" button to the left with some padding
        self.add_button.pack(side=tk.LEFT, padx=5)
        # Create a "Delete" button to delete selected items from the listbox
        self.delete_button = tk.Button(root, text="Delete", command=self.delete_item, fg=text_color, activebackground=header_color, bg=Button_color)
        # Pack the "Delete" button to the left with some padding
        self.delete_button.pack(side=tk.LEFT, padx=5)
        
        # Bind the double-click event to the listbox
        self.listbox.bind("<Double-1>", self.open_selected_item)

    def add_item(self):
        # Get the text from the entry widget
        entry_text = self.entry.get()
        # Insert the text into the listbox at the end
        self.listbox.insert(tk.END, entry_text)

        # Adds function to file
        FileHandle.AddToFile("functions.txt", entry_text)

    def delete_item(self):
        functions = FileHandle.GetAll("functions.txt")

        # Get the index of the selected item(s)
        selected_index = self.listbox.curselection()[0]

        functionData = functions[selected_index]

        # Get the index of the selected item(s)
        selected_index = self.listbox.curselection()
        # If an item is selected, delete it from the listbox
        if selected_index:
            self.listbox.delete(selected_index)

            # Delete selected function from file
            FileHandle.DeleteInFile("functions.txt", functionData["id"])

    def open_selected_item(self, event):
        functions = FileHandle.GetAll("functions.txt")

        # Get the index of the double-clicked item
        index = self.listbox.curselection()[0]
        # Get the text of the double-clicked item
        functionData = functions[index]
        # Open a new window with the item's name as the title
        item_window = tk.Toplevel(self.root)
        item_window.title(functionData["name"])
        # Create an instance of the App class inside the new window
        app = FunctionsSettings(item_window, functionData)

class FunctionsSettings:
    def __init__(self, root, data):
        # Initialize the FunctionsPage within the specified root window
        self.root = root
        # Set the title of the window to "HUB"
        self.root.title("Setting For Function")    
        # Set the size of the window to 800x480 pixels
        width = 800
        height = 480
        # Apply the calculated size and position to set the geometry of the window
        self.root.geometry(f'{width}x{height}')
        # Make the window non-resizable in width and height
        self.root.resizable(width=False, height=False)

        # Fonts
        ft38 = tkFont.Font(family='Times', size=38,weight='bold')
        ft17 = tkFont.Font(family='Times', size=17,weight='bold')
        ft = tkFont.Font(family='Times', size=12,weight='bold')
        
        # Background configur
        root.config(bg=bg_color)

        # Header Text
        HeaderFS_Label = tk.Label(root, text=f"Settings for {data['name']}", font=ft38, fg=text_color, bg=header_color, justify="center")
        HeaderFS_Label.place(x=0, y=0, width=800, height=100)
        
        # Text
        TextForFS_Label = tk.Label(root, text="Set wanted temperature or maximum price to pay", font=ft17, fg=text_color, bg=bg_color, justify="center")
        TextForFS_Label.place(x=150, y=100, width=500, height=50)

        # Label
        label_ideal = tk.Label(root, text="Ideal", font=ft, fg=text_color, bg=bg_color, justify="center")
        label_ideal.place(x=525, y=210)

        label_Acceptable = tk.Label(root, text="Acceptable", font=ft, fg=text_color, bg=bg_color, justify="center")
        label_Acceptable.place(x=580, y=235)

        label_Minimum = tk.Label(root, text="Minimum", font=ft, fg=text_color, bg=bg_color, justify="center")
        label_Minimum.place(x=640, y=265)

        # Variable to control the radio buttons
        self.radio = tk.IntVar()  

        # Radio buttons
        Price_Radio = tk.Radiobutton(root, text="Price 💰", font=ft, fg=text_color, bg=bg_color, activebackground=bg_color, variable=self.radio, value=1, command=self.Price_Radio_command)
        Price_Radio.place(x=100, y=160, width=150, height=50)

        Temp_Radio = tk.Radiobutton(root, text="Temperature 🌡️", font=ft, fg=text_color, bg=bg_color, activebackground=bg_color, variable=self.radio, value=2, command=self.Temp_Radio_command)
        Temp_Radio.place(x=550, y=160, width=150, height=50)

        # Scales
        self.price_scale = tk.Scale(root, from_=0, to=5, orient="vertical", bg=bg_color, activebackground=bg_color, highlightbackground=header_color, troughcolor=header_color, width=20, sliderlength=30,resolution=0.01)
        self.price_scale.set(data["prisloft"])
        self.price_scale.place(x=150, y=220, height=200) 

        self.temp_scale = tk.Scale(root, from_=0, to=30, orient="vertical", bg=bg_color, activebackground=bg_color, highlightbackground=header_color, troughcolor=header_color, width=20, sliderlength=30, resolution=0.1)
        self.temp_scale.set(data["temperatur"]) 
        self.temp_scale.place(x=520, y=240, height=180) 

        self.Acceptable_scale = tk.Scale(root,  from_=0, to=30, orient="vertical", bg=bg_color, activebackground=bg_color, highlightbackground=header_color, troughcolor=header_color, width=20, sliderlength=30, resolution=0.1)
        self.Acceptable_scale.set(data["markerHigh"]) 
        self.Acceptable_scale.place(x=580, y=260, height=160)

        self.Minimum_scale = tk.Scale(root,  from_=0, to=30, orient="vertical", bg=bg_color, activebackground=bg_color, highlightbackground=header_color, troughcolor=header_color, width=20, sliderlength=30, resolution=0.1)
        self.Minimum_scale.set(data["markerLow"])  
        self.Minimum_scale.place(x=640, y=290, height=130)
        
        # Save button
        self.save_button = tk.Button(root, text="Save", font=ft, fg=text_color, bg=bg_color, activebackground=bg_color, command=lambda: self.save_settings(data["id"]))
        self.save_button.place(x=350, y=420, width=100, height=30)

        # Temp radio on as default
        self.radio.set(2)
        self.Temp_Radio_command() 


    def Price_Radio_command(self):
        print("Price selected")
        self.price_scale.config(state="normal")
        self.temp_scale.config(state="disabled")
        self.Acceptable_scale.config(state="disabled") 
        self.Minimum_scale.config(state="disabled")  

    def Temp_Radio_command(self):
        print("Temperature selected")
        self.price_scale.config(state="disabled")
        self.temp_scale.config(state="normal")
        self.Acceptable_scale.config(state="normal")  
        self.Minimum_scale.config(state="normal")  
    

    def save_settings(self, ID):
        editValues = []

        # Price value
        editValues.append(self.price_scale.get())

        # Temp value
        editValues.append(self.temp_scale.get())

        # Marker one value
        editValues.append(self.Acceptable_scale.get())

        # Marker two value
        editValues.append(self.Minimum_scale.get())


        FileHandle.EditLines("functions.txt", ID, editValues)
        print("Settings saved")



class RoomsPage:
    def __init__(self, root):
         # Initialize the FunctionsPage within the specified root window
        self.root = root
        # Set the title of the window to "HUB"
        self.root.title("Rooms")
        # Set the size of the window to 800x480 pixels
        width = 200
        height = 250
        # Get the screen width and height
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        # Calculate the position of the window to center it on the screen
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        # Apply the calculated size and position to set the geometry of the window
        self.root.geometry(alignstr)
        # Make the window non-resizable in width and height
        self.root.resizable(width=False, height=False)

        root.config(bg=bg_color)

        # Create a listbox widget within the root window
        self.listbox = tk.Listbox(root, bg=Button_color, fg=text_color)
        # Pack the listbox with some padding
        self.listbox.pack(pady=10)

        # Display names of functions in the list
        DisplayNames(self.listbox, "rooms.txt")

        # Create an entry widget for user input
        self.entry = tk.Entry(root, width=30, fg=text_color, bg=Button_color)
        # Pack the entry widget with some padding
        self.entry.pack(pady=5)
        # Create an "Add" button to add items to the listbox
        self.add_button = tk.Button(root, text="Add", command=self.add_item, fg=text_color, activebackground=header_color, bg=Button_color)
        # Pack the "Add" button to the left with some padding
        self.add_button.pack(side=tk.LEFT, padx=5)
        # Create a "Delete" button to delete selected items from the listbox
        self.delete_button = tk.Button(root, text="Delete", command=self.delete_item, fg=text_color, activebackground=header_color, bg=Button_color)
        # Pack the "Delete" button to the left with some padding
        self.delete_button.pack(side=tk.LEFT, padx=5)

        # Bind the double-click event to the listbox
        self.listbox.bind("<Double-1>", self.open_selected_item)

    def add_item(self):
        # Get the text from the entry widget
        entry_text = self.entry.get()
        # Insert the text into the listbox at the end
        self.listbox.insert(tk.END, entry_text)
        # Add room to file
        FileHandle.AddToFile("rooms.txt", entry_text)

    def delete_item(self):
        rooms = FileHandle.GetAll("rooms.txt")

        # Get the index of the selected item(s)
        selected_index = self.listbox.curselection()[0]
        roomData = rooms[selected_index]
        # If an item is selected, delete it from the listbox
        if selected_index:
            self.listbox.delete(selected_index)

            # Delete selected room from file
            FileHandle.DeleteInFile("rooms.txt", roomData["id"])

    def open_selected_item(self, event):
        rooms = FileHandle.GetAll("rooms.txt")

        # Get the index of the double-clicked item
        index = self.listbox.curselection()[0]
        # Get the text of the double-clicked item
        roomData = rooms[index]
        # Open a new window with the item's name as the title
        item_window = tk.Toplevel(self.root)
        item_window.title(roomData["name"])
        # Create an instance of the App class inside the new window
        app = RoomsSettings(item_window, roomData)

class RoomsSettings:
    def __init__(self, root, data):
        # Initialize the FunctionsPage within the specified root window
        self.root = root
        # Set the title of the window to "HUB"
        self.root.title("Setting For Room")    
        # Set the size of the window to 800x480 pixels
        width = 800
        height = 480
        # Apply the calculated size and position to set the geometry of the window
        self.root.geometry(f'{width}x{height}')
        # Make the window non-resizable in width and height
        self.root.resizable(width=False, height=False)
        
        # Fonts
        ft38 = tkFont.Font(family='Times', size=38, weight='bold')
        ft17 = tkFont.Font(family='Times', size=17, weight='bold')
        ft15 = tkFont.Font(family='Times', size=15, weight='bold')
        ft = tkFont.Font(family='Times', size=12, weight='bold')
        
        # Background configur
        root.config(bg=bg_color)

        # Header Text
        HeaderRS_Label = tk.Label(root, text=f"Settings for {data['name']}", font=ft38, fg=text_color, bg=header_color, justify="center", pady=20)
        HeaderRS_Label.place(x=0, y=0, width=800, height=100)

        # Text
        TextForRS_Label = tk.Label(root, text="Set wanted temperature, maximum price to pay or a saved function", font=ft15, fg=text_color, bg=bg_color, justify="center")
        TextForRS_Label.place(x=75, y=100, width=650, height=50)
        
        # Label
        label_ideal = tk.Label(root, text="Ideal", font=ft, fg=text_color, bg=bg_color, justify="center")
        label_ideal.place(x=525, y=210)

        label_Acceptable = tk.Label(root, text="Acceptable", font=ft, fg=text_color, bg=bg_color, justify="center")
        label_Acceptable.place(x=580, y=235)

        label_Minimum = tk.Label(root, text="Minimum", font=ft, fg=text_color, bg=bg_color, justify="center")
        label_Minimum.place(x=640, y=265)

        # Variable to control the radio buttons
        self.radio = tk.IntVar()  

        # Radio buttons
        Price_Radio = tk.Radiobutton(root, text="Price 💰", font=ft, fg=text_color, bg=bg_color, activebackground=bg_color, variable=self.radio, value=1, command=self.Price_Radio_command)
        Price_Radio.place(x=100, y=160, height=50)

        Saved_Functions_Radio = tk.Radiobutton(root, text="Saved Functions", font=ft, fg=text_color, bg=bg_color, activebackground=bg_color, variable=self.radio, value=3, command=self.Saved_Functions_Radio_command)
        Saved_Functions_Radio.place(x=325, y=160, height=50)

        Temp_Radio = tk.Radiobutton(root, text="Temperature 🌡️", font=ft, fg=text_color, bg=bg_color, activebackground=bg_color, variable=self.radio, value=2, command=self.Temp_Radio_command)
        Temp_Radio.place(x=550, y=160, height=50)

        # Scales
        self.price_scale = tk.Scale(root, from_=0, to=5, orient="vertical", bg=bg_color, activebackground=bg_color, highlightbackground=header_color, troughcolor=header_color, width=20, sliderlength=30,resolution=0.01)
        self.price_scale.set(data["prisloft"])
        self.price_scale.place(x=150, y=220, height=200) 

        self.temp_scale = tk.Scale(root, from_=0, to=30, orient="vertical", bg=bg_color, activebackground=bg_color, highlightbackground=header_color, troughcolor=header_color, width=20, sliderlength=30, resolution=0.1)
        self.temp_scale.set(data["temperatur"]) 
        self.temp_scale.place(x=520, y=240, height=180) 

        self.Acceptable_scale = tk.Scale(root,  from_=0, to=30, orient="vertical", bg=bg_color, activebackground=bg_color, highlightbackground=header_color, troughcolor=header_color, width=20, sliderlength=30, resolution=0.1)
        self.Acceptable_scale.set(data["markerHigh"]) 
        self.Acceptable_scale.place(x=580, y=260, height=160)

        self.Minimum_scale = tk.Scale(root,  from_=0, to=30, orient="vertical", bg=bg_color, activebackground=bg_color, highlightbackground=header_color, troughcolor=header_color, width=20, sliderlength=30, resolution=0.1)
        self.Minimum_scale.set(data["markerLow"])
        self.Minimum_scale.place(x=640, y=290, height=130)
        
        # Lists
        self.saved_functions_list = tk.Listbox(root, font=ft, fg=text_color, bg=bg_color, selectmode=tk.SINGLE)
        self.saved_functions_list.place(x=325, y=220, width=150, height=150)

        # Insert some initial items into the listbox
        # Display names of functions
        DisplayNames(self.saved_functions_list, "functions.txt")

        # Save button
        self.save_button = tk.Button(root, text="Save", font=ft, fg=text_color, bg=bg_color, activebackground=bg_color, command=lambda:self.save_settings(data["id"]))
        self.save_button.place(x=350, y=420, width=100, height=30)
        
        # Temp radio on as default
        self.radio.set(2)
        self.Temp_Radio_command()


    def Price_Radio_command(self):
        print("Price selected")
        self.saved_functions_list.config(state="disabled")  # Disable the list for saved functions
        self.price_scale.config(state="normal")  # Enable the scale for Price
        self.temp_scale.config(state="disabled")  # Disable the scale for Temperature
        self.Acceptable_scale.config(state="disabled") 
        self.Minimum_scale.config(state="disabled")  

    def Saved_Functions_Radio_command(self):
        print("Saved Functions selected")
        self.saved_functions_list.config(state="normal")  # Enable the list for saved functions
        self.price_scale.config(state="disabled")  # Disable the scale for Price
        self.temp_scale.config(state="disabled")  # Disable the scale for Temperature
        self.Acceptable_scale.config(state="disabled") 
        self.Minimum_scale.config(state="disabled")  

    def Temp_Radio_command(self):
        print("Temperature selected")
        self.saved_functions_list.config(state="disabled")  # Disable the list for saved functions
        self.price_scale.config(state="disabled")  # Disable the scale for Price
        self.temp_scale.config(state="normal")  # Enable the scale for Temperature
        self.Acceptable_scale.config(state="normal")  
        self.Minimum_scale.config(state="normal")  

    def save_settings(self, ID):
        editValues = []

        # Price value
        editValues.append(self.price_scale.get())

         # Temp value
        editValues.append(self.temp_scale.get())

        # Price value
        editValues.append(self.Acceptable_scale.get())

        # Price value
        editValues.append(self.Minimum_scale.get())
        print(editValues)

        FileHandle.EditLines("rooms.txt", ID, editValues)



class UnitsPage:
    def __init__(self, root):
        # Initialize the FunctionsPage within the specified root window
        self.root = root
        # Set the title of the window to "HUB"
        self.root.title("Units")
        # Set the size of the window to 800x480 pixels
        width = 200
        height = 250
        # Get the screen width and height
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        # Calculate the position of the window to center it on the screen
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        # Apply the calculated size and position to set the geometry of the window
        self.root.geometry(alignstr)
        # Make the window non-resizable in width and height
        self.root.resizable(width=False, height=False)

        root.config(bg=bg_color)

        # Create a listbox widget within the root window
        self.listbox = tk.Listbox(root, bg=Button_color, fg=text_color)
        # Pack the listbox with some padding
        self.listbox.pack(pady=10)

        # Insert some initial items into the listbox
        initial_items = ["Bike Battery", "Iphone"]
        for item in initial_items:
            self.listbox.insert(tk.END, item)

        # Create an entry widget for user input
        self.entry = tk.Entry(root, width=30, bg=Button_color, fg=text_color)
        # Pack the entry widget with some padding
        self.entry.pack(pady=5)
        # Create an "Add" button to add items to the listbox
        self.add_button = tk.Button(root, text="Add", command=self.add_item, activebackground=header_color, bg=Button_color, fg=text_color)
        # Pack the "Add" button to the left with some padding
        self.add_button.pack(side=tk.LEFT, padx=5)
        # Create a "Delete" button to delete selected items from the listbox
        self.delete_button = tk.Button(root, text="Delete", command=self.delete_item, activebackground=header_color, bg=Button_color, fg=text_color)
        # Pack the "Delete" button to the left with some padding
        self.delete_button.pack(side=tk.LEFT, padx=5)

        # Bind the double-click event to the listbox
        self.listbox.bind("<Double-1>", self.open_selected_item)

    def add_item(self):
        # Get the text from the entry widget
        entry_text = self.entry.get()
        # Insert the text into the listbox at the end
        self.listbox.insert(tk.END, entry_text)

    def delete_item(self):
        # Get the index of the selected item(s)
        selected_index = self.listbox.curselection()
        # If an item is selected, delete it from the listbox
        if selected_index:
            self.listbox.delete(selected_index)

    def open_selected_item(self, event):
        # Get the index of the double-clicked item
        index = self.listbox.curselection()
        # Get the text of the double-clicked item
        item = self.listbox.get(index)
        # Open a new window with the item's name as the title
        item_window = tk.Toplevel(self.root)
        item_window.title(item)
        # Create an instance of the App class inside the new window
        app = UnitsSettings(item_window)

class UnitsSettings:
    def __init__(self, root):
        # Initialize the FunctionsPage within the specified root window
        self.root = root
        # Set the title of the window to "HUB"
        self.root.title("Setting For Unit")    
        # Set the size of the window to 800x480 pixels
        width = 800
        height = 480
        # Apply the calculated size and position to set the geometry of the window
        self.root.geometry(f'{width}x{height}')
        # Make the window non-resizable in width and height
        self.root.resizable(width=False, height=False)
        
        #Fonts
        ft38 = tkFont.Font(family='Times', size=38, weight='bold')
        ft17 = tkFont.Font(family='Times', size=17, weight='bold')
        ft20 = tkFont.Font(family='Times', size=20, weight='bold')
        ft15 = tkFont.Font(family='Times', size=15, weight='bold')
        ft = tkFont.Font(family='Times', size=12, weight='bold')
        
        # Background configur
        root.config(bg=bg_color)

        # Header Text
        HeaderRS_Label = tk.Label(root, text="Setting for your unit", font=ft38, fg=text_color, bg=header_color, justify="center", pady=20)
        HeaderRS_Label.place(x=0, y=0, width=800, height=100)

        # Text
        TextForRS_Label = tk.Label(root, text="Set maximum price to pay 💰", font=ft20, fg=text_color, bg=bg_color, justify="center")
        TextForRS_Label.place(x=150, y=150, width=500, height=50)

        # Horizontal scale for price
        self.price_scale = tk.Scale(root, from_=0, to=5, orient="horizontal", bg=bg_color, activebackground=bg_color, highlightbackground=header_color, troughcolor=header_color, width=20, sliderlength=30,resolution=0.01)
        self.price_scale.set(1) #Default Price = 1
        self.price_scale.place(x=150, y=230,width=500) 

        # Save button
        self.save_button = tk.Button(root, text="Save", font=ft, fg=text_color, bg=bg_color, activebackground=bg_color, command=self.save_settings)
        self.save_button.place(x=350, y=320, width=100, height=30)

    def save_settings(self):
        # Implement functionality to save settings here
        print("Settings saved")



class DataPage:
    def __init__(self, root):
        # Initialize the FunctionsPage within the specified root window
        self.root = root
        # Set the title of the window to "HUB"
        self.root.title("Setting For Unit")    
        # Set the size of the window to 800x480 pixels
        width = 800
        height = 480
        # Apply the calculated size and position to set the geometry of the window
        self.root.geometry(f'{width}x{height}')
        # Make the window non-resizable in width and height
        self.root.resizable(width=False, height=False)
        
        # Fonts
        ft38 = tkFont.Font(family='Times', size=38, weight='bold')
        ft17 = tkFont.Font(family='Times', size=17, weight='bold')
        ft15 = tkFont.Font(family='Times', size=15, weight='bold')
        ft = tkFont.Font(family='Times', size=12, weight='bold')
        
        # Background configur
        root.config(bg=bg_color)

        # Header Text
        HeaderRS_Label = tk.Label(root, text="Your Data (Exampel)", font=ft38, fg=text_color, bg=header_color, justify="center")
        HeaderRS_Label.place(x=0, y=0, width=800, height=100)

        # Temp header
        TempData_Label = tk.Label(root, text="Temperture", font=ft15, fg=text_color, bg=bg_color, justify="center")
        TempData_Label.place(x=120, y=130, width=100, height=50)
        # Temp_list
        self.temp_list = tk.Listbox(root, font=ft, fg=text_color, bg=bg_color, selectmode=tk.BROWSE)
        self.temp_list.place(x=100, y=200, width=150, height=180)
        # Insert some temperature_data into the listboxes
        temperature_data = ["Living Room:     22°C",
                            "Bedroom:           20°C",
                            "Kitchen:             24°C",
                            "Bathroom:          21°C",
                            "Outdoor:            15°C"]
        for item in temperature_data:
            self.temp_list.insert(tk.END, item)
        # Disable the list
        self.temp_list.config(state=tk.DISABLED, disabledforeground=text_color)


        # Price header
        PriceData_Label = tk.Label(root, text="Price", font=ft15, fg=text_color, bg=bg_color, justify="center")
        PriceData_Label.place(x=350, y=130, width=100, height=50)
        # Price_list
        self.price_list = tk.Listbox(root, font=ft, fg=text_color, bg=bg_color, selectmode=tk.BROWSE)
        self.price_list.place(x=280, y=200, width=250, height=180)
        # Insert some electricity_data into the listboxes
        electricity_data = ["Current Price:                     0.15/kWh",
                            "Total Consumption:             500 kWh",
                            "Living Room Consumption: 100 kWh",
                            "Bedroom Consumption:         80 kWh",
                            "Kitchen Consumption:         120 kWh"]     
        for item in electricity_data:
            self.price_list.insert(tk.END, item)
        # Disable the list
        self.price_list.config(state=tk.DISABLED, disabledforeground=text_color)

        # Heating header
        HeatingData_Label = tk.Label(root, text="Heating", font=ft15, fg=text_color, bg=bg_color, justify="center")
        HeatingData_Label.place(x=580, y=130, width=100, height=50)
        # heating_list
        self.heating_list = tk.Listbox(root, font=ft, fg=text_color, bg=bg_color,  selectmode=tk.BROWSE)
        self.heating_list.place(x=560, y=200, width=150, height=180)
        # Insert some heating_data into the listboxes
        heating_data = ["Living Room:       On",
                        "Bedroom:             Off",
                        "Kitchen:               On",
                        "Bathroom:            Off",
                        "Outdoor:              Off"]        
        for item in heating_data:
            self.heating_list.insert(tk.END, item)
        # Disable the list
        self.heating_list.config(state=tk.DISABLED, disabledforeground=text_color)

        # Save button
        self.Refresh_button = tk.Button(root, text="Refresh data", font=ft, fg=text_color, bg=bg_color, activebackground=bg_color, command=self.refresh_data)
        self.Refresh_button.place(x=350, y=400, width=100, height=30)

    def refresh_data(self):
        # Here you can define the action when the refresh button is clicked
        print("Refreshing data...")



class SettingsPage:
    def __init__(self, root):
        # Setting title
        root.title("General Setting")
        # Setting window size
        width = 800
        height = 480
        root.geometry(f'{width}x{height}')
        root.resizable(width=False, height=False)
        
        ft38 = tkFont.Font(family='Times', size=38, weight='bold')
        ft17 = tkFont.Font(family='Times', size=17, weight='bold')
        ft15 = tkFont.Font(family='Times', size=15, weight='bold')
        ft = tkFont.Font(family='Times', size=12, weight='bold')
        
        root.config(bg=bg_color)
        
        HeaderRS_Label = tk.Label(root, text="General Settings", font=ft38, fg=text_color, bg=header_color, justify="center")
        HeaderRS_Label.place(x=0, y=0, width=800, height=100)

        # Black line
        black_label = tk.Label(root, bg="black")
        black_label.place(x=650, y=150, width=2, height=200)
        black_label1 = tk.Label(root, bg="black")
        black_label1.place(x=150, y=150, width=2, height=200)

        # Username Selection
        username_label = tk.Label(root, text="Username:", font=ft, fg=text_color, bg=bg_color, justify="left")
        username_label.place(x=250, y=130)
        username_entry = tk.Entry(root, font=ft, bg=Button_color)
        username_entry.place(x=400, y=130, width=150)
        # Indsæt placeholder-tekst
        username_text = "HUB"
        username_entry.insert(0, username_text)

        # Postcode Selection
        postcode_label = tk.Label(root, text="Postcode:", font=ft, fg=text_color, bg=bg_color, justify="left")
        postcode_label.place(x=250, y=160)
        postcode_entry = tk.Entry(root, font=ft, bg=Button_color)
        postcode_entry.place(x=400, y=160, width=100)
        # Indsæt placeholder-tekst
        postcode_text = "8200"
        postcode_entry.insert(0, postcode_text)

        # Levrendør Selection
        Company_label = tk.Label(root, text="Electric Company:", font=ft, fg=text_color, bg=bg_color, justify="left")
        Company_label.place(x=250, y=190)
        Company_entry = tk.Entry(root, font=ft, bg=Button_color)
        Company_entry.place(x=400, y=190, width=100)
        # Indsæt placeholder-tekst
        Company_text = "DK1"
        Company_entry.insert(0, Company_text)

        # WiFi Label
        wifi_label = tk.Label(root, text="WiFi:", font=ft17, fg=text_color, bg=bg_color, justify="left")
        wifi_label.place(x=250, y=240)

        # Network Name Label and Entry
        network_name_label = tk.Label(root, text="Network Name:", font=ft, fg=text_color, bg=bg_color, justify="left")
        network_name_label.place(x=250, y=280)
        network_name_entry = tk.Entry(root, font=ft, bg=Button_color)
        network_name_entry.place(x=400, y=280, width=150)
        # Indsæt placeholder-tekst
        network_name_text = "Feeling a Connection"
        network_name_entry.insert(0, network_name_text)

        # Password Label and Entry
        password_label = tk.Label(root, text="Password:", font=ft, fg=text_color, bg=bg_color, justify="left")
        password_label.place(x=250, y=310)
        password_entry = tk.Entry(root, font=ft, bg=Button_color, show="*")  # Show '*' for password
        password_entry.place(x=400, y=310, width=150)
        # Indsæt placeholder-tekst
        password_text = "IseeIt"
        password_entry.insert(0, password_text)

        # Connect/Check Connection button
        connect_button = tk.Button(root, text="Connect/Check Connection", font=ft, fg=text_color, bg=bg_color, activebackground="#6fa8dc", command=self.connect_wifi)
        connect_button.place(x=300, y=360, width=200, height=30)

        # Save button
        save_button = tk.Button(root, text="Save", font=ft, fg=text_color, bg=bg_color, activebackground="#6fa8dc", command=self.save_settings)
        save_button.place(x=350, y=400, width=100, height=30)

    def save_settings(self):
        # Implement functionality to save settings here
        print("Settings saved")
    
    def connect_wifi(self):
        # Implement functionality to connect/check WiFi connection here
        print("Connecting/Checking WiFi connection...")



# Main function to create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    interfase = InterFase(root)
    root.mainloop()