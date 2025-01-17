import os
import tkinter
import customtkinter as ctk
from tkinter import filedialog, ttk, messagebox
import tkinter.font as tkFont
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
        self.geometry("600x350")
        self.minsize(350,200)

        # Initialize Font_Family and Font_size
        self.font_family = "Comic Sans MS"
        self.font_size = 12
        self.font_weight = "normal"

        # Initialize a Navbar
        self.navbar = ctk.CTkFrame(self, bg_color="#1d1e1e", fg_color = "#1d1e1e")
        self.navbar.pack(side="top", fill="x")

        nav_file = ctk.CTkButton(self.navbar, text="File", width=45, height=20, corner_radius=0, command=self.toggle_file_menu, fg_color = "#1d1e1e", bg_color = "#1d1e1e", hover_color="#3b3b3b", text_color = "#ffffff")
        nav_edit = ctk.CTkButton(self.navbar, text="Edit", width=45, height=20, corner_radius=0, command=self.toggle_edit_menu, fg_color = "#1d1e1e", bg_color = "#1d1e1e", hover_color="#3b3b3b", text_color = "#ffffff")
        nav_view = ctk.CTkButton(self.navbar, text="View", width=45, height=20, corner_radius=0, command=self.toggle_view_menu, fg_color = "#1d1e1e", bg_color = "#1d1e1e", hover_color="#3b3b3b", text_color = "#ffffff")
        nav_file.pack(side = "left", padx = 1)
        nav_edit.pack(side = "left", padx = 2)
        nav_view.pack(side = "left", padx = 2)

        # Configure 'Style' for Notebook
        self.style = ttk.Style()
        self.style.theme_use("default")  # Select the Base_Theme
        self.style.configure("TNotebook",background = "#2e2e2e", foreground = "#000000", borderwidth = 0, padding = [0,1])
        self.style.configure("TNotebook.Tab", background = "#242424", foreground = "#ffc300", padding = [10,6], font = ("Comic Sans MS", 10, "normal"), corner_radius = 0)
        self.style.map("TNotebook.Tab",background = [("selected", "#1d1d1d")], foreground = [("selected", "#ffd60a")], borderwidth="0")

        # Initialize a Notebook for creating Tabbed-Interface
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        # Add the First Tab
        self.add_new_tab()

        # Add a "+" button to 'Create a New Tab' 
        plus_tab = ctk.CTkFrame(self.notebook)
        self.notebook.add(plus_tab, text="  +  ")

        # Add Status_Bar
        self.add_status_bar()

        # Handles "Tab_Change" Events
        self.notebook.bind("<<NotebookTabChanged>>", self.tab_change_event)



    # Base_Operations---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    #Initialize a Dictionary to store File_Path
    file_path = {}

    # Initialize a Dictionary to store Saved_Content
    saved_content = {}

    # Initialize Text_Area (With respect to each Notebook Frame (Tab))
    def add_text_area(self,frame):
        try:
            text_area = ctk.CTkTextbox(frame, wrap="word", font = ('Comic Sans MS', 12, "normal"), corner_radius=2, padx=6, pady=5, undo = True)
            text_area.pack(expand = True, fill="both")

            # Create a "X" button to close the tab
            close_tab = ctk.CTkButton(frame, text=" X ", font = ('Comic Sans MS', 9, "bold"), corner_radius = 3, text_color = "#ffc300", fg_color = "#3b3b3b", bg_color = "#3b3b3b", hover_color = "#404040", width = 10, height = 20, command = lambda: self.close_tab(frame))
            close_tab.place(relx=1.0, rely=0.0, anchor="ne", x=0, y=0)

            # Handles the Event that "Text_Area" is "Clicked"
            text_area.bind("<Button-1>", self.click_on_textbox)
            # Handles the "Char_Count" Event
            text_area.bind("<KeyRelease>", self.update_char_count)

            return text_area
        except AttributeError as e:
            self.op_status.configure(text=": /")
            print(f"{e}")      
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")
    
    # Configure and Add New Tabs
    def add_new_tab(self):
        try:
            tab_id = uuid.uuid4()
            frame = ctk.CTkFrame(self.notebook)
            text_area = Scribe.add_text_area(self,frame) 

            # Attach the text_area to the frame using a Dynamically Created Attribute: 'text_widget' [Used for detecting 'Unsaved_Changes']
            frame.text_widget = text_area

            # Initialize the saved content for the new tab
            self.saved_content[frame] = ""

            if len(self.notebook.tabs()) != 0:
                # Add the new tab before the "+" Tab i.e, Add the new tab at the Index of "+" Tab shifting "+" Tab to the next Index
                plus_tab_index = len(self.notebook.tabs()) - 1
                self.notebook.insert(plus_tab_index, frame, text=f"New Scribet")

                # Automatically Switch to the Newly_Created_Tab
                self.notebook.select(plus_tab_index)
            else:
                # Helps to Generate the "First Tab" when: "len(self.notebook.tabs()) = 0"
                self.notebook.add(frame, text = f"New Scribet")

            return tab_id,text_area
        except AttributeError as e:
            self.op_status.configure(text=": /")
            print(f"{e}")
        except IndexError as e:
            self.op_status.configure(text=": /")
            print(f"{e}")
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")

    # Add Status_Bar
    def add_status_bar(self):
        try:
            self.status_bar = ctk.CTkFrame(self, bg_color="#2e2e2e", fg_color = "#2e2e2e", height = 25)
            self.status_bar.pack(side="bottom", fill="x")

            self.status_bar.grid_columnconfigure(0, weight=3, minsize=185) # Configure "Status_Bar" to have the First Column [0] with "Weight" of "3" and atleast "Minimum_Size" of "200px"
            self.status_bar.grid_columnconfigure(1, weight=1, minsize=150)
            self.status_bar.grid_columnconfigure(2, weight=1, minsize=110)
            self.status_bar.grid_columnconfigure((3, 4), weight=1, minsize=125) # Configure "Status_Bar" to have  the other 4 Columns[1 - 4] with Equal "Weight" of "1" and atleast "Minimum_Size" of "125px"

            self.op_status = ctk.CTkLabel(self.status_bar, text="Scribe", bg_color="#2e2e2e", fg_color="#2e2e2e", padx=10, text_color = "#ffc300")
            self.char_count = ctk.CTkLabel(self.status_bar, text="Characters: 0", bg_color="#2e2e2e", fg_color="#2e2e2e", padx=10, text_color = "#bdbdbd")
            separator_1 = self.separator_v(self.status_bar)
            self.zoom_status= ctk.CTkLabel(self.status_bar, text="Zoom: 100%", bg_color="#2e2e2e", fg_color="#2e2e2e", padx=10,text_color = "#bdbdbd")
            separator_2 = self.separator_v(self.status_bar)
            self.word_wrap_status = ctk.CTkLabel(self.status_bar, text="Word Wrap: On", bg_color="#2e2e2e", fg_color="#2e2e2e", padx=10,text_color = "#bdbdbd")
            separator_3 = self.separator_v(self.status_bar)
            self.font_status = ctk.CTkLabel(self.status_bar, text=f"Font: {self.font_family}", bg_color="#2e2e2e", fg_color="#2e2e2e", padx=10,text_color = "#bdbdbd")
            separator_4 = self.separator_v(self.status_bar)

            self.op_status.grid(row=0, column=0, sticky="w")
            self.char_count.grid(row=0, column=1, sticky="w")
            separator_1.grid(row=0, column=1, sticky="w")
            self.zoom_status.grid(row=0, column=2, sticky="w")
            separator_2.grid(row=0, column=2, sticky="w")
            self.word_wrap_status.grid(row=0, column=3, sticky="w")
            separator_3.grid(row=0, column=3, sticky="w")
            self.font_status.grid(row=0, column=4, sticky="w")
            separator_4.grid(row=0, column=4, sticky="w")
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")

    # Close Existing Tabs
    def close_tab(self,frame):
        try: 
            # Check if changes are made
            if self.unsaved_changes(frame): 
                # If 'Unsaved_Changes' are detected ask user 'Whether they wish to Save or Not?'
                choice = messagebox.askyesno("Unsaved Changes", "Do you want to Save the Changes?")
                if choice:
                    self.save_scribe()
    
            if len(self.notebook.tabs()) == 2: # Close the application if only Last Tab and "+" Tab are open and "X" button is Clicked 
                self.quit() 
            else: # Remove/Close the 'Current_Tab(i.e frame)' from Notebook
                current_tab_index = self.notebook.index(frame) # Stores the Current_Tab's_Index
                self.notebook.forget(frame) 
                if current_tab_index != 0:
                    self.notebook.select(self.notebook.tabs()[current_tab_index - 1]) # Selects the Tab at the [Current_Tab's_Index - 1] if [Current_Tab's_Index != 0], after removing the Current_Tab
        except AttributeError as e:
            self.op_status.configure(text=": /")
            print(f"{e}")
        except IndexError as e:
            self.op_status.configure(text=": /")
            print(f"{e}")
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")

    # Check for Unsaved_Changes
    def unsaved_changes(self, frame):
        try:
            current_content = frame.text_widget.get("1.0", "end-1c")
            exisitng_content = self.saved_content.get(frame, "") 
        
            # Compare 'Current_Text_Area Content' with 'Saved_Content' 
            if current_content != exisitng_content:
                 return True
            else :
                return False
        except AttributeError as e:
            self.op_status.configure(text=": /")
            print(f"{e}")
        except KeyError as e:
            self.op_status.configure(text=": /")
            print(f"{e}")
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")



    # Nav_Sub_Menu-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    # File_Menu
    file_menu = None
    
    def toggle_file_menu(self):
        try:
            if self.file_menu and self.file_menu.winfo_ismapped():
                self.file_menu.place_forget() #Hide File_Menu
            else:
                if self.edit_menu and self.edit_menu.winfo_ismapped():
                    self.edit_menu.place_forget() #Hide Edit_Menu
                if self.view_menu and self.view_menu.winfo_ismapped():
                    self.view_menu.place_forget() #Hide View_Menu
                    if self.zoom_menu and self.zoom_menu.winfo_ismapped():
                        self.zoom_menu.place_forget() #Hide Zoom_Menu
                if self.find_widget and self.find_widget.winfo_ismapped():
                    self.find_widget.place_forget() #Hide Find_Widget
                self.display_file_menu() #Show File_Menu
        except AttributeError as e:
            self.op_status.configure(text=": /")
            print(f"{e}")
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")
    
    def display_file_menu(self):
        try:
            if not self.file_menu:
                self.file_menu = ctk.CTkFrame(self, fg_color = "#1c1c1c", bg_color = "#1c1c1c", corner_radius = 6)
                new = ctk.CTkButton(self.file_menu, text="New", command = self.new_scribe, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, height = 25, anchor="w")
                open = ctk.CTkButton(self.file_menu, text="Open", command = self.open_in_scribe, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, height = 25, anchor="w")
                save = ctk.CTkButton(self.file_menu, text="Save", command = self.save_scribe, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, height = 25, anchor="w")
                save_as = ctk.CTkButton(self.file_menu, text="Save As", command = self.save_as_scribe, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, anchor="w")
                separator = self.separator_h(self.file_menu)
                close_tab = ctk.CTkButton(self.file_menu, text="Close Tab", command = lambda: self.close_tab(self.current_tab_name()), fg_color = "#1c1c1c", hover_color = "#333333", width = 100, height = 25, anchor="w")
                exit = ctk.CTkButton(self.file_menu, text="Exit", command = self.quit, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, height = 25, anchor="w")

                new.pack(pady=0, padx=2)
                open.pack(pady=0, padx=2)
                save.pack(pady=0, padx=2)
                save_as.pack(pady=0, padx=2)          
                separator.pack(pady=0, padx=2)
                close_tab.pack(pady=0, padx=2)
                exit.pack(pady=0, padx=2)

            self.file_menu.place(x=2, y=22) #Show File_Menu
        except AttributeError as e:
            self.op_status.configure(text=": /")
            print(f"{e}")
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")

    # Edit_Menu
    edit_menu = None

    def toggle_edit_menu(self):
        try:
            if self.edit_menu and self.edit_menu.winfo_ismapped():
                self.edit_menu.place_forget() #Hide Edit_Menu
            else:
                if self.file_menu and self.file_menu.winfo_ismapped():
                    self.file_menu.place_forget() #Hide File_Menu
                if self.view_menu and self.view_menu.winfo_ismapped():
                    self.view_menu.place_forget() #Hide View_Menu
                    if self.zoom_menu and self.zoom_menu.winfo_ismapped():
                        self.zoom_menu.place_forget() #Hide Zoom_Menu
                self.display_edit_menu() #Show Edit_Menu
        except AttributeError as e:
            self.op_status.configure(text=": /")
            print(f"{e}")
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")
    
    def display_edit_menu(self):
        try:
            if not self.edit_menu:
                self.edit_menu = ctk.CTkFrame(self, fg_color = "#1c1c1c",  bg_color = "#1c1c1c", corner_radius = 6)
                undo = ctk.CTkButton(self.edit_menu, text="Undo", command = self.undo_scribe, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, anchor="w")
                redo = ctk.CTkButton(self.edit_menu, text="Redo", command = self.redo_scribe, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, anchor="w")
                separator_1 = self.separator_h(self.edit_menu)
                cut = ctk.CTkButton(self.edit_menu, text="Cut", command = self.cut_scribe, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, anchor="w")
                copy = ctk.CTkButton(self.edit_menu, text="Copy", command = self.copy_scribe, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, anchor="w")
                paste = ctk.CTkButton(self.edit_menu, text="Paste", command = self.paste_scribe, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, anchor="w")
                separator_2 = self.separator_h(self.edit_menu)
                find = ctk.CTkButton(self.edit_menu, text="Find", command = self.toggle_find_widget, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, anchor="w")
                separator_3 = self.separator_h(self.edit_menu)
                font = ctk.CTkButton(self.edit_menu, text="Font", command = self.font_menu_slider, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, anchor="w")
          

                undo.pack(pady=0, padx=2)
                redo.pack(pady=0, padx=2)
                separator_1.pack(pady=0, padx=2)
                cut.pack(pady=0, padx=2)
                redo.pack(pady=0, padx=2)
                copy.pack(pady=0, padx=2)
                paste.pack(pady=0, padx=2)
                separator_2.pack(pady=0, padx=2)
                find.pack(pady=0, padx=2)
                separator_3.pack(pady=0, padx=2)
                font.pack(pady=0, padx=2)

            self.edit_menu.place(x=55, y=22) #Show Edit_Menu
        except AttributeError as e:
            self.op_status.configure(text=": /")
            print(f"{e}")
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")

    # View_Menu
    view_menu = None
    
    def toggle_view_menu(self):
        try:
            if self.view_menu and self.view_menu.winfo_ismapped():
                self.view_menu.place_forget() #Hide View_Menu
                if self.zoom_menu and self.zoom_menu.winfo_ismapped():
                    self.zoom_menu.place_forget() #Hide Zoom_Menu
            else:
                if self.file_menu and self.file_menu.winfo_ismapped():
                    self.file_menu.place_forget() #Hide File_Menu
                if self.edit_menu and self.edit_menu.winfo_ismapped():
                    self.edit_menu.place_forget() #Hide Edit_Menu
                if self.find_widget and self.find_widget.winfo_ismapped():
                    self.find_widget.place_forget() #Hide Find_Widget
                self.display_view_menu() #Show View_Menu
        except AttributeError as e:
            self.op_status.configure(text=": /")
            print(f"{e}")
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")
    
    def display_view_menu(self):
        try:
            if not self.view_menu:
                self.view_menu = ctk.CTkFrame(self, fg_color = "#1c1c1c", bg_color = "#1c1c1c", corner_radius = 6)
                zoom = ctk.CTkButton(self.view_menu, text="Zoom           ❯", command = self.toggle_zoom_menu, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, height = 25, anchor="w")
                separator = self.separator_h(self.view_menu)
                status_bar = ctk.CTkButton(self.view_menu, text = self.toggle_word_wrap_text(), command = self.toggle_word_wrap, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, height = 25, anchor="w")
                word_wrap = ctk.CTkButton(self.view_menu, text = self.toggle_status_bar_text(), command = self.toggle_status_bar, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, height = 25, anchor="w")

                zoom.pack(pady=0, padx=2)
                separator.pack(pady=0, padx=2)
                status_bar.pack(pady=0, padx=2)
                word_wrap.pack(pady=0, padx=2)

            self.view_menu.place(x = 105, y = 22) #Show View_Menu
        except AttributeError as e:
            self.op_status.configure(text=": /")
            print(f"{e}")
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")



    # Sub_Menu_Operations------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    
    # Separators
    def separator_h(self,x): # Separator_Horizontal
        try: 
            separator = ctk.CTkFrame(x, fg_color="#ffc300", height = 2, width = 90)
            return separator
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")

    def separator_v(self,x): # Separator_Vertical
        try: 
            separator = ctk.CTkFrame(x, fg_color="#5c5c5c", height = 15, width = 2)
            return separator
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")

    # Get 'current_tab' Name
    def current_tab_name(self):
        try:
            return self.notebook.nametowidget(self.notebook.select()) # Returns the 'Internal_Tkinter_Widget_Name' for the 'current_tab' Frame. 
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")

    # Get 'current_tab' Text_Content
    def current_tab_text(self):
        try:
            current_tab = self.current_tab_name()
            return current_tab.winfo_children()[0] # Gets Content from a Tab's 'ctk.CTkTextbox' widget. 'winfo_children[0]' means that the 'CTkTextbox' is the First Child in a Tab's Frame.
        except Exception as e:
            self.op_status.configure(text=": /") 
            print(f"{e}")
    
    # Update Font Attributes
    def update_font(self):
        try:
            # Get "Current_Tab" Content
            text_area = self.current_tab_text()
        
            # Configure "Text_Area" Attributes for "Font_Style"
            text_area.configure(font=(self.font_family, self.font_size, self.font_weight))
        except AttributeError as e:
            self.op_status.configure(text=": /")
            print(f"{e}")
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")



    #---------------------------------------------------------------------- File_Menu Operations -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    # New
    def new_scribe(self):
        try:  
            self.add_new_tab()
            self.title("Scribe")
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")

    # Open
    def open_in_scribe(self):
        try:
            file_path = filedialog.askopenfilename()
            if file_path:
                try:
                    with open(file_path, "r") as file:
                        content = file.read()
                    tab_id, text_area = self.add_new_tab()
                    text_area.insert("1.0", content)

                    # Save File_Path 
                    current_tab = self.current_tab_name()
                    self.file_path[current_tab] = file_path # Set the value of 'file_path' attribute for 'current_tab'

                    # Save the File's Content in the 'Saved_Content' Dictionary
                    self.saved_content[current_tab] = content

                    # Set Window_Title and Tab_Title to Selected_File_Name
                    file_name = os.path.basename(file_path)
                    self.notebook.tab(current_tab, text = file_name) # Set the value of 'text' attribute to 'file_name'
                    self.title(file_name) # Update window Title with 'file_name'.

                    if hasattr(self, 'op_status'):
                        self.op_status.configure(text=f"File Ready . . .")
                except IOError as e:
                    self.op_status.configure(text=": / File Not Readable")
                    print(f"{e}")
        except FileNotFoundError as e:
            self.op_status.configure(text=": /")
            print(f"{e}")
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")
    
    # Save
    def save_scribe(self):
        try:
            current_tab = self.current_tab_name()
            path = self.file_path.get(current_tab)  # Get the value of 'file_path' attribute for 'current_tab'

            # If a path exists, 'Save' the Content to that File
            if path:
                try:
                    current_tab_text = self.current_tab_text()  # Get the text area content
                    with open(path, "w") as file:
                        content = file.write(current_tab_text.get(1.0, "end-1c").strip())  # Save content to the file

                    # Save the File's Content in the 'Saved_Content' Dictionary
                    self.saved_content[current_tab] = content

                    # Save File_Path 
                    self.file_path[current_tab] = path

                    # Set Window_Title and Tab_Title to Selected_File_Name
                    file_name = os.path.basename(path)
                    self.notebook.tab(current_tab, text = file_name) # Set the value of 'text' attribute to 'file_name'
                    self.title(file_name) # Update window Title with 'file_name'.

                    if hasattr(self, 'op_status'):
                        self.op_status.configure(text=f"File Saved . . .")
                except IOError as e:
                    self.op_status.configure(text=": / File Not Editable")
                    print(f"{e}")
            else:
                # If no path exists, prompt for 'Save As'
                self.save_as_scribe()
        except AttributeError as e:
            self.op_status.configure(text=": /")
            print(f"{e}")
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")
    
    # Save As
    def save_as_scribe(self):
        try:
            current_tab = self.current_tab_name()
            current_tab_text = self.current_tab_text()
            file_path = filedialog.asksaveasfilename(defaultextension = ".txt",filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])

            if file_path:
                try:
                    with open(file_path, "w") as file:
                        content = file.write(current_tab_text.get(1.0, "end-1c").strip())

                    # Save the File's Content in the 'Saved_Content' Dictionary
                    self.saved_content[current_tab] = content

                    # Save File_Path
                    self.file_path[current_tab] = file_path # Set the value of 'file_path' attribute for 'current_tab'

                    # Update Window_Title and Tab_Title to Selected_File_Name
                    file_name = os.path.basename(file_path)
                    self.notebook.tab(current_tab, text = file_name) # Set the value of 'text' attribute to 'file_name'
                    self.title(file_name) # Update window Title with 'file_name'.

                    if hasattr(self, 'op_status'):
                        self.op_status.configure(text=f"File Saved as : {file_name}")
                except IOError as e:
                    self.op_status.configure(text=": / File Not Editable")
                    print(f"{e}")
        except AttributeError as e:
            self.op_status.configure(text=": /")
            print(f"{e}")
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")



    #---------------------------------------------------------------------- Edit_Menu Operations -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    # Undo
    def undo_scribe(self):
        try:
            current_tab = self.current_tab_name()
            text = getattr(current_tab, 'text_widget', None)
            if text:
                text.edit_undo() # Inbuilt "Tkinter 'Text' Widget"/"Custom Tkinter 'CTkTextbox'" Widget Method to Undo Changes
                if hasattr(self, 'op_status'):
                        self.op_status.configure(text=f"Scribe")
            
            self.update_char_count()
        except tkinter.TclError as e:
            self.op_status.configure(text=": / No Changes to Undo") 
            print(f"{e}")      
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")
        
    
    # Redo
    def redo_scribe(self):
        try:
            current_tab = self.current_tab_name()
            text = getattr(current_tab, 'text_widget', None)
            if text:
                text.edit_redo() # Inbuilt "Tkinter 'Text' Widget"/"Custom Tkinter 'CTkTextbox'" Method to Redo Changes
                if hasattr(self, 'op_status'):
                        self.op_status.configure(text=f"Scribe")

            self.update_char_count()
        except tkinter.TclError as e:
            self.op_status.configure(text=": / No Changes to Redo")
            print(f"{e}")
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")

    # Cut
    def cut_scribe(self):
        try:
            current_tab = self.current_tab_name()

            # Get the "Selected_Text"
            selected_text = current_tab.text_widget.get("sel.first", "sel.last")

            # Save "Selected_Text" to the "Clipboard"
            self.clipboard_clear()
            self.clipboard_append(selected_text)

            # Delete the "Selected_Text" from the "Text_Area" [Implementing "Cut"]
            current_tab.text_widget.delete("sel.first", "sel.last")
        except Exception as e:
            messagebox.showwarning("Null_Selection Error!", "Please select some text to 'Cut'.")

    # Copy
    def copy_scribe(self):
        try:
            current_tab = self.current_tab_name()

            # Get the "Selected_Text"
            selected_text = current_tab.text_widget.get("sel.first", "sel.last")

            # Save "Selected_Text" to the "Clipboard"
            self.clipboard_clear()
            self.clipboard_append(selected_text)
        except Exception as e:
            messagebox.showwarning("Null_Selection Error!", "Please select some text to 'Copy'.")
    
    # Paste
    def paste_scribe(self):
        try:
            current_tab = self.current_tab_name()
            clipboard_text = self.clipboard_get()

            # Paste the "Clipboard_Text" into the "Text_Area"
            current_tab.text_widget.insert("insert", clipboard_text)

            self.update_char_count()
        except Exception as e:
            messagebox.showwarning("Clipboard Error!", "Empty Clipboard. Nothing to Paste.")

    # Find
    find_widget = None

    def toggle_find_widget(self):
        try:
            if self.find_widget and self.find_widget.winfo_ismapped():
                self.find_widget.place_forget() #Hide Find_Widget

                text_area = self.current_tab_text()
                text_area.tag_remove("highlight", "1.0", "end") #Remove Highlights
            else:
                if self.file_menu and self.file_menu.winfo_ismapped():
                    self.file_menu.place_forget() #Hide File_Menu
                if self.edit_menu and self.edit_menu.winfo_ismapped():
                    self.edit_menu.place_forget() #Hide Edit_Menu
                if self.view_menu and self.view_menu.winfo_ismapped():
                    self.view_menu.place_forget() #Hide View_Menu
                    if self.zoom_menu and self.zoom_menu.winfo_ismapped():
                        self.zoom_menu.place_forget() #Hide Zoom_Menu
                self.display_find_widget() #Show Find_widget
        except AttributeError as e:
            self.op_status.configure(text=": /")
            print(f"{e}")
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")

    def display_find_widget(self):
        try:
            if not self.find_widget:
                self.find_widget = ctk.CTkFrame(self, fg_color="#1c1c1c", bg_color="#1c1c1c", width=350, height=50, corner_radius=6)
                self.find_widget.grid_columnconfigure((0,1), weight=1)

                label = ctk.CTkLabel(self.find_widget, text="Find :")
                self.find_search_entry = ctk.CTkEntry(self.find_widget, corner_radius=4, width=150, height=20, border_color="#575757", border_width=1, font = (self.font_family,self.font_size,"bold"))
                button_frame = ctk.CTkFrame(self.find_widget, fg_color="#1c1c1c")
                button_frame.grid_columnconfigure((0,1,2,3), weight=1)
           
                find_previous = ctk.CTkButton(button_frame, text="◀", command=self.find_previous_in_scribe, fg_color="#1c1c1c", bg_color="#1c1c1c", hover_color="#3b3b3b", text_color = "#ffc300", corner_radius=3, width=25, height=10)
                find = ctk.CTkButton(button_frame, text="🔍", command=self.find_in_scribe, fg_color="#1c1c1c", bg_color="#1c1c1c", hover_color="#3b3b3b", text_color = "#ffffff", corner_radius=3, width=25, height=10)
                find_next = ctk.CTkButton(button_frame, text="▶", command=self.find_next_in_scribe, fg_color="#1c1c1c", bg_color="#1c1c1c", hover_color="#3b3b3b", text_color = "#ffc300", corner_radius=3, width=25, height=10)
                find_all = ctk.CTkButton(button_frame, text="All", command=self.find_all_in_scribe, fg_color="#1c1c1c", bg_color="#1c1c1c", hover_color="#3b3b3b", text_color = "#ffc300", corner_radius=3, width=40, height=10)
                
                label.grid(row=0, column=0, padx=5)
                self.find_search_entry.grid(row=0, column=1, padx=10, pady=2)
                self.find_search_entry.bind("<FocusIn>", self.find_search_entry_focusIn)
                self.find_search_entry.bind("<FocusOut>", self.find_search_entry_focusOut)
                button_frame.grid(row=1, column=1)
                
                find_previous.grid(row=0, column=0, padx=0)
                find.grid(row=0, column=1, padx=2)
                find_next.grid(row=0, column=2, padx=2)
                find_all.grid(row=0, column=3, padx=0)
            self.set_find_widget_position()
            self.bind("<Configure>", self.set_find_widget_position)
        except AttributeError as e:
            self.op_status.configure(text=": /")
            print(f"{e}")
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")

    search_word = None # Initialize "self.search_word" Value to be "None"

    # 🔍
    def find_in_scribe(self):
        try:
            self.find_search_entry_focusOut()
            self.op_status.configure(text="Scribe")

            self.search_word = self.find_search_entry.get()
            if not self.search_word:
                messagebox.showerror("Empty Find Input", "Please enter a word to search.")
            else:
                self.search_indices = [] # Reset "self.search_indices" i.e "List of Search_Matches", to [] / (None) 
                self.search_match_index = -1 # Reset "search_match_index" Pointer to '-1'

                current_tab = self.current_tab_name()
                text_content = current_tab.text_widget.get("1.0","end-1c")
           
                start_index=0 # Initialize Start Index to '0'
                while True:
                    start_index = text_content.find(self.search_word, start_index) # The 'find()' Method Returns the Index (0,1,2, . . . ) of the First Occurrence of the Specified Substring(self.search_word). Returns "-1" if the Substring is Not Found.
                    if start_index == -1:
                        break #Exits Loop if "No Further Matches Found"

                    line, col = self.index_to_linexcol(start_index) # Map "start_index"(Occurences of "self.search_word") to 'line' and 'col' Coordinates
                    self.search_indices.append((line, col)) # Add [line][col] to "self.search_indices" List
                    start_index += len(self.search_word) # Suppose self.search_word = "hello", start_index = 0 (where "hello" occurs), then "start_index" becomes :: start_index = 0 + len(self.search_word) = 0 + 5 = 5 i.e, the "start_index" navigates ahead of the current "self.search_word" Occurence. 
            
                if not self.search_indices:
                    self.op_status.configure(text="❗ No Matches Found")
                else:
                    self.search_match_index = 0 # Initialize "self.search_match_index" to '0' to target "self.search_indices[0]" i.e First_Occurence of "self.search_word"
                    self.highlight_match()
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")

    # ▶
    def find_next_in_scribe(self):
        try:
            self.find_search_entry_focusOut()
            self.op_status.configure(text="Scribe")

            if not self.search_indices:
                self.op_status.configure(text="❗ No Matches Found")
            else:
                self.search_match_index = (self.search_match_index + 1) % len(self.search_indices) # It updates "self.search_match_index" to point to the Next_Match in "self.search_indices". When it reaches the Last_Index in "self.search_indices", it wraps around to the First_Index (using modulo '%' operator)).
                                                                                                   # Ex: Suppose "len(self.search_indices) = 2" and "self.search_match_index = 2 [Indicates_Last_Index]" then operation becomes :: (2+1) % 2 = 3 % 2 = 1[First_Index]
                self.highlight_match()
        except AttributeError as e:
            self.op_status.configure(text='Initiate "🔍 Find" to utilize this feature.') 
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")

    # ◀
    def find_previous_in_scribe(self):
        try:
            self.find_search_entry_focusOut()
            self.op_status.configure(text="Scribe")

            if not self.search_indices:
                self.op_status.configure(text="❗ No Matches Found")
            else:
                self.search_match_index = (self.search_match_index - 1) % len(self.search_indices)# It updates "self.search_match_index" to point to the Previous_Match in "self.search_indices". When it reaches the First_Index in "self.search_indices", it wraps around to the Last_Index (using modulo '%' operator)).
                                                                                                   # Ex: Suppose "len(self.search_indices) = 2" and "self.search_match_index = 1 [Indicates_First_Index]" then operation becomes :: (1-1) % 2 = 0 % 2 = 2[Last_Index]
                self.highlight_match()
        except AttributeError as e:
            self.op_status.configure(text='Initiate "🔍 Find" to utilize this feature.') 
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")

    # All
    def find_all_in_scribe(self):
        try:
            self.find_in_scribe() # Find all instances of "self.search_word"

            if not self.search_indices:
                self.op_status.configure(text=f'Found 0 occurrences of "{self.search_word}".')
            else:
                text_area = self.current_tab_text()

                text_area.tag_remove("highlight", "1.0", "end")  # Remove Existing Highlights

                # Highlight all Matches stored in "self.search_indices"
                for line, col in self.search_indices:
                    start = f"{line}.{col}"
                    end = f"{line}.{col + len(self.search_word)}"                    
                    text_area.tag_add("highlight", start, end)

                text_area.tag_config("highlight", background="#ffc300", foreground="#000000")

                text_area.see(f"{self.search_indices[0][0]}.{self.search_indices[0][1]}") # "self.search_indices[0]" refers to the First Tuple in the "self.search_indices" List | Formats the "Line(self.search_indices[0][0])" and "Column(self.search_indices[0][1])" into a string in the format "line.column", which is required by the 'see()' Method
                                                                                          # The "see()" Method of a "Text_Widget" in Tkinter is used to Scroll the Widget's View, so that the specified index is visible to the User.
                self.op_status.configure(text=f'Found {len(self.search_indices)} occurrences of "{self.search_word}".')
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")


    def index_to_linexcol(self, index):
        try:
            current_tab = self.current_tab_name()
            text_content = current_tab.text_widget.get("1.0", "end-1c")

            lines = text_content.splitlines() # Split Content into 'Individual Lines'

            running_length = 0  # Initialize "running_length" to '0' i.e, '0 Characters processed'.
                                # The "running_length" keeps track of the Total Number of "Characters" processed up till the "Current_line", including Newline Characters.
            for i, line in enumerate(lines): # i = Line_Index, line = Line_Text
                if index < running_length + len(line): # Checks if word(index) lies in the "Current_line"
                    return i + 1, index - running_length # Returns "line_coordinates" as "i+1" (Shifts Line Indexing to start from '1' instead of '0')
                                                         # Returns "col_coordinates" as "index - running length". Suppose "index=30", and each "line" has upto "20 characters only" i.e, len(line) = 20, hence word lies in 2nd line as :: 30(index) > 20(0[initial running_length] + 20[len(line)]), therefore (update) running_length = 20 + 1(newline character) = 21, so "col_coordinate" = 30 - 21 = 9, hence word lies in "line" = i + 1 = 1 + 1 = 2 [2nd Line is indicated by "i = 1" in "splitlines()" Method] and "col"  = 9 [calculated in "col_coordinate"]
                running_length += len(line) + 1  # If word(index) is not found in "Current_line" i.e "index" exceeds "running_length + len(line)", then Update "running_length" by adding number_of_characters_parsed_in_Current_line i.e, running_length + len(line) + 1 (Includes Newline Character)

            return 1, 0  # Return Default Value "1.0" where Line="1",Column="0" i.e "Start" of the Text
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")

    def highlight_match(self): 
        try:
            text_area = self.current_tab_text()
            text_area.tag_remove("highlight", "1.0", "end")  # Remove Existing Highlights using 'tag_remove()'

            if self.search_match_index > -1:
                line, col = self.search_indices[self.search_match_index] 

                start = f"{line}.{col}" # start="line_Number_Where_Search_Word_Is_Detected . column_Number_For_Line_Where_The_Word_Starts "
                end = f"{line}.{col + len(self.search_word)}" # end="line_Number_Where_Search_Word_Is_Detected . (column_Number_For_Line_Where_The_Word_Starts + len(self.search_word))"

                text_area.tag_add("highlight", start, end) # Add Highlight using 'tag_add'
                text_area.tag_config("highlight", background="#ffc300", foreground="#000000") # Configure Tag_Attributes (background, foreground) using 'tag_config'
                text_area.see(end) # The "see()" Method of a "Text_Widget" in Tkinter is used to Scroll the Widget's View, so that the specified index is visible to the User.
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")
    
    # Font_Menu
    def font_menu_slider(self):
        if hasattr(self,"op_status"):
            self.op_status.configure(text="File Saved . . . ")



    #---------------------------------------------------------------------- View_Menu Operations -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    # Zoom Menu
    zoom_menu = None

    def toggle_zoom_menu(self):
        try:
            if self.zoom_menu and self.zoom_menu.winfo_ismapped():
                self.zoom_menu.place_forget() #Hide Zoom_Menu
            else:
                if self.file_menu and self.file_menu.winfo_ismapped():
                    self.file_menu.place_forget() #Hide File_Menu
                if self.edit_menu and self.edit_menu.winfo_ismapped():
                    self.edit_menu.place_forget() #Hide Edit_Menu
                self.display_zoom_menu() #Show Zoom_Menu   
        except AttributeError as e:
            self.op_status.configure(text=": /")
            print(f"{e}")
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")

    def display_zoom_menu(self):
        try:
            if not self.zoom_menu:
                self.zoom_menu = ctk.CTkFrame(self, fg_color = "#1c1c1c", bg_color = "#1c1c1c", corner_radius = 6)
                zoom_in = ctk.CTkButton(self.zoom_menu, text="Zoom In", command = self.zoom_in, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, height = 25, anchor="w")
                zoom_out = ctk.CTkButton(self.zoom_menu, text="Zoom Out", command = self.zoom_out, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, height = 25, anchor="w")
                separator = self.separator_h(self.zoom_menu)
                reset = ctk.CTkButton(self.zoom_menu, text="Reset", command = self.zoom_reset, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, height = 25, anchor="w")

                zoom_in.pack(pady=0, padx=2)
                zoom_out.pack(pady=0, padx=2)
                separator.pack(pady=0, padx=2)
                reset.pack(pady=0, padx=2)

            self.zoom_menu.place(x=210, y=22) #Show File_Menu
        except AttributeError as e:
            self.op_status.configure(text=": /")
            print(f"{e}")
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")

    def zoom_in(self):
        try:
            if ((self.font_size + 1.2) / 12) * 100 < 510:
                self.font_size += 1.2
                self.update_font()

                if hasattr(self, 'zoom_status'):
                    self.zoom_status.configure(text=f"Zoom: {round((self.font_size / 12) * 100)}%")
        except AttributeError as e:
            self.op_status.configure(text=": /")
            print(f"{e}")
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")

    def zoom_out(self):
        try:
            if ((self.font_size - 1.2) / 12) * 100 > 0:
                self.font_size -= 1.2
                self.update_font()

                if hasattr(self, 'zoom_status'):
                    self.zoom_status.configure(text=f"Zoom: {round((self.font_size / 12) * 100)}%")
        except AttributeError as e:
            self.op_status.configure(text=": /")
            print(f"{e}")
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")

    def zoom_reset(self):
        try:
            self.font_size = 12
            self.update_font()

            if hasattr(self, 'zoom_status'):
                    self.zoom_status.configure(text=f"Zoom: 100%")
        except AttributeError as e:
            self.op_status.configure(text=": /")
            print(f"{e}")
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")
    
    # Word_Wrap
    word_wrap_enabled = True # Initialize "Word_Wrap" Visibility State [Initially Configured to "True"]

    def toggle_word_wrap_text(self): # Toggle "Word_Wrap" Button "Text"
        try:
            return "Word Wrap ✖" if not self.word_wrap_enabled else "Word Wrap ✔ "
        except Exception:
            return "Word Wrap ✔"
     
    def toggle_word_wrap(self): # Toggle "Word_Wrap_State"
        try:
            self.word_wrap_enabled = not self.word_wrap_enabled # Toggles Word_Wrap_State
         
            current_tab = self.current_tab_name()
            text_area = getattr(current_tab, 'text_widget', None)

            if self.word_wrap_enabled: # Configure the "Current_Tab's Text_Widget" to enable or disable "Word_Wrap"
                text_area.configure(wrap="word")
                self.op_status.configure(text=" ✔  Word Wrap enabled ")
            else:
                text_area.configure(wrap="none")
                self.op_status.configure(text="❗ Word Wrap disabled ")

            if self.view_menu:
                for widget in self.view_menu.winfo_children():
                    if isinstance(widget, ctk.CTkButton) and "Word Wrap" in widget.cget("text"):
                        widget.configure(text=self.toggle_word_wrap_text()) # Toggle "Word_Wrap" Button "Text" in "View_Menu" according to "Word_Wrap_State" using "toggle_word_wrap_text()" Method on Each "Click"

            if hasattr(self, "word_wrap_status"):
                word_wrap_status_text = "Word Wrap: On" if self.word_wrap_enabled else "Word Wrap: ❗"
                self.word_wrap_status.configure(text = word_wrap_status_text)  # Update status bar label
        except AttributeError as e:
            self.op_status.configure(text=": /")
            print(f"{e}")
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")

    # Status_Bar
    status_bar_enabled = True # Initialize "Status_Bar" Visibility State [Initially Configured to "True"]

    def toggle_status_bar_text(self): # Toggle "Status_Bar" Button "Text"
        try:
            return "Status Bar  ✖" if not self.status_bar_enabled else "Status Bar  ✔ "
        except Exception:
            return "Status Bar  ✔"
        
    def toggle_status_bar(self):
        try:
            self.status_bar_enabled = not self.status_bar_enabled # Toggles Status_Bar_State

            if not self.status_bar_enabled: # If self.status_bar_enabled != True
                self.status_bar.pack_forget() 
                self.op_status.configure(text="❗ Status Bar disabled ")
            else: # If self.status_bar_enabled == True
                self.status_bar.pack(side="bottom", fill="x") # Hide or Show "Status_Bar" based on "status_bar_enabled" State
                self.op_status.configure(text=" ✔  Status Bar enabled ")

            if self.view_menu:
                for widget in self.view_menu.winfo_children():
                    if isinstance(widget, ctk.CTkButton) and "Status Bar" in widget.cget("text"):
                        widget.configure(text=self.toggle_status_bar_text()) # Toggle "Status_Bat" Button "Text" in "View_Menu" according to "Status_Bar_State" using "toggle_status_bar__text()" Method on Each "Click"
        except AttributeError as e:
            self.op_status.configure(text=": /")
            print(f"{e}")
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")



    # Event_Handlers------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    def tab_change_event(self,event):
        try:
            # Update the Window_Title to Match the Selected_Tab's Title.
            current_tab = self.notebook.select()
            tab_title = self.notebook.tab(current_tab)["text"] # Get the value for 'text' attribute from the corresponding 'current_tab'.
            self.title(tab_title)  # Update window Title with 'current_tab' Title.

            # Handles the Event that '+' Tab was selected.
            current_tab_index = self.notebook.index(self.notebook.select()) # Get 'Index' of current_tab.
            if current_tab_index == len(self.notebook.tabs()) - 1:  # "Selected_Tab" is the "Last_Tab" i.e, "+" Tab
                self.add_new_tab()

            # Track the 'current_tabs' content(lenght) using 'Current_tab_name' i.e, the 'Internal_Tkinter_Widget_Name' for the 'current_tab' Frame
            current_tab_name = self.current_tab_name()
            content = current_tab_name.text_widget.get("1.0", "end-1c")
            char_count = len(content)  # Count no. of "Characters" in the "Content"

            # Update the Status_Bar "char_count Label"
            self.char_count.configure(text=f"Characters: {char_count}")

            # Update the Status_Bar "op_status Label"
            self.op_status.configure(text="Scribe")
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")
    
    def click_on_textbox(self,event):
        try:
            if self.file_menu and self.file_menu.winfo_ismapped():
                self.file_menu.place_forget()
            if self.edit_menu and self.edit_menu.winfo_ismapped():
                self.edit_menu.place_forget()
            if self.view_menu and self.view_menu.winfo_ismapped():
                self.view_menu.place_forget()
                if self.zoom_menu and self.zoom_menu.winfo_ismapped():
                    self.zoom_menu.place_forget() 
            if hasattr(self, 'op_status'):
                self.op_status.configure(text="Scribe")
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")
    
    def update_char_count(self,event=None):
        try:
            # Get the "Current_Tab_Name"
            current_tab = self.current_tab_name()

            # Get the "Current_Tab_Content"
            content = current_tab.text_widget.get("1.0", "end-1c")
            char_count = len(content)  # Count no. of "Characters" in the "Content"

            # Update the Status_Bar "char_count Label"
            if hasattr(self, 'char_count'):
                self.char_count.configure(text=f"Characters: {char_count}")
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")

    def set_find_widget_position(self,event=None):
        try:
            if self.find_widget:
                window_width = self.winfo_width()
                balance_offset = 180
                self.find_widget.place(x=(window_width/2)+balance_offset, y=0, anchor="ne")
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")
    
    def find_search_entry_focusIn(self,event=None):
        try:
            self.find_search_entry.configure(border_color="#ffb700")
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")


    def find_search_entry_focusOut(self,event=None):
        try:
            self.find_search_entry.configure(border_color="#575757")
        except Exception as e:
            self.op_status.configure(text=": /")
            print(f"{e}")


app = Scribe()
app.mainloop()


