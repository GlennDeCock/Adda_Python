import logging
from tkinter import ttk
from tkinter.messagebox import showinfo
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from datetime import datetime


class TextHandler(logging.Handler):
    """Custom logging handler that writes to a Tkinter Text widget"""
    
    def __init__(self, text_widget):
        logging.Handler.__init__(self)
        self.text_widget = text_widget
        
        # Set up color tags
        self.text_widget.tag_config("INFO", foreground="black")
        self.text_widget.tag_config("WARNING", foreground="orange")
        self.text_widget.tag_config("ERROR", foreground="red")
        self.text_widget.tag_config("SUCCESS", foreground="green")
        self.text_widget.tag_config("DEBUG", foreground="gray")

    def emit(self, record):
        msg = self.format(record)
        
        def append():
            self.text_widget.configure(state='normal')
            
            # Add timestamp
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.text_widget.insert(tk.END, f"[{timestamp}] ", "INFO")
            
            # Add message with color based on level
            tag = record.levelname
            if tag not in ["INFO", "WARNING", "ERROR", "DEBUG"]:
                tag = "INFO"
            
            self.text_widget.insert(tk.END, f"{msg}\n", tag)
            self.text_widget.configure(state='disabled')
            
            # Auto-scroll to bottom
            self.text_widget.yview(tk.END)
        
        # Schedule on main thread
        self.text_widget.after(0, append)


