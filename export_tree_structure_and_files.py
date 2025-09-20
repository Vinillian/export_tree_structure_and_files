import os

# Указываем только нужные папки/файлы
paths = [
    r"C:\Users\user\task_tracker_new\lib",
    r"C:\Users\user\task_tracker_new\android\app\src\main\AndroidManifest.xml",
    r"C:\Users\user\task_tracker_new\android\app\build.gradle.kts",
    r"C:\Users\user\task_tracker_new\android\build.gradle.kts",
    r"C:\Users\user\task_tracker_new\android\gradle.properties",
    r"C:\Users\user\task_tracker_new\android\local.properties",
    r"C:\Users\user\task_tracker_new\android\settings.gradle.kts",
    r"C:\Users\user\task_tracker_new\.gitignore",
    r"C:\Users\user\task_tracker_new\pubspec.yaml",
]

output_file = "project_tree.txt"


# ---------- Построение структуры ----------
def add_to_tree(tree, root, path, include_children=False):
    """Добавляет файл или папку в дерево"""
    rel_path = os.path.relpath(path, root)
    parts = rel_path.split(os.sep)
    node = tree
    for i, part in enumerate(parts):
        if part not in node:
            node[part] = {}
        node = node[part]

    # если это папка и нужно рекурсивно добавить все содержимое
    if include_children and os.path.isdir(path):
        for child in sorted(os.listdir(path)):
            add_to_tree(tree, root, os.path.join(path, child), include_children=True)


def build_tree(paths, root):
    tree = {}
    for path in paths:
        if os.path.isdir(path):
            add_to_tree(tree, root, path, include_children=True)
        else:
            add_to_tree(tree, root, path, include_children=False)
    return tree


def print_tree(tree, prefix="", text_file=None):
    keys = sorted(tree.keys())
    for i, key in enumerate(keys):
        is_last = (i == len(keys) - 1)
        connector = "└── " if is_last else "├── "
        entry = key + "/" if tree[key] else key
        if text_file:
            text_file.write(f"{prefix}{connector}{entry}\n")
        extension = "    " if is_last else "│   "
        if tree[key]:
            print_tree(tree[key], prefix + extension, text_file)


# ---------- Запись содержимого ----------
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
            for root, dirs, fs in os.walk(path):
                for f in fs:
                    files.append(os.path.join(root, f))
    return files


# ---------- Основной код ----------
root_path = os.path.commonpath(paths)
tree = build_tree(paths, root_path)
files = collect_files_from_paths(paths)

with open(output_file, "w", encoding="utf-8") as f:
    f.write(f"=== Проект: {root_path} ===\n\n")

    # 1. Дерево проекта (ограниченное paths)
    f.write("=== Структура выбранных файлов и папок ===\n")
    f.write(f"{os.path.basename(root_path)}/\n")
    print_tree(tree, text_file=f)

    # 2. Содержимое файлов
    f.write("\n\n=== Содержимое файлов ===\n")
    for file in files:
        write_file_content(file, f, base_path=root_path)

print(f"Готово! Структура и содержимое записаны в {output_file}")
