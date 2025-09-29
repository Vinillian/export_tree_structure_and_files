
````markdown
# export_tree_structure_and_files

Python script to export folder structure and file contents to a text file.  
It works with any folder and records both the tree of folders/files and the contents of the files.

## Features

- Exports folder structure as a text tree
- Records file contents in readable format
- Works with any folder, not just `lib`
- Preserves relative paths
- Supports multiple file types

## Installation

1. Make sure you have Python 3 installed.
2. Clone the repository or download the script.

```bash
git clone https://github.com/Vinillian/export_tree_structure_and_files.git
cd export_tree_structure_and_files
````

## Usage

Run the script in your project directory:

```bash
python export_tree_structure_and_files.py
```

The script will generate a text file with the folder structure and file contents.

### Example output: Folder Structure

```text
lib/
├── main.dart
├── models/
│   ├── project.dart
│   └── task.dart
└── screens/
    └── project_list_screen.dart
```

### Example output: File Content

```text
File: main.dart
──────────────────────────────

import 'package:flutter/material.dart';

void main() {
    runApp(const MyApp());
}
```

### Notes on formatting

* Folders end with `/` to visually distinguish from files.
* Subfolders use `│`, `├──`, and `└──` for clear tree structure.
* Files have a separating line (`─`) before content for readability.
* This formatting works well in GitHub preview and preserves alignment.

## Attribution

This project uses the "Folder Tree" icon provided by Icons8:
[https://icons8.com/icon/49846/folder-tree](https://icons8.com/icon/49846/folder-tree)

## License

This project is open-source under the MIT License. See the LICENSE file for details.

```

