import os
import tkinter as tk
from tkinter import ttk, messagebox
import utils
import student_manager
import file_handler

class StudentRecordApp(tk.Tk):
    def __init__(self, students, db_path):
        super().__init__()
        
        self.students = students
        self.db_path = db_path
        
        self.title("Student Record Management System")
        self.geometry("1100x680")
        self.configure(bg="#1a1a24")
        
        # Make the window responsive
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Custom Styling
        self.setup_styles()
        
        # Create Layout
        self.create_sidebar()
        self.create_main_container()
        
        # Show Dashboard by default
        self.show_page("dashboard")

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Configure overall widget styling
        self.style.configure(".", background="#1a1a24", foreground="#e0e0e0")
        
        # Treeview styling (Dynamic Student Table)
        self.style.configure("Treeview", 
                             background="#222232", 
                             foreground="#e0e0e0", 
                             fieldbackground="#222232", 
                             rowheight=35,
                             font=("Segoe UI", 11),
                             borderwidth=0)
        self.style.map("Treeview", 
                       background=[("selected", "#5c6bc0")], 
                       foreground=[("selected", "#ffffff")])
        
        self.style.configure("Treeview.Heading", 
                             background="#2e2e42", 
                             foreground="#ffffff", 
                             font=("Segoe UI", 11, "bold"),
                             borderwidth=1, 
                             relief="flat")
        self.style.map("Treeview.Heading",
                       background=[("active", "#3f3f5a")])

        # Scrollbar styling
        self.style.configure("Vertical.TScrollbar", 
                             gripcount=0, 
                             background="#2e2e42", 
                             troughcolor="#1a1a24", 
                             bordercolor="#1a1a24",
                             arrowcolor="#ffffff",
                             lightcolor="#2e2e42", 
                             darkcolor="#2e2e42")

    def create_sidebar(self):
        sidebar = tk.Frame(self, bg="#13131a", width=220)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        
        # Sidebar Title
        title_label = tk.Label(sidebar, text="SRMS Portal", bg="#13131a", fg="#ffffff", font=("Segoe UI", 16, "bold"))
        title_label.pack(pady=30, padx=20, anchor="w")
        
        # Divider Line
        divider = tk.Frame(sidebar, height=1, bg="#2e2e3a")
        divider.pack(fill="x", padx=20, pady=(0, 20))
        
        # Sidebar buttons
        self.sidebar_buttons = {}
        menu_items = [
            ("dashboard", "📊 Dashboard"),
            ("directory", "👥 Directory"),
            ("add_student", "➕ Add Record")
        ]
        
        for page_id, text in menu_items:
            btn = tk.Button(sidebar, text=text, font=("Segoe UI", 12), anchor="w",
                            bg="#13131a", fg="#8888aa", activebackground="#222232", activeforeground="#ffffff",
                            bd=0, padx=20, pady=10, cursor="hand2",
                            command=lambda p=page_id: self.show_page(p))
            btn.pack(fill="x", padx=10, pady=5)
            self.sidebar_buttons[page_id] = btn

    def create_main_container(self):
        self.main_container = tk.Frame(self, bg="#1a1a24")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=30, pady=25)
        
        # Let's make main container grids expand
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)
        
        # Frames dictionary to keep track of pages
        self.pages = {}
        
        # Create all frames
        self.create_dashboard_page()
        self.create_directory_page()
        self.create_add_student_page()

    def show_page(self, page_id):
        # Update active sidebar buttons
        for pid, btn in self.sidebar_buttons.items():
            if pid == page_id:
                btn.config(bg="#222232", fg="#ffffff", font=("Segoe UI", 12, "bold"))
            else:
                btn.config(bg="#13131a", fg="#8888aa", font=("Segoe UI", 12))
                
        # Raise specified page
        if page_id == "dashboard":
            self.update_statistics()
        elif page_id == "directory":
            self.populate_student_table()
            
        page = self.pages[page_id]
        page.tkraise()

    # ==================== PAGE 1: DASHBOARD ====================
    def create_dashboard_page(self):
        page = tk.Frame(self.main_container, bg="#1a1a24")
        page.grid(row=0, column=0, sticky="nsew")
        self.pages["dashboard"] = page
        
        # Title
        lbl = tk.Label(page, text="Dashboard Overview", bg="#1a1a24", fg="#ffffff", font=("Segoe UI", 20, "bold"))
        lbl.pack(anchor="w", pady=(0, 20))
        
        # Cards container
        cards_frame = tk.Frame(page, bg="#1a1a24")
        cards_frame.pack(fill="x", pady=10)
        cards_frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="equal")
        
        self.stats_cards = {}
        stats_info = [
            ("total", "Total Students", "👥", "#5c6bc0"),
            ("avg", "Average Marks", "📈", "#26a69a"),
            ("pass", "Pass Rate", "🎯", "#66bb6a"),
            ("range", "High / Low", "📊", "#ffa726")
        ]
        
        for idx, (sid, label, icon, color) in enumerate(stats_info):
            card = tk.Frame(cards_frame, bg="#222232", bd=0, highlightthickness=1, highlightbackground="#2e2e3a")
            card.grid(row=0, column=idx, padx=8, pady=5, sticky="nsew")
            
            # Card header
            card_hdr = tk.Frame(card, bg="#222232")
            card_hdr.pack(fill="x", padx=15, pady=(15, 5))
            
            lbl_title = tk.Label(card_hdr, text=label, bg="#222232", fg="#8888aa", font=("Segoe UI", 11, "bold"))
            lbl_title.pack(side="left")
            
            lbl_icon = tk.Label(card_hdr, text=icon, bg="#222232", fg=color, font=("Segoe UI", 16))
            lbl_icon.pack(side="right")
            
            # Card Value
            lbl_value = tk.Label(card, text="--", bg="#222232", fg="#ffffff", font=("Segoe UI", 22, "bold"))
            lbl_value.pack(anchor="w", padx=15, pady=(5, 15))
            
            self.stats_cards[sid] = lbl_value
            
        # Lower section: Toppers & Export Card
        lower_frame = tk.Frame(page, bg="#1a1a24")
        lower_frame.pack(fill="both", expand=True, pady=20)
        lower_frame.columnconfigure(0, weight=2)
        lower_frame.columnconfigure(1, weight=1)
        lower_frame.rowconfigure(0, weight=1)
        
        # Toppers Panel
        topper_panel = tk.Frame(lower_frame, bg="#222232", highlightthickness=1, highlightbackground="#2e2e3a")
        topper_panel.grid(row=0, column=0, padx=8, pady=5, sticky="nsew")
        
        tk.Label(topper_panel, text="🏆 Top Performing Students", bg="#222232", fg="#ffffff", font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=20, pady=15)
        
        # Treeview inside toppers panel
        topper_cols = ("ID", "Name", "Course", "Marks", "Grade")
        self.topper_tree = ttk.Treeview(topper_panel, columns=topper_cols, show="headings", height=6)
        self.topper_tree.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        for col in topper_cols:
            self.topper_tree.heading(col, text=col)
            self.topper_tree.column(col, anchor="center", width=80)
        self.topper_tree.column("Name", anchor="w", width=150)

        # Quick Actions Panel
        action_panel = tk.Frame(lower_frame, bg="#222232", highlightthickness=1, highlightbackground="#2e2e3a")
        action_panel.grid(row=0, column=1, padx=8, pady=5, sticky="nsew")
        
        tk.Label(action_panel, text="⚡ Quick Actions", bg="#222232", fg="#ffffff", font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=20, pady=15)
        
        btn_export = tk.Button(action_panel, text="📥 Export Stats to CSV", font=("Segoe UI", 11, "bold"),
                               bg="#26a69a", fg="#ffffff", activebackground="#2bbbad", activeforeground="#ffffff",
                               bd=0, padx=15, pady=12, cursor="hand2", command=self.export_stats_action)
        btn_export.pack(fill="x", padx=20, pady=10)
        
        btn_add_quick = tk.Button(action_panel, text="➕ Add New Student", font=("Segoe UI", 11, "bold"),
                                  bg="#5c6bc0", fg="#ffffff", activebackground="#7986cb", activeforeground="#ffffff",
                                  bd=0, padx=15, pady=12, cursor="hand2", command=lambda: self.show_page("add_student"))
        btn_add_quick.pack(fill="x", padx=20, pady=10)

    def update_statistics(self):
        if not self.students:
            for val in self.stats_cards.values():
                val.config(text="0")
            self.stats_cards["range"].config(text="N/A")
            for item in self.topper_tree.get_children():
                self.topper_tree.delete(item)
            return
            
        total = len(self.students)
        marks = [float(s['Marks']) for s in self.students]
        avg = sum(marks) / total
        high = max(marks)
        low = min(marks)
        
        pass_count = sum(1 for m in marks if m >= 50)
        pass_rate = (pass_count / total) * 100
        
        self.stats_cards["total"].config(text=str(total))
        self.stats_cards["avg"].config(text=f"{avg:.1f}")
        self.stats_cards["pass"].config(text=f"{pass_rate:.1f}%")
        self.stats_cards["range"].config(text=f"{high:.0f} / {low:.0f}")
        
        # Populate Toppers Tree
        for item in self.topper_tree.get_children():
            self.topper_tree.delete(item)
            
        sorted_studs = sorted(self.students, key=lambda x: float(x['Marks']), reverse=True)[:5]
        for s in sorted_studs:
            self.topper_tree.insert("", "end", values=(s['ID'], s['Name'], s['Course'], s['Marks'], s['Grade']))

    def export_stats_action(self):
        if not self.students:
            messagebox.showwarning("Export Failed", "There are no students in the database to compile statistics.")
            return
        # Pull details
        total = len(self.students)
        marks = [float(s['Marks']) for s in self.students]
        avg = sum(marks) / total
        high = max(marks)
        low = min(marks)
        pass_count = sum(1 for m in marks if m >= 50)
        pass_rate = (pass_count / total) * 100
        toppers = [s for s in self.students if float(s['Marks']) == high]
        topper_names = ", ".join(f"{t['Name']} (ID: {t['ID']})" for t in toppers)
        
        # Save
        student_manager.export_statistics(total, avg, high, low, pass_rate, topper_names)
        messagebox.showinfo("Export Successful", f"Database statistics have been exported successfully to:\n{os.path.join(self.db_path, '..', 'statistics.csv')}")

    # ==================== PAGE 2: DIRECTORY ====================
    def create_directory_page(self):
        page = tk.Frame(self.main_container, bg="#1a1a24")
        page.grid(row=0, column=0, sticky="nsew")
        self.pages["directory"] = page
        
        # Top panel: title + search
        top_bar = tk.Frame(page, bg="#1a1a24")
        top_bar.pack(fill="x", pady=(0, 15))
        
        lbl = tk.Label(top_bar, text="Student Directory", bg="#1a1a24", fg="#ffffff", font=("Segoe UI", 20, "bold"))
        lbl.pack(side="left")
        
        # Search Container
        search_frame = tk.Frame(top_bar, bg="#1a1a24")
        search_frame.pack(side="right")
        
        tk.Label(search_frame, text="🔍 Search:", bg="#1a1a24", fg="#ffffff", font=("Segoe UI", 11)).pack(side="left", padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.populate_student_table())
        
        search_ent = tk.Entry(search_frame, textvariable=self.search_var, bg="#222232", fg="#ffffff",
                              bd=0, font=("Segoe UI", 11), insertbackground="white", width=22)
        search_ent.pack(side="left", padx=5, ipady=5)
        
        # Add Search Type Dropdown
        self.search_type_var = tk.StringVar(value="All")
        search_type_cb = ttk.Combobox(search_frame, textvariable=self.search_type_var, values=["All", "ID", "Name", "Course"],
                                      width=8, state="readonly")
        search_type_cb.pack(side="left", padx=5)
        search_type_cb.bind("<<ComboboxSelected>>", lambda e: self.populate_student_table())
        
        # Controls Frame (Filter & Sort)
        ctrl_frame = tk.Frame(page, bg="#222232", highlightthickness=1, highlightbackground="#2e2e3a")
        ctrl_frame.pack(fill="x", pady=(0, 15), ipady=5)
        
        # Sort Dropdown
        tk.Label(ctrl_frame, text="Sort by:", bg="#222232", fg="#8888aa", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, padx=(15, 5), pady=8, sticky="w")
        self.sort_var = tk.StringVar(value="ID (A-Z)")
        sort_cb = ttk.Combobox(ctrl_frame, textvariable=self.sort_var, 
                               values=["ID (A-Z)", "Name (A-Z)", "Marks (High to Low)", "Marks (Low to High)"],
                               state="readonly", width=18)
        sort_cb.grid(row=0, column=1, padx=5, pady=8, sticky="w")
        sort_cb.bind("<<ComboboxSelected>>", lambda e: self.populate_student_table())
        
        # Filter Course
        tk.Label(ctrl_frame, text="Course:", bg="#222232", fg="#8888aa", font=("Segoe UI", 10, "bold")).grid(row=0, column=2, padx=(20, 5), pady=8, sticky="w")
        self.filter_course_var = tk.StringVar(value="All")
        self.course_filter_cb = ttk.Combobox(ctrl_frame, textvariable=self.filter_course_var, state="readonly", width=12)
        self.course_filter_cb.grid(row=0, column=3, padx=5, pady=8, sticky="w")
        self.course_filter_cb.bind("<<ComboboxSelected>>", lambda e: self.populate_student_table())
        
        # Filter Semester
        tk.Label(ctrl_frame, text="Semester:", bg="#222232", fg="#8888aa", font=("Segoe UI", 10, "bold")).grid(row=0, column=4, padx=(20, 5), pady=8, sticky="w")
        self.filter_sem_var = tk.StringVar(value="All")
        self.sem_filter_cb = ttk.Combobox(ctrl_frame, textvariable=self.filter_sem_var, state="readonly", width=12)
        self.sem_filter_cb.grid(row=0, column=5, padx=5, pady=8, sticky="w")
        self.sem_filter_cb.bind("<<ComboboxSelected>>", lambda e: self.populate_student_table())
        
        # Reset Filters button
        btn_reset = tk.Button(ctrl_frame, text="🔄 Reset Filters", bg="#4e4e5e", fg="#ffffff", bd=0, padx=10, cursor="hand2",
                              command=self.reset_filters)
        btn_reset.grid(row=0, column=6, padx=(20, 15), pady=8, sticky="e")
        ctrl_frame.grid_columnconfigure(6, weight=1)

        # Table & Scrollbar container
        table_container = tk.Frame(page, bg="#1a1a24")
        table_container.pack(fill="both", expand=True)
        
        cols = ("ID", "Name", "Age", "Gender", "Course", "Semester", "Phone", "Email", "Marks", "Grade")
        self.tree = ttk.Treeview(table_container, columns=cols, show="headings", selectmode="browse")
        self.tree.pack(side="left", fill="both", expand=True)
        
        # Custom columns settings
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=65, anchor="center")
        self.tree.column("Name", width=120, anchor="w")
        self.tree.column("Email", width=150, anchor="w")
        self.tree.column("Phone", width=95, anchor="center")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Double click to edit
        self.tree.bind("<Double-1>", lambda e: self.edit_selected_student())
        
        # Bottom controls for table (Edit, Delete)
        bot_bar = tk.Frame(page, bg="#1a1a24")
        bot_bar.pack(fill="x", pady=(15, 0))
        
        btn_delete = tk.Button(bot_bar, text="❌ Delete Selected", font=("Segoe UI", 11, "bold"),
                               bg="#f44336", fg="#ffffff", activebackground="#ef5350", activeforeground="#ffffff",
                               bd=0, padx=15, pady=8, cursor="hand2", command=self.delete_selected_student)
        btn_delete.pack(side="right", padx=(10, 0))
        
        btn_edit = tk.Button(bot_bar, text="✏️ Edit / Update Selected", font=("Segoe UI", 11, "bold"),
                             bg="#5c6bc0", fg="#ffffff", activebackground="#7986cb", activeforeground="#ffffff",
                             bd=0, padx=15, pady=8, cursor="hand2", command=self.edit_selected_student)
        btn_edit.pack(side="right")
        
        tk.Label(bot_bar, text="* Hint: Double-click a student row to update details.", bg="#1a1a24", fg="#8888aa",
                 font=("Segoe UI", 10, "italic")).pack(side="left")

    def reset_filters(self):
        self.search_var.set("")
        self.search_type_var.set("All")
        self.sort_var.set("ID (A-Z)")
        self.filter_course_var.set("All")
        self.filter_sem_var.set("All")
        self.populate_student_table()

    def populate_student_table(self):
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Compile unique courses and semesters for filters
        courses = sorted(list(set(s['Course'] for s in self.students if s.get('Course'))))
        semesters = sorted(list(set(s['Semester'] for s in self.students if s.get('Semester'))))
        
        self.course_filter_cb['values'] = ["All"] + courses
        self.sem_filter_cb['values'] = ["All"] + semesters
        
        # Filter and Search
        q = self.search_var.get().strip().lower()
        search_type = self.search_type_var.get()
        course_filter = self.filter_course_var.get()
        sem_filter = self.filter_sem_var.get()
        
        filtered_list = []
        for s in self.students:
            # 1. Search Query Match
            if q:
                if search_type == "ID" and q not in s['ID'].lower():
                    continue
                elif search_type == "Name" and q not in s['Name'].lower():
                    continue
                elif search_type == "Course" and q not in s['Course'].lower():
                    continue
                elif search_type == "All":
                    matches_any = (
                        q in s['ID'].lower() or
                        q in s['Name'].lower() or
                        q in s['Course'].lower() or
                        q in s['Email'].lower()
                    )
                    if not matches_any:
                        continue
            
            # 2. Course Filter
            if course_filter != "All" and s['Course'] != course_filter:
                continue
                
            # 3. Sem Filter
            if sem_filter != "All" and s['Semester'] != sem_filter:
                continue
                
            filtered_list.append(s)
            
        # Sorting
        sort_mode = self.sort_var.get()
        if sort_mode == "ID (A-Z)":
            filtered_list.sort(key=lambda x: x['ID'].lower())
        elif sort_mode == "Name (A-Z)":
            filtered_list.sort(key=lambda x: x['Name'].lower())
        elif sort_mode == "Marks (High to Low)":
            filtered_list.sort(key=lambda x: float(x['Marks']), reverse=True)
        elif sort_mode == "Marks (Low to High)":
            filtered_list.sort(key=lambda x: float(x['Marks']))
            
        # Display
        for s in filtered_list:
            self.tree.insert("", "end", values=(
                s['ID'], s['Name'], s['Age'], s['Gender'], s['Course'], s['Semester'],
                s['Phone'], s['Email'], s['Marks'], s['Grade']
            ))

    def delete_selected_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select a student from the directory table to delete.")
            return
            
        row_values = self.tree.item(selected[0], "values")
        student_id = row_values[0]
        name = row_values[1]
        
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to permanently delete student {name} (ID: {student_id})?")
        if confirm:
            # Find and remove
            target = next((s for s in self.students if s['ID'] == student_id), None)
            if target:
                self.students.remove(target)
                file_handler.save_students(self.db_path, self.students)
                self.populate_student_table()
                messagebox.showinfo("Success", f"Student {name} was successfully deleted.")
            else:
                messagebox.showerror("Error", "Selected student could not be located in database.")

    def edit_selected_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select a student from the directory table to edit.")
            return
            
        row_values = self.tree.item(selected[0], "values")
        student_id = row_values[0]
        student = next((s for s in self.students if s['ID'] == student_id), None)
        if not student:
            messagebox.showerror("Error", "Could not load selected student record.")
            return
            
        # Open Update Dialog
        UpdateStudentDialog(self, student, self.on_student_updated)

    def on_student_updated(self):
        file_handler.save_students(self.db_path, self.students)
        self.populate_student_table()

    # ==================== PAGE 3: ADD RECORD ====================
    def create_add_student_page(self):
        page = tk.Frame(self.main_container, bg="#1a1a24")
        page.grid(row=0, column=0, sticky="nsew")
        self.pages["add_student"] = page
        
        lbl = tk.Label(page, text="Add New Student Record", bg="#1a1a24", fg="#ffffff", font=("Segoe UI", 20, "bold"))
        lbl.pack(anchor="w", pady=(0, 20))
        
        # Grid frame for input form
        form_frame = tk.Frame(page, bg="#222232", highlightthickness=1, highlightbackground="#2e2e3a", padx=30, pady=25)
        form_frame.pack(fill="x", pady=10)
        form_frame.grid_columnconfigure((1, 3), weight=1)
        
        # Form field parameters
        self.form_vars = {}
        self.error_labels = {}
        
        fields = [
            ("ID", "Student ID *", 0, 0),
            ("Name", "Full Name *", 0, 2),
            ("Age", "Age (16-35) *", 1, 0),
            ("Gender", "Gender *", 1, 2),
            ("Course", "Course *", 2, 0),
            ("Semester", "Semester *", 2, 2),
            ("Phone", "Phone (10 digits) *", 3, 0),
            ("Email", "Email *", 3, 2),
            ("Marks", "Marks (0-100) *", 4, 0)
        ]
        
        for name, label_text, row, col in fields:
            # Field Label
            tk.Label(form_frame, text=label_text, bg="#222232", fg="#8888aa", font=("Segoe UI", 10, "bold")).grid(row=row*2, column=col, sticky="w", padx=10, pady=(10, 2))
            
            # Entry variable
            self.form_vars[name] = tk.StringVar()
            
            # Entry widget
            entry = tk.Entry(form_frame, textvariable=self.form_vars[name], bg="#1a1a24", fg="#ffffff",
                             bd=0, font=("Segoe UI", 11), insertbackground="white")
            entry.grid(row=row*2+1, column=col, sticky="ew", padx=10, pady=(0, 2), ipady=6)
            
            # Live inline validation error label
            err_lbl = tk.Label(form_frame, text="", bg="#222232", fg="#ff5252", font=("Segoe UI", 9, "italic"))
            err_lbl.grid(row=row*2+1, column=col+1, sticky="w", padx=(5, 10))
            self.error_labels[name] = err_lbl
            
        # Submit Button
        btn_frame = tk.Frame(page, bg="#1a1a24")
        btn_frame.pack(fill="x", pady=25)
        
        btn_submit = tk.Button(btn_frame, text="💾 Save Student Record", font=("Segoe UI", 12, "bold"),
                               bg="#26a69a", fg="#ffffff", activebackground="#2bbbad", activeforeground="#ffffff",
                               bd=0, padx=25, pady=12, cursor="hand2", command=self.add_student_action)
        btn_submit.pack(side="left")
        
        btn_clear = tk.Button(btn_frame, text="🧹 Clear Fields", font=("Segoe UI", 12, "bold"),
                              bg="#4e4e5e", fg="#ffffff", activebackground="#5e5e6e", activeforeground="#ffffff",
                              bd=0, padx=25, pady=12, cursor="hand2", command=self.clear_form_fields)
        btn_clear.pack(side="left", padx=15)

    def clear_form_fields(self):
        for var in self.form_vars.values():
            var.set("")
        for err_lbl in self.error_labels.values():
            err_lbl.config(text="")

    def add_student_action(self):
        # Clear previous errors
        for err_lbl in self.error_labels.values():
            err_lbl.config(text="")
            
        # Fetch inputs
        inputs = {name: var.get().strip() for name, var in self.form_vars.items()}
        
        # Validations
        valid = True
        
        # ID check
        if not inputs["ID"]:
            self.error_labels["ID"].config(text="Required")
            valid = False
        elif any(s['ID'] == inputs["ID"] for s in self.students):
            self.error_labels["ID"].config(text="Duplicate ID")
            valid = False
            
        # Name check
        if not inputs["Name"]:
            self.error_labels["Name"].config(text="Required")
            valid = False
            
        # Age check
        if not inputs["Age"]:
            self.error_labels["Age"].config(text="Required")
            valid = False
        elif not utils.validate_age(inputs["Age"]):
            self.error_labels["Age"].config(text="16 to 35 required")
            valid = False
            
        # Gender, Course, Semester check
        for field in ("Gender", "Course", "Semester"):
            if not inputs[field]:
                self.error_labels[field].config(text="Required")
                valid = False
                
        # Phone check
        if not inputs["Phone"]:
            self.error_labels["Phone"].config(text="Required")
            valid = False
        elif not utils.validate_phone(inputs["Phone"]):
            self.error_labels["Phone"].config(text="10 digits required")
            valid = False
            
        # Email check
        if not inputs["Email"]:
            self.error_labels["Email"].config(text="Required")
            valid = False
        elif not utils.validate_email(inputs["Email"]):
            self.error_labels["Email"].config(text="Invalid email (@, .com)")
            valid = False
            
        # Marks check
        if not inputs["Marks"]:
            self.error_labels["Marks"].config(text="Required")
            valid = False
        elif not utils.validate_marks(inputs["Marks"]):
            self.error_labels["Marks"].config(text="0 to 100 required")
            valid = False
            
        if not valid:
            messagebox.showerror("Validation Error", "Please correct validation errors highlighted in the form.")
            return
            
        # Calculations
        marks = float(inputs["Marks"])
        grade = student_manager.calculate_grade(marks)
        
        # Create student dictionary
        new_student = {
            'ID': inputs["ID"],
            'Name': inputs["Name"],
            'Age': str(int(inputs["Age"])),
            'Gender': inputs["Gender"],
            'Course': inputs["Course"],
            'Semester': inputs["Semester"],
            'Phone': inputs["Phone"],
            'Email': inputs["Email"],
            'Marks': str(marks),
            'Grade': grade
        }
        
        self.students.append(new_student)
        file_handler.save_students(self.db_path, self.students)
        
        messagebox.showinfo("Success", f"Student {inputs['Name']} successfully added!")
        self.clear_form_fields()
        self.show_page("directory")


