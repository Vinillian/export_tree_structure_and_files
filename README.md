```markdown
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

```
git clone https://github.com/Vinillian/export_tree_structure_and_files.git
cd export_tree_structure_and_files
```

## Usage

Run the script in your project directory:

```
python export_tree_structure_and_files.py
```

The script will generate a text file with the folder structure and file contents.

### Example output:

```
Folder: lib
|-- File: main.dart
|-- Folder: models
|    |-- File: project.dart
|    |-- File: task.dart
|-- Folder: screens
|    |-- File: project_list_screen.dart
```

```
File: main.dart

import 'package:flutter/material.dart';

void main() {
    runApp(const MyApp());
}
```

## Attribution

This project uses the "Folder Tree" icon provided by Icons8:  
[https://icons8.com/icon/49846/folder-tree](https://icons8.com/icon/49846/folder-tree)

## License

This project is open-source under the MIT License. See the LICENSE file for details.
```

