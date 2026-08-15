import tkinter as tk
from tkinter import ttk, messagebox
from student import Student
from student_manager import StudentManager
from validators import (
    validate_student_id, validate_age, validate_email,
    validate_phone, validate_cgpa, validate_semester, validate_required
)

class StudentManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Administration Dashboard")
        self.root.geometry("1200x750")
        self.root.minsize(1050, 650)

        # Initialize backend StudentManager
        try:
            self.manager = StudentManager()
        except Exception as e:
            messagebox.showerror("Database Connection Error", f"Failed to initialize Student Database: {e}")
            self.root.destroy()
            return

        # Setup Modern Color Palette & Typography Theme
        self.primary_color = "#1e293b"    # Slate Dark (Sidebar & Headers)
        self.accent_color = "#3b82f6"     # Modern Accent Blue (Buttons & Focus)
        self.accent_hover = "#2563eb"     # Deep Blue Accent
        self.bg_color = "#f8fafc"         # Slate Light background
        self.card_bg = "#ffffff"          # White cards
        self.text_dark = "#0f172a"        # Dark slate text
        self.text_muted = "#64748b"       # Muted gray text
        self.border_color = "#e2e8f0"     # Soft grey borders
        self.danger_color = "#ef4444"     # Soft Red for Delete operations
        
        self.root.configure(bg=self.bg_color)
        
        # Configure styles
        self.setup_styles()

        # Build UI layout structures
        self.create_layout()

        # Initialize views
        self.create_dashboard_view()
        self.create_add_student_view()
        self.create_view_students_view()
        self.create_search_filter_view()
        self.create_update_student_view()

        # Start on dashboard
        self.show_frame(self.dashboard_frame)

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Base Frame & Label styles
        self.style.configure(".", background=self.bg_color, foreground=self.text_dark, font=("Segoe UI", 10))
        self.style.configure("Card.TFrame", background=self.card_bg, relief="flat")
        
        # Modern Flat Entry Style
        self.style.configure("TEntry", fieldbackground="white", bordercolor=self.border_color, lightcolor=self.border_color, darkcolor=self.border_color)
        self.style.configure("TCombobox", fieldbackground="white", bordercolor=self.border_color, lightcolor=self.border_color, darkcolor=self.border_color)
        
        # Heading styles
        self.style.configure("DashboardTitle.TLabel", font=("Segoe UI", 20, "bold"), foreground=self.primary_color, background=self.bg_color)
        self.style.configure("DashboardSubtitle.TLabel", font=("Segoe UI", 10), foreground=self.text_muted, background=self.bg_color)
        self.style.configure("SectionHeader.TLabel", font=("Segoe UI", 14, "bold"), foreground=self.primary_color, background=self.bg_color)
        
        # Card Labels
        self.style.configure("CardTitle.TLabel", font=("Segoe UI", 9, "bold"), foreground=self.text_muted, background=self.card_bg)
        self.style.configure("CardValue.TLabel", font=("Segoe UI", 20, "bold"), foreground=self.primary_color, background=self.card_bg)

        # Buttons configurations
        self.style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"), background=self.accent_color, foreground="white", borderwidth=0, focuscolor=self.accent_hover)
        self.style.map("Primary.TButton", background=[("active", self.accent_hover)])

        self.style.configure("Secondary.TButton", font=("Segoe UI", 10, "bold"), background="#e2e8f0", foreground=self.text_dark, borderwidth=0)
        self.style.map("Secondary.TButton", background=[("active", "#cbd5e1")])

        self.style.configure("Danger.TButton", font=("Segoe UI", 10, "bold"), background=self.danger_color, foreground="white", borderwidth=0)
        self.style.map("Danger.TButton", background=[("active", "#dc2626")])

        # Modern Treeview Styling
        self.style.configure("Treeview", font=("Segoe UI", 10), rowheight=32, background="white", fieldbackground="white", bordercolor=self.border_color, borderwidth=1)
        self.style.map("Treeview", background=[("selected", self.accent_color)], foreground=[("selected", "white")])
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background=self.primary_color, foreground="white", relief="flat")
        self.style.map("Treeview.Heading", background=[("active", self.primary_color)])

    def create_layout(self):
        # Sidebar Frame
        self.sidebar = tk.Frame(self.root, bg=self.primary_color, width=240)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo and Title in Sidebar
        logo_container = tk.Frame(self.sidebar, bg=self.primary_color, height=80)
        logo_container.pack(fill="x", pady=(20, 10))
        
        tk.Label(logo_container, text="SMS ADMIN", fg="white", bg=self.primary_color, font=("Segoe UI", 16, "bold")).pack(anchor="w", padx=25)
        tk.Label(logo_container, text="Academic Portal v2.0", fg=self.accent_color, bg=self.primary_color, font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=25)

        # Sidebar Menu Separator
        separator = tk.Frame(self.sidebar, bg="#334155", height=1)
        separator.pack(fill="x", padx=20, pady=10)

        # Navigation Buttons mapping
        self.menu_buttons = {}
        menu_items = [
            ("Dashboard", "dashboard", lambda: self.show_frame(self.dashboard_frame)),
            ("Register Student", "add", lambda: self.show_frame(self.add_frame)),
            ("All Students Database", "view", lambda: self.show_frame(self.view_frame)),
            ("Advanced Filters", "filter", lambda: self.show_frame(self.filter_frame)),
            ("Update Student Profile", "update", lambda: self.show_frame(self.update_frame)),
            ("Delete Student Record", "delete", self.trigger_sidebar_delete)
        ]

        for name, key, cmd in menu_items:
            btn = tk.Button(
                self.sidebar, text=f"  {name}", command=cmd, bg=self.primary_color, fg="#94a3b8",
                activebackground="#334155", activeforeground="white", bd=0, anchor="w",
                font=("Segoe UI", 10, "bold"), height=2, cursor="hand2", padx=20
            )
            btn.pack(fill="x", pady=2, padx=10)
            self.menu_buttons[key] = btn

        # Exit Button at Sidebar Bottom
        exit_btn = tk.Button(
            self.sidebar, text="  Exit Application", command=self.root.quit, bg=self.primary_color, fg="#f87171",
            activebackground="#334155", activeforeground="#f87171", bd=0, anchor="w",
            font=("Segoe UI", 10, "bold"), height=2, cursor="hand2", padx=20
        )
        exit_btn.pack(side="bottom", fill="x", pady=20, padx=10)

        # Main Layout: Top Header + Content Area
        self.main_workarea = tk.Frame(self.root, bg=self.bg_color)
        self.main_workarea.pack(side="right", fill="both", expand=True)

        # Header Frame
        self.header_bar = tk.Frame(self.main_workarea, bg="white", height=70, bd=1, relief="flat")
        self.header_bar.pack(side="top", fill="x")
        self.header_bar.pack_propagate(False)

        # Bottom border on Header Frame
        hdr_border = tk.Frame(self.header_bar, bg=self.border_color, height=1)
        hdr_border.pack(side="bottom", fill="x")

        # Dynamic Header Titles
        self.header_title = ttk.Label(self.header_bar, text="Dashboard", font=("Segoe UI", 15, "bold"), background="white", foreground=self.primary_color)
        self.header_title.pack(side="left", padx=25, pady=(15, 0))

        # Content frame container
        self.content_container = tk.Frame(self.main_workarea, bg=self.bg_color)
        self.content_container.pack(fill="both", expand=True, padx=25, pady=25)

        self.frames = []

    def show_frame(self, frame_to_show):
        for f in self.frames:
            f.pack_forget()
        frame_to_show.pack(fill="both", expand=True)

        # Update sidebar visual selection
        for key, btn in self.menu_buttons.items():
            if (frame_to_show == self.dashboard_frame and key == "dashboard") or \
               (frame_to_show == self.add_frame and key == "add") or \
               (frame_to_show == self.view_frame and key == "view") or \
               (frame_to_show == self.filter_frame and key == "filter") or \
               (frame_to_show == self.update_frame and key == "update"):
                btn.config(bg="#334155", fg="white")
            else:
                btn.config(bg=self.primary_color, fg="#94a3b8")

        # Sync Header Titles
        titles = {
            self.dashboard_frame: ("Admin Control Panel", "Overall system stats & shortcuts"),
            self.add_frame: ("Register Student", "Insert a new profile record into the database"),
            self.view_frame: ("All Students Database", "View, edit, refresh and delete records"),
            self.filter_frame: ("Advanced Filter Engine", "Query specific students using custom filter combinations"),
            self.update_frame: ("Update Student Profile", "Modify student information accurately")
        }

        if frame_to_show in titles:
            title_text, subtitle_text = titles[frame_to_show]
            self.header_title.config(text=title_text)

        # Auto-refresh logic on view change
        if frame_to_show == self.dashboard_frame:
            self.update_dashboard_stats()
        elif frame_to_show == self.view_frame:
            self.refresh_all_students_table()
        elif frame_to_show == self.filter_frame:
            self.refresh_filter_table()

    def trigger_sidebar_delete(self):
        # Redirect user to view table screen to select row to delete
        self.show_frame(self.view_frame)
        messagebox.showinfo("Action Required", "Please select a student from the database table below and click 'Delete Selected' to remove their profile.")

    # ==================== VIEW 1: DASHBOARD ====================
    def create_dashboard_view(self):
        self.dashboard_frame = tk.Frame(self.content_container, bg=self.bg_color)
        self.frames.append(self.dashboard_frame)

        # Stats Cards Grid Frame
        stats_grid = tk.Frame(self.dashboard_frame, bg=self.bg_color)
        stats_grid.pack(fill="x", pady=(0, 25))

        # Card definitions
        self.cards_data = [
            ("Total Students", "stat_total", self.accent_color),
            ("Average CGPA", "stat_avg_cgpa", "#10b981"),
            ("Courses Registered", "stat_courses", "#f59e0b"),
            ("Active Branches", "stat_branches", "#8b5cf6")
        ]

        self.stat_labels = {}
        for idx, (label_text, key, accent) in enumerate(self.cards_data):
            card = tk.Frame(stats_grid, bg="white", bd=1, relief="flat", highlightbackground=self.border_color, highlightthickness=1)
            card.pack(side="left", fill="both", expand=True, padx=(0 if idx == 0 else 15, 0))
            card.pack_propagate(False)
            card.config(height=110)

            # Left accent highlight stripe
            stripe = tk.Frame(card, bg=accent, width=4)
            stripe.pack(side="left", fill="y")

            container = tk.Frame(card, bg="white")
            container.pack(fill="both", expand=True, padx=15, pady=15)

            ttk.Label(container, text=label_text.upper(), style="CardTitle.TLabel").pack(anchor="w")
            val_lbl = ttk.Label(container, text="0", style="CardValue.TLabel")
            val_lbl.pack(anchor="w", pady=(5, 0))
            self.stat_labels[key] = val_lbl

        # Main Layout: 2 Columns (Quick Actions Shortcuts | Recent System Activity Log)
        action_activity_frame = tk.Frame(self.dashboard_frame, bg=self.bg_color)
        action_activity_frame.pack(fill="both", expand=True)

        action_activity_frame.columnconfigure(0, weight=1)
        action_activity_frame.columnconfigure(1, weight=1)

        # Left Column - Quick Actions Card
        qa_card = tk.Frame(action_activity_frame, bg="white", bd=1, relief="flat", highlightbackground=self.border_color, highlightthickness=1)
        qa_card.grid(row=0, column=0, sticky="nsew", padx=(0, 15))

        tk.Label(qa_card, text="Quick Shortcuts Menu", bg="white", fg=self.primary_color, font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=20, pady=(20, 15))

        shortcuts = [
            ("Register New Student", lambda: self.show_frame(self.add_frame), "Add new student details with validation"),
            ("View Detailed Database", lambda: self.show_frame(self.view_frame), "List all profiles, edit information & delete rows"),
            ("Advanced Query Filters", lambda: self.show_frame(self.filter_frame), "Search using conditional semester, CGPA, or branch fields")
        ]

        for title, cmd, desc in shortcuts:
            item_frame = tk.Frame(qa_card, bg="white", cursor="hand2")
            item_frame.pack(fill="x", padx=20, pady=8)
            item_frame.bind("<Button-1>", lambda e, c=cmd: c())

            btn_lbl = tk.Label(item_frame, text=title, fg=self.accent_color, bg="white", font=("Segoe UI", 10, "bold"), anchor="w")
            btn_lbl.pack(fill="x")
            btn_lbl.bind("<Button-1>", lambda e, c=cmd: c())

            desc_lbl = tk.Label(item_frame, text=desc, fg=self.text_muted, bg="white", font=("Segoe UI", 9), anchor="w")
            desc_lbl.pack(fill="x")
            desc_lbl.bind("<Button-1>", lambda e, c=cmd: c())

            sep = tk.Frame(qa_card, bg=self.border_color, height=1)
            sep.pack(fill="x", padx=20, pady=5)

        # Right Column - About Project Details Card
        about_card = tk.Frame(action_activity_frame, bg="white", bd=1, relief="flat", highlightbackground=self.border_color, highlightthickness=1)
        about_card.grid(row=0, column=1, sticky="nsew")

        tk.Label(about_card, text="System Information", bg="white", fg=self.primary_color, font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=20, pady=(20, 15))

        # Project Summary Details
        info_lines = [
            ("Project Context:", "Python Internship Showcase / College Project"),
            ("Database Engine:", "Local JSON file (data/students.json)"),
            ("Backend Architecture:", "Object-Oriented Programming (OOP) MVC Layout"),
            ("Design Aesthetics:", "Modern Slate UI styled with ttk & Tkinter elements"),
            ("Validation Layer:", "Real-time regex formats validation for emails, phone & ID")
        ]

        for lbl, val in info_lines:
            row = tk.Frame(about_card, bg="white")
            row.pack(fill="x", padx=20, pady=6)
            tk.Label(row, text=lbl, bg="white", fg=self.text_muted, font=("Segoe UI", 9, "bold"), width=20, anchor="w").pack(side="left")
            tk.Label(row, text=val, bg="white", fg=self.text_dark, font=("Segoe UI", 9), anchor="w").pack(side="left", fill="x", expand=True)

    def update_dashboard_stats(self):
        students = self.manager.get_all_students()
        total = len(students)
        self.stat_labels["stat_total"].config(text=str(total))
        
        # Calculate stats
        if total > 0:
            avg_cgpa = sum(s.cgpa for s in students) / total
            courses = len(set(s.course.strip().upper() for s in students if s.course))
            branches = len(set(s.branch.strip().upper() for s in students if s.branch))
            
            self.stat_labels["stat_avg_cgpa"].config(text=f"{avg_cgpa:.2f}")
            self.stat_labels["stat_courses"].config(text=str(courses))
            self.stat_labels["stat_branches"].config(text=str(branches))
        else:
            self.stat_labels["stat_avg_cgpa"].config(text="0.00")
            self.stat_labels["stat_courses"].config(text="0")
            self.stat_labels["stat_branches"].config(text="0")

    # ==================== VIEW 2: ADD STUDENT ====================
    def create_add_student_view(self):
        self.add_frame = tk.Frame(self.content_container, bg=self.bg_color)
        self.frames.append(self.add_frame)

        # Outer Form Card
        form_card = tk.Frame(self.add_frame, bg="white", bd=1, relief="flat", highlightbackground=self.border_color, highlightthickness=1)
        form_card.pack(fill="both", expand=True, padx=5, pady=5)

        # Internal container for padding
        container = tk.Frame(form_card, bg="white")
        container.pack(fill="both", expand=True, padx=30, pady=25)

        tk.Label(container, text="Student Enrollment Profile Details", bg="white", fg=self.primary_color, font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 20))

        # Split form fields into 2 grid columns
        grid_frame = tk.Frame(container, bg="white")
        grid_frame.pack(fill="x")
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)

        # Left Column - Academic Box
        left_box = tk.LabelFrame(grid_frame, text="Academic Information", font=("Segoe UI", 9, "bold"), bg="white", padx=15, pady=15, bd=1, relief="solid", fg=self.text_muted)
        left_box.grid(row=0, column=0, sticky="nsew", padx=(0, 15))

        self.add_fields = {}
        acad_fields = [
            ("Student ID (Unique Alphanumeric)", "student_id"),
            ("Course (e.g. B.Tech, M.Tech)", "course"),
            ("Branch (e.g. CSE, ECE, ME)", "branch"),
            ("Current Semester", "semester"),
            ("CGPA / Marks (0.0 - 10.0)", "cgpa")
        ]
        self.build_fields_grid(left_box, acad_fields)

        # Right Column - Personal Info Box
        right_box = tk.LabelFrame(grid_frame, text="Personal details", font=("Segoe UI", 9, "bold"), bg="white", padx=15, pady=15, bd=1, relief="solid", fg=self.text_muted)
        right_box.grid(row=0, column=1, sticky="nsew")

        pers_fields = [
            ("Full Name", "name"),
            ("Age", "age"),
            ("Gender", "gender"),
            ("Email Address", "email"),
            ("Phone Number", "phone"),
            ("Contact Address", "address")
        ]
        self.build_fields_grid(right_box, pers_fields)

        # Action Buttons
        btn_frame = tk.Frame(container, bg="white")
        btn_frame.pack(fill="x", pady=(30, 0))

        submit_btn = ttk.Button(btn_frame, text="Register Student Profile", style="Primary.TButton", command=self.submit_new_student, width=25)
        submit_btn.pack(side="left", padx=(0, 15))

        clear_btn = ttk.Button(btn_frame, text="Clear Form", style="Secondary.TButton", command=self.clear_add_form, width=15)
        clear_btn.pack(side="left", padx=15)

    def build_fields_grid(self, container, fields_list):
        for idx, (label_text, key) in enumerate(fields_list):
            tk.Label(container, text=label_text, bg="white", fg=self.text_dark, font=("Segoe UI", 9)).grid(row=idx*2, column=0, sticky="w", pady=(8, 2))
            
            # Widget creation with clean borders
            if key == "gender":
                entry = ttk.Combobox(container, values=["Male", "Female", "Other"], state="readonly")
            elif key == "semester":
                entry = ttk.Combobox(container, values=[str(i) for i in range(1, 9)], state="readonly")
            else:
                entry = ttk.Entry(container)

            entry.grid(row=idx*2 + 1, column=0, sticky="ew", pady=(0, 8))
            container.columnconfigure(0, weight=1)
            self.add_fields[key] = entry

    def clear_add_form(self):
        for entry in self.add_fields.values():
            if isinstance(entry, ttk.Combobox):
                entry.set("")
            else:
                entry.delete(0, tk.END)

    def submit_new_student(self):
        data = {k: v.get().strip() for k, v in self.add_fields.items()}
        
        # Validation checks
        for field, val in data.items():
            if not val:
                messagebox.showerror("Validation Error", f"Field '{field.replace('_', ' ').title()}' is required.")
                return

        try:
            # Backend validators run
            val_id = validate_student_id(data["student_id"])
            val_age = validate_age(data["age"])
            val_email = validate_email(data["email"])
            val_phone = validate_phone(data["phone"])
            val_semester = validate_semester(data["semester"])
            val_cgpa = validate_cgpa(data["cgpa"])

            if self.manager.search_by_id(val_id):
                messagebox.showerror("Validation Error", f"Duplicate Student ID: A student record with ID '{val_id}' already exists.")
                return

            new_student = Student(
                student_id=val_id, name=data["name"], age=val_age, gender=data["gender"],
                course=data["course"], branch=data["branch"], semester=val_semester,
                email=val_email, phone=val_phone, address=data["address"], cgpa=val_cgpa
            )

            self.manager.add_student(new_student)
            messagebox.showinfo("Success", f"Student profile for '{new_student.name}' registered successfully.")
            self.clear_add_form()
            self.show_frame(self.view_frame)
        except ValueError as e:
            messagebox.showerror("Validation Error", f"{e}")

    # ==================== VIEW 3: VIEW & EDIT ALL STUDENTS ====================
    def create_view_students_view(self):
        self.view_frame = tk.Frame(self.content_container, bg=self.bg_color)
        self.frames.append(self.view_frame)

        # Top search / refresh control bar
        control_card = tk.Frame(self.view_frame, bg="white", bd=1, relief="flat", highlightbackground=self.border_color, highlightthickness=1)
        control_card.pack(fill="x", pady=(0, 15))

        ctrl_container = tk.Frame(control_card, bg="white")
        ctrl_container.pack(fill="x", padx=20, pady=12)

        # Quick Search Box inside control card
        tk.Label(ctrl_container, text="Quick Search (ID / Name):", bg="white", fg=self.text_muted, font=("Segoe UI", 9, "bold")).pack(side="left")
        self.view_search_entry = ttk.Entry(ctrl_container, width=25)
        self.view_search_entry.pack(side="left", padx=10)
        self.view_search_entry.bind("<KeyRelease>", lambda e: self.run_view_quick_search())

        refresh_btn = ttk.Button(ctrl_container, text="Refresh Database", style="Secondary.TButton", command=self.refresh_all_students_table)
        refresh_btn.pack(side="right")

        # Treeview frame card
        table_card = tk.Frame(self.view_frame, bg="white", bd=1, relief="flat", highlightbackground=self.border_color, highlightthickness=1)
        table_card.pack(fill="both", expand=True)

        self.view_table_container, self.view_table = self.create_treeview_widget(table_card)
        self.view_table_container.pack(fill="both", expand=True, padx=15, pady=15)

        # Context action bar under the table
        action_bar = tk.Frame(self.view_frame, bg=self.bg_color)
        action_bar.pack(fill="x", pady=(15, 0))

        edit_btn = ttk.Button(action_bar, text="Update Selected Student", style="Primary.TButton", command=self.edit_selected_student)
        edit_btn.pack(side="left", padx=(0, 15))

        delete_btn = ttk.Button(action_bar, text="Delete Student Record", style="Danger.TButton", command=self.delete_selected_student)
        delete_btn.pack(side="left")

    def run_view_quick_search(self):
        query = self.view_search_entry.get().strip().lower()
        students = self.manager.get_all_students()
        if query:
            filtered = [
                s for s in students if query in s.student_id.lower() or query in s.name.lower()
            ]
            self.populate_table(self.view_table, filtered)
        else:
            self.populate_table(self.view_table, students)

    def refresh_all_students_table(self):
        self.manager.load_students()
        students = self.manager.get_all_students()
        self.populate_table(self.view_table, students)

    def edit_selected_student(self):
        selected = self.view_table.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a student row from the table first.")
            return

        student_id = self.view_table.item(selected, "values")[0]
        self.show_frame(self.update_frame)
        self.update_search_id_entry.delete(0, tk.END)
        self.update_search_id_entry.insert(0, student_id)
        self.load_student_for_update()

    def delete_selected_student(self):
        selected = self.view_table.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a student row to delete.")
            return

        vals = self.view_table.item(selected, "values")
        student_id = vals[0]
        name = vals[1]

        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete this student record permanently?\n\nID: {student_id}\nName: {name}")
        if confirm:
            if self.manager.delete_student(student_id):
                messagebox.showinfo("Success", f"Student '{name}' has been deleted from database.")
                self.refresh_all_students_table()
            else:
                messagebox.showerror("Error", "Could not delete student record.")

    # ==================== VIEW 4: SEARCH & FILTER ENGINE ====================
    def create_search_filter_view(self):
        self.filter_frame = tk.Frame(self.content_container, bg=self.bg_color)
        self.frames.append(self.filter_frame)

        # Filters panel card
        filter_card = tk.Frame(self.filter_frame, bg="white", bd=1, relief="flat", highlightbackground=self.border_color, highlightthickness=1)
        filter_card.pack(fill="x", pady=(0, 15))

        container = tk.Frame(filter_card, bg="white")
        container.pack(fill="x", padx=20, pady=15)

        # Form Layout split inside container
        row1 = tk.Frame(container, bg="white")
        row1.pack(fill="x", pady=5)

        tk.Label(row1, text="Branch:", bg="white", fg=self.text_muted, font=("Segoe UI", 9, "bold")).pack(side="left")
        self.filter_branch = ttk.Entry(row1, width=15)
        self.filter_branch.pack(side="left", padx=(10, 20))

        tk.Label(row1, text="Course:", bg="white", fg=self.text_muted, font=("Segoe UI", 9, "bold")).pack(side="left")
        self.filter_course = ttk.Entry(row1, width=15)
        self.filter_course.pack(side="left", padx=(10, 20))

        tk.Label(row1, text="Semester:", bg="white", fg=self.text_muted, font=("Segoe UI", 9, "bold")).pack(side="left")
        self.filter_sem = ttk.Combobox(row1, values=[""] + [str(i) for i in range(1, 9)], state="readonly", width=8)
        self.filter_sem.pack(side="left", padx=(10, 20))

        row2 = tk.Frame(container, bg="white")
        row2.pack(fill="x", pady=(10, 5))

        tk.Label(row2, text="Min CGPA:", bg="white", fg=self.text_muted, font=("Segoe UI", 9, "bold")).pack(side="left")
        self.filter_min_cgpa = ttk.Entry(row2, width=10)
        self.filter_min_cgpa.pack(side="left", padx=(10, 20))

        tk.Label(row2, text="Max CGPA:", bg="white", fg=self.text_muted, font=("Segoe UI", 9, "bold")).pack(side="left")
        self.filter_max_cgpa = ttk.Entry(row2, width=10)
        self.filter_max_cgpa.pack(side="left", padx=(10, 20))

        # Query buttons
        apply_btn = ttk.Button(row2, text="Filter Results", style="Primary.TButton", command=self.refresh_filter_table, width=18)
        apply_btn.pack(side="left", padx=(20, 10))

        reset_btn = ttk.Button(row2, text="Reset Filters", style="Secondary.TButton", command=self.reset_filter_inputs, width=15)
        reset_btn.pack(side="left")

        # Result Table Card
        table_card = tk.Frame(self.filter_frame, bg="white", bd=1, relief="flat", highlightbackground=self.border_color, highlightthickness=1)
        table_card.pack(fill="both", expand=True)

        self.filter_table_container, self.filter_table = self.create_treeview_widget(table_card)
        self.filter_table_container.pack(fill="both", expand=True, padx=15, pady=15)

    def reset_filter_inputs(self):
        self.filter_branch.delete(0, tk.END)
        self.filter_course.delete(0, tk.END)
        self.filter_sem.set("")
        self.filter_min_cgpa.delete(0, tk.END)
        self.filter_max_cgpa.delete(0, tk.END)
        self.refresh_filter_table()

    def refresh_filter_table(self):
        branch = self.filter_branch.get().strip() or None
        course = self.filter_course.get().strip() or None
        sem = self.filter_sem.get() or None
        min_cgpa = self.filter_min_cgpa.get().strip() or None
        max_cgpa = self.filter_max_cgpa.get().strip() or None

        students = self.manager.filter_students(
            branch=branch, course=course, semester=sem, min_cgpa=min_cgpa, max_cgpa=max_cgpa
        )
        self.populate_table(self.filter_table, students)

    # ==================== VIEW 5: UPDATE STUDENT PROFILE ====================
    def create_update_student_view(self):
        self.update_frame = tk.Frame(self.content_container, bg=self.bg_color)
        self.frames.append(self.update_frame)

        # Form card
        update_card = tk.Frame(self.update_frame, bg="white", bd=1, relief="flat", highlightbackground=self.border_color, highlightthickness=1)
        update_card.pack(fill="both", expand=True, padx=5, pady=5)

        container = tk.Frame(update_card, bg="white")
        container.pack(fill="both", expand=True, padx=30, pady=25)

        # Search / Load Header Box
        search_row = tk.Frame(container, bg="white")
        search_row.pack(fill="x", pady=(0, 20))

        tk.Label(search_row, text="Enter Student ID to update:", bg="white", fg=self.primary_color, font=("Segoe UI", 10, "bold")).pack(side="left")
        self.update_search_id_entry = ttk.Entry(search_row, width=20)
        self.update_search_id_entry.pack(side="left", padx=10)

        load_btn = ttk.Button(search_row, text="Fetch Details", style="Primary.TButton", command=self.load_student_for_update)
        load_btn.pack(side="left")

        # Form fields area
        self.update_form_grid = tk.Frame(container, bg="white")
        self.update_form_grid.pack(fill="x")
        self.update_form_grid.columnconfigure(0, weight=1)
        self.update_form_grid.columnconfigure(1, weight=1)

        # Fields split
        self.update_fields = {}
        left_box = tk.LabelFrame(self.update_form_grid, text="Academic details", font=("Segoe UI", 9, "bold"), bg="white", padx=15, pady=15, bd=1, relief="solid", fg=self.text_muted)
        left_box.grid(row=0, column=0, sticky="nsew", padx=(0, 15))

        acad_fields = [
            ("Course", "course"), ("Branch", "branch"), ("Semester", "semester"), ("CGPA / Marks", "cgpa")
        ]
        self.build_update_fields_grid(left_box, acad_fields)

        right_box = tk.LabelFrame(self.update_form_grid, text="Personal Details", font=("Segoe UI", 9, "bold"), bg="white", padx=15, pady=15, bd=1, relief="solid", fg=self.text_muted)
        right_box.grid(row=0, column=1, sticky="nsew")

        pers_fields = [
            ("Full Name", "name"), ("Age", "age"), ("Gender", "gender"),
            ("Email Address", "email"), ("Phone Number", "phone"), ("Address", "address")
        ]
        self.build_update_fields_grid(right_box, pers_fields)

        # Apply Modifications Button
        btn_row = tk.Frame(container, bg="white")
        btn_row.pack(fill="x", pady=(30, 0))

        apply_btn = ttk.Button(btn_row, text="Apply Info Modifications", style="Primary.TButton", command=self.apply_student_updates, width=25)
        apply_btn.pack(side="left")

    def build_update_fields_grid(self, container, fields_list):
        for idx, (lbl_txt, key) in enumerate(fields_list):
            tk.Label(container, text=lbl_txt, bg="white", fg=self.text_dark, font=("Segoe UI", 9)).grid(row=idx*2, column=0, sticky="w", pady=(8, 2))
            
            if key == "gender":
                entry = ttk.Combobox(container, values=["Male", "Female", "Other"], state="readonly")
            elif key == "semester":
                entry = ttk.Combobox(container, values=[str(i) for i in range(1, 9)], state="readonly")
            else:
                entry = ttk.Entry(container)

            entry.grid(row=idx*2 + 1, column=0, sticky="ew", pady=(0, 8))
            container.columnconfigure(0, weight=1)
            self.update_fields[key] = entry

    def load_student_for_update(self):
        s_id = self.update_search_id_entry.get().strip()
        if not s_id:
            messagebox.showwarning("Warning", "Please enter a Student ID to fetch.")
            return

        student = self.manager.search_by_id(s_id)
        if not student:
            messagebox.showerror("Error", f"Student with ID '{s_id}' not found.")
            return

        for key, entry in self.update_fields.items():
            val = getattr(student, key)
            if isinstance(entry, ttk.Combobox):
                entry.set(str(val))
            else:
                entry.delete(0, tk.END)
                entry.insert(0, str(val))

    def apply_student_updates(self):
        s_id = self.update_search_id_entry.get().strip()
        if not s_id:
            messagebox.showwarning("Warning", "Please fetch a student record first.")
            return

        student = self.manager.search_by_id(s_id)
        if not student:
            messagebox.showerror("Error", "Selected student record not found in the database.")
            return

        updates = {k: v.get().strip() for k, v in self.update_fields.items()}

        try:
            # Backend validators run
            if updates.get("email"):
                validate_email(updates["email"])
            if updates.get("phone"):
                validate_phone(updates["phone"])
            if updates.get("cgpa"):
                validate_cgpa(updates["cgpa"])
            if updates.get("age"):
                validate_age(updates["age"])
            if updates.get("semester"):
                validate_semester(updates["semester"])

            self.manager.update_student(s_id, **updates)
            messagebox.showinfo("Success", f"Information for student '{student.name}' updated successfully.")
            self.show_frame(self.view_frame)
        except ValueError as e:
            messagebox.showerror("Validation Error", f"{e}")

    # ==================== UTILITY: TABLE WIDGET CREATOR ====================
    def create_treeview_widget(self, parent_frame):
        container = tk.Frame(parent_frame, bg="white")
        
        columns = ("id", "name", "course", "branch", "semester", "email", "phone", "cgpa")
        tree = ttk.Treeview(container, columns=columns, show="headings", selectmode="browse")

        col_configs = {
            "id": ("Student ID", 100),
            "name": ("Full Name", 140),
            "course": ("Course", 90),
            "branch": ("Branch", 90),
            "semester": ("Sem", 60),
            "email": ("Email Address", 160),
            "phone": ("Phone", 110),
            "cgpa": ("CGPA", 70)
        }

        for col, config in col_configs.items():
            tree.heading(col, text=config[0])
            tree.column(col, width=config[1], anchor="center" if col in ("id", "semester", "cgpa") else "w")

        # Custom scrollbars style
        vsb = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(container, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        container.columnconfigure(0, weight=1)
        container.rowconfigure(0, weight=1)
        return container, tree

    def populate_table(self, table_widget, students_list):
        for item in table_widget.get_children():
            table_widget.delete(item)

        for s in students_list:
            table_widget.insert("", "end", values=(
                s.student_id, s.name, s.course, s.branch, s.semester, s.email, s.phone, f"{s.cgpa:.2f}"
            ))

def main():
    root = tk.Tk()
    app = StudentManagementGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