# ==================== DIALOG WINDOWS ====================
class UpdateStudentDialog(tk.Toplevel):
    def __init__(self, parent, student, callback):
        super().__init__(parent)
        self.student = student
        self.callback = callback
        
        self.title(f"Update Student - {student['Name']} (ID: {student['ID']})")
        self.geometry("550x520")
        self.configure(bg="#222232")
        self.transient(parent)
        self.grab_set()
        
        # Center in parent window
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 275
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 260
        self.geometry(f"+{x}+{y}")
        
        # Build Title Header
        tk.Label(self, text=f"Update Record (ID: {student['ID']})", bg="#222232", fg="#ffffff",
                 font=("Segoe UI", 15, "bold")).pack(anchor="w", padx=30, pady=20)
        
        form_frame = tk.Frame(self, bg="#222232")
        form_frame.pack(fill="both", expand=True, padx=30)
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Config inputs
        self.inputs = {}
        self.error_labels = {}
        fields = [
            ("Name", "Name", student["Name"]),
            ("Semester", "Semester", student["Semester"]),
            ("Phone", "Phone (10 digits)", student["Phone"]),
            ("Email", "Email", student["Email"]),
            ("Marks", "Marks (0-100)", student["Marks"])
        ]
        
        for idx, (name, label_text, val) in enumerate(fields):
            tk.Label(form_frame, text=label_text, bg="#222232", fg="#8888aa",
                     font=("Segoe UI", 10, "bold")).grid(row=idx*3, column=0, sticky="w", pady=(8, 2))
                     
            self.inputs[name] = tk.StringVar(value=val)
            
            entry = tk.Entry(form_frame, textvariable=self.inputs[name], bg="#1a1a24", fg="#ffffff",
                             bd=0, font=("Segoe UI", 11), insertbackground="white")
            entry.grid(row=idx*3+1, column=0, columnspan=2, sticky="ew", ipady=6)
            
            err_lbl = tk.Label(form_frame, text="", bg="#222232", fg="#ff5252", font=("Segoe UI", 9, "italic"))
            err_lbl.grid(row=idx*3+2, column=0, columnspan=2, sticky="w", pady=(1, 5))
            self.error_labels[name] = err_lbl
            
        # Buttons Bottom Frame
        btn_frame = tk.Frame(self, bg="#222232")
        btn_frame.pack(fill="x", padx=30, pady=20, side="bottom")
        
        btn_save = tk.Button(btn_frame, text="💾 Save Changes", font=("Segoe UI", 11, "bold"),
                             bg="#26a69a", fg="#ffffff", activebackground="#2bbbad", activeforeground="#ffffff",
                             bd=0, padx=20, pady=8, cursor="hand2", command=self.save_update_action)
        btn_save.pack(side="left")
        
        btn_cancel = tk.Button(btn_frame, text="Cancel", font=("Segoe UI", 11, "bold"),
                               bg="#4e4e5e", fg="#ffffff", activebackground="#5e5e6e", activeforeground="#ffffff",
                               bd=0, padx=20, pady=8, cursor="hand2", command=self.destroy)
        btn_cancel.pack(side="right")

    def save_update_action(self):
        # Reset errors
        for label in self.error_labels.values():
            label.config(text="")
            
        name = self.inputs["Name"].get().strip()
        sem = self.inputs["Semester"].get().strip()
        phone = self.inputs["Phone"].get().strip()
        email = self.inputs["Email"].get().strip()
        marks_str = self.inputs["Marks"].get().strip()
        
        valid = True
        
        if not name:
            self.error_labels["Name"].config(text="Name cannot be empty.")
            valid = False
            
        if not sem:
            self.error_labels["Semester"].config(text="Semester cannot be empty.")
            valid = False
            
        if not phone or not utils.validate_phone(phone):
            self.error_labels["Phone"].config(text="Phone must be exactly 10 digits.")
            valid = False
            
        if not email or not utils.validate_email(email):
            self.error_labels["Email"].config(text="Invalid email (must contain '@' and '.com').")
            valid = False
            
        if not marks_str or not utils.validate_marks(marks_str):
            self.error_labels["Marks"].config(text="Marks must be a number between 0 and 100.")
            valid = False
            
        if not valid:
            return
            
        # Update properties
        self.student["Name"] = name
        self.student["Semester"] = sem
        self.student["Phone"] = phone
        self.student["Email"] = email
        self.student["Marks"] = str(float(marks_str))
        
        # Recalculate Grade
        self.student["Grade"] = student_manager.calculate_grade(float(marks_str))
        
        # Invoke callback and close dialog
        self.callback()
        messagebox.showinfo("Success", "Student record successfully updated.")
        self.destroy()
