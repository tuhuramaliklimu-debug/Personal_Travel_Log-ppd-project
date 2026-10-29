import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os

DATA_FILE = "travel_log.json"

class TravelLogApp:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg="#C99CC1") 
        self.root.title("Personal Travel Log System")
        self.root.geometry("700x700")

        
        self.travel_data = []
        self.load_data()
        style = ttk.Style()
        style.configure("Menu.TButton",font=("Arial", 14),padding=8,background="#C497B4",foreground='black')
        style.map("Menu.TButton",background=[("active","#C09BB7")],foreground=[("active","black")])

        # Main menu
        ttk.Label(root, text="Personal Travel Log", font=("Georgia", 39,"bold")).pack(pady=70)
        btn_width = 30

        ttk.Button(root, text="Add Entry", width=btn_width, style="Menu.TButton", command=self.add_entry_window).pack(pady=5)
        ttk.Button(root, text="View Entries", width=btn_width, style="Menu.TButton", command=self.view_entries_window).pack(pady=5)
        ttk.Button(root, text="Edit Entry", width=btn_width, style="Menu.TButton", command=self.edit_entry_window).pack(pady=5)
        ttk.Button(root, text="Search Entry", width=btn_width, style="Menu.TButton", command=self.search_entry_window).pack(pady=5)
        ttk.Button(root, text="Filter Entries", width=btn_width, style="Menu.TButton", command=self.filter_entries_window).pack(pady=5)
        ttk.Button(root, text="Sort Entry", width=btn_width, style="Menu.TButton", command=self.sort_entries_window).pack(pady=5)
        ttk.Button(root, text="Delete Entry", width=btn_width, style="Menu.TButton", command=self.delete_entry_window).pack(pady=5)
        ttk.Button(root, text="Exit", width=btn_width, style="Menu.TButton", command=root.quit).pack(pady=5)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    self.travel_data = json.load(f)
            except(json.JSONDecodeError,FileNotFoundError):
                self.travel_data=[]

    def save_data(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.travel_data, f, indent=4)


    def add_entry_window(self):
        
        win = tk.Toplevel(self.root)
        win.title("Add Travel Entry")
        win.geometry("760x720")
        win.configure(bg="#e0accf")

        # Main container frame with  background
        main_frame = tk.Frame(win, bg="#f6e1f2", bd=0, relief="flat")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title label at the top
        title_label = tk.Label(main_frame,text="✈ Add Travel Entry",font=("Georgia", 20, "bold"), bg="#f6e1f2", fg="#4b2e39")
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # List of input field labels
        labels = ["Place", "Country", "Type (Visited/Wishlist)", "Year", "Rating (1–5)","Priority", "Budget/Cost", "Companions", "Accommodation","Transport", "Duration", "Comments"]
        entries = {} 

        # Entry styling variables
        entry_bg = "#f5eff6"  # Background color inside Entry
        entry_border_color = "#dfaac6"  # Border color

        # Function to create styled entry with border effect
        def make_styled_entry(parent):
            frame = tk.Frame(parent, bg=entry_border_color, bd=0)  # Outer border frame
            entry = tk.Entry(frame, font=("Helvetica", 14), relief="flat", bg=entry_bg)
            entry.pack(fill="both", padx=2, pady=2)  # Padding inside border frame
            return frame, entry

        # Loop through all labels and create inputs
        row_counter = 1
        for label in labels:
            # Create label text
            tk.Label( main_frame, text=label,font=("Helvetica", 14, "bold"), bg="#f6e1f2",fg="#4b2e39").grid(row=row_counter, column=0, sticky="w", padx=5, pady=8)

            # Special case for Visited/Wishlist toggle
            if label == "Type (Visited/Wishlist)":
                switch_var = tk.IntVar(value=1)  # 1 = Visited, 0 = Wishlist
                switch_label = tk.Label(main_frame, text="Visited", font=("Helvetica", 12, "bold"),bg="#f6e1f2")
                switch_label.grid(row=row_counter, column=2, padx=(10, 0), pady=8, sticky="w")

                # Change text when toggled
                def toggle_text():
                    switch_label.config(text="Visited" if switch_var.get() else "Wishlist")

                switch_button = tk.Checkbutton( main_frame,variable=switch_var,command=toggle_text,bg="#9db290",activebackground="#f6e1f2")
                switch_button.grid(row=row_counter, column=1, sticky="w", padx=(10, 0), pady=8)

                entries[label] = (switch_var, switch_label)  # Store as tuple

            else:
                # Create styled entry field
                frame, entry = make_styled_entry(main_frame)
                frame.grid(row=row_counter, column=1, columnspan=2, padx=5, pady=4, sticky="we")
                entries[label] = entry

            row_counter += 1

        # Buttons frame
        btn_frame = tk.Frame(main_frame, bg="#f6e1f2")
        btn_frame.grid(row=row_counter, column=0, columnspan=3, pady=20)

        save_btn = tk.Button( btn_frame,text="Save Entry",font=("Helvetica", 14, "bold"), bg="#6675A2",  fg="white",relief="flat",activebackground="#b36a92",activeforeground="white",padx=15, pady=5)

        # Cancel button (gray)
        cancel_btn = tk.Button( btn_frame, text="Cancel",font=("Helvetica", 14, "bold"),bg="#cccccc", fg="black", relief="flat", activebackground="#999999",activeforeground="white", padx=15, pady=5,command=win.destroy)

        save_btn.pack(side="left", padx=10)
        cancel_btn.pack(side="left", padx=10)

        # Save function
        def save_entry():
            entry_data = {}
            missing_field=[]
            for label, widget in entries.items():
                if label == "Type (Visited/Wishlist)":
                    var, lbl = widget
                    entry_data[label] = lbl.cget("text")  # Get label text
                else:
                    value= widget.get().strip()  
                    entry_data[label] =value  # Get entry value
                    if not value:
                        missing_field.append(label)
                    entry_data[label]=value
            
            if missing_field:
                messagebox.showwarning("Missing Information", f"Please fill in the following fields:\n\n" + "\n".join(missing_field))
                return

            # Add to data list and save
            self.travel_data.append(entry_data)
            self.save_data()

            # Confirmation popup
            messagebox.showinfo("Success", "Entry added successfully")
            win.destroy()

        save_btn.config(command=save_entry)  # Attach save function to button



    def display_entries_as_cards(self, entries, title="Travel Entries", on_delete=None):
        win = tk.Toplevel()
        win.title(title)
        win.geometry("600x500")
        win.configure(bg="#e3bbd8")

        canvas = tk.Canvas(win, height=380, bg="#f3c5e0", bd=0, highlightthickness=0)
        v_scroll = ttk.Scrollbar(win, orient="vertical", command=canvas.yview)
        h_scroll = ttk.Scrollbar(win, orient="horizontal", command=canvas.xview)
        canvas.configure(xscrollcommand=h_scroll.set)

        wrapper = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=wrapper, anchor="nw")

        wrapper.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.pack(side="top", fill="both", expand=True)
        h_scroll.pack(side="bottom", fill="x")
        v_scroll.pack(side="right", fill="y")

        if not entries:
            ttk.Label(wrapper, text="No entries found.", font=("Arial", 12)).pack(pady=20)
            return

        def make_delete_handler(entry_ref, win_ref):
            def handle_delete():
                # Find the actual index of this entry in self.travel_data
                try:
                    real_idx = self.travel_data.index(entry_ref)
                except ValueError:
                    messagebox.showerror("Error", "Entry not found in data.")
                    return
                confirm = messagebox.askyesno(
                    "Confirm Delete",
                    f"Are you sure you want to delete Entry {real_idx + 1}?"
                )
                if confirm:
                    del self.travel_data[real_idx]
                    self.save_data()
                    messagebox.showinfo("Deleted", "Entry deleted successfully.")
                    win_ref.destroy()
                    # Re-open the view with updated data
                    self.display_entries_as_cards(self.travel_data, title)
            return handle_delete

        for idx, entry in enumerate(entries):
            card = tk.Frame(wrapper, bg="white", bd=1, relief="solid")
            card.grid(row=0, column=idx, padx=15, pady=15, sticky="n")

            # Card header row: title + delete icon
            header = tk.Frame(card, bg="#f9f0f6")
            header.pack(fill="x", padx=0, pady=0)

            title_label = tk.Label(
                header, text=f"Entry {idx + 1}",
                font=("Arial", 12, "bold"), bg="#f9f0f6", fg="#333"
            )
            title_label.pack(side="left", padx=10, pady=(8, 4))

            delete_btn = tk.Button(
                header,
                text="🗑",
                font=("Arial", 13),
                bg="#f9f0f6",
                fg="#c0392b",
                relief="flat",
                cursor="hand2",
                activebackground="#fddede",
                activeforeground="#c0392b",
                bd=0,
                command=make_delete_handler(entry, win)
            )
            delete_btn.pack(side="right", padx=8, pady=(6, 2))

            # Separator line under header
            sep = tk.Frame(card, bg="#e0c8d8", height=1)
            sep.pack(fill="x", padx=5)

            for key, val in entry.items():
                row = tk.Frame(card, bg="white")
                row.pack(anchor="w", padx=10, pady=2)

                tk.Label(row, text=f"{key}:", font=("Arial", 10, "bold"), bg="white", fg="#555").pack(side="left")
                tk.Label(row, text=f" {val}", font=("Arial", 10), bg="white", fg="#111").pack(side="left")

            card.update_idletasks()
            card.config(width=250)

    def view_entries_window(self):
        self.display_entries_as_cards(self.travel_data,"All Travel Entries")


    def edit_entry_window(self):
        index = simpledialog.askinteger("Edit", "Enter entry number to edit (starting from 1):")
        if index is None or index < 1 or index > len(self.travel_data):
            messagebox.showerror("Error", "Invalid entry number")
            return

        entry_data = self.travel_data[index - 1]
        win = tk.Toplevel()
        win.title("Edit Entry")
        win.configure(bg="#D4A2BE")
        win.geometry("500x455")

        form_frame=tk.Frame(win,bg="#C06E9C")
        form_frame.pack(padx=20,pady=20,fill="both",expand=True)

        entries = {}

        for i, (key, value) in enumerate(entry_data.items()):
            ttk.Label(form_frame, text=key + " : ").grid(row=i, column=0, sticky="w", padx=10, pady=5)
            entry = ttk.Entry(form_frame, width=40)
            entry.insert(0, value)
            entry.grid(row=i, column=1, padx=5, pady=2)
            entries[key] = entry

        def update_entry():
            self.travel_data[index - 1] = {key: entry.get() for key, entry in entries.items()}
            self.save_data()
            messagebox.showinfo("Success", "Entry updated successfully")
            win.destroy()
            self.view_entries_window()
        update_btn=tk.Button(win,text="UPDATE ENTRY ",font=("Arial",16,"bold"),bg="#ae86dc",fg="white", relief="raised",command=update_entry)
        update_btn.pack(pady=15)

    def delete_entry_window(self):
        index=simpledialog.askinteger("Delete","Entry entry number to delete (starting from 1):")
        if index is None or index<1 or index>len(self.travel_data):
            messagebox.showerror("Error","Invalid entry number")
            return
        confirm=messagebox.askyesno("Confirm Delete",f"Are you sure you want to delete Entery{index}?")
        if confirm:
            del self.travel_data[index-1]
            self.save_data()
            messagebox.showinfo("Deleted","Entry deleted sucessfully")
            
    def search_entry_window(self):
        keyword = simpledialog.askstring("Search", "Enter keyword to search in all fields:")
        if not keyword:
            return

        win = tk.Toplevel()
        win.title(f"Search Results for '{keyword}'")
        win.geometry("700x500")
        win.configure(bg="#ed92c7")

        title_label=tk.Label(win,text=f"Search Result For : \"{keyword}\"",font=("Segoe UI", 16, "bold"),bg="#c7c195",fg="#3d405b")
        title_label.pack(pady=(15,5))

        text_frame=ttk.Frame(win,padding=10)
        text_frame.pack(fill="both",expand=True)

        scrollbar=ttk.Scrollbar(text_frame)
        scrollbar.pack(side="right",fill="y")

        text = tk.Text(text_frame,wrap="word",font=("Segoe UI", 11),yscrollcommand=scrollbar.set,bg="#fff",fg="#333",  relief="flat", padx=10, pady=10)
        text.pack(fill="both",expand=True)
        scrollbar.config(command=text.yview)

        
        

        found = False
        for idx, entry in enumerate(self.travel_data):
            
            if any(keyword.lower() in str(val).lower() for val in entry.values()):
                text.insert("end", f"\n--- Entry {idx + 1} ---\n")
                for key, val in entry.items():
                    text.insert("end", f"{key}: {val}\n")
                found = True

        if not found:
            text.insert("end", "No matching entries found.")

    def filter_entries_window(self):
        win = tk.Toplevel()
        win.title("Filter Entries")
        win.geometry("401x250")
        win.configure(bg="#ecbcef")

        title_label=tk.Label(win,text="Filter Travel Entries",font=("Segoe UI", 16, "bold"),bg="#e09fbf",fg="#3d405b")
        title_label.pack(pady=(15,5))

        form_frame = ttk.Frame(win, padding=15)
        form_frame.pack(fill="both", expand=True)


        # Dropdown for selecting field
        ttk.Label(form_frame, text="Filter by:").grid(row=0, column=0, padx=5, pady=5)
        filter_options = ["Place", "Country", "Type (Visited/Wishlist)", "Year", "Rating (1–5)", "Priority"]
        filter_type = ttk.Combobox(form_frame, values=filter_options, state="readonly", width=25)
        filter_type.grid(row=0, column=1, padx=5,pady=8)
        filter_type.current(0)  # Default to first option

        ttk.Label(form_frame, text="Filter Value:",font=("Segoe UI", 11)).grid(row=1, column=0, padx=5, pady=5)
        filter_value = ttk.Entry(form_frame, width=27,font=("Segoe UI",11))
        filter_value.grid(row=1, column=1, padx=5,pady=8)

        style = ttk.Style()
        style.configure("Accent.TButton", font=("Segoe UI", 11, "bold"), padding=8)

        btn_frame = ttk.Frame(win) 
        btn_frame.pack(pady=10)

        def apply_filter():
            key = filter_type.get()
            value = filter_value.get().strip()

            results = [
                entry for entry in self.travel_data
                if key in entry and value.lower() in entry[key].lower()
            ]
            self.display_entries_as_cards(results, f"Filtered by {key}: {value}")
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Segoe UI", 11, "bold"), padding=8)

        apply_btn = ttk.Button(btn_frame, text="Apply Filter", style="Accent.TButton", command=apply_filter)
        apply_btn.pack(side="left", padx=5)

        btn_frame = ttk.Frame(win)
        btn_frame.pack(pady=10)

        cancel_btn = ttk.Button(btn_frame, text="Cancel", command=win.destroy)
        cancel_btn.pack(side="left", padx=5)
        
    def sort_entries_window(self):
        win = tk.Toplevel()
        win.title("Sort Entries")
        win.geometry("400x250")
        win.configure(bg="#A97BA6")  # Soft pastel blue

        frame = ttk.Frame(win, padding=20)
        frame.pack(expand=True, fill="both")

        style = ttk.Style()
        style.configure("TLabel", background="#A97BA6", foreground="white", font=("Arial", 11, "bold"))
        style.configure("TButton", font=("Arial", 10, "bold"), padding=6)
        style.map("TButton", background=[("active", "#8c638d")])

        tk.Label(frame, text="Sort by:").grid(row=0, column=0, padx=10, pady=10)

        sort_options = ["Place", "Country", "Type", "Year", "Rating", "Priority"]
        sort_key_map = {
            "Place": "Place",
            "Country": "Country",
            "Type": "Type (Visited/Wishlist)",
            "Year": "Year",
            "Rating": "Rating (1–5)",
            "Priority": "Priority"
        }

        ttk.Label(frame, text="Sort by:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        sort_by_var = tk.StringVar(value=sort_options[0])
        ttk.Combobox(frame, textvariable=sort_by_var, values=sort_options, state="readonly", width=20)\
        .grid(row=0, column=1, padx=10, pady=10)


        ttk.Label(frame, text="Order:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        order_var = tk.StringVar(value="Ascending")
        ttk.Combobox(frame, textvariable=order_var, values=["Ascending", "Descending"], state="readonly", width=20)\
        .grid(row=1, column=1, padx=10, pady=10)


        def apply_sort():
            display_name = sort_by_var.get()
            actual_key = sort_key_map[display_name]  # <-- Use the correct dict key
            reverse_order = (order_var.get() == "Descending")

            try:
                if "Rating" in actual_key:
                    self.travel_data.sort(key=lambda x: float(x.get(actual_key, 0)), reverse=reverse_order)
                elif "Year" in actual_key:
                    self.travel_data.sort(key=lambda x: int(x.get(actual_key, 0)), reverse=reverse_order)
                else:
                    self.travel_data.sort(key=lambda x: str(x.get(actual_key, "")).lower(), reverse=reverse_order)

                self.save_data()
                messagebox.showinfo("Sorted", f"Entries sorted by {display_name} ({order_var.get()})")
                self.update_display()
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Could not sort: {e}")

        tk.Button(frame, text="Sort", command=apply_sort).grid(row=2, column=0, columnspan=2, pady=10)

    def update_display(self):
        self.display_entries_as_cards(self.travel_data, "All Travel Entries")


if __name__ == "__main__":
    root = tk.Tk()
    app = TravelLogApp(root)
    root.mainloop()
