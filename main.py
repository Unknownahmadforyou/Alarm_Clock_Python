from tkinter import *
from tkinter import ttk, messagebox, filedialog
import datetime
import time
import winsound
import threading
import os
import json
from PIL import Image, ImageTk
import pytz
import math
import io
import base64

class EnhancedAlarmClockApp:
    def __init__(self, root):
        # Initialize main window
        self.root = root
        self.root.title("Enhanced Alarm Clock")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Variables
        self.alarms = []
        self.active_alarms = {}
        self.is_dark_mode = BooleanVar(value=False)
        self.alarm_sound = "sound.wav"
        self.snooze_time = IntVar(value=5)
        self.stopwatch_running = False
        self.stopwatch_start = 0
        self.stopwatch_elapsed = 0
        self.lap_times = []
        self.world_clocks = [
            {"city": "New York", "timezone": "America/New_York"},
            {"city": "London", "timezone": "Europe/London"},
            {"city": "Tokyo", "timezone": "Asia/Tokyo"},
            {"city": "Sydney", "timezone": "Australia/Sydney"}
        ]
        
        # Create settings file if it doesn't exist
        self.config_file = "alarm_settings.json"
        self.load_settings()
        
        # Load world map image (using base64 encoded placeholder)
        self.world_map_img = self.create_world_map_placeholder()
        
        # Create UI
        self.create_menu()
        self.create_widgets()
        self.apply_theme()
        
        # Start world clock updates
        self.update_world_clocks()
        
    def create_world_map_placeholder(self):
        """Create a simple world map placeholder with time zones"""
        try:
            # In a real app, you would use an actual world map image
            # This is a placeholder that creates a simple gradient with time zones
            from PIL import Image, ImageDraw
            
            # Create a blank image
            img = Image.new('RGB', (800, 400), (255, 255, 255))
            draw = ImageDraw.Draw(img)
            
            # Draw simple continents
            draw.rectangle([100, 100, 300, 300], outline=(0, 0, 255), width=2)  # Americas
            draw.rectangle([350, 100, 550, 300], outline=(0, 0, 255), width=2)  # Europe/Africa
            draw.rectangle([600, 100, 700, 300], outline=(0, 0, 255), width=2)  # Asia
            
            # Draw time zone lines
            for i in range(0, 800, 100):
                draw.line([i, 0, i, 400], fill=(200, 200, 200), width=1)
                draw.text((i+10, 10), f"UTC{i//100 - 8}", fill=(0, 0, 0))
            
            return ImageTk.PhotoImage(img)
        except:
            # Fallback if PIL is not available
            return None
        
    def load_settings(self):
        """Load user settings from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, "r") as f:
                    settings = json.load(f)
                    self.is_dark_mode.set(settings.get("dark_mode", False))
                    self.alarm_sound = settings.get("alarm_sound", "sound.wav")
                    self.snooze_time.set(settings.get("snooze_time", 5))
                    self.alarms = settings.get("saved_alarms", [])
                    self.world_clocks = settings.get("world_clocks", [
                        {"city": "New York", "timezone": "America/New_York"},
                        {"city": "London", "timezone": "Europe/London"},
                        {"city": "Tokyo", "timezone": "Asia/Tokyo"},
                        {"city": "Sydney", "timezone": "Australia/Sydney"}
                    ])
        except Exception as e:
            print(f"Error loading settings: {e}")
    
    def save_settings(self):
        """Save user settings to file"""
        settings = {
            "dark_mode": self.is_dark_mode.get(),
            "alarm_sound": self.alarm_sound,
            "snooze_time": self.snooze_time.get(),
            "saved_alarms": self.alarms,
            "world_clocks": self.world_clocks
        }
        try:
            with open(self.config_file, "w") as f:
                json.dump(settings, f)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def create_menu(self):
        """Create menu bar"""
        menu_bar = Menu(self.root)
        
        # File menu
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Save Settings", command=self.save_settings)
        file_menu.add_command(label="Select Alarm Sound", command=self.select_sound)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        
        # Themes menu
        theme_menu = Menu(menu_bar, tearoff=0)
        theme_menu.add_checkbutton(label="Dark Mode", variable=self.is_dark_mode, 
                                  command=self.apply_theme)
        menu_bar.add_cascade(label="Themes", menu=theme_menu)
        
        # Help menu
        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Instructions", command=self.show_instructions)
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menu_bar)
    
    def create_widgets(self):
        """Create all UI elements"""
        # Main frame with padding
        self.main_frame = Frame(self.root, padx=20, pady=20)
        self.main_frame.pack(fill=BOTH, expand=True)
        
        # Title with custom font and color
        self.title_label = Label(self.main_frame, text="Enhanced Alarm Clock", 
                                font=("Helvetica", 24, "bold"))
        self.title_label.pack(pady=10)
        
        # Current time display
        self.time_label = Label(self.main_frame, font=("Helvetica", 14))
        self.time_label.pack(pady=5)
        self.update_time()
        
        # Notebook for multiple tabs
        self.tab_control = ttk.Notebook(self.main_frame)
        
        # Set Alarm Tab
        self.alarm_tab = Frame(self.tab_control)
        self.tab_control.add(self.alarm_tab, text="Set Alarm")
        self.create_alarm_tab()
        
        # Alarms Tab
        self.alarms_tab = Frame(self.tab_control)
        self.tab_control.add(self.alarms_tab, text="Active Alarms")
        self.create_alarms_tab()
        
        # Stopwatch Tab
        self.stopwatch_tab = Frame(self.tab_control)
        self.tab_control.add(self.stopwatch_tab, text="Stopwatch")
        self.create_stopwatch_tab()
        
        # World Clock Tab
        self.world_clock_tab = Frame(self.tab_control)
        self.tab_control.add(self.world_clock_tab, text="World Clock")
        self.create_world_clock_tab()
        
        # World Map Tab
        self.world_map_tab = Frame(self.tab_control)
        self.tab_control.add(self.world_map_tab, text="World Map")
        self.create_world_map_tab()
        
        # Pack the notebook
        self.tab_control.pack(expand=True, fill=BOTH)
        
        # Status bar
        self.status_var = StringVar()
        self.status_var.set("Ready")
        self.status_bar = Label(self.main_frame, textvariable=self.status_var, bd=1, relief=SUNKEN, anchor=W)
        self.status_bar.pack(side=BOTTOM, fill=X)
        
        # Load saved alarms
        self.load_saved_alarms()
    
    def create_alarm_tab(self):
        """Create content for the alarm tab"""
        # Time selection frame
        time_frame = Frame(self.alarm_tab)
        time_frame.pack(pady=10)
        
        # Hour selection
        Label(time_frame, text="Hour:").grid(row=0, column=0, padx=5)
        self.hour = StringVar(self.root)
        self.hours = tuple(f"{i:02d}" for i in range(24))
        self.hour.set(self.hours[datetime.datetime.now().hour])
        ttk.Combobox(time_frame, textvariable=self.hour, values=self.hours, width=5).grid(row=1, column=0, padx=5)
        
        # Minute selection
        Label(time_frame, text="Minute:").grid(row=0, column=1, padx=5)
        self.minute = StringVar(self.root)
        self.minutes = tuple(f"{i:02d}" for i in range(60))
        self.minute.set(self.minutes[datetime.datetime.now().minute])
        ttk.Combobox(time_frame, textvariable=self.minute, values=self.minutes, width=5).grid(row=1, column=1, padx=5)
        
        # Second selection
        Label(time_frame, text="Second:").grid(row=0, column=2, padx=5)
        self.second = StringVar(self.root)
        self.seconds = tuple(f"{i:02d}" for i in range(60))
        self.second.set(self.seconds[0])
        ttk.Combobox(time_frame, textvariable=self.second, values=self.seconds, width=5).grid(row=1, column=2, padx=5)
        
        # Alarm name entry
        name_frame = Frame(self.alarm_tab)
        name_frame.pack(pady=10)
        Label(name_frame, text="Alarm Name:").pack(side=LEFT, padx=5)
        self.alarm_name = StringVar(value="My Alarm")
        Entry(name_frame, textvariable=self.alarm_name, width=20).pack(side=LEFT)
        
        # Snooze frame
        snooze_frame = Frame(self.alarm_tab)
        snooze_frame.pack(pady=5)
        Label(snooze_frame, text="Snooze Time (minutes):").pack(side=LEFT, padx=5)
        ttk.Spinbox(snooze_frame, from_=1, to=30, textvariable=self.snooze_time, width=5).pack(side=LEFT)
        
        # Buttons frame
        buttons_frame = Frame(self.alarm_tab)
        buttons_frame.pack(pady=10)
        
        # Set alarm button with improved styling
        self.set_button = Button(buttons_frame, text="Set Alarm", font=("Helvetica", 12), 
                               command=self.set_alarm, width=10)
        self.set_button.pack(side=LEFT, padx=5)
        
        # Test sound button
        self.test_button = Button(buttons_frame, text="Test Sound", font=("Helvetica", 12), 
                                command=self.test_alarm_sound, width=10)
        self.test_button.pack(side=LEFT, padx=5)
    
    def create_alarms_tab(self):
        """Create content for the alarms tab"""
        # Alarms list
        Label(self.alarms_tab, text="Your Alarms", font=("Helvetica", 14, "bold")).pack(pady=5)
        
        # Create frame for alarms list with scrollbar
        alarms_frame = Frame(self.alarms_tab)
        alarms_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)
        
        self.alarms_listbox = Listbox(alarms_frame, height=10, width=50)
        self.alarms_listbox.pack(side=LEFT, fill=BOTH, expand=True)
        
        scrollbar = Scrollbar(alarms_frame, orient="vertical")
        scrollbar.config(command=self.alarms_listbox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        self.alarms_listbox.config(yscrollcommand=scrollbar.set)
        
        # Buttons for alarms management
        alarms_buttons_frame = Frame(self.alarms_tab)
        alarms_buttons_frame.pack(pady=10)
        
        Button(alarms_buttons_frame, text="Remove Alarm", command=self.remove_alarm, 
              font=("Helvetica", 12)).pack(side=LEFT, padx=5)
    
    def create_stopwatch_tab(self):
        """Create content for the stopwatch tab"""
        # Stopwatch display
        self.stopwatch_label = Label(self.stopwatch_tab, text="00:00:00.000", font=("Helvetica", 36))
        self.stopwatch_label.pack(pady=20)
        
        # Buttons frame
        buttons_frame = Frame(self.stopwatch_tab)
        buttons_frame.pack(pady=10)
        
        # Start/Stop button
        self.start_stop_button = Button(buttons_frame, text="Start", font=("Helvetica", 12), 
                                      command=self.toggle_stopwatch, width=10)
        self.start_stop_button.pack(side=LEFT, padx=5)
        
        # Lap button
        self.lap_button = Button(buttons_frame, text="Lap", font=("Helvetica", 12), 
                                command=self.record_lap, width=10, state=DISABLED)
        self.lap_button.pack(side=LEFT, padx=5)
        
        # Reset button
        self.reset_button = Button(buttons_frame, text="Reset", font=("Helvetica", 12), 
                                 command=self.reset_stopwatch, width=10)
        self.reset_button.pack(side=LEFT, padx=5)
        
        # Lap times frame
        lap_frame = Frame(self.stopwatch_tab)
        lap_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)
        
        # Lap times list
        self.lap_listbox = Listbox(lap_frame, height=10, width=50)
        self.lap_listbox.pack(side=LEFT, fill=BOTH, expand=True)
        
        scrollbar = Scrollbar(lap_frame, orient="vertical")
        scrollbar.config(command=self.lap_listbox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        self.lap_listbox.config(yscrollcommand=scrollbar.set)
    
    def create_world_clock_tab(self):
        """Create content for the world clock tab"""
        # Frame for clock displays
        self.world_clock_frame = Frame(self.world_clock_tab)
        self.world_clock_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Add/remove city frame
        city_frame = Frame(self.world_clock_tab)
        city_frame.pack(fill=X, padx=10, pady=5)
        
        # City selection
        Label(city_frame, text="City:").pack(side=LEFT, padx=5)
        self.city_name = StringVar()
        Entry(city_frame, textvariable=self.city_name, width=20).pack(side=LEFT, padx=5)
        
        # Timezone selection
        Label(city_frame, text="Timezone:").pack(side=LEFT, padx=5)
        self.timezone_var = StringVar()
        timezones = sorted(pytz.all_timezones)
        self.timezone_combo = ttk.Combobox(city_frame, textvariable=self.timezone_var, 
                                          values=timezones, width=30)
        self.timezone_combo.pack(side=LEFT, padx=5)
        
        # Add button
        Button(city_frame, text="Add Clock", font=("Helvetica", 10), 
              command=self.add_world_clock).pack(side=LEFT, padx=5)
        
        # Create initial clock displays
        self.update_world_clock_displays()
    
    def create_world_map_tab(self):
        """Create content for the world map tab"""
        # World map display
        self.world_map_label = Label(self.world_map_tab)
        self.world_map_label.pack(pady=10)
        
        if self.world_map_img:
            self.world_map_label.config(image=self.world_map_img)
        
        # Timezone information
        self.timezone_info = Label(self.world_map_tab, text="", font=("Helvetica", 12))
        self.timezone_info.pack(pady=10)
        
        # Current time display
        self.map_time_label = Label(self.world_map_tab, font=("Helvetica", 14))
        self.map_time_label.pack(pady=5)
        
        # Bind mouse motion to show timezone info
        self.world_map_label.bind("<Motion>", self.show_timezone_info)
    
    def show_timezone_info(self, event):
        """Show timezone information based on mouse position"""
        # Calculate approximate timezone based on x position
        width = self.world_map_label.winfo_width()
        if width == 1:  # Sometimes returns 1 before being rendered
            width = 800  # Default to our placeholder image width
            
        x_pos = event.x
        timezone_offset = round((x_pos / width) * 24 - 12)  # -12 to +12
        
        # Get current time in that timezone
        now = datetime.datetime.now(pytz.utc)
        tz_time = now + datetime.timedelta(hours=timezone_offset)
        
        # Display info
        self.timezone_info.config(text=f"UTC{timezone_offset:+d}: {tz_time.strftime('%H:%M:%S')}")
    
    def add_world_clock(self):
        """Add a new world clock to display"""
        city = self.city_name.get()
        timezone = self.timezone_var.get()
        
        if not city or not timezone:
            messagebox.showwarning("Input Error", "Please enter both city name and timezone")
            return
        
        # Add to world clocks
        self.world_clocks.append({"city": city, "timezone": timezone})
        
        # Save settings
        self.save_settings()
        
        # Update displays
        self.update_world_clock_displays()
        
        # Clear inputs
        self.city_name.set("")
        self.timezone_var.set("")
    
    def remove_world_clock(self, city):
        """Remove a world clock from display"""
        self.world_clocks = [clock for clock in self.world_clocks if clock["city"] != city]
        
        # Save settings
        self.save_settings()
        
        # Update displays
        self.update_world_clock_displays()
    
    def update_world_clock_displays(self):
        """Update the world clock displays"""
        # Clear existing clocks
        for widget in self.world_clock_frame.winfo_children():
            widget.destroy()
        
        # Create new clock displays
        for i, clock in enumerate(self.world_clocks):
            clock_frame = Frame(self.world_clock_frame, bd=2, relief=GROOVE, padx=10, pady=10)
            clock_frame.grid(row=i//2, column=i%2, padx=5, pady=5, sticky="nsew")
            
            # City name
            city_label = Label(clock_frame, text=clock["city"], font=("Helvetica", 14, "bold"))
            city_label.pack()
            
            # Timezone
            tz_label = Label(clock_frame, text=clock["timezone"], font=("Helvetica", 10))
            tz_label.pack()
            
            # Time display
            time_label = Label(clock_frame, font=("Helvetica", 18))
            time_label.pack(pady=5)
            
            # Store reference to update later
            clock["time_label"] = time_label
            
            # Remove button
            Button(clock_frame, text="Remove", 
                  command=lambda c=clock["city"]: self.remove_world_clock(c)).pack()
        
        # Configure grid weights
        for i in range((len(self.world_clocks) + 1) // 2):
            self.world_clock_frame.rowconfigure(i, weight=1)
        for i in range(2):
            self.world_clock_frame.columnconfigure(i, weight=1)
    
    def update_world_clocks(self):
        """Update all world clock displays"""
        for clock in self.world_clocks:
            try:
                tz = pytz.timezone(clock["timezone"])
                current_time = datetime.datetime.now(tz)
                clock["time_label"].config(text=current_time.strftime("%H:%M:%S"))
            except Exception as e:
                print(f"Error updating world clock: {e}")
        
        # Update map time display
        current_time = datetime.datetime.now().strftime("%H:%M:%S - %B %d, %Y")
        self.map_time_label.config(text=f"Current Time: {current_time}")
        
        # Schedule next update
        self.root.after(1000, self.update_world_clocks)
    
    def toggle_stopwatch(self):
        """Start or stop the stopwatch"""
        if not self.stopwatch_running:
            # Start the stopwatch
            self.stopwatch_running = True
            self.stopwatch_start = time.time() - self.stopwatch_elapsed
            self.start_stop_button.config(text="Stop")
            self.lap_button.config(state=NORMAL)
            self.update_stopwatch()
        else:
            # Stop the stopwatch
            self.stopwatch_running = False
            self.stopwatch_elapsed = time.time() - self.stopwatch_start
            self.start_stop_button.config(text="Start")
            self.lap_button.config(state=DISABLED)
    
    def reset_stopwatch(self):
        """Reset the stopwatch"""
        self.stopwatch_running = False
        self.stopwatch_elapsed = 0
        self.stopwatch_label.config(text="00:00:00.000")
        self.start_stop_button.config(text="Start")
        self.lap_button.config(state=DISABLED)
        self.lap_times = []
        self.lap_listbox.delete(0, END)
    
    def record_lap(self):
        """Record a lap time"""
        if self.stopwatch_running:
            elapsed = time.time() - self.stopwatch_start
            lap_time = self.format_stopwatch_time(elapsed)
            self.lap_times.append(lap_time)
            self.lap_listbox.insert(END, f"Lap {len(self.lap_times)}: {lap_time}")
            self.lap_listbox.see(END)
    
    def update_stopwatch(self):
        """Update the stopwatch display"""
        if self.stopwatch_running:
            elapsed = time.time() - self.stopwatch_start
            self.stopwatch_label.config(text=self.format_stopwatch_time(elapsed))
            self.root.after(50, self.update_stopwatch)
    
    def format_stopwatch_time(self, seconds):
        """Format seconds into HH:MM:SS.mmm"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"
    
    def update_time(self):
        """Update current time display"""
        current_time = datetime.datetime.now().strftime("%H:%M:%S - %B %d, %Y")
        self.time_label.config(text=f"Current Time: {current_time}")
        self.root.after(1000, self.update_time)
    
    def set_alarm(self):
        """Set a new alarm"""
        try:
            alarm_time = f"{self.hour.get()}:{self.minute.get()}:{self.second.get()}"
            alarm_name = self.alarm_name.get()
            
            if not alarm_name:
                alarm_name = "Unnamed Alarm"
            
            # Add to alarms list
            alarm_data = {
                "time": alarm_time,
                "name": alarm_name,
                "active": True
            }
            
            self.alarms.append(alarm_data)
            
            # Start the alarm thread
            alarm_thread = threading.Thread(target=self.start_alarm, args=(alarm_data,))
            alarm_thread.daemon = True
            alarm_thread.start()
            
            self.active_alarms[alarm_time] = alarm_thread
            
            # Update alarms list
            self.update_alarms_list()
            
            # Show confirmation
            self.status_var.set(f"Alarm set for {alarm_time} - {alarm_name}")
            messagebox.showinfo("Alarm Set", f"Alarm '{alarm_name}' has been set for {alarm_time}")
            
            # Save settings
            self.save_settings()
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not set alarm: {str(e)}")
    
    def start_alarm(self, alarm_data):
        """Monitor for alarm time and trigger alarm"""
        alarm_time = alarm_data["time"]
        alarm_name = alarm_data["name"]
        
        while alarm_data["active"]:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            
            if current_time == alarm_time:
                # Play sound
                try:
                    # Show alarm notification with snooze option
                    self.show_alarm_notification(alarm_data)
                    winsound.PlaySound(self.alarm_sound, winsound.SND_ASYNC)
                except Exception as e:
                    print(f"Error playing sound: {e}")
                    # Fallback to default system sound
                    winsound.PlaySound("SystemExclamation", winsound.SND_ASYNC)
                
                # Wait a bit to avoid triggering multiple times
                time.sleep(2)
            
            time.sleep(0.5)
    
    def show_alarm_notification(self, alarm_data):
        """Show alarm notification with snooze option"""
        alarm_name = alarm_data["name"]
        result = messagebox.askquestion("Alarm", 
                                      f"Alarm: {alarm_name}\nTime: {alarm_data['time']}\n\nSnooze?")
        
        # Stop sound
        winsound.PlaySound(None, winsound.SND_PURGE)
        
        if result == 'yes':
            # Snooze the alarm
            threading.Thread(target=self.snooze_alarm, args=(alarm_data,)).start()
        else:
            # Just stop the alarm
            pass
    
    def snooze_alarm(self, alarm_data):
        """Snooze alarm for specified minutes"""
        snooze_minutes = self.snooze_time.get()
        
        # Calculate new alarm time
        current_time = datetime.datetime.now()
        new_time = current_time + datetime.timedelta(minutes=snooze_minutes)
        new_alarm_time = new_time.strftime("%H:%M:%S")
        
        # Create new alarm data
        new_alarm_data = {
            "time": new_alarm_time,
            "name": f"{alarm_data['name']} (Snoozed)",
            "active": True
        }
        
        # Add to alarms list
        self.alarms.append(new_alarm_data)
        
        # Start the alarm thread
        alarm_thread = threading.Thread(target=self.start_alarm, args=(new_alarm_data,))
        alarm_thread.daemon = True
        alarm_thread.start()
        
        self.active_alarms[new_alarm_time] = alarm_thread
        
        # Update alarms list
        self.update_alarms_list()
        
        # Show confirmation
        self.status_var.set(f"Alarm snoozed for {snooze_minutes} minutes")
    
    def load_saved_alarms(self):
        """Load saved alarms from settings"""
        for alarm in self.alarms:
            # Start alarm thread
            alarm_thread = threading.Thread(target=self.start_alarm, args=(alarm,))
            alarm_thread.daemon = True
            alarm_thread.start()
            
            self.active_alarms[alarm["time"]] = alarm_thread
        
        # Update alarms list
        self.update_alarms_list()
    
    def update_alarms_list(self):
        """Update the alarms listbox"""
        self.alarms_listbox.delete(0, END)
        
        for alarm in self.alarms:
            status = "Active" if alarm["active"] else "Inactive"
            self.alarms_listbox.insert(END, f"{alarm['time']} - {alarm['name']} ({status})")
    
    def remove_alarm(self):
        """Remove selected alarm"""
        try:
            # Get selected alarm
            selected = self.alarms_listbox.curselection()
            
            if not selected:
                messagebox.showinfo("Selection Required", "Please select an alarm to remove")
                return
            
            index = selected[0]
            alarm = self.alarms[index]
            
            # Set as inactive
            alarm["active"] = False
            
            # Remove from list
            self.alarms.pop(index)
            
            # Update display
            self.update_alarms_list()
            
            # Save settings
            self.save_settings()
            
            self.status_var.set(f"Alarm removed: {alarm['time']} - {alarm['name']}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not remove alarm: {str(e)}")
    
    def select_sound(self):
        """Let user select a custom alarm sound"""
        sound_file = filedialog.askopenfilename(
            title="Select Alarm Sound",
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")]
        )
        
        if sound_file:
            self.alarm_sound = sound_file
            self.save_settings()
            self.status_var.set(f"Alarm sound set to: {os.path.basename(sound_file)}")
    
    def test_alarm_sound(self):
        """Test the current alarm sound"""
        try:
            winsound.PlaySound(self.alarm_sound, winsound.SND_ASYNC)
            self.status_var.set("Testing alarm sound...")
        except Exception as e:
            messagebox.showerror("Error", f"Could not play sound: {str(e)}")
            # Fallback to default system sound
            winsound.PlaySound("SystemExclamation", winsound.SND_ASYNC)
    
    def apply_theme(self):
        """Apply light or dark theme"""
        if self.is_dark_mode.get():
            # Dark mode
            bg_color = "#2E2E2E"
            fg_color = "white"
            accent_color = "#007ACC"
            self.root.configure(bg=bg_color)
            self.main_frame.configure(bg=bg_color)
            self.title_label.configure(bg=bg_color, fg=accent_color)
            self.time_label.configure(bg=bg_color, fg=fg_color)
            self.alarm_tab.configure(bg=bg_color)
            self.alarms_tab.configure(bg=bg_color)
            self.stopwatch_tab.configure(bg=bg_color)
            self.world_clock_tab.configure(bg=bg_color)
            self.world_map_tab.configure(bg=bg_color)
            self.status_bar.configure(bg="#3E3E3E", fg=fg_color)
            
            # Update all labels and buttons
            self.update_widget_colors(bg_color, fg_color, accent_color)
            
        else:
            # Light mode
            bg_color = "#F0F0F0"
            fg_color = "black"
            accent_color = "#0078D7"
            self.root.configure(bg=bg_color)
            self.main_frame.configure(bg=bg_color)
            self.title_label.configure(bg=bg_color, fg="red")
            self.time_label.configure(bg=bg_color, fg=fg_color)
            self.alarm_tab.configure(bg=bg_color)
            self.alarms_tab.configure(bg=bg_color)
            self.stopwatch_tab.configure(bg=bg_color)
            self.world_clock_tab.configure(bg=bg_color)
            self.world_map_tab.configure(bg=bg_color)
            self.status_bar.configure(bg="#E0E0E0", fg=fg_color)
            
            # Update all labels and buttons
            self.update_widget_colors(bg_color, fg_color, accent_color)
        
        self.save_settings()
    
    def update_widget_colors(self, bg_color, fg_color, accent_color):
        """Update colors for all widgets in all tabs"""
        tabs = [self.alarm_tab, self.alarms_tab, self.stopwatch_tab, 
                self.world_clock_tab, self.world_map_tab]
        
        for tab in tabs:
            for widget in tab.winfo_children():
                if isinstance(widget, Frame):
                    widget.configure(bg=bg_color)
                    for child in widget.winfo_children():
                        if isinstance(child, Label):
                            child.configure(bg=bg_color, fg=fg_color)
                        elif isinstance(child, Button):
                            child.configure(bg=bg_color, fg=fg_color, 
                                          activebackground=accent_color)
                        elif isinstance(child, Listbox):
                            child.configure(bg=bg_color, fg=fg_color, 
                                          selectbackground=accent_color)
                elif isinstance(widget, Label):
                    widget.configure(bg=bg_color, fg=fg_color)
                elif isinstance(widget, Button):
                    widget.configure(bg=bg_color, fg=fg_color, 
                                   activebackground=accent_color)
                elif isinstance(widget, Listbox):
                    widget.configure(bg=bg_color, fg=fg_color, 
                                   selectbackground=accent_color)
        
        # Configure buttons specifically
        self.set_button.configure(bg=bg_color, fg=fg_color, activebackground=accent_color)
        self.test_button.configure(bg=bg_color, fg=fg_color, activebackground=accent_color)
        self.start_stop_button.configure(bg=bg_color, fg=fg_color, activebackground=accent_color)
        self.lap_button.configure(bg=bg_color, fg=fg_color, activebackground=accent_color)
        self.reset_button.configure(bg=bg_color, fg=fg_color, activebackground=accent_color)
    
    def show_instructions(self):
        """Display instructions dialog"""
        instruction_text = """
        Enhanced Alarm Clock Instructions:
        
        1. Alarm Features:
           - Set multiple alarms with custom names
           - Snooze functionality
           - Custom alarm sounds
        
        2. Stopwatch:
           - Start/Stop button to control timing
           - Lap button to record lap times
           - Reset to clear all times
        
        3. World Clock:
           - View multiple time zones simultaneously
           - Add/remove cities as needed
           - Automatic time updates
        
        4. World Map:
           - Visual representation of time zones
           - Hover to see time in different zones
        
        5. Settings:
           - Dark/Light theme
           - Save your preferences
        """
        messagebox.showinfo("Instructions", instruction_text)
    
    def show_about(self):
        """Display about dialog"""
        about_text = """
        Enhanced Alarm Clock
        Version 3.0
        
        A feature-rich time management application with:
        - Alarm clock with snooze
        - Stopwatch with lap times
        - World clock with multiple time zones
        - World map visualization
        
        Created with Python and Tkinter.
        """
        messagebox.showinfo("About", about_text)

# Main application
if __name__ == "__main__":
    root = Tk()
    app = EnhancedAlarmClockApp(root)
    root.mainloop()