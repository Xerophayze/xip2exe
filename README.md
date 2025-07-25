# Xip2exe Self-Extracting EXE Creator

A Python application that creates self-extracting executables from ZIP files with customizable extraction and execution options.

## Features

-   **GUI Interface**: Easy-to-use graphical interface built with `tkinter`.
-   **Flexible Extraction**: Choose where files are extracted (e.g., current directory or a custom path).
-   **Auto-Run**: Optionally run a program after extraction completes.
-   **Cleanup Option**: Automatically delete extracted files after the program finishes.
-   **Console Control**: Show or hide the console window during extraction.
-   **Admin Privileges**: Option to require the final executable to run as an administrator.
-   **Custom Icon**: Specify a custom `.ico` file for the generated executable.
-   **Single File Output**: Creates a standalone `.exe` that contains everything needed.

## Requirements

-   Python 3.6 or higher
-   `PyInstaller` (automatically installed by the setup script)

## Quick Start

1.  **Setup**: Run `setup.bat` to install dependencies.
2.  **Launch**: Run `run.bat` or execute `python main.py`.
3.  **Configure**: Select your ZIP file and configure the options in the GUI.
4.  **Build**: Click **Create Self-Extracting EXE**.

## How It Works

The application takes a `.zip` file and a set of configuration options and uses `PyInstaller` to bundle them into a single executable. The process is as follows:

1.  **Generate Payload**: A temporary Python script (`payload.py`) is created. This script contains:
    -   The base64-encoded `.zip` file.
    -   The user-defined configuration (extraction path, program to run, etc.).
2.  **Compile with PyInstaller**: `PyInstaller` is called to compile the `payload.py` into a standalone `.exe`.
    -   If a custom icon is provided, it's passed to `PyInstaller` with the `--icon` flag.
    -   If admin privileges are required, a manifest file is generated and passed with the `--manifest` flag.
3.  **Execution of Generated EXE**: When the final `.exe` is run:
    -   It decodes the base64 string back into the original `.zip` file in memory.
    -   It extracts the contents to the specified directory.
    -   It runs the target program (if specified) and waits for it to complete.
    -   It deletes the extracted files (if specified).

## Configuration Options

-   **Source ZIP File**: The `.zip` archive to be packaged.
-   **Output EXE Path**: Where to save the final self-extracting executable.
-   **Extract to Folder**: The directory where files will be extracted. Environment variables like `%TEMP%` are supported. Use `.` for the current directory.
-   **Run Program After Extract**: The relative path to a program inside the ZIP to run after extraction (e.g., `setup.exe` or `run.bat`).
-   **Delete Extracted Files After Run**: If checked, the extracted files will be removed after the specified program finishes.
-   **Show Console Window**: If checked, the console window will be visible during extraction. Uncheck for a silent background process.
-   **Require Administrator Privileges**: If checked, the generated `.exe` will prompt for admin rights when run.
-   **Custom Icon File**: Path to an `.ico` file to use as the icon for the generated `.exe`.

## File Structure

```
SelfExtractingEXE/
├── main.py           # The main GUI application
├── requirements.txt  # Python dependencies
├── setup.bat         # Setup script for Windows
├── run.bat           # Launch script for the application
└── README.md         # This file
```

## Troubleshooting

-   **Permission Denied / Access is Denied**: This error is often caused by antivirus software. Try temporarily disabling your antivirus or running the application as an administrator.
-   **PyInstaller not found**: Run `setup.bat` or install it manually via `pip install pyinstaller`.
-   **Generated EXE doesn't run program**: Ensure the path in "Run Program After Extract" is correct and relative to the root of the `.zip` file.

## License

This project is open source and available under the MIT License.
