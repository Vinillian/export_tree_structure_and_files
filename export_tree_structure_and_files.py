import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# ---------- Функции ----------
def add_file():
    file = filedialog.askopenfilename()
    if file:
        insert_path(file)

def add_folder():
    folder = filedialog.askdirectory()
    if folder:
        insert_path(folder)

def insert_path(path):
    """Вставляет путь в единое текстовое поле"""
    current = paths_text.get("1.0", tk.END).strip()
    if current:
        paths_text.insert(tk.END, f"\n{path}")
    else:
        paths_text.insert(tk.END, path)
    auto_expand_paths_text()

def clear_paths():
    paths_text.delete("1.0", tk.END)
    update_tree_display()
    auto_expand_paths_text()

def get_paths():
    text = paths_text.get("1.0", tk.END).strip()
    return [line.strip() for line in text.splitlines() if line.strip()]

# ---------- Авторасширение поля путей ----------
def auto_expand_paths_text():
    lines = len(paths_text.get("1.0", tk.END).splitlines())
    lines = min(max(lines, 5), 20)  # от 5 до 20 строк
    paths_text.config(height=lines)

# ---------- Построение дерева ----------
def add_to_tree(tree, root_path, path, include_children=False):
    rel_path = os.path.relpath(path, root_path)
    parts = rel_path.split(os.sep)
    node = tree
    for part in parts:
        if part not in node:
            node[part] = {}
        node = node[part]
    if include_children and os.path.isdir(path):
        for child in sorted(os.listdir(path)):
            add_to_tree(tree, root_path, os.path.join(path, child), include_children=True)

def build_tree(paths, root_path):
    tree = {}
    for path in paths:
        if os.path.isdir(path):
            add_to_tree(tree, root_path, path, include_children=True)
        else:
            add_to_tree(tree, root_path, path, include_children=False)
    return tree

def print_tree_to_text(tree, prefix=""):
    lines = []
    keys = sorted(tree.keys())
    for i, key in enumerate(keys):
        is_last = (i == len(keys) - 1)
        connector = "└── " if is_last else "├── "
        entry = key + "/" if tree[key] else key
        lines.append(f"{prefix}{connector}{entry}")
        if tree[key]:
            lines.extend(print_tree_to_text(tree[key], prefix + ("    " if is_last else "│   ")))
    return lines

def update_tree_display():
    paths = get_paths()
    tree_text.delete("1.0", tk.END)
    if not paths:
        return
    try:
        root_path = os.path.commonpath(paths)
        tree = build_tree(paths, root_path)
        tree_lines = [f"{os.path.basename(root_path)}/"] + print_tree_to_text(tree)
        tree_text.insert(tk.END, "\n".join(tree_lines))
    except Exception as e:
        tree_text.insert(tk.END, f"Error building tree: {e}")

# ---------- Экспорт ----------
def write_file_content(file_path, text_file, base_path=None):
    rel_path = os.path.relpath(file_path, base_path) if base_path else file_path
    text_file.write(f"\n=== File: {rel_path} ===\n\n")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text_file.write(f.read())
    except Exception as e:
        text_file.write(f"[Cannot read file: {e}]\n")

def collect_files_from_paths(paths):
    files = []
    for path in paths:
        if os.path.isfile(path):
            files.append(path)
        elif os.path.isdir(path):
            for dir_root, dirs, fs in os.walk(path):
                for f in fs:
                    files.append(os.path.join(dir_root, f))
    return files

def export_tree():
    paths = get_paths()
    if not paths:
        messagebox.showwarning("Warning", "No files or folders specified!")
        return
    output_file = output_entry.get().strip()
    if not output_file:
        output_file = "project_tree.txt"
    if not output_file.endswith(".txt"):
        output_file += ".txt"
    try:
        root_path = os.path.commonpath(paths)
        tree = build_tree(paths, root_path)
        files_to_write = collect_files_from_paths(paths)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"=== Project: {root_path} ===\n\n")
            f.write(f"{os.path.basename(root_path)}/\n")
            for line in print_tree_to_text(tree):
                f.write(line + "\n")
            f.write("\n\n=== Files content ===\n")
            for file in files_to_write:
                write_file_content(file, f, base_path=root_path)
        messagebox.showinfo("Success", f"Exported to {output_file}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ---------- Обработка вставки ----------
def handle_paste(event):
    try:
        # Получаем текст из буфера обмена
        clipboard = root.clipboard_get()
        if clipboard:
            # Вставляем текст в текущую позицию курсора
            event.widget.insert(tk.INSERT, clipboard)
        return "break"  # Предотвращаем стандартную обработку
    except tk.TclError:
        pass  # Если в буфере обмена нет текста

# ---------- GUI ----------
root = tk.Tk()
root.title("Project Tree Exporter")
root.geometry("1000x600")

main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Левая панель кнопок
buttons_frame = tk.Frame(main_frame)
buttons_frame.pack(side="left", fill="y", padx=5)

tk.Button(buttons_frame, text="Add File", width=15, command=add_file).pack(pady=3)
tk.Button(buttons_frame, text="Add Folder", width=15, command=add_folder).pack(pady=3)
tk.Button(buttons_frame, text="Clear Paths", width=15, command=clear_paths).pack(pady=3)
tk.Button(buttons_frame, text="Update Tree", width=15, command=update_tree_display).pack(pady=3)
tk.Button(buttons_frame, text="Export", width=15, command=export_tree).pack(pady=20)

# Правая панель
right_frame = tk.Frame(main_frame)
right_frame.pack(side="left", fill="both", expand=True)

tk.Label(right_frame, text="Enter paths (one per line):").pack(anchor="w")
paths_text = scrolledtext.ScrolledText(right_frame, width=80, height=5)
paths_text.pack(fill="x", pady=5)

# Правильная обработка Ctrl+V и Shift+Insert
paths_text.bind("<Control-v>", handle_paste)
paths_text.bind("<Control-V>", handle_paste)  # Для Caps Lock
paths_text.bind("<Shift-Insert>", handle_paste)

# Авторасширение при старте
auto_expand_paths_text()

# Поле для имени итогового файла
output_frame = tk.Frame(right_frame)
output_frame.pack(pady=5, fill="x")
tk.Label(output_frame, text="Output file name:").pack(side="left")
output_entry = tk.Entry(output_frame)
output_entry.pack(side="left", fill="x", expand=True)
output_entry.insert(0, "project_tree.txt")

# Также добавим поддержку вставки для поля ввода имени файла
output_entry.bind("<Control-v>", handle_paste)
output_entry.bind("<Control-V>", handle_paste)
output_entry.bind("<Shift-Insert>", handle_paste)

# Текстовое поле для дерева проекта
tk.Label(right_frame, text="Project Tree:").pack(anchor="w", pady=(10,0))
tree_text = scrolledtext.ScrolledText(right_frame, width=80, height=25)
tree_text.pack(fill="both", expand=True, pady=5)

# Также добавим поддержку вставки для поля отображения дерева
tree_text.bind("<Control-v>", handle_paste)
tree_text.bind("<Control-V>", handle_paste)
tree_text.bind("<Shift-Insert>", handle_paste)

# Обработка закрытия окна корректно
def on_close():
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()