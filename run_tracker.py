import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext

class ShadowrunRun:
    STATUSES = ["Active", "Completed", "Abandoned"]
    
    def __init__(self, name="", description="", reward=0):
        self.name = name
        self.description = description
        self.reward = reward
        self.status = "Active"
        self.character_file = ""
        self.character_name = ""

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "reward": self.reward,
            "status": self.status,
            "character_name": self.character_name
        }
    
    def from_dict(self, data):
        self.name = data.get("name", "")
        self.description = data.get("description", "")
        self.reward = data.get("reward", 0)
        self.status = data.get("status", "Active")
        self.character_file = ""
        self.character_name = data.get("character_name", "")

class RunTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shadowrun 6E Run Tracker")
        self.root.geometry("1000x700")
        self.runs = []
        self.current_character = None
        
        # Configure dark theme
        self.style = ttk.Style()
        self.style.theme_use("clam")
        bg_color = "#1c1c1c"
        fg_color = "#e0e0e0"
        self.style.configure(".", background=bg_color, foreground=fg_color, font=("Arial", 10))
        self.style.configure("TFrame", background=bg_color)
        self.style.configure("TLabel", background=bg_color, foreground=fg_color)
        self.style.configure("TButton", background="#333", foreground=fg_color, borderwidth=1)
        self.style.map("TButton", background=[('active', '#444')], foreground=[('active', fg_color)])
        self.style.configure("TEntry", fieldbackground="#333", foreground=fg_color, insertcolor=fg_color)
        self.style.configure("Treeview", background="#333", foreground=fg_color, fieldbackground="#333")
        self.style.map("Treeview", background=[('selected', '#4a6984')])
        self.style.configure("Treeview.Heading", background="#2d2d2d", foreground=fg_color)
        
        # Create main frames
        self.header_frame = ttk.Frame(root)
        self.header_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.footer_frame = ttk.Frame(root)
        self.footer_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Header
        ttk.Label(self.header_frame, text="Shadowrun 6E Run Tracker", 
                 font=("Arial", 16, "bold")).pack(side=tk.LEFT)
        
        # Character info
        char_frame = ttk.Frame(self.header_frame)
        char_frame.pack(side=tk.RIGHT, padx=10)
        
        ttk.Label(char_frame, text="Character:").pack(side=tk.LEFT)
        self.char_name_label = ttk.Label(char_frame, text="None", font=("Arial", 10, "bold"))
        self.char_name_label.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(char_frame, text="Nuyen:").pack(side=tk.LEFT, padx=(10, 0))
        self.nuyen_label = ttk.Label(char_frame, text="0¥", font=("Arial", 10, "bold"))
        self.nuyen_label.pack(side=tk.LEFT)
        
        # Main content - split view
        paned_window = ttk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Run list
        list_frame = ttk.Frame(paned_window, width=300)
        paned_window.add(list_frame, weight=1)
        
        # Run list controls
        ctrl_frame = ttk.Frame(list_frame)
        ctrl_frame.pack(fill=tk.X, padx=5, pady=5)
        
        new_btn = ttk.Button(ctrl_frame, text="New Run", command=self.new_run)
        new_btn.pack(side=tk.LEFT, padx=2)
        self.create_tooltip(new_btn, "Create a new run")
        
        import_btn = ttk.Button(ctrl_frame, text="Import Runs", command=self.import_runs)
        import_btn.pack(side=tk.LEFT, padx=2)
        self.create_tooltip(import_btn, "Import runs from JSON file")
        
        export_btn = ttk.Button(ctrl_frame, text="Export Runs", command=self.export_runs)
        export_btn.pack(side=tk.LEFT, padx=2)
        self.create_tooltip(export_btn, "Export runs to JSON file")
        
        # Run list treeview
        self.run_tree = ttk.Treeview(
            list_frame, 
            columns=("Status", "Reward", "Character"),
            show="headings",
            selectmode="browse"
        )
        self.run_tree.heading("#0", text="Run")
        self.run_tree.column("#0", width=200, stretch=tk.YES)
        self.run_tree.heading("Status", text="Status")
        self.run_tree.column("Status", width=100, anchor=tk.CENTER)
        self.run_tree.heading("Reward", text="Reward")
        self.run_tree.column("Reward", width=100, anchor=tk.CENTER)
        self.run_tree.heading("Character", text="Character")
        self.run_tree.column("Character", width=150, anchor=tk.CENTER)
        
        # Configure status colors
        self.run_tree.tag_configure("Active", foreground="#e0e0e0")
        self.run_tree.tag_configure("Completed", foreground="#4CAF50")
        self.run_tree.tag_configure("Abandoned", foreground="#F44336")
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.run_tree.yview)
        self.run_tree.configure(yscrollcommand=scrollbar.set)
        
        self.run_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.run_tree.bind("<<TreeviewSelect>>", self.show_run_details)
        
        # Right panel - Run details
        detail_frame = ttk.Frame(paned_window)
        paned_window.add(detail_frame, weight=2)
        
        # Run details
        detail_container = ttk.LabelFrame(detail_frame, text="Run Details")
        detail_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Name and reward
        name_frame = ttk.Frame(detail_container)
        name_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(name_frame, text="Name:").pack(side=tk.LEFT)
        self.detail_name = ttk.Label(name_frame, text="", font=("Arial", 10, "bold"))
        self.detail_name.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(name_frame, text="Reward:").pack(side=tk.LEFT, padx=(20, 0))
        self.detail_reward = ttk.Label(name_frame, text="0¥", font=("Arial", 10, "bold"))
        self.detail_reward.pack(side=tk.LEFT)
        
        # Status and character
        status_frame = ttk.Frame(detail_container)
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(status_frame, text="Status:").pack(side=tk.LEFT)
        self.detail_status = ttk.Label(status_frame, text="", font=("Arial", 10))
        self.detail_status.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(status_frame, text="Character:").pack(side=tk.LEFT, padx=(20, 0))
        self.detail_character = ttk.Label(status_frame, text="", font=("Arial", 10))
        self.detail_character.pack(side=tk.LEFT)
        
        # Description
        desc_frame = ttk.LabelFrame(detail_container, text="Description")
        desc_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.detail_desc = scrolledtext.ScrolledText(
            desc_frame, wrap=tk.WORD, bg="#333", fg="#e0e0e0"
        )
        self.detail_desc.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.detail_desc.config(state=tk.DISABLED)
        
        # Action buttons
        action_frame = ttk.Frame(detail_container)
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.complete_btn = ttk.Button(
            action_frame, text="Complete Run", 
            command=self.complete_run, state=tk.DISABLED
        )
        self.complete_btn.pack(side=tk.LEFT, padx=5)
        self.create_tooltip(self.complete_btn, "Complete run and award nuyen to current character")
        
        self.abandon_btn = ttk.Button(
            action_frame, text="Abandon Run", 
            command=self.abandon_run, state=tk.DISABLED
        )
        self.abandon_btn.pack(side=tk.LEFT, padx=5)
        self.create_tooltip(self.abandon_btn, "Mark run as abandoned (no nuyen awarded)")
        
        # Footer - character actions
        load_char_btn = ttk.Button(self.footer_frame, text="Load Character", command=self.load_character)
        load_char_btn.pack(side=tk.LEFT, padx=5)
        self.create_tooltip(load_char_btn, "Load a character file (.sr6) to use for completing runs")
        
        clear_char_btn = ttk.Button(self.footer_frame, text="Clear Character", command=self.clear_character)
        clear_char_btn.pack(side=tk.LEFT, padx=5)
        self.create_tooltip(clear_char_btn, "Clear the current character")
        
        # Initialize
        self.update_run_list()
    
    def create_tooltip(self, widget, text):
        """Create a tooltip for a widget"""
        tooltip = tk.Toplevel(self.root)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_attributes("-topmost", True)
        label = tk.Label(tooltip, text=text, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack()
        tooltip.withdraw()
        
        def enter(event):
            x = widget.winfo_rootx() + 10
            y = widget.winfo_rooty() + widget.winfo_height() + 5
            tooltip.geometry(f"+{x}+{y}")
            tooltip.deiconify()
            
        def leave(event):
            tooltip.withdraw()
            
        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)
    
    def load_character(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Shadowrun Characters", "*.sr6"), ("All Files", "*.*")]
        )
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, "r") as f:
                    char_data = json.load(f)
                self.current_character = {
                    "file": file_path,
                    "name": char_data.get("name", "Unknown"),
                    "nuyen": char_data.get("nuyen", 0)
                }
                self.char_name_label.config(text=self.current_character["name"])
                self.nuyen_label.config(text=f"{self.current_character['nuyen']}¥")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load character: {str(e)}")
    
    def clear_character(self):
        self.current_character = None
        self.char_name_label.config(text="None")
        self.nuyen_label.config(text="0¥")
    
    def new_run(self):
        dialog = RunDialog(self.root)
        self.root.wait_window(dialog)
        
        if dialog.run:
            self.runs.append(dialog.run)
            self.update_run_list()
    
    def import_runs(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, "r") as f:
                    runs_data = json.load(f)
                
                for run_data in runs_data:
                    run = ShadowrunRun()
                    run.from_dict(run_data)
                    self.runs.append(run)
                
                self.update_run_list()
                messagebox.showinfo("Success", f"Imported {len(runs_data)} runs")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import runs: {str(e)}")
    
    def export_runs(self):
        if not self.runs:
            messagebox.showwarning("Warning", "No runs to export")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        if file_path:
            runs_data = [run.to_dict() for run in self.runs]
            try:
                with open(file_path, "w") as f:
                    json.dump(runs_data, f, indent=2)
                messagebox.showinfo("Success", "Runs exported successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export runs: {str(e)}")
    
    def update_run_list(self):
        # Clear existing items
        for item in self.run_tree.get_children():
            self.run_tree.delete(item)
        
        # Add runs to treeview with status-based coloring
        for run in self.runs:
            self.run_tree.insert("", "end", text=run.name, 
                                values=(run.status, f"{run.reward}¥", run.character_name),
                                tags=(run.status,))
    
    def show_run_details(self, event):
        selected = self.run_tree.selection()
        if not selected:
            return
            
        index = self.run_tree.index(selected[0])
        if 0 <= index < len(self.runs):
            run = self.runs[index]
            
            # Update detail fields
            self.detail_name.config(text=run.name)
            self.detail_reward.config(text=f"{run.reward}¥")
            self.detail_status.config(text=run.status)
            self.detail_character.config(text=run.character_name or "None")
            
            # Update description
            self.detail_desc.config(state=tk.NORMAL)
            self.detail_desc.delete(1.0, tk.END)
            self.detail_desc.insert(tk.END, run.description)
            self.detail_desc.config(state=tk.DISABLED)
            
            # Update buttons based on status
            if run.status == "Active":
                self.complete_btn.config(state=tk.NORMAL)
                self.abandon_btn.config(state=tk.NORMAL)
            else:
                self.complete_btn.config(state=tk.DISABLED)
                self.abandon_btn.config(state=tk.DISABLED)
    
    def complete_run(self):
        selected = self.run_tree.selection()
        if not selected:
            return
            
        index = self.run_tree.index(selected[0])
        if 0 <= index < len(self.runs):
            run = self.runs[index]
            
            if run.status != "Active":
                messagebox.showwarning("Warning", "Only active runs can be completed")
                return
                
            if not self.current_character:
                messagebox.showwarning("Warning", "Load a character first to complete the run")
                return
                
            # Update run status
            run.status = "Completed"
            run.character_name = self.current_character["name"]
            run.character_file = self.current_character["file"]
            
            # Reward character
            try:
                with open(run.character_file, "r") as f:
                    char_data = json.load(f)
                
                char_data["nuyen"] = char_data.get("nuyen", 0) + run.reward
                
                with open(run.character_file, "w") as f:
                    json.dump(char_data, f, indent=2)
                
                # Update UI
                self.current_character["nuyen"] = char_data["nuyen"]
                self.nuyen_label.config(text=f"{char_data['nuyen']}¥")
                self.update_run_list()
                self.show_run_details(None)  # Refresh details
                
                messagebox.showinfo("Success", 
                                   f"Run completed! {run.reward}¥ awarded to {run.character_name}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to reward character: {str(e)}")
    
    def abandon_run(self):
        selected = self.run_tree.selection()
        if not selected:
            return
            
        index = self.run_tree.index(selected[0])
        if 0 <= index < len(self.runs):
            run = self.runs[index]
            
            if run.status != "Active":
                messagebox.showwarning("Warning", "Only active runs can be abandoned")
                return
                
            if not messagebox.askyesno(
                "Confirm Abandon", 
                "Are you sure you want to abandon this run?\nThis action cannot be undone."
            ):
                return
                
            run.status = "Abandoned"
            self.update_run_list()
            self.show_run_details(None)  # Refresh details
            messagebox.showinfo("Run Abandoned", "This run has been marked as abandoned")

class RunDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.run = None
        
        self.title("New Shadowrun")
        self.geometry("500x400")
        self.configure(bg="#1c1c1c")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets()
    
    def create_widgets(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Run name
        ttk.Label(main_frame, text="Run Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.name_entry = ttk.Entry(main_frame, width=40)
        self.name_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Reward
        ttk.Label(main_frame, text="Reward (¥):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.reward_spin = ttk.Spinbox(main_frame, from_=0, to=1000000, width=10)
        self.reward_spin.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        self.reward_spin.set(5000)  # Default reward
        
        # Description
        ttk.Label(main_frame, text="Description:").grid(row=2, column=0, sticky=tk.NW, padx=5, pady=5)
        self.desc_text = scrolledtext.ScrolledText(main_frame, width=40, height=10, 
                                                  bg="#333", fg="#e0e0e0", insertbackground="white")
        self.desc_text.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Create", command=self.create_run).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side=tk.LEFT, padx=5)
    
    def create_run(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Run name is required")
            return
            
        try:
            reward = int(self.reward_spin.get())
        except ValueError:
            messagebox.showerror("Error", "Reward must be a number")
            return
            
        description = self.desc_text.get("1.0", tk.END).strip()
        
        self.run = ShadowrunRun(name, description, reward)
        self.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = RunTrackerApp(root)
    root.mainloop()