class ImprovedGUI(tk.Tk):
    """Enhanced GUI with better layout and live logging window"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize variables
        self.input_frame = None
        self.log_frame = None
        self.log_text = None
        self.status_label = None
        self.form_completed = False  # Flag to indicate form is complete
        
        # Player data variables
        self.player_name = None
        self.player_id = None
        self.player_age = None
        self.player_gender = None
        self.contingency = None
        self.block = None
        self.support_frequency = None
        self.trial_number = None
        
        # Validation labels
        self.age_error = None
        self.trial_number_error = None
        self.close_error = None
        
        # Entry list for validation
        self.entry_list = []
        
        # Window setup
        self.title("AddAttachment - Participant Data Entry")
        self.setup_window()
        self.create_widgets()
        self.setup_logging()
        
        # Log startup
        logging.info("AddAttachment GUI started")
        logging.info("Please fill in participant information")
    
    def setup_window(self):
        """Configure window size and position"""
        window_width = 900
        window_height = 700
        
        # Center window on screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.resizable(True, True)
        
        # Set minimum size
        self.minsize(800, 600)
    
    def create_widgets(self):
        """Create all GUI widgets with improved layout"""
        
        # Main container with padding
        main_frame = ttk.Frame(self, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for resizing
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # === LEFT SIDE: Input Form ===
        self.create_input_form(main_frame)
        
        # === RIGHT SIDE: Live Log ===
        self.create_log_panel(main_frame)
        
        # === BOTTOM: Status Bar ===
        self.create_status_bar(main_frame)
    
    def create_input_form(self, parent):
        """Create the input form on the left side"""
        
        # Input frame with border
        input_container = ttk.LabelFrame(parent, text="Participant Information", padding="15")
        input_container.grid(row=0, column=0, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        self.input_frame = ttk.Frame(input_container)
        self.input_frame.pack(fill='both', expand=True)
        
        # Configure column widths
        self.input_frame.columnconfigure(1, weight=1)
        
        row = 0
        
        # === Name ===
        ttk.Label(self.input_frame, text="Naam speler:", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=5, padx=(0, 10))
        self.player_name = tk.StringVar()
        name_entry = ttk.Entry(self.input_frame, textvariable=self.player_name, width=30)
        name_entry.grid(row=row, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        self.entry_list.append(self.player_name)
        row += 1
        
        # === ID ===
        ttk.Label(self.input_frame, text="Identificatie:", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=5, padx=(0, 10))
        self.player_id = tk.StringVar()
        id_entry = ttk.Entry(self.input_frame, textvariable=self.player_id, width=30)
        id_entry.grid(row=row, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        self.entry_list.append(self.player_id)
        row += 1
        
        # === Age ===
        ttk.Label(self.input_frame, text="Leeftijd (9-13):", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=5, padx=(0, 10))
        self.player_age = tk.IntVar()
        age_entry = ttk.Entry(self.input_frame, textvariable=self.player_age, width=10)
        age_entry.grid(row=row, column=1, sticky=tk.W, pady=5)
        age_entry.config(validate='focusout',
                        validatecommand=(self.register(self.validate_age), '%P'),
                        invalidcommand=(self.register(self.on_invalid_age),))
        self.age_error = ttk.Label(self.input_frame, foreground='red', font=('Arial', 8))
        self.age_error.grid(row=row, column=2, sticky=tk.W, pady=5, padx=(5, 0))
        self.entry_list.append(self.player_age)
        row += 1
        
        # Separator
        ttk.Separator(self.input_frame, orient='horizontal').grid(
            row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        row += 1
        
        # === Gender ===
        ttk.Label(self.input_frame, text="Geslacht:", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=5, padx=(0, 10))
        self.player_gender = tk.StringVar()
        gender_frame = ttk.Frame(self.input_frame)
        gender_frame.grid(row=row, column=1, columnspan=2, sticky=tk.W, pady=5)
        ttk.Radiobutton(gender_frame, text="Mannelijk (M)", variable=self.player_gender, 
                       value="M").pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(gender_frame, text="Vrouwelijk (V)", variable=self.player_gender, 
                       value="V").pack(side=tk.LEFT)
        self.entry_list.append(self.player_gender)
        row += 1
        
        # === Contingency (linked to support frequency) ===
        ttk.Label(self.input_frame, text="Contingentie:", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=5, padx=(0, 10))
        self.contingency = tk.IntVar()
        cont_frame = ttk.Frame(self.input_frame)
        cont_frame.grid(row=row, column=1, columnspan=2, sticky=tk.W, pady=5)
        ttk.Radiobutton(cont_frame, text="20% (Infrequent Support)", variable=self.contingency, 
                       value=20, command=self.sync_contingency_to_support).pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(cont_frame, text="80% (Frequent Support)", variable=self.contingency, 
                       value=80, command=self.sync_contingency_to_support).pack(side=tk.LEFT)
        self.entry_list.append(self.contingency)
        row += 1
        
        # === Block ===
        ttk.Label(self.input_frame, text="Trial Block:", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=5, padx=(0, 10))
        self.block = tk.StringVar()
        block_frame = ttk.Frame(self.input_frame)
        block_frame.grid(row=row, column=1, columnspan=2, sticky=tk.W, pady=5)
        ttk.Radiobutton(block_frame, text="Block 1", variable=self.block, 
                       value="1").pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(block_frame, text="Block 2", variable=self.block, 
                       value="2").pack(side=tk.LEFT)
        self.entry_list.append(self.block)
        row += 1
        
        # === Support Frequency (auto-synced with contingency) ===
        ttk.Label(self.input_frame, text="Support Frequentie:", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=5, padx=(0, 10))
        self.support_frequency = tk.StringVar(value="frequent")
        freq_frame = ttk.Frame(self.input_frame)
        freq_frame.grid(row=row, column=1, columnspan=2, sticky=tk.W, pady=5)
        ttk.Radiobutton(freq_frame, text="Frequent (80%)", variable=self.support_frequency, 
                       value="frequent", command=self.sync_support_to_contingency).pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(freq_frame, text="Infrequent (20%)", variable=self.support_frequency, 
                       value="infrequent", command=self.sync_support_to_contingency).pack(side=tk.LEFT)
        self.entry_list.append(self.support_frequency)
        row += 1
        
        # Info label about syncing
        ttk.Label(self.input_frame, 
                  text="ℹ️ Support frequency and contingency are linked", 
                  font=('Arial', 8, 'italic'), foreground='blue').grid(
            row=row, column=1, columnspan=2, sticky=tk.W, pady=(0, 5))
        row += 1
        
        # === Starting Support Figure ===
        ttk.Label(self.input_frame, text="Start Figuur:", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=5, padx=(0, 10))
        self.starting_support = tk.StringVar(value="mama")
        support_frame = ttk.Frame(self.input_frame)
        support_frame.grid(row=row, column=1, columnspan=2, sticky=tk.W, pady=5)
        ttk.Radiobutton(support_frame, text="Mama (bruin haar, groen shirt)", 
                       variable=self.starting_support, value="mama").pack(side=tk.TOP, anchor=tk.W, pady=2)
        ttk.Radiobutton(support_frame, text="Alternative (blond haar, wit shirt)", 
                       variable=self.starting_support, value="alternative").pack(side=tk.TOP, anchor=tk.W, pady=2)
        self.entry_list.append(self.starting_support)
        row += 1
        
        # === Language Selection ===
        ttk.Label(self.input_frame, text="Taal / Language:", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=5, padx=(0, 10))
        self.language = tk.StringVar(value="dutch")
        lang_frame = ttk.Frame(self.input_frame)
        lang_frame.grid(row=row, column=1, columnspan=2, sticky=tk.W, pady=5)
        ttk.Radiobutton(lang_frame, text="Nederlands (Dutch)", 
                       variable=self.language, value="dutch").pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(lang_frame, text="English", 
                       variable=self.language, value="english").pack(side=tk.LEFT)
        self.entry_list.append(self.language)
        row += 1
        
        # Separator
        ttk.Separator(self.input_frame, orient='horizontal').grid(
            row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        row += 1
        
        # === Trial Number (Optional) ===
        ttk.Label(self.input_frame, text="Trial nummer:", font=('Arial', 9)).grid(
            row=row, column=0, sticky=tk.W, pady=5, padx=(0, 10))
        self.trial_number = tk.IntVar(value=0)
        trial_entry = ttk.Entry(self.input_frame, textvariable=self.trial_number, width=10)
        trial_entry.grid(row=row, column=1, sticky=tk.W, pady=5)
        trial_entry.config(validate='focusout',
                          validatecommand=(self.register(self.validate_trial_number), '%P'),
                          invalidcommand=(self.register(self.on_invalid_trial_number),))
        ttk.Label(self.input_frame, text="(optioneel, standaard=0)", 
                 font=('Arial', 8), foreground='gray').grid(row=row, column=2, sticky=tk.W, pady=5, padx=(5, 0))
        self.trial_number_error = ttk.Label(self.input_frame, foreground='red', font=('Arial', 8))
        self.trial_number_error.grid(row=row+1, column=1, columnspan=2, sticky=tk.W)
        self.entry_list.append(self.trial_number)
        row += 2
        
        # === Save Button ===
        button_frame = ttk.Frame(self.input_frame)
        button_frame.grid(row=row, column=0, columnspan=3, pady=20)
        
        save_button = ttk.Button(button_frame, text="💾 Start Experiment", 
                                command=self.clear_input, style='Accent.TButton')
        save_button.pack(fill='x', padx=5)
        
        # Info label
        info_label = ttk.Label(self.input_frame, 
                              text="(Window will stay open to show progress)", 
                              font=('Arial', 8, 'italic'), foreground='gray')
        info_label.grid(row=row+1, column=0, columnspan=3)
        
        self.close_error = ttk.Label(self.input_frame, foreground='red', font=('Arial', 9, 'bold'))
        self.close_error.grid(row=row+2, column=0, columnspan=3, pady=5)
    
    def create_log_panel(self, parent):
        """Create the live logging panel on the right side"""
        
        # Log frame with border
        log_container = ttk.LabelFrame(parent, text="Live Activity Log", padding="10")
        log_container.grid(row=0, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        log_container.columnconfigure(0, weight=1)
        log_container.rowconfigure(0, weight=1)
        
        # Create scrolled text widget
        self.log_text = ScrolledText(log_container, state='disabled', 
                                     wrap='word', width=50, height=30,
                                     font=('Consolas', 9), bg='#f5f5f5')
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Clear log button
        clear_button = ttk.Button(log_container, text="🗑️ Clear Log", 
                                 command=self.clear_log)
        clear_button.grid(row=1, column=0, pady=(5, 0), sticky=tk.E)
    
    def create_status_bar(self, parent):
        """Create status bar at the bottom"""
        
        status_frame = ttk.Frame(parent, relief=tk.SUNKEN)
        status_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.status_label = ttk.Label(status_frame, text="Ready | Fill in participant information to continue", 
                                     font=('Arial', 9))
        self.status_label.pack(side=tk.LEFT, padx=5, pady=2)
    
    def setup_logging(self):
        """Setup logging to the text widget"""
        
        # Create text handler
        text_handler = TextHandler(self.log_text)
        text_handler.setFormatter(logging.Formatter('%(message)s'))
        
        # Add handler to root logger
        logger = logging.getLogger()
        logger.addHandler(text_handler)
        logger.setLevel(logging.INFO)
    
    def clear_log(self):
        """Clear the log window"""
        self.log_text.configure(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.configure(state='disabled')
        logging.info("Log cleared")
    
    def update_status(self, message, color='black'):
        """Update the status bar message"""
        self.status_label.config(text=message, foreground=color)
    
    def validate_age(self, value):
        """Validate age input (9-13)"""
        if value == "":
            self.age_error.config(text="")
            return True
        
        try:
            age = int(value)
            if age < 9 or age > 13:
                return False
            self.age_error.config(text="✓", foreground='green')
            return True
        except ValueError:
            return False
    
    def on_invalid_age(self):
        """Handle invalid age input"""
        self.age_error.config(text="❌ Must be 9-13", foreground='red')
        logging.warning("Invalid age entered (must be between 9-13)")
    
    def validate_trial_number(self, value):
        """Validate trial number input (0-25)"""
        if value == "":
            self.trial_number_error.config(text="")
            return True
        
        try:
            trial_num = int(value)
            if trial_num < 0 or trial_num > 25:
                return False
            if trial_num == 0:
                self.trial_number_error.config(text="")
            else:
                self.trial_number_error.config(text=f"✓ Start from trial {trial_num}", foreground='green')
            return True
        except ValueError:
            return False
    
    def on_invalid_trial_number(self):
        """Handle invalid trial number input"""
        self.trial_number_error.config(text="❌ Must be 0-25", foreground='red')
        logging.warning("Invalid trial number entered (must be between 0-25)")
    
    def sync_contingency_to_support(self):
        """Sync support frequency when contingency is changed"""
        contingency_val = self.contingency.get()
        if contingency_val == 80:
            self.support_frequency.set("frequent")
            logging.info("Contingency set to 80% → Support frequency set to Frequent")
        elif contingency_val == 20:
            self.support_frequency.set("infrequent")
            logging.info("Contingency set to 20% → Support frequency set to Infrequent")
    
    def sync_support_to_contingency(self):
        """Sync contingency when support frequency is changed"""
        support_val = self.support_frequency.get()
        if support_val == "frequent":
            self.contingency.set(80)
            logging.info("Support frequency set to Frequent → Contingency set to 80%")
        elif support_val == "infrequent":
            self.contingency.set(20)
            logging.info("Support frequency set to Infrequent → Contingency set to 20%")
    
    def clear_input(self):
        """Validate all inputs and close if valid"""
        logging.info("Validating participant information...")
        self.update_status("Validating input...", 'blue')
        
        all_entries_ok = True
        missing_fields = []
        
        for entry in self.entry_list:
            if entry is None:
                logging.error("Validation error: None entry found")
                all_entries_ok = False
                break
            
            try:
                value = entry.get()
                
                # Allow 0 for trial_number (it's the default), but not for other fields
                if entry == self.trial_number:
                    if value == "":
                        missing_fields.append("Trial nummer")
                        all_entries_ok = False
                elif value == "" or value == 0:
                    # Find field name for better error message
                    if entry == self.player_name:
                        missing_fields.append("Naam")
                    elif entry == self.player_id:
                        missing_fields.append("ID")
                    elif entry == self.player_age:
                        missing_fields.append("Leeftijd")
                    elif entry == self.player_gender:
                        missing_fields.append("Geslacht")
                    elif entry == self.contingency:
                        missing_fields.append("Contingentie")
                    elif entry == self.block:
                        missing_fields.append("Block")
                    elif entry == self.support_frequency:
                        missing_fields.append("Support Frequentie")
                    elif entry == self.starting_support:
                        missing_fields.append("Start Figuur")
                    elif entry == self.language:
                        missing_fields.append("Language")
                    all_entries_ok = False
                    
            except Exception as e:
                logging.error(f"Validation error: {e}")
                all_entries_ok = False
                break
        
        if all_entries_ok:
            logging.info("✓ All fields validated successfully")
            logging.info(f"Participant: {self.player_name.get()} (ID: {self.player_id.get()})")
            logging.info(f"Age: {self.player_age.get()}, Gender: {self.player_gender.get()}")
            logging.info(f"Contingency: {self.contingency.get()}%, Block: {self.block.get()}")
            logging.info(f"Support Frequency: {self.support_frequency.get()}")
            logging.info(f"Starting Trial: {self.trial_number.get()}")
            logging.info(f"Starting Figure: {self.starting_support.get()}")
            logging.info(f"Language: {self.language.get()}")
            self.update_status("✓ Validation successful! Proceeding...", 'green')
            
            # Disable the form so it can't be changed
            self.disable_form()
            
            # Set flag and close the window to continue
            self.form_completed = True
            self.after(500, self.quit)  # Use quit() instead of destroy() to keep window for later
        else:
            if missing_fields:
                error_msg = f"❌ Missing: {', '.join(missing_fields)}"
                self.close_error.config(text=error_msg)
                logging.error(f"Missing required fields: {', '.join(missing_fields)}")
                self.update_status("Error: Missing required fields", 'red')
            else:
                self.close_error.config(text="❌ Please check all fields")
                logging.error("Validation failed: Please check all fields")
                self.update_status("Error: Invalid input", 'red')
    
    def disable_form(self):
        """Disable all form inputs after submission"""
        # Disable all widgets in the input frame
        for child in self.input_frame.winfo_children():
            if isinstance(child, (ttk.Entry, ttk.Radiobutton, ttk.Button)):
                child.config(state='disabled')
            elif isinstance(child, ttk.Frame):
                # Disable children of frames (like radio button groups)
                for subchild in child.winfo_children():
                    if isinstance(subchild, (ttk.Entry, ttk.Radiobutton, ttk.Button)):
                        try:
                            subchild.config(state='disabled')
                        except:
                            pass
    
    def get_results(self):
        """Get all participant data as dictionary"""
        return {
            "name": self.player_name.get(),
            "id": self.player_id.get(),
            "contingency": self.contingency.get(),
            "age": self.player_age.get(),
            "gender": self.player_gender.get(),
            "height": 120,
            "trial_block": self.block.get(),
            "trial_number": self.trial_number.get(),
            "support_frequency": self.support_frequency.get(),
            "starting_support": self.starting_support.get(),
            "language": self.language.get()
        }
