import os

lib_path = "lib"
output_file = "lib_project.txt"


def write_tree_graph(root_path, text_file, prefix=""):
    entries = sorted(os.listdir(root_path))
    total = len(entries)
    for index, entry in enumerate(entries):
        entry_path = os.path.join(root_path, entry)
        is_last = (index == total - 1)
        connector = "└── " if is_last else "├── "
        if os.path.isdir(entry_path):
            text_file.write(f"{prefix}{connector}Folder: {entry}\n")
            extension = "    " if is_last else "│   "
            write_tree_graph(entry_path, text_file, prefix + extension)
        else:
            text_file.write(f"{prefix}{connector}File: {entry}\n")


def write_files_content(root_path, text_file):
    for root, dirs, files in os.walk(root_path):
        for file_name in sorted(files):
            file_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(file_path, root_path)
            text_file.write(f"\nFile: {relative_path}\n\n")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        text_file.write(line)  # сохраняем естественные отступы
            except Exception as e:
                text_file.write(f"[Cannot read file: {e}]\n")


with open(output_file, 'w', encoding='utf-8') as f:
    f.write("=== Дерево папок и файлов ===\n\n")
    f.write("Folder lib\n")
    write_tree_graph(lib_path, f)

    f.write("\n=== Содержимое файлов ===\n")
    write_files_content(lib_path, f)

print(f"Готово! Дерево и содержимое папки lib записано в {output_file}")
