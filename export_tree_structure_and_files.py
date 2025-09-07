import os
import argparse

def export_tree(folder_path, output_file):
    lines = []

    def walk_dir(current_path, prefix=""):
        entries = sorted(os.listdir(current_path))
        for i, item in enumerate(entries):
            item_path = os.path.join(current_path, item)
            is_last = i == len(entries) - 1
            connector = "└──" if is_last else "├──"

            if os.path.isdir(item_path):
                lines.append(f"{prefix}{connector} Folder: {item}")
                extension = "    " if is_last else "│   "
                walk_dir(item_path, prefix + extension)
            else:
                lines.append(f"{prefix}{connector} File: {item}")

    # Создаём дерево
    folder_name = os.path.basename(os.path.abspath(folder_path))
    lines.append(f"Folder {folder_name}")
    walk_dir(folder_path)

    # Записываем дерево и содержимое файлов
    with open(output_file, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")

        f.write("\n\n=== File contents ===\n\n")
        for root, dirs, files in os.walk(folder_path):
            for file in sorted(files):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, folder_path)
                f.write(f"File: {rel_path}\n\n")
                try:
                    with open(file_path, "r", encoding="utf-8") as code_file:
                        f.write(code_file.read() + "\n\n")
                except Exception as e:
                    f.write(f"[Error reading file: {e}]\n\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export folder structure and file contents to a text file.")
    parser.add_argument("--folder", type=str, default="lib", help="Folder to export")
    parser.add_argument("--output", type=str, default="folder_structure.txt", help="Output text file name")
    args = parser.parse_args()

    export_tree(args.folder, args.output)
    print(f"Export completed: {args.output}")
