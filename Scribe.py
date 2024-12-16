import os
import customtkinter as ctk
from tkinter import filedialog, ttk
import uuid # Used for creating Unique_IDs

# Customize theme for the Custom-Tkinter App
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class Scribe(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set Application_Title-and-Logo
        self.title("Scribe")
        self.iconbitmap('./images/scribe_logo.ico')

        # Display-Window_Settings
        self.geometry("800x600")
        self.minsize(250,120)

        # Initialize Word_Wrap State
        self.word_wrap = True

        # Initialize a Navbar
        self.navbar = ctk.CTkFrame(self, bg_color="#1d1e1e", fg_color = "#1d1e1e")
        self.navbar.pack(side="top", fill="x")

        nav_file = ctk.CTkButton(self.navbar, text="File", width=45, height=20, corner_radius=0, command=self.toggle_file_menu, fg_color = "#1d1e1e", bg_color = "#1d1e1e", hover_color="#3b3b3b", font = ("Lexend", 10.5, "bold"))
        nav_edit = ctk.CTkButton(self.navbar, text="Edit", width=45, height=20, corner_radius=0, command=self.toggle_edit_menu, fg_color = "#1d1e1e", bg_color = "#1d1e1e", hover_color="#3b3b3b", font = ("Lexend", 10.5, "bold"))
        nav_view = ctk.CTkButton(self.navbar, text="View", width=45, height=20, corner_radius=0, command=self.toggle_view_menu, fg_color = "#1d1e1e", bg_color = "#1d1e1e", hover_color="#3b3b3b", font = ("Lexend", 10.5, "bold"))
        nav_file.pack(side = "left")
        nav_edit.pack(side = "left")
        nav_view.pack(side = "left")

        # Configure 'Style' for Notebook
        self.style = ttk.Style()
        self.style.theme_use("default")  # Use a base theme
        self.style.configure("TNotebook",background = "#2b2b2b", foreground = "#000000", borderwidth = 0, padding = [0,5])
        self.style.configure("TNotebook.Tab", background = "#1d1e1e", foreground = "#ffc300", padding = [10,6], font = ("Comic Sans MS", 10, "italic"))
        self.style.map("TNotebook.Tab",background = [("selected", "#2b2b2b")], foreground = [("selected", "#ffd60a")], borderwidth="0")

        # Initialize a Notebook for creating Tabbed-Interface
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        # Initialize the Initial_File-Path for Tabs(Notebooks)
        self.file_path = {}

        # Add the First Tab
        self.add_new_tab()

        # Add a plus button to 'Create a New Tab' 
        plus_tab = ctk.CTkFrame(self.notebook)
        self.notebook.add(plus_tab, text="  +  ")

        # Handles Events
        self.notebook.bind("<<NotebookTabChanged>>", self.event_handler)
      


    # Base_Operations---------------------------------------------------------------------------------------------------------------------------------------#

    # Initialize Text_Area (With respect to each Notebook Frame (Tab))
    def add_text_area(frame):
        text_area = ctk.CTkTextbox(frame, wrap="word", font = ('Comic Sans MS', 13, "normal"))
        text_area.pack(expand = True, fill="both", padx = 5, pady = 5)
        return text_area

    # Configure and Add New Tabs
    def add_new_tab(self):
        tab_id = uuid.uuid4()
        frame = ctk.CTkFrame(self.notebook)
        text_area = Scribe.add_text_area(frame) 

        if len(self.notebook.tabs()) != 0:
            # Add the new tab before the "+" tab
            plus_tab_index = len(self.notebook.tabs()) - 1
            self.notebook.insert(plus_tab_index, frame, text=f"Untitled - Scribet {len(self.notebook.tabs())}")

            # Automatically Switch to the Newly_Created_Tab
            self.notebook.select(plus_tab_index)
        else:
            self.notebook.add(frame, text = f"Untitled - Scribet {len(self.notebook.tabs())  + 1}")
        return tab_id,text_area
    

    def event_handler(self,event):
        # Update the Window_Title to Match the Selected_Tab's Title.
        current_tab = self.notebook.select()
        tab_title = self.notebook.tab(current_tab)["text"] # Get the value for 'text' attribute from the corresponding 'current_tab'.
        self.title(f"{tab_title}")  # Update window Title with 'current_tab' Title.

        #Handles the Event that '+' Tab was selected.
        current_tab_index = self.notebook.index(self.notebook.select()) # Get 'Index' of current_tab.
        if current_tab_index == len(self.notebook.tabs()) - 1:  # Last tab is the "+"
            self.add_new_tab()
    


    # Nav_Sub_Menu----------------------------------------------------------------------------------------------------------------------------------------------#

    #File_Menu
    file_menu = None
    
    def toggle_file_menu(self):
        if self.file_menu and self.file_menu.winfo_ismapped():
            self.file_menu.place_forget() #Hide File_Menu
        else:
            if self.edit_menu and self.edit_menu.winfo_ismapped():
                self.edit_menu.place_forget() #Hide Edit_Menu
            if self.view_menu and self.view_menu.winfo_ismapped():
                self.view_menu.place_forget() #Hide View_Menu
            self.display_file_menu() #Show File_Menu
    
    def display_file_menu(self):
        if not self.file_menu:
            self.file_menu = ctk.CTkFrame(self, fg_color = "#1c1c1c", corner_radius = 6)
            new = ctk.CTkButton(self.file_menu, text="New", command = self.new, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, anchor="w")
            open = ctk.CTkButton(self.file_menu, text="Open", command = self.open, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, anchor="w")
            save = ctk.CTkButton(self.file_menu, text="Save", command = self.save, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, anchor="w")

            new.pack(pady=0, padx=5)
            open.pack(pady=0, padx=5)
            save.pack(pady=0, padx=5)

        self.file_menu.place(x=5, y=25) #Show File_Menu


    #Edit_Menu
    edit_menu = None

    def toggle_edit_menu(self):
        if self.edit_menu and self.edit_menu.winfo_ismapped():
            self.edit_menu.place_forget() #Hide Edit_Menu
        else:
            if self.file_menu and self.file_menu.winfo_ismapped():
                self.file_menu.place_forget() #Hide File_Menu
            if self.view_menu and self.view_menu.winfo_ismapped():
                self.view_menu.place_forget() #Hide View_Menu
            self.display_edit_menu() #Show Edit_Menu
    
    def display_edit_menu(self):
        if not self.edit_menu:
            self.edit_menu = ctk.CTkFrame(self, fg_color = "#1c1c1c", corner_radius = 6)
            new = ctk.CTkButton(self.edit_menu, text="New", command = self.new, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, anchor="w")
            open = ctk.CTkButton(self.edit_menu, text="Open", command = self.open, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, anchor="w")
            save = ctk.CTkButton(self.edit_menu, text="Save", command = self.save, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, anchor="w")

            new.pack(pady=0, padx=5)
            open.pack(pady=0, padx=5)
            save.pack(pady=0, padx=5)

        self.edit_menu.place(x=55, y=25) #Show Edit_Menu


    #View_Menu
    view_menu = None
    
    def toggle_view_menu(self):
        if self.view_menu and self.view_menu.winfo_ismapped():
            self.view_menu.place_forget() #Hide View_Menu
        else:
            if self.file_menu and self.file_menu.winfo_ismapped():
                self.file_menu.place_forget() #Hide File_Menu
            if self.edit_menu and self.edit_menu.winfo_ismapped():
                self.edit_menu.place_forget() #Hide Edit_Menu
            self.display_view_menu() #Show View_Menu
    
    def display_view_menu(self):
        if not self.view_menu:
            self.view_menu = ctk.CTkFrame(self, fg_color = "#1c1c1c", corner_radius = 6)
            new = ctk.CTkButton(self.view_menu, text="New", command = self.new, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, anchor="w")
            open = ctk.CTkButton(self.view_menu, text="Open", command = self.open, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, anchor="w")
            save = ctk.CTkButton(self.view_menu, text="Save", command = self.save, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, anchor="w")

            new.pack(pady=0, padx=5)
            open.pack(pady=0, padx=5)
            save.pack(pady=0, padx=5)

        self.view_menu.place(x=95, y=25) #Show View_Menu



    # Sub_Menu_Operations---------------------------------------------------------------------------------------------------------------------------------------#
    
    # Get 'current_tab' Name
    def current_tab_name(self):
        return self.notebook.nametowidget(self.notebook.select()) # Returns the 'Internal_Tkinter_Widget_Name' for the 'current_tab' Frame. 

    # Get 'current_tab' Text_Content
    def current_tab_text(self):
        current_tab = self.current_tab_name()
        return current_tab.winfo_children()[0] # Gets Content from a Tab's 'ctk.CTkTextbox' widget. 'winfo_children[0]' means that the 'CTkTextbox' is the First Child in a Tab's Frame.

    # New
    def new(self):  
        self.add_new_tab()
        self.title("Scribe")

    # Open
    def open(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
            tab_id, text_area = self.add_new_tab()
            text_area.insert("1.0", content)
            print(f"Opened file: {file_path}")

            #Save File_Path && Set Window_Title and Tab_Title to Selected_File_Name
            current_tab = self.notebook.select()
            self.file_path[current_tab] = file_path
            file_name = os.path.basename(file_path)
            self.notebook.tab(current_tab, text = file_name)
            self.title(file_name)
    
    # Save
    def save(self):
        current_tab_name = self.current_tab_name()
        path = self.file_path.get(current_tab_name)  # Get the stored file path for the current tab

         # If a path exists, save the content to that file
        if path:
            current_tab_text = self.current_tab_text()  # Get the text area content
            with open(path, "w") as file:
                file.write(current_tab_text.get(1.0, "end").strip())  # Save content to the file

            # Update the tab and window title with the saved file name
            self.file_path[current_tab_name] = path
            file_name = os.path.basename(path)
            self.notebook.tab(current_tab_name, text=file_name)
            self.title(file_name)
        else:
            # If no path exists, prompt for 'Save As'
            self.save_as_file()

    
    #Save As
    def save_as_file(self):
        current_tab_name = self.current_tab_name()
        current_tab_text = self.current_tab_text()
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        )
        if file_path:
            with open(file_path, "w") as file:
                file.write(current_tab_text.get(1.0, "end").strip())
            self.file_path[current_tab_name] = file_path
            self.notebook.tab(current_tab_name, text=file_path.split("/")[-1])

        #Save File_Path && Set Window_Title and Tab_Title to Selected_File_Name
        current_tab = self.notebook.select()
        self.file_path[current_tab] = file_path
        file_name = os.path.basename(file_path)
        self.notebook.tab(current_tab, text = file_name)
        self.title(file_name)

           
app = Scribe()
app.mainloop()


