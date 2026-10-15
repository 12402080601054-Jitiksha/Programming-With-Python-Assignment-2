
import re
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

# Change these settings to match your MySQL installation.
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "jiti-1054",
}

DATABASE_NAME = "contact_manager"

# Accepts .com, .edu and .org email addresses.
EMAIL_PATTERN = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.(com|edu|org)$",
    re.IGNORECASE
)

SORT_COLUMNS = {
    "Name": "name",
    "Email": "email",
    "Category": "category",
    "Phone": "phone",
}

SEARCH_COLUMNS = {
    "Name": "name",
    "Email": "email",
    "Phone": "phone",
}


def create_database():
    """Create the database and required table."""
    connection = mysql.connector.connect(**DB_CONFIG)
    cursor = connection.cursor()

    cursor.execute(
        f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}"
    )
    cursor.close()
    connection.close()

    config = DB_CONFIG.copy()
    config["database"] = DATABASE_NAME
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Contact (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(254) NOT NULL UNIQUE,
            phone VARCHAR(30) NOT NULL,
            category VARCHAR(50) NOT NULL,
            notes TEXT,
            INDEX idx_contact_name (name),
            INDEX idx_contact_phone (phone)
        )
    """)

    connection.commit()
    cursor.close()
    connection.close()


def get_connection():
    config = DB_CONFIG.copy()
    config["database"] = DATABASE_NAME
    return mysql.connector.connect(**config)


class ContactManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager")
        self.root.geometry("1050x680")
        self.root.minsize(850, 580)

        self.selected_id = None
        self.visible_contacts = []

        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.category_var = tk.StringVar(value="Personal")
        self.search_var = tk.StringVar()
        self.search_field_var = tk.StringVar(value="Name")
        self.sort_var = tk.StringVar(value="Name")

        self.build_menu()
        self.build_interface()
        self.load_contacts()

    def build_menu(self):
        menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Refresh", command=self.load_contacts)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)

        menu_bar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menu_bar)

    def build_interface(self):
        form = ttk.LabelFrame(
            self.root, text="Contact Details", padding=10
        )
        form.pack(fill="x", padx=10, pady=8)

        ttk.Label(form, text="Name").grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )
        ttk.Entry(form, textvariable=self.name_var, width=32).grid(
            row=0, column=1, sticky="ew", padx=5, pady=5
        )

        ttk.Label(form, text="Email").grid(
            row=1, column=0, sticky="w", padx=5, pady=5
        )
        ttk.Entry(form, textvariable=self.email_var, width=32).grid(
            row=1, column=1, sticky="ew", padx=5, pady=5
        )

        ttk.Label(form, text="Phone").grid(
            row=2, column=0, sticky="w", padx=5, pady=5
        )
        ttk.Entry(form, textvariable=self.phone_var, width=32).grid(
            row=2, column=1, sticky="ew", padx=5, pady=5
        )

        ttk.Label(form, text="Category").grid(
            row=3, column=0, sticky="w", padx=5, pady=5
        )
        ttk.Combobox(
            form,
            textvariable=self.category_var,
            values=["Personal", "Faculty", "Friend", "Family", "Work"],
            state="readonly",
            width=29,
        ).grid(row=3, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(form, text="Notes").grid(
            row=4, column=0, sticky="nw", padx=5, pady=5
        )
        self.notes_text = tk.Text(form, height=3, width=32)
        self.notes_text.grid(
            row=4, column=1, sticky="ew", padx=5, pady=5
        )

        form.columnconfigure(1, weight=1)

        buttons = ttk.Frame(self.root)
        buttons.pack(fill="x", padx=10, pady=4)

        ttk.Button(
            buttons, text="Add Contact", command=self.add_contact
        ).pack(side="left", padx=4)

        ttk.Button(
            buttons, text="Update Contact", command=self.update_contact
        ).pack(side="left", padx=4)

        ttk.Button(
            buttons, text="Delete Contact", command=self.delete_contact
        ).pack(side="left", padx=4)

        ttk.Button(
            buttons, text="Clear Fields", command=self.clear_fields
        ).pack(side="left", padx=4)

        search_frame = ttk.LabelFrame(
            self.root, text="Search and Sort", padding=8
        )
        search_frame.pack(fill="x", padx=10, pady=8)

        ttk.Label(search_frame, text="Search by:").pack(side="left", padx=4)

        for field in ("Name", "Email", "Phone"):
            ttk.Radiobutton(
                search_frame,
                text=field,
                variable=self.search_field_var,
                value=field,
            ).pack(side="left", padx=3)

        ttk.Entry(
            search_frame, textvariable=self.search_var, width=22
        ).pack(side="left", padx=5)

        ttk.Button(
            search_frame, text="Search", command=self.search_contacts
        ).pack(side="left", padx=4)

        ttk.Button(
            search_frame, text="Show All", command=self.load_contacts
        ).pack(side="left", padx=4)

        ttk.Label(search_frame, text="Sort by:").pack(
            side="left", padx=(12, 3)
        )

        ttk.Combobox(
            search_frame,
            textvariable=self.sort_var,
            values=list(SORT_COLUMNS.keys()),
            state="readonly",
            width=12,
        ).pack(side="left", padx=4)

        ttk.Button(
            search_frame, text="Sort", command=self.load_contacts
        ).pack(side="left", padx=4)

        list_frame = ttk.LabelFrame(
            self.root, text="Contacts (select a contact to edit)", padding=8
        )
        list_frame.pack(fill="both", expand=True, padx=10, pady=8)

        self.contact_list = tk.Listbox(
            list_frame, font=("Consolas", 10), height=12
        )
        scrollbar = ttk.Scrollbar(
            list_frame, orient="vertical",
            command=self.contact_list.yview
        )
        self.contact_list.configure(yscrollcommand=scrollbar.set)

        self.contact_list.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.contact_list.bind(
            "<<ListboxSelect>>", self.select_contact
        )

        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(
            self.root, textvariable=self.status_var, anchor="w"
        ).pack(fill="x", padx=12, pady=(0, 8))

    def validate_fields(self):
        name = self.name_var.get().strip()
        email = self.email_var.get().strip()
        phone = self.phone_var.get().strip()
        category = self.category_var.get().strip()
        notes = self.notes_text.get("1.0", "end-1c").strip()

        if not name or not email or not phone or not category:
            messagebox.showwarning(
                "Validation Error",
                "Name, email, phone and category are required."
            )
            return None

        if not EMAIL_PATTERN.fullmatch(email):
            messagebox.showwarning(
                "Invalid Email",
                "Enter a valid email ending in .com, .edu or .org."
            )
            return None

        return name, email.lower(), phone, category, notes

    def add_contact(self):
        values = self.validate_fields()
        if values is None:
            return

        connection = None
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO Contact
                    (name, email, phone, category, notes)
                VALUES (%s, %s, %s, %s, %s)
            """, values)
            connection.commit()

            self.status_var.set("Contact inserted successfully.")
            self.clear_fields()
            self.load_contacts()

        except Error as error:
            if connection:
                connection.rollback()

            if getattr(error, "errno", None) == 1062:
                messagebox.showerror(
                    "Duplicate Email",
                    "A contact with this email already exists."
                )
            else:
                messagebox.showerror("Database Error", str(error))
        finally:
            if connection and connection.is_connected():
                connection.close()

    def update_contact(self):
        if self.selected_id is None:
            messagebox.showwarning(
                "Select Contact", "Select a contact to update."
            )
            return

        values = self.validate_fields()
        if values is None:
            return

        connection = None
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE Contact
                SET name=%s, email=%s, phone=%s, category=%s, notes=%s
                WHERE id=%s
            """, values + (self.selected_id,))
            connection.commit()

            self.status_var.set("Contact updated successfully.")
            self.clear_fields()
            self.load_contacts()

        except Error as error:
            if connection:
                connection.rollback()

            if getattr(error, "errno", None) == 1062:
                messagebox.showerror(
                    "Duplicate Email",
                    "Another contact already uses this email."
                )
            else:
                messagebox.showerror("Database Error", str(error))
        finally:
            if connection and connection.is_connected():
                connection.close()

    def delete_contact(self):
        if self.selected_id is None:
            messagebox.showwarning(
                "Select Contact", "Select a contact to delete."
            )
            return

        if not messagebox.askyesno(
            "Confirm Delete", "Delete the selected contact?"
        ):
            return

        connection = None
        try:
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute(
                "DELETE FROM Contact WHERE id=%s",
                (self.selected_id,)
            )
            connection.commit()

            self.status_var.set("Contact deleted successfully.")
            self.clear_fields()
            self.load_contacts()

        except Error as error:
            if connection:
                connection.rollback()
            messagebox.showerror("Database Error", str(error))
        finally:
            if connection and connection.is_connected():
                connection.close()

    def load_contacts(self):
        sort_column = SORT_COLUMNS.get(self.sort_var.get(), "name")
        self.display_contacts(sort_column=sort_column)

    def search_contacts(self):
        term = self.search_var.get().strip()

        if not term:
            self.load_contacts()
            return

        field = SEARCH_COLUMNS[self.search_field_var.get()]
        self.display_contacts(search_field=field, term=term)

    def display_contacts(self, sort_column="name",
                         search_field=None, term=None):
        connection = None
        try:
            connection = get_connection()
            cursor = connection.cursor()

            sql = """
                SELECT id, name, email, phone, category, notes
                FROM Contact
            """
            parameters = []

            if search_field and term is not None:
                # The field comes from a whitelist; the value is parameterized.
                sql += f" WHERE {search_field} LIKE %s"
                parameters.append(term + "%")

            # Sort identifiers also come from a fixed whitelist.
            sql += f" ORDER BY {sort_column} ASC, id ASC"
            cursor.execute(sql, parameters)
            rows = cursor.fetchall()

            self.contact_list.delete(0, tk.END)
            self.visible_contacts = rows

            for contact_id, name, email, phone, category, notes in rows:
                line = (
                    f"{contact_id} | {name} | {email} | "
                    f"{phone} | {category}"
                )
                self.contact_list.insert(tk.END, line)

            self.status_var.set(f"{len(rows)} contact(s) displayed.")

        except Error as error:
            messagebox.showerror("Database Error", str(error))
        finally:
            if connection and connection.is_connected():
                connection.close()

    def select_contact(self, _event=None):
        selection = self.contact_list.curselection()
        if not selection:
            return

        row = self.visible_contacts[selection[0]]
        contact_id, name, email, phone, category, notes = row

        self.selected_id = contact_id
        self.name_var.set(name)
        self.email_var.set(email)
        self.phone_var.set(phone)
        self.category_var.set(category)

        self.notes_text.delete("1.0", tk.END)
        self.notes_text.insert("1.0", notes or "")

        self.status_var.set(f"Selected contact ID: {contact_id}")

    def clear_fields(self):
        self.selected_id = None
        self.name_var.set("")
        self.email_var.set("")
        self.phone_var.set("")
        self.category_var.set("Personal")
        self.notes_text.delete("1.0", tk.END)
        self.contact_list.selection_clear(0, tk.END)


def main():
    try:
        create_database()
        root = tk.Tk()
        ContactManager(root)
        root.mainloop()
    except Error as error:
        messagebox.showerror(
            "MySQL Connection Error",
            "Could not connect to MySQL.\n"
            "Check that the server is running and the username and "
            f"password are correct.\n\nDetails: {error}"
        )
    except tk.TclError as error:
        print("Tkinter GUI error:", error)


if __name__ == "__main__":
    main()
