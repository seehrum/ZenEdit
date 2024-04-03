import tkinter as tk
from tkinter import filedialog, colorchooser, font, simpledialog, Toplevel, Listbox, messagebox
import json
import os

class Zedit:
    def __init__(self, root):
        self.root = root
        self.root.title("Zedit")
        self.config_file = 'editor_config.json'
        self.auto_save_file = 'autosave.txt'
        self.load_config()
        self.fullScreenState = False
        self.root.bind("<F11>", self.toggleFullScreen)
        self.root.bind("<F2>", lambda event: self.quit())
        self.root.bind("<F10>", lambda event: self.open_file())
        self.root.bind("<F12>", lambda event: self.save_file())
        self.menu = tk.Menu(root)
        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label="Open (F10)", command=self.open_file)
        self.file_menu.add_command(label="Save (F12)", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit (F2)", command=self.quit)
        self.edit_menu = tk.Menu(self.menu, tearoff=0)
        self.edit_menu.add_command(label="Change Root Background Color", command=self.change_root_bg_color)
        self.edit_menu.add_command(label="Change Background Color", command=self.change_bg_color)
        self.edit_menu.add_command(label="Change Text Color", command=self.change_fg_color)
        self.edit_menu.add_command(label="Change Cursor Color", command=self.change_cursor_color)
        self.edit_menu.add_command(label="Change Selection Color", command=self.change_selection_color)
        self.edit_menu.add_command(label="Change Selection Text Color", command=self.change_selection_text_color)
        self.edit_menu.add_command(label="Toggle Block Cursor", command=self.toggle_block_cursor)
        self.edit_menu.add_command(label="Change Font", command=self.change_font)
        self.edit_menu.add_command(label="Change Font Size", command=self.change_font_size)
        self.edit_menu.add_command(label="Set Line Spacing", command=self.set_line_spacing)
        self.view_menu = tk.Menu(self.menu, tearoff=0)
        self.view_menu.add_command(label="FullScreen (F11)", command=self.toggleFullScreen)
        self.view_menu.add_command(label="Set Text Area Size", command=self.set_text_area_size)
        self.view_menu.add_command(label="Toggle Border", command=self.toggle_border)
        self.view_menu.add_command(label="Toggle Cursor Visibility", command=self.toggle_cursor_visibility)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.menu.add_cascade(label="View", menu=self.view_menu)
        self.root.config(menu=self.menu, bg=self.config['root_bg_color'])
        self.frame = tk.Frame(root, bg=self.config['bg_color'])
        self.frame.pack(expand=True)
        self.current_font = font.Font(family=self.config['font_family'], size=self.config['font_size'],
                                      weight="bold" if self.config.get('font_bold', False) else "normal",
                                      slant="italic" if self.config.get('font_italic', False) else "roman")
        self.text_area = tk.Text(self.frame, font=self.current_font, bg=self.config['bg_color'], fg=self.config['fg_color'],
                                 insertbackground=self.config['cursor_color'], insertwidth=4 if self.config['block_cursor'] else 2,
                                 spacing3=self.config.get('line_spacing', 4), borderwidth=0, wrap=tk.WORD, highlightthickness=0,
                                 selectbackground=self.config.get('selection_color', '#3399ff'),
                                 selectforeground=self.config.get('selection_text_color', '#ffffff'),
                                 width=self.config.get('text_width', 80), height=self.config.get('text_height', 25))
        self.text_area.pack(side="top", fill="both", expand="yes")
        self.auto_save_interval = 5000
        self.auto_save()

    def load_config(self):
        if os.path.isfile(self.config_file):
            with open(self.config_file, 'r') as file:
                self.config = json.load(file)
        else:
            self.config = {}
        self.config.setdefault('root_bg_color', '#1e1e1e')
        self.config.setdefault('font_family', 'Arial')
        self.config.setdefault('font_size', 16)
        self.config.setdefault('font_bold', False)
        self.config.setdefault('font_italic', False)
        self.config.setdefault('bg_color', '#1e1e1e')
        self.config.setdefault('fg_color', '#ffffff')
        self.config.setdefault('cursor_color', 'white')
        self.config.setdefault('selection_color', '#3399ff')
        self.config.setdefault('selection_text_color', '#ffffff')
        self.config.setdefault('block_cursor', False)
        self.config.setdefault('text_width', 80)
        self.config.setdefault('text_height', 25)
        self.config.setdefault('line_spacing', 4)

    def save_config(self):
        with open(self.config_file, 'w') as file:
            json.dump(self.config, file)

    def auto_save(self):
        with open(self.auto_save_file, 'w') as file:
            file.write(self.text_area.get(1.0, tk.END))
        self.root.after(self.auto_save_interval, self.auto_save)

    def toggleFullScreen(self, event=None):
        self.fullScreenState = not self.fullScreenState
        self.root.attributes("-fullscreen", self.fullScreenState)
        if self.fullScreenState:
            self.root.config(menu="")
        else:
            self.root.config(menu=self.menu)

    def quit(self):
        if messagebox.askyesno("Save on Exit", "Do you want to save the changes before exiting?"):
            self.save_file()
        self.save_config()
        self.root.quit()

    def open_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if not filepath:
            return
        self.text_area.delete(1.0, tk.END)
        with open(filepath, "r") as file:
            self.text_area.insert(tk.END, file.read())

    def save_file(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if not filepath:
            return
        with open(filepath, "w") as file:
            file.write(self.text_area.get(1.0, tk.END))

    def toggle_block_cursor(self):
        self.config['block_cursor'] = not self.config['block_cursor']
        insert_width = 4 if self.config['block_cursor'] else 2
        self.text_area.config(insertwidth=insert_width)
        self.save_config()

    def change_bg_color(self):
        color = colorchooser.askcolor(title="Choose background color")[1]
        if color:
            self.config['bg_color'] = color
            self.text_area.config(bg=color)
            self.frame.config(bg=color)
            self.save_config()

    def change_fg_color(self):
        color = colorchooser.askcolor(title="Choose text color")[1]
        if color:
            self.config['fg_color'] = color
            self.text_area.config(fg=color)
            self.save_config()

    def change_cursor_color(self):
        color = colorchooser.askcolor(title="Choose cursor color")[1]
        if color:
            self.config['cursor_color'] = color
            self.text_area.config(insertbackground=color)
            self.save_config()

    def change_selection_color(self):
        color = colorchooser.askcolor(title="Choose selection color")[1]
        if color:
            self.config['selection_color'] = color
            self.text_area.config(selectbackground=color)
            self.save_config()

    def change_selection_text_color(self):
        color = colorchooser.askcolor(title="Choose selection text color")[1]
        if color:
            self.config['selection_text_color'] = color
            self.text_area.config(selectforeground=color)
            self.save_config()

    def change_root_bg_color(self):
        color = colorchooser.askcolor(title="Choose root background color")[1]
        if color:
            self.config['root_bg_color'] = color
            self.root.config(bg=color)
            self.save_config()

    def change_font(self):
        font_window = Toplevel(self.root)
        font_window.title("Choose Font")
        font_listbox = Listbox(font_window)
        font_listbox.pack(side="left", fill="y")
        scrollbar = tk.Scrollbar(font_window, orient="vertical", command=font_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        font_listbox.config(yscrollcommand=scrollbar.set)
        for fnt in font.families():
            font_listbox.insert(tk.END, fnt)

        is_bold = tk.BooleanVar(value=self.config.get('font_bold', False))
        is_italic = tk.BooleanVar(value=self.config.get('font_italic', False))
        bold_check = tk.Checkbutton(font_window, text="Bold", variable=is_bold)
        italic_check = tk.Checkbutton(font_window, text="Italic", variable=is_italic)
        bold_check.pack(side="top", fill="x")
        italic_check.pack(side="top", fill="x")

        def on_font_select(event):
            selection = font_listbox.curselection()
            if selection:
                font_name = font_listbox.get(selection[0])
                font_size = simpledialog.askinteger("Font Size", "Enter font size:", initialvalue=self.config['font_size'])
                if font_size:
                    self.config['font_family'] = font_name
                    self.config['font_size'] = font_size
                    self.config['font_bold'] = is_bold.get()
                    self.config['font_italic'] = is_italic.get()
                    self.current_font = font.Font(family=font_name, size=font_size,
                                                  weight="bold" if is_bold.get() else "normal",
                                                  slant="italic" if is_italic.get() else "roman")
                    self.text_area.config(font=self.current_font)
                    self.save_config()
                    font_window.destroy()

        font_listbox.bind('<<ListboxSelect>>', on_font_select)

    def set_text_area_size(self):
        width = simpledialog.askinteger("Text Area Width", "Enter width:", initialvalue=self.config.get('text_width', 80))
        height = simpledialog.askinteger("Text Area Height", "Enter height:", initialvalue=self.config.get('text_height', 25))
        if width and height:
            self.config['text_width'] = width
            self.config['text_height'] = height
            self.text_area.config(width=width, height=height)
            self.save_config()

    def set_line_spacing(self):
        spacing = simpledialog.askfloat("Line Spacing", "Enter line spacing:", initialvalue=self.config.get('line_spacing', 4))
        if spacing:
            self.config['line_spacing'] = spacing
            self.text_area.config(spacing3=spacing)
            self.save_config()

    def change_font_size(self):
        font_size = simpledialog.askinteger("Font Size", "Enter font size:", initialvalue=self.config['font_size'])
        if font_size:
            self.config['font_size'] = font_size
            self.current_font = font.Font(family=self.config['font_family'], size=font_size,
                                          weight="bold" if self.config.get('font_bold', False) else "normal",
                                          slant="italic" if self.config.get('font_italic', False) else "roman")
            self.text_area.config(font=self.current_font)
            self.save_config()

    def toggle_border(self):
        current_thickness = self.text_area.cget('highlightthickness')
        new_thickness = 0 if current_thickness > 0 else 1
        self.text_area.config(highlightthickness=new_thickness)

    def toggle_cursor_visibility(self):
        if self.text_area['cursor'] in ['', 'xterm']:
            self.text_area.config(cursor='none')
        else:
            self.text_area.config(cursor='xterm')

if __name__ == "__main__":
    root = tk.Tk()
    editor = Zedit(root)
    root.mainloop()