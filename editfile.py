import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
import sqlite3
import databasenew
from tkinter import filedialog as fd
import languagepack
from centerscreen import center_screen_geometry


class EditFile(tk.Toplevel):
    def __init__(self, parent, rowid, file_id, file_name, file_type, file_link):
        super().__init__()
        self.db = databasenew.FileManager()
        self.parent = parent
        self.selected_language = tk.StringVar(value="tr")
        self.i18n = languagepack.I18N(self.selected_language.get())
        self.geometry(center_screen_geometry(screen_width=self.winfo_screenwidth(),
                                             screen_height=self.winfo_screenheight(),
                                             window_width=420,
                                             window_height=165))
        self.title(self.i18n.title_filebook)
        self.resizable(False, False)
        self.configure(bg="#D7C6EE")
        self.file_name = tk.StringVar(value=file_name)
        self.file_type = tk.StringVar(value=file_type)
        self.file_link = tk.StringVar(value=file_link)
        self.file_id = file_id
        self.rowid = rowid
        self.create_widgets()
        self.bind_widgets()
        self.txt_file_name.focus_set()
        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def reload_gui_text(self, language):
        self.i18n = languagepack.I18N(language)
        self.title(self.i18n.title_filebook)
        self.lbl_file_name.configure(text=self.i18n.file_name)
        self.lbl_file_type.configure(text=self.i18n.file_type)
        self.lbl_file_link.configure(text=self.i18n.file_link)
        self.btn_file_link.configure(text=self.i18n.select_file)
        self.btn_update.configure(text=self.i18n.update_file)
        self.all_types = self.i18n.all_types
        self.text_file = self.i18n.text_file
        self.pdf_file = self.i18n.pdf_file
        self.file_name_empty = self.i18n.file_name_empty
        self.file_type_empty = self.i18n.file_type_empty
        self.file_link_empty = self.i18n.file_link_empty
        self.message_done = self.i18n.message_done
        self.message_file_saved = self.i18n.message_file_saved
        self.message_file_cannot_saved_update = self.i18n.message_file_cannot_saved_update

    def open_file(self):
        file_filter = (
            (self.i18n.all_types, "*.*"),
            (self.i18n.text_file, "*.txt"),
            (self.i18n.pdf_file, "*.pdf")
        )
        selected_file = fd.askopenfilename(filetypes=file_filter)
        self.txt_file_link.delete(0, "end")
        self.txt_file_link.insert(0, selected_file)

    def update_files(self):
        try:
            if (self.file_name.get() == ""):
                msg.showwarning(title=self.i18n.title_filebook, message=self.i18n.file_name_empty)
            elif (self.file_type.get() == ""):
                msg.showwarning(title=self.i18n.title_filebook, message=self.i18n.file_type_empty)
            elif (self.file_link.get() == ""):
                msg.showwarning(title=self.i18n.title_filebook, message=self.i18n.file_link_empty)
            else:
                # Update the recorded values in the database.
                self.db.edit_file(file_id=self.file_id, file_name=self.file_name.get(), file_type=self.file_type.get(),
                                  file_link=self.file_link.get())
                msg.showinfo(self.i18n.message_done, self.i18n.message_file_saved)
                # Update the values of the selected Treeview row that is in the parent window.
                self.parent.tv.item(self.rowid, values=(
                self.file_id, self.file_name.get(), self.file_type.get(), self.file_link.get()))
                self.close_window()
        except (tk.TclError, sqlite3.Error) as err:
            msg.showerror(title=self.i18n.title_filebook,
                          message=self.i18n.message_file_cannot_saved_update + "\n" + str(err))

    def clear_text_boxes(self):
        self.txt_file_name.delete(0, "end")
        self.txt_file_type.delete(0, "end")
        self.txt_file_link.delete(0, "end")

    def create_widgets(self):
        self.lbl_file_name = ttk.Label(self, text=self.i18n.file_name)
        self.lbl_file_name.grid(column=0, row=0, padx=15, pady=15)
        self.lbl_file_type = ttk.Label(self, text=self.i18n.file_type)
        self.lbl_file_type.grid(column=0, row=1, padx=15, pady=(0, 15))
        self.lbl_file_link = ttk.Label(self, text=self.i18n.file_link)
        self.lbl_file_link.grid(column=0, row=2, padx=15, pady=(0, 15))

        self.txt_file_name = ttk.Entry(self, textvariable=self.file_name, width=35)
        self.txt_file_name.grid(column=1, row=0, padx=(0, 15), pady=15)
        self.txt_file_type = ttk.Entry(self, textvariable=self.file_type, width=35)
        self.txt_file_type.grid(column=1, row=1, padx=(0, 15), pady=(0, 15))
        self.txt_file_link = ttk.Entry(self, textvariable=self.file_link, width=35)
        self.txt_file_link.grid(column=1, row=2, padx=(0, 15), pady=(0, 15))

        self.btn_file_link = ttk.Button(self, text=self.i18n.select_file, command=self.open_file)
        self.btn_file_link.grid(column=2, row=2, padx=(0, 15), pady=(0, 15))

        self.btn_update = ttk.Button(self, text=self.i18n.update_file, command=self.update_files)
        self.btn_update.grid(column=0, row=3, columnspan=2, pady=(0, 15))

        # Add a context menu
        self.context_menu = tk.Menu(self, tearoff=False)
        self.context_menu.add_radiobutton(label="English", variable=self.selected_language, value="en",
                                          command=lambda: self.reload_gui_text("en"))
        self.context_menu.add_radiobutton(label="Türkçe", variable=self.selected_language, value="tr",
                                          command=lambda: self.reload_gui_text("tr"))

    def bind_widgets(self):
        self.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        self.context_menu.tk_popup(x=event.x_root, y=event.y_root)

    def close_window(self):
        self.parent.deiconify()
        self.destroy()
