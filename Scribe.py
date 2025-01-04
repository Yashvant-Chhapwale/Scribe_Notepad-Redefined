import os
import tkinter
import customtkinter as ctk
from tkinter import filedialog, ttk, messagebox
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
        self.minsize(250,120)

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
        self.style.theme_use("default")  # Select the Base_Theme
        self.style.configure("TNotebook",background = "#2e2e2e", foreground = "#000000", borderwidth = 0, padding = [0,6])
        self.style.configure("TNotebook.Tab", background = "#242424", foreground = "#ffc300", padding = [10,6], font = ("Comic Sans MS", 10, "italic"), corner_radius = 0)
        self.style.map("TNotebook.Tab",background = [("selected", "#1d1d1d")], foreground = [("selected", "#ffd60a")], borderwidth="0", corner_radius = [("selected", "5")])

        # Initialize a Notebook for creating Tabbed-Interface
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        # Add the First Tab
        self.add_new_tab()

        # Add a "+" button to 'Create a New Tab' 
        plus_tab = ctk.CTkFrame(self.notebook)
        self.notebook.add(plus_tab, text="  +  ")

        # Handles Events
        self.notebook.bind("<<NotebookTabChanged>>", self.tab_change_event)



    # Base_Operations---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

    #Initialize a Dictionary to store File_Path
    file_path = {}

    # Initialize a Dictionary to store Saved_Content
    saved_content = {}

    # Initialize Text_Area (With respect to each Notebook Frame (Tab))
    def add_text_area(self,frame):
        try:
            text_area = ctk.CTkTextbox(frame, wrap="word", font = ('Comic Sans MS', 13, "normal"), corner_radius=2, undo = True)
            text_area.pack(expand = True, fill="both", pady=0)

            # Create a "X" button to close the tab
            close_tab = ctk.CTkButton(frame, text=" X ", font = ('Comic Sans MS', 9, "normal"), corner_radius = 3, text_color = "#ffc300", fg_color = "#3b3b3b", bg_color = "#3b3b3b", hover_color = "#404040", width = 10, height = 35, command = lambda: self.close_tab(frame))
            close_tab.place(relx=1.0, rely=0.0, anchor="ne", x=-20, y=-3)

            # Handles the event that "Text_Area" is "Clicked"
            text_area.bind("<Button-1>", self.click_on_textbox)

            return text_area
        except AttributeError as e:
            print(":/ Attribute Error")
            print(f"{e}")      
        except Exception as e:
            print(":/ Unexpected Error Occurred")
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
            print(":/ Attribute Error")
            print(f"{e}")
        except IndexError as e:
            print(":/ Invalid Index")
            print(f"{e}")
        except Exception as e:
            print(":/ Unexpected Error Occurred")
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
            print(":/ Attribute Error")
            print(f"{e}")
        except IndexError as e:
            print(":/ Invalid Index")
            print(f"{e}")
        except Exception as e:
            print(":/ Unexpected Error Occurred")
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
            print(":/ Attribute Error")
            print(f"{e}")
        except KeyError as e:
            print(":/ Key-Value Error")
            print(f"{e}")
        except Exception as e:
            print(":/ Unexpected Error Occurred")
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
                self.display_file_menu() #Show File_Menu
        except AttributeError as e:
            print(":/ Attribute Error")
            print(f"{e}")
        except Exception as e:
            print(f":/ Unexpected Error Occured")
            print(f"{e}")
    
    def display_file_menu(self):
        try:
            if not self.file_menu:
                self.file_menu = ctk.CTkFrame(self, fg_color = "#1c1c1c", corner_radius = 6)
                new = ctk.CTkButton(self.file_menu, text="New", command = self.new_scribe, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, height = 25, anchor="w")
                open = ctk.CTkButton(self.file_menu, text="Open", command = self.open_in_scribe, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, height = 25, anchor="w")
                save = ctk.CTkButton(self.file_menu, text="Save", command = self.save_scribe, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, height = 25, anchor="w")
                save_as = ctk.CTkButton(self.file_menu, text="Save As", command = self.save_as_scribe, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, anchor="w")
                separator = self.separator(self.file_menu)
                close_tab = ctk.CTkButton(self.file_menu, text="Close Tab", command = lambda: self.close_tab(self.current_tab_name()), fg_color = "#1c1c1c", hover_color = "#333333", width = 100, height = 25, anchor="w")
                exit = ctk.CTkButton(self.file_menu, text="Exit", command = self.quit, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, height = 25, anchor="w")

                new.pack(pady=0, padx=5)
                open.pack(pady=0, padx=5)
                save.pack(pady=0, padx=5)
                save_as.pack(pady=0, padx=5)          
                separator.pack(pady=0, padx=5)
                close_tab.pack(pady=0, padx=5)
                exit.pack(pady=0, padx=5)

            self.file_menu.place(x=5, y=25) #Show File_Menu
        except AttributeError as e:
            print(":/ Attribute Error")
            print(f"{e}")
        except Exception as e:
            print(f":/ Unexpected Error Occured")
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
                self.display_edit_menu() #Show Edit_Menu
        except AttributeError as e:
            print(":/ Attribute Error")
            print(f"{e}")
        except Exception as e:
            print(f":/ Unexpected Error Occured")
            print(f"{e}")

    
    def display_edit_menu(self):
        try:
            if not self.edit_menu:
                self.edit_menu = ctk.CTkFrame(self, fg_color = "#1c1c1c", corner_radius = 6)
                undo = ctk.CTkButton(self.edit_menu, text="Undo", command = self.undo_scribe, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, anchor="w")
                redo = ctk.CTkButton(self.edit_menu, text="Redo", command = self.redo_scribe, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, anchor="w")
                separator_1 = self.separator(self.edit_menu)
                cut = ctk.CTkButton(self.edit_menu, text="Cut", command = self.cut_scribe, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, anchor="w")
                copy = ctk.CTkButton(self.edit_menu, text="Copy", command = self.copy_scribe, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, anchor="w")
                paste = ctk.CTkButton(self.edit_menu, text="Paste", command = self.paste_scribe, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, anchor="w")
                separator_2 = self.separator(self.edit_menu)
                find = ctk.CTkButton(self.edit_menu, text="Find", command = self.new_scribe, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, anchor="w")
                find_previous = ctk.CTkButton(self.edit_menu, text="Find Previous", command = self.new_scribe, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, anchor="w")
                find_next = ctk.CTkButton(self.edit_menu, text="Find Next", command = self.new_scribe, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, anchor="w")
                separator_3 = self.separator(self.edit_menu)
                font = ctk.CTkButton(self.edit_menu, text="Font", command = self.new_scribe, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, anchor="w")
          

                undo.pack(pady=0, padx=5)
                redo.pack(pady=0, padx=5)
                separator_1.pack(pady=0, padx=5)
                cut.pack(pady=0, padx=5)
                redo.pack(pady=0, padx=5)
                copy.pack(pady=0, padx=5)
                paste.pack(pady=0, padx=5)
                separator_2.pack(pady=0, padx=5)
                find.pack(pady=0, padx=5)
                find_previous.pack(pady=0, padx=5)
                find_next.pack(pady=0, padx=5)
                separator_3.pack(pady=0, padx=5)
                font.pack(pady=0, padx=5)

            self.edit_menu.place(x=55, y=25) #Show Edit_Menu
        except AttributeError as e:
            print(":/ Attribute Error")
            print(f"{e}")
        except Exception as e:
            print(f":/ Unexpected Error Occured")
            print(f"{e}")

    # View_Menu
    view_menu = None
    
    def toggle_view_menu(self):
        try:
            if self.view_menu and self.view_menu.winfo_ismapped():
                self.view_menu.place_forget() #Hide View_Menu
            else:
                if self.file_menu and self.file_menu.winfo_ismapped():
                    self.file_menu.place_forget() #Hide File_Menu
                if self.edit_menu and self.edit_menu.winfo_ismapped():
                    self.edit_menu.place_forget() #Hide Edit_Menu
                self.display_view_menu() #Show View_Menu
        except AttributeError as e:
            print(":/ Attribute Error")
            print(f"{e}")
        except Exception as e:
            print(f":/ Unexpected Error Occured")
            print(f"{e}")
    
    def display_view_menu(self):
        try:
            if not self.view_menu:
                self.view_menu = ctk.CTkFrame(self, fg_color = "#1c1c1c", corner_radius = 6)
                zoom = ctk.CTkButton(self.view_menu, text="Zoom", command = self.new_scribe, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, anchor="w")
                separator = self.separator(self.view_menu)
                status_bar = ctk.CTkButton(self.view_menu, text = self.toggle_word_wrap_text(), command = self.toggle_word_wrap, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, anchor="w")
                word_wrap = ctk.CTkButton(self.view_menu, text = self.toggle_status_bar_text(), command = self.toggle_word_wrap, fg_color = "#1c1c1c", hover_color = "#333333", width = 100, anchor="w")

                zoom.pack(pady=0, padx=5)
                separator.pack(pady=0, padx=5)
                status_bar.pack(pady=0, padx=5)
                word_wrap.pack(pady=0, padx=5)

            self.view_menu.place(x = 95, y = 25) #Show View_Menu
        except AttributeError as e:
            print(":/ Attribute Error")
            print(f"{e}")
        except Exception as e:
            print(f":/ Unexpected Error Occured")
            print(f"{e}")



    # Sub_Menu_Operations------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    
    # Separators
    def separator(self,x):
        try: 
            separator = ctk.CTkFrame(x, fg_color="#ffc300", height = 2, width = 90)
            return separator
        except Exception as e:
            print(f":/ Unexpected Error Occured")
            print(f"{e}")

    # Get 'current_tab' Name
    def current_tab_name(self):
        try:
            return self.notebook.nametowidget(self.notebook.select()) # Returns the 'Internal_Tkinter_Widget_Name' for the 'current_tab' Frame. 
        except Exception as e:
            print(f":/ Unexpected Error Occured")
            print(f"{e}")

    # Get 'current_tab' Text_Content
    def current_tab_text(self):
        try:
            current_tab = self.current_tab_name()
            return current_tab.winfo_children()[0] # Gets Content from a Tab's 'ctk.CTkTextbox' widget. 'winfo_children[0]' means that the 'CTkTextbox' is the First Child in a Tab's Frame.
        except Exception as e:
            print(f":/ Unexpected Error Occured") 
            print(f"{e}")

    #---------------------------------------------------------------------- File_Menu Operations -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    # New
    def new_scribe(self):
        try:  
            self.add_new_tab()
            self.title("Scribe")
        except Exception as e:
            print(f":/ Unexpected Error Occured")
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
                except IOError as e:
                    print(":/ File Not Readable")
                    print(f"{e}")
        except FileNotFoundError as e:
            print(":/ File Not Found")
            print(f"{e}")
        except Exception as e:
            print(f":/ Unexpected Error Occured")
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
                except IOError as e:
                    print(":/ File Not Editable")
                    print(f"{e}")
            else:
                # If no path exists, prompt for 'Save As'
                self.save_as_scribe()
        except AttributeError as e:
            print(":/ Attribute Error :: Error Accessing Current Tab or Text Widget")
            print(f"{e}")
        except Exception as e:
            print(f":/ Unexpected Error Occured")
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
                except IOError as e:
                    print(":/ File Not Editable")
                    print(f"{e}")
        except AttributeError as e:
            print(":/ Attribute Error :: Error Accessing Current Tab or Text Widget")
            print(f"{e}")
        except Exception as e:
            print(f":/ Unexpected Error Occured")
            print(f"{e}")

    #---------------------------------------------------------------------- Edit_Menu Operations -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    # Undo
    def undo_scribe(self):
        try:
            current_tab = self.current_tab_name()
            text = getattr(current_tab, 'text_widget', None)
            if text:
                text.edit_undo() # Inbuilt "Tkinter 'Text' Widget"/"Custom Tkinter 'CTkTextbox'" Widget Method to Undo Changes
        except tkinter.TclError as e:
            print(":/ No Changes to Undo") 
            print(f"{e}")      
        except Exception as e:
            print(f":/ Unexpected Error Occured")
            print(f"{e}")
        
    
    # Redo
    def redo_scribe(self):
        try:
            current_tab = self.current_tab_name()
            text = getattr(current_tab, 'text_widget', None)
            if text:
                text.edit_redo() # Inbuilt "Tkinter 'Text' Widget"/"Custom Tkinter 'CTkTextbox'" Method to Redo Changes
        except tkinter.TclError as e:
            print(":/ No Changes to Redo")
            print(f"{e}")
        except Exception as e:
            print(f":/ Unexpected Error Occured")
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
        except Exception:
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
        except Exception:
            messagebox.showwarning("Null_Selection Error!", "Please select some text to 'Copy'.")
    
    # Paste
    def paste_scribe(self):
        try:
            current_tab = self.current_tab_name()
            clipboard_text = self.clipboard_get()

            # Paste the "Clipboard_Text" into the "Text_Area"
            current_tab.text_widget.insert("insert", clipboard_text)
        except Exception:
            messagebox.showwarning("Clipboard Error!", "Empty Clipboard. Nothing to Paste.")

    #---------------------------------------------------------------------- View_Menu Operations -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    # Word_Wrap
    word_wrap_enabled = True # Initialize "Word_Wrap" Visibility State [Initially Configured to "True"]

    def toggle_word_wrap_text(self): # Toggle "Word_Wrap" Button "Text"
        try:
            return "Word Wrap" if not self.word_wrap_enabled else "Word Wrap ✔ "
        except Exception:
            return "Word Wrap"
     
    def toggle_word_wrap(self): # Toggle "Word_Wrap_State"
        self.word_wrap_enabled = not self.word_wrap_enabled # Toggles Word_Wrap_State
         
        current_tab = self.current_tab_name()
        text_area = getattr(current_tab, 'text_widget', None)
        text_area.configure(wrap="word" if self.word_wrap_enabled else "none") # Configure the "Current_Tab's Text_Widget" to enable or disable "Word_Wrap"

        if self.view_menu:
            for widget in self.view_menu.winfo_children():
                if isinstance(widget, ctk.CTkButton) and "Word Wrap" in widget.cget("text"):
                    widget.configure(text=self.toggle_word_wrap_text())

    # Status_Bar
    status_bar_enabled = True # Initialize "Status_Bar" Visibility State [Initially Configured to "True"]

    def toggle_status_bar_text(self):  # Toggle "Status_Bar" Button "Text"
        try:
            return "Status Bar" if not self.word_wrap_enabled else "Status Bar ✔"
        except Exception:
            return "Status Bar"

    # Event_Handlers------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    
    def tab_change_event(self,event):
        try:
            # Update the Window_Title to Match the Selected_Tab's Title.
            current_tab = self.notebook.select()
            tab_title = self.notebook.tab(current_tab)["text"] # Get the value for 'text' attribute from the corresponding 'current_tab'.
            self.title(tab_title)  # Update window Title with 'current_tab' Title.

            # Handles the Event that '+' Tab was selected.
            current_tab_index = self.notebook.index(self.notebook.select()) # Get 'Index' of current_tab.
            if current_tab_index == len(self.notebook.tabs()) - 1:  # Last tab is the "+"
                self.add_new_tab()
        except Exception as e:
            print(":/ Unexpected Error Occured")
            print(f"{e}")
    
    def click_on_textbox(self,event):
        try:
            if self.file_menu and self.file_menu.winfo_ismapped():
                self.file_menu.place_forget()
            if self.edit_menu and self.edit_menu.winfo_ismapped():
                self.edit_menu.place_forget()
            if self.view_menu and self.view_menu.winfo_ismapped():
                self.view_menu.place_forget()
        except Exception as e:
            print(":/ Unexpected Error Occurred")
            print(f"{e}")



app = Scribe()
app.mainloop()


