import json
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

# Dark theme colors
BG_COLOR = "#2e2e2e"
FG_COLOR = "#e0e0e0"
ENTRY_BG = "#333333"
ENTRY_FG = FG_COLOR
BUTTON_BG = "#444444"
BUTTON_FG = FG_COLOR
BUTTON_ACTIVE_BG = "#555555"
BUTTON_ACTIVE_FG = FG_COLOR

class ShadowrunRun:
    STATUSES = ["Active", "Completed", "Abandoned"]

    def __init__(self, name="", description="", reward=0):
        self.name = name
        self.description = description
        self.reward = reward
        self.status = "Active"
        self.character_file = ""
        self.character_name = ""
        # Each task is a dict: {"description": str, "mandatory": bool, "completed": bool}
        self.tasks = []

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "reward": self.reward,
            "status": self.status,
            "character_name": self.character_name,
            "character_file": self.character_file,
            "tasks": self.tasks
        }

    def from_dict(self, data):
        self.name = data.get("name", "")
        self.description = data.get("description", "")
        self.reward = data.get("reward", 0)
        self.status = data.get("status", "Active")
        self.character_name = data.get("character_name", "")
        self.character_file = data.get("character_file", "")
        self.tasks = data.get("tasks", [])

class RunDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Create New Run")
        self.configure(bg=BG_COLOR)
        self.resizable(False, False)
        self.grab_set()
        self.parent = parent
        self.run = None
        self.tasks = []
        self._build_ui()

    def _build_ui(self):
        main = tk.Frame(self, bg=BG_COLOR)
        main.pack(padx=10, pady=10)

        # Run Name
        tk.Label(main, text="Run Name:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.name_entry = tk.Entry(main, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=ENTRY_FG, width=40)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.name_entry.focus_set()

        # Reward
        tk.Label(main, text="Reward (¥):", bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.reward_entry = tk.Spinbox(main, from_=0, to=1000000, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=ENTRY_FG, width=10)
        self.reward_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)

        # Description
        tk.Label(main, text="Description:", bg=BG_COLOR, fg=FG_COLOR).grid(row=2, column=0, sticky="nw", padx=5, pady=5)
        self.desc_text = scrolledtext.ScrolledText(
            main, width=40, height=5, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=ENTRY_FG, wrap="word"
        )
        self.desc_text.grid(row=2, column=1, padx=5, pady=5)

        # Task Input
        tk.Label(main, text="Task Description:", bg=BG_COLOR, fg=FG_COLOR).grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.task_desc_entry = tk.Entry(main, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=ENTRY_FG, width=40)
        self.task_desc_entry.grid(row=3, column=1, padx=5, pady=5)

        self.mand_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            main, text="Mandatory", variable=self.mand_var,
            bg=BG_COLOR, fg=FG_COLOR,
            selectcolor=ENTRY_BG, activebackground=BG_COLOR, activeforeground=FG_COLOR
        ).grid(row=4, column=1, sticky="w", padx=5)

        tk.Button(
            main, text="Add Task", command=self._add_task,
            bg=BUTTON_BG, fg=BUTTON_FG,
            activebackground=BUTTON_ACTIVE_BG, activeforeground=BUTTON_ACTIVE_FG
        ).grid(row=4, column=1, sticky="e", padx=5, pady=5)

        # Tasks List
        tk.Label(main, text="Tasks:", bg=BG_COLOR, fg=FG_COLOR).grid(row=5, column=0, sticky="nw", padx=5, pady=5)
        tasks_frame = tk.Frame(main, bg=BG_COLOR)
        tasks_frame.grid(row=5, column=1, padx=5, pady=5, sticky="nsew")

        self.tasks_listbox = tk.Listbox(
            tasks_frame, width=50, height=6,
            bg=ENTRY_BG, fg=ENTRY_FG,
            selectbackground=BUTTON_ACTIVE_BG, activestyle="none"
        )
        self.tasks_listbox.pack(side="left", fill="both", expand=True)
        scrollbar = tk.Scrollbar(tasks_frame, orient="vertical", command=self.tasks_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.tasks_listbox.config(yscrollcommand=scrollbar.set)

        tk.Button(
            main, text="Remove Selected Task", command=self._remove_task,
            bg=BUTTON_BG, fg=BUTTON_FG,
            activebackground=BUTTON_ACTIVE_BG, activeforeground=BUTTON_ACTIVE_FG
        ).grid(row=6, column=1, sticky="e", padx=5, pady=5)

        # Action Buttons
        btn_frame = tk.Frame(main, bg=BG_COLOR)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=10)
        tk.Button(
            btn_frame, text="Create Run", command=self._on_ok,
            bg=BUTTON_BG, fg=BUTTON_FG,
            activebackground=BUTTON_ACTIVE_BG, activeforeground=BUTTON_ACTIVE_FG
        ).pack(side="left", padx=5)
        tk.Button(
            btn_frame, text="Cancel", command=self._on_cancel,
            bg=BUTTON_BG, fg=BUTTON_FG,
            activebackground=BUTTON_ACTIVE_BG, activeforeground=BUTTON_ACTIVE_FG
        ).pack(side="left", padx=5)

    def _add_task(self):
        desc = self.task_desc_entry.get().strip()
        if not desc:
            messagebox.showwarning("Warning", "Task description cannot be empty")
            return
        mand = self.mand_var.get()
        task = {"description": desc, "mandatory": mand, "completed": False}
        self.tasks.append(task)
        label = f"{desc} [{'M' if mand else 'O'}]"
        self.tasks_listbox.insert("end", label)
        self.task_desc_entry.delete(0, "end")

    def _remove_task(self):
        sel = self.tasks_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        self.tasks_listbox.delete(idx)
        del self.tasks[idx]

    def _on_ok(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Warning", "Run name cannot be empty")
            return
        try:
            reward = int(self.reward_entry.get())
        except ValueError:
            messagebox.showwarning("Warning", "Invalid reward value")
            return
        description = self.desc_text.get("1.0", "end").strip()
        run = ShadowrunRun(name, description, reward)
        for task in self.tasks:
            run.tasks.append(task.copy())
        self.run = run
        self.destroy()

    def _on_cancel(self):
        self.destroy()

class RunTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shadowrun 6E Run Tracker")
        self.root.configure(bg=BG_COLOR)
        self.runs = []
        self.current_character = None
        self.current_run = None

        # Progressbar style
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TProgressbar", troughcolor=ENTRY_BG, background="#4CAF50")

        # Layout
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=3)
        self.root.rowconfigure(0, weight=1)

        # Header: New/Import/Export + Character info
        header = tk.Frame(self.root, bg=BG_COLOR)
        header.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=(5, 0))
        header.columnconfigure(0, weight=1)
        header.columnconfigure(1, weight=1)
        btn_frame = tk.Frame(header, bg=BG_COLOR)
        btn_frame.grid(row=0, column=0, sticky="w")
        tk.Button(
            btn_frame, text="New Run", width=10, command=self.new_run,
            bg=BUTTON_BG, fg=BUTTON_FG,
            activebackground=BUTTON_ACTIVE_BG, activeforeground=BUTTON_ACTIVE_FG
        ).pack(side="left", padx=2)
        tk.Button(
            btn_frame, text="Import Runs", width=12, command=self.import_runs,
            bg=BUTTON_BG, fg=BUTTON_FG,
            activebackground=BUTTON_ACTIVE_BG, activeforeground=BUTTON_ACTIVE_FG
        ).pack(side="left", padx=2)
        tk.Button(
            btn_frame, text="Export Runs", width=12, command=self.export_runs,
            bg=BUTTON_BG, fg=BUTTON_FG,
            activebackground=BUTTON_ACTIVE_BG, activeforeground=BUTTON_ACTIVE_FG
        ).pack(side="left", padx=2)

        char_frame = tk.Frame(header, bg=BG_COLOR)
        char_frame.grid(row=0, column=1, sticky="e")
        self.char_label = tk.Label(
            char_frame, text="Character: None    Nuyen: 0¥",
            bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 10)
        )
        self.char_label.pack(side="left", padx=5)
        tk.Button(
            char_frame, text="Load Character", command=self.load_character,
            bg=BUTTON_BG, fg=BUTTON_FG,
            activebackground=BUTTON_ACTIVE_BG, activeforeground=BUTTON_ACTIVE_FG
        ).pack(side="left", padx=2)
        tk.Button(
            char_frame, text="Clear Character", command=self.clear_character,
            bg=BUTTON_BG, fg=BUTTON_FG,
            activebackground=BUTTON_ACTIVE_BG, activeforeground=BUTTON_ACTIVE_FG
        ).pack(side="left", padx=2)

        # Left panel: Runs list as Treeview
        left_frame = tk.Frame(self.root, bg=BG_COLOR)
        left_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        tk.Label(left_frame, text="Runs", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 12, "bold")).pack(anchor="w", padx=5, pady=(0,5))

        cols = ("Name", "Status", "Reward", "Character")
        self.run_tree = ttk.Treeview(
            left_frame, columns=cols, show="headings", height=15
        )
        for c in cols:
            self.run_tree.heading(c, text=c)
            self.run_tree.column(c, anchor="w")
        self.run_tree.pack(fill="both", expand=True)
        self.run_tree.bind("<<TreeviewSelect>>", self._on_run_select)

        # Right panel: Run details
        right_frame = tk.Frame(self.root, bg=BG_COLOR)
        right_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        right_frame.columnconfigure(0, weight=1)
        tk.Label(right_frame, text="Run Details", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=(0,5))

        detail_frame = tk.Frame(right_frame, bg=BG_COLOR)
        detail_frame.grid(row=1, column=0, sticky="nsew")

        # Header: Name & Status
        hdr = tk.Frame(detail_frame, bg=BG_COLOR)
        hdr.pack(fill="x", padx=5, pady=5)
        tk.Label(hdr, text="Name:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, sticky="w")
        self.detail_name = tk.Label(hdr, text="", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 10, "bold"))
        self.detail_name.grid(row=0, column=1, sticky="w", padx=5)
        tk.Label(hdr, text="Status:", bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=0, sticky="w", pady=(5,0))
        self.detail_status = tk.Label(hdr, text="", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 10, "bold"))
        self.detail_status.grid(row=1, column=1, sticky="w", padx=5, pady=(5,0))

        # Progress
        prog = tk.Frame(detail_frame, bg=BG_COLOR)
        prog.pack(fill="x", padx=5, pady=5)
        tk.Label(prog, text="Progress:", bg=BG_COLOR, fg=FG_COLOR).pack(side="left")
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(prog, variable=self.progress_var, maximum=100, length=200, style="TProgressbar")
        self.progress_bar.pack(side="left", padx=5)
        self.progress_lbl = tk.Label(prog, text="0%", bg=BG_COLOR, fg=FG_COLOR)
        self.progress_lbl.pack(side="left")

        # Description
        tk.Label(detail_frame, text="Description:", bg=BG_COLOR, fg=FG_COLOR).pack(anchor="w", padx=5)
        self.detail_desc = scrolledtext.ScrolledText(
            detail_frame, width=60, height=5,
            bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=ENTRY_FG, wrap="word"
        )
        self.detail_desc.pack(fill="x", padx=5, pady=5)
        self.detail_desc.config(state="disabled")

        # Tasks
        tk.Label(detail_frame, text="Tasks:", bg=BG_COLOR, fg=FG_COLOR).pack(anchor="w", padx=5)
        tasks_container = tk.Frame(detail_frame, bg=BG_COLOR)
        tasks_container.pack(fill="both", expand=True, padx=5, pady=5)

        self.tasks_canvas = tk.Canvas(tasks_container, bg=BG_COLOR, highlightthickness=0)
        self.tasks_canvas.pack(side="left", fill="both", expand=True)
        self.tasks_scrollbar = tk.Scrollbar(tasks_container, orient="vertical", command=self.tasks_canvas.yview)
        self.tasks_scrollbar.pack(side="right", fill="y")
        self.tasks_canvas.configure(yscrollcommand=self.tasks_scrollbar.set)
        self.tasks_inner = tk.Frame(self.tasks_canvas, bg=BG_COLOR)
        self.tasks_canvas.create_window((0,0), window=self.tasks_inner, anchor="nw")
        self.tasks_inner.bind("<Configure>", lambda e: self.tasks_canvas.configure(scrollregion=self.tasks_canvas.bbox("all")))

        # Reward display
        rc = tk.Frame(detail_frame, bg=BG_COLOR)
        rc.pack(fill="x", padx=5, pady=5)
        tk.Label(rc, text="Reward:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, sticky="w")
        self.detail_reward = tk.Label(rc, text="0¥", bg=BG_COLOR, fg=FG_COLOR, font=("Arial", 10, "bold"))
        self.detail_reward.grid(row=0, column=1, sticky="w", padx=5)
        tk.Label(rc, text="Character:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=2, sticky="w", padx=(20,0))
        self.detail_char = tk.Label(rc, text="None", bg=BG_COLOR, fg=FG_COLOR)
        self.detail_char.grid(row=0, column=3, sticky="w", padx=5)

        # Bottom action buttons
        bottom_btns = tk.Frame(self.root, bg=BG_COLOR)
        bottom_btns.grid(row=2, column=0, columnspan=2, pady=10)
        self.complete_btn = tk.Button(
            bottom_btns, text="Complete Run", command=self.complete_run, state="disabled",
            width=20,
            bg=BUTTON_BG, fg=BUTTON_FG,
            activebackground=BUTTON_ACTIVE_BG, activeforeground=BUTTON_ACTIVE_FG
        )
        self.complete_btn.pack(side="left", padx=50)
        self.abandon_btn = tk.Button(
            bottom_btns, text="Abandon Run", command=self.abandon_run, state="disabled",
            width=20,
            bg=BUTTON_BG, fg=BUTTON_FG,
            activebackground=BUTTON_ACTIVE_BG, activeforeground=BUTTON_ACTIVE_FG
        )
        self.abandon_btn.pack(side="left", padx=50)

        # Initial population
        self.update_run_list()

    def new_run(self):
        dlg = RunDialog(self.root)
        self.root.wait_window(dlg)
        if dlg.run:
            self.runs.append(dlg.run)
            self.update_run_list()

    def import_runs(self):
        path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")])
        if path and os.path.exists(path):
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                for rd in data:
                    run = ShadowrunRun()
                    run.from_dict(rd)
                    self.runs.append(run)
                self.update_run_list()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import runs: {e}")

    def export_runs(self):
        if not self.runs:
            messagebox.showwarning("Warning", "No runs to export")
            return
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")])
        if path:
            try:
                with open(path, "w") as f:
                    json.dump([r.to_dict() for r in self.runs], f, indent=2)
                messagebox.showinfo("Success", "Runs exported successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export runs: {e}")

    def update_run_list(self):
        for item in self.run_tree.get_children():
            self.run_tree.delete(item)
        for idx, run in enumerate(self.runs):
            # Choose which character to display
            if run.character_name:
                char_lbl = run.character_name
            elif self.current_character:
                char_lbl = self.current_character["name"]
            else:
                char_lbl = ""
            self.run_tree.insert(
                "", "end", iid=str(idx),
                values=(run.name, run.status, f"{run.reward}¥", char_lbl)
            )
        # Clear details display
        self.current_run = None
        self.clear_details()

    def _on_run_select(self, event):
        sel = self.run_tree.selection()
        if not sel:
            return
        idx = int(sel[0])
        self.current_run = self.runs[idx]
        self.update_details()

    def update_details(self):
        run = self.current_run
        if not run:
            return
        self.detail_name.config(text=run.name)
        self.detail_status.config(text=run.status)
        self.detail_reward.config(text=f"{run.reward}¥")

        # Character label: show assigned or loaded
        if run.character_name:
            char_lbl = run.character_name
        elif self.current_character:
            char_lbl = f"{self.current_character['name']} ({self.current_character['nuyen']}¥)"
        else:
            char_lbl = "None"
        self.detail_char.config(text=char_lbl)
        self.char_label.config(text=f"Character: {char_lbl}")

        # Description
        self.detail_desc.config(state="normal")
        self.detail_desc.delete("1.0", "end")
        self.detail_desc.insert("1.0", run.description)
        self.detail_desc.config(state="disabled")

        # Tasks
        self._refresh_tasks()

        # Buttons state
        self.abandon_btn.config(state="normal" if run.status == "Active" else "disabled")
        self.update_complete_button_state()

    def clear_details(self):
        self.detail_name.config(text="")
        self.detail_status.config(text="")
        self.detail_desc.config(state="normal")
        self.detail_desc.delete("1.0", "end")
        self.detail_desc.config(state="disabled")
        self._clear_tasks()
        self.abandon_btn.config(state="disabled")
        self.complete_btn.config(state="disabled")
        self.detail_reward.config(text="0¥")
        self.detail_char.config(text="None")
        self.progress_var.set(0)
        self.progress_lbl.config(text="0%")

    def _clear_tasks(self):
        for w in self.tasks_inner.winfo_children():
            w.destroy()

    def _refresh_tasks(self):
        self._clear_tasks()
        self.task_vars = []
        run = self.current_run
        if not run or not run.tasks:
            self._update_progress()
            return
        for task in run.tasks:
            completed = task.get("completed", False)
            var = tk.BooleanVar(value=completed)
            txt = task["description"] + (" *" if task.get("mandatory") else "")
            cb = tk.Checkbutton(
                self.tasks_inner, text=txt, variable=var,
                bg=BG_COLOR, fg=FG_COLOR,
                selectcolor=ENTRY_BG, activebackground=BG_COLOR, activeforeground=FG_COLOR,
                command=self._on_task_toggle
            )
            cb.pack(anchor="w", pady=2)
            # Disable if task already completed or run is not active
            if completed or run.status != "Active":
                cb.config(state="disabled")
            self.task_vars.append(var)
        self._update_progress()

    def _on_task_toggle(self):
        run = self.current_run
        if not run:
            return
        for i, var in enumerate(self.task_vars):
            run.tasks[i]["completed"] = var.get()
        self._update_progress()
        self.update_complete_button_state()

    def _update_progress(self):
        run = self.current_run
        if not run or not run.tasks:
            self.progress_var.set(0)
            self.progress_lbl.config(text="0%")
            return
        total = len(run.tasks)
        done = sum(1 for t in run.tasks if t.get("completed"))
        pct = int(done / total * 100)
        self.progress_var.set(pct)
        self.progress_lbl.config(text=f"{pct}%")

    def update_complete_button_state(self):
        run = self.current_run
        if not run or run.status != "Active" or not self.current_character:
            self.complete_btn.config(state="disabled")
            return
        # All mandatory tasks must be completed
        for t in run.tasks:
            if t.get("mandatory") and not t.get("completed"):
                self.complete_btn.config(state="disabled")
                return
        self.complete_btn.config(state="normal")

    def load_character(self):
        # Allow .sr6 extension as well as JSON
        path = filedialog.askopenfilename(
            filetypes=[("SR6 Files", "*.sr6"), ("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        if path:
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                self.current_character = {
                    "file": path,
                    "name": data.get("name", "Unknown"),
                    "nuyen": data.get("nuyen", 0)
                }
                if self.current_run:
                    self.current_run.character_file = path
                char_lbl = f"{self.current_character['name']} ({self.current_character['nuyen']}¥)"
                self.char_label.config(text=f"Character: {char_lbl}")
                self.detail_char.config(text=char_lbl)
                self.update_complete_button_state()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load character: {e}")

    def clear_character(self):
        self.current_character = None
        self.char_label.config(text="Character: None    Nuyen: 0¥")
        if self.current_run and self.current_run.character_name == "":
            self.detail_char.config(text="None")
        self.update_complete_button_state()

    def complete_run(self):
        run = self.current_run
        if not run or run.status != "Active":
            return
        if not self.current_character:
            messagebox.showwarning("Warning", "Load a character first")
            return
        total = len(run.tasks)
        if total > 0:
            done = sum(1 for t in run.tasks if t.get("completed"))
            reward_pct = done / total
            actual_reward = int(run.reward * reward_pct)
        else:
            actual_reward = run.reward

        run.status = "Completed"
        run.character_name = self.current_character["name"]
        run.character_file = self.current_character["file"]

        try:
            with open(self.current_character["file"], "r") as f:
                char_data = json.load(f)
            char_data["nuyen"] = char_data.get("nuyen", 0) + actual_reward
            with open(self.current_character["file"], "w") as f:
                json.dump(char_data, f, indent=2)
            self.current_character["nuyen"] = char_data["nuyen"]
            char_lbl = f"{self.current_character['name']} ({self.current_character['nuyen']}¥)"
            self.char_label.config(text=f"Character: {char_lbl}")
            self.detail_char.config(text=char_lbl)
            self.update_run_list()
            self.update_details()
            messagebox.showinfo("Run Completed", f"Completed! {actual_reward}¥ awarded")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update character: {e}")

    def abandon_run(self):
        run = self.current_run
        if not run or run.status != "Active":
            return
        if not messagebox.askyesno("Confirm", "Are you sure you want to abandon this run?"):
            return
        run.status = "Abandoned"
        self.update_run_list()
        self.update_details()
        messagebox.showinfo("Run Abandoned", "Run has been abandoned")

def main():
    root = tk.Tk()
    app = RunTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
