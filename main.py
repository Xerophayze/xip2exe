#!/usr/bin/env python3
"""
Title: Xip2exe
Self-Extracting EXE Creator
Creates self-extracting executables from ZIP files with customizable options.

Author: Eric Thorup
Date: 2025-07-25
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import shutil
import tempfile
import subprocess
from pathlib import Path

class SelfExtractingEXECreator:
    def __init__(self, root):
        self.root = root
        self.root.title("Self-Extracting EXE Creator")
        self.root.geometry("600x650")
        self.root.resizable(True, True)
        
        # Variables
        self.zip_file_path = tk.StringVar()
        self.output_exe_path = tk.StringVar()
        self.extract_folder = tk.StringVar(value="%TEMP%\\SysUpdate")  # Default to Windows temp directory
        self.run_after_extract = tk.StringVar()
        self.delete_after_run = tk.BooleanVar(value=False)
        self.show_console = tk.BooleanVar(value=True)
        self.require_admin = tk.BooleanVar(value=False)
        self.inherit_admin = tk.BooleanVar(value=True)
        self.icon_file_path = tk.StringVar()
        self.upx_enabled_var = tk.BooleanVar(value=False)
        self.upx_path_var = tk.StringVar()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        row = 0
        
        # Title
        title_label = ttk.Label(main_frame, text="Self-Extracting EXE Creator", 
                               font=('TkDefaultFont', 16, 'bold'))
        title_label.grid(row=row, column=0, columnspan=3, pady=(0, 20))
        row += 1
        
        # ZIP file selection
        ttk.Label(main_frame, text="Source ZIP File:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.zip_file_path, width=50).grid(row=row, column=1, sticky=(tk.W, tk.E), padx=(5, 5))
        ttk.Button(main_frame, text="Browse", command=self.browse_zip_file).grid(row=row, column=2, padx=(0, 0))
        row += 1
        
        # Output EXE path
        ttk.Label(main_frame, text="Output EXE File:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_exe_path, width=50).grid(row=row, column=1, sticky=(tk.W, tk.E), padx=(5, 5))
        ttk.Button(main_frame, text="Browse", command=self.browse_output_exe).grid(row=row, column=2, padx=(0, 0))
        row += 1
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=20)
        row += 1
        
        # Extraction options label
        ttk.Label(main_frame, text="Extraction Options", 
                 font=('TkDefaultFont', 12, 'bold')).grid(row=row, column=0, columnspan=3, pady=(0, 10))
        row += 1
        
        # Extract folder
        ttk.Label(main_frame, text="Extract to Folder:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.extract_folder, width=50).grid(row=row, column=1, sticky=(tk.W, tk.E), padx=(5, 5))
        ttk.Button(main_frame, text="Browse", command=self.browse_extract_folder).grid(row=row, column=2, padx=(0, 0))
        row += 1
        
        # Help text for extract folder
        help_text = ttk.Label(main_frame, text="Use '.' for current directory, '%TEMP%\\folder' for temp, or specify a path", 
                             font=('TkDefaultFont', 8), foreground='gray')
        help_text.grid(row=row, column=1, sticky=tk.W, padx=(5, 0))
        row += 1
        
        # Run after extract
        ttk.Label(main_frame, text="Run After Extract:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.run_after_extract, width=50).grid(row=row, column=1, sticky=(tk.W, tk.E), padx=(5, 5))
        ttk.Button(main_frame, text="Browse", command=self.browse_run_file).grid(row=row, column=2, padx=(0, 0))
        row += 1
        
        # Help text for run after extract
        help_text2 = ttk.Label(main_frame, text="Relative path to file within the ZIP (e.g., 'setup.exe' or 'bin/myapp.exe')", 
                              font=('TkDefaultFont', 8), foreground='gray')
        help_text2.grid(row=row, column=1, sticky=tk.W, padx=(5, 0))
        row += 1
        
        # Checkboxes
        ttk.Checkbutton(main_frame, text="Delete extracted files after program finishes", 
                       variable=self.delete_after_run).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Checkbutton(main_frame, text="Show console window during extraction", 
                       variable=self.show_console).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Checkbutton(main_frame, text="Require administrator privileges to run", 
                       variable=self.require_admin).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        row += 1
        
        ttk.Checkbutton(main_frame, text="Pass admin privileges to launched program", 
                       variable=self.inherit_admin).grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        row += 1
        
        # Icon file selection
        ttk.Label(main_frame, text="Application Icon:").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.icon_file_path, width=50).grid(row=row, column=1, sticky=(tk.W, tk.E), padx=(5, 5))
        ttk.Button(main_frame, text="Browse", command=self.browse_icon_file).grid(row=row, column=2, padx=(0, 0))
        row += 1
        
        # Help text for icon
        help_text3 = ttk.Label(main_frame, text="Optional: Select .ico file for custom application icon", 
                              font=('TkDefaultFont', 8), foreground='gray')
        help_text3.grid(row=row, column=1, sticky=tk.W, padx=(5, 0))
        row += 1
        
        # UPX compression
        self.upx_enabled_checkbutton = ttk.Checkbutton(main_frame, text="Compress EXE with UPX", variable=self.upx_enabled_var, command=self.toggle_upx_path)
        self.upx_enabled_checkbutton.grid(row=row, column=0, columnspan=3, sticky='w', padx=5, pady=2)
        row += 1
        
        self.upx_path_label = ttk.Label(main_frame, text="UPX Directory:")
        self.upx_path_label.grid(row=row, column=0, sticky='w', padx=5)
        self.upx_path_entry = ttk.Entry(main_frame, textvariable=self.upx_path_var, width=50)
        self.upx_path_entry.grid(row=row, column=1, sticky='ew', padx=5)
        self.upx_browse_button = ttk.Button(main_frame, text="Browse...", command=self.browse_upx_path)
        self.upx_browse_button.grid(row=row, column=2, sticky='w', padx=5)
        row += 1
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=20)
        row += 1
        
        # Create button
        create_button = ttk.Button(main_frame, text="Create Self-Extracting EXE", 
                                  command=self.create_exe, style='Accent.TButton')
        create_button.grid(row=row, column=0, columnspan=3, pady=10)
        row += 1
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        row += 1
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready to create self-extracting EXE")
        self.status_label.grid(row=row, column=0, columnspan=3, pady=5)
        
        self.toggle_upx_path() # Set initial state
        
    def browse_zip_file(self):
        filename = filedialog.askopenfilename(
            title="Select ZIP file",
            filetypes=[("ZIP files", "*.zip"), ("All files", "*.*")]
        )
        if filename:
            self.zip_file_path.set(filename)
            # Auto-suggest output filename
            if not self.output_exe_path.get():
                base_name = os.path.splitext(os.path.basename(filename))[0]
                output_path = os.path.join(os.path.dirname(filename), f"{base_name}_installer.exe")
                self.output_exe_path.set(output_path)
    
    def browse_output_exe(self):
        filename = filedialog.asksaveasfilename(
            title="Save self-extracting EXE as",
            defaultextension=".exe",
            filetypes=[("Executable files", "*.exe"), ("All files", "*.*")]
        )
        if filename:
            self.output_exe_path.set(filename)
    
    def browse_extract_folder(self):
        folder = filedialog.askdirectory(title="Select extraction folder")
        if folder:
            self.extract_folder.set(folder)
    
    def browse_run_file(self):
        # This is a bit tricky since we need to show files within the ZIP
        # For now, just let the user type the path
        messagebox.showinfo("Run After Extract", 
                           "Enter the relative path to the file within the ZIP archive.\n\n"
                           "Examples:\n"
                           "• setup.exe\n"
                           "• bin/myapp.exe\n"
                           "• installer/install.bat")
    
    def browse_icon_file(self):
        filename = filedialog.askopenfilename(
            title="Select icon file",
            filetypes=[("Icon files", "*.ico"), ("All files", "*.*")]
        )
        if filename:
            self.icon_file_path.set(filename)
    
    def browse_upx_path(self):
        dirpath = filedialog.askdirectory(title="Select UPX Directory")
        if dirpath:
            self.upx_path_var.set(dirpath)
    
    def toggle_upx_path(self):
        state = 'normal' if self.upx_enabled_var.get() else 'disabled'
        self.upx_path_entry.config(state=state)
        self.upx_browse_button.config(state=state)
        self.upx_path_label.config(state=state)
    
    def create_exe(self):
        # Validate inputs
        if not self.zip_file_path.get():
            messagebox.showerror("Error", "Please select a ZIP file")
            return
        
        if not self.output_exe_path.get():
            messagebox.showerror("Error", "Please specify output EXE path")
            return
        
        if not os.path.exists(self.zip_file_path.get()):
            messagebox.showerror("Error", "ZIP file does not exist")
            return
        
        # Start progress
        self.progress.start()
        self.status_label.config(text="Creating self-extracting EXE...")
        self.root.update()
        
        try:
            self._create_extractor()
            self.progress.stop()
            self.status_label.config(text="Self-extracting EXE created successfully!")
            messagebox.showinfo("Success", f"Self-extracting EXE created:\n{self.output_exe_path.get()}")
        except Exception as e:
            self.progress.stop()
            self.status_label.config(text="Error creating EXE")
            messagebox.showerror("Error", f"Failed to create EXE:\n{str(e)}")
    
    def _create_extractor(self):
        """Create the self-extracting executable"""
        # Try different build strategies to avoid antivirus interference
        strategies = [
            ("User Temp Directory", self._build_in_user_temp),
            ("Desktop Directory", self._build_in_desktop),
            ("Custom Temp Directory", self._build_in_custom_temp)
        ]
        
        last_error = None
        for strategy_name, build_func in strategies:
            try:
                self.status_label.config(text=f"Trying build strategy: {strategy_name}...")
                self.root.update()
                build_func()
                return  # Success!
            except Exception as e:
                last_error = e
                print(f"Strategy '{strategy_name}' failed: {e}")
                continue
        
        # If all strategies failed, raise the last error
        raise last_error
    
    def _build_in_user_temp(self):
        """Build using user's temp directory"""
        temp_base = os.path.expanduser("~/AppData/Local/Temp")
        temp_dir = os.path.join(temp_base, f"SelfExtractingEXE_{os.getpid()}")
        os.makedirs(temp_dir, exist_ok=True)
        
        try:
            self._build_in_directory(temp_dir)
        finally:
            # Clean up
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
    
    def _build_in_desktop(self):
        """Build using desktop directory"""
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        temp_dir = os.path.join(desktop, f"SelfExtractingEXE_Build_{os.getpid()}")
        os.makedirs(temp_dir, exist_ok=True)
        
        try:
            self._build_in_directory(temp_dir)
        finally:
            # Clean up
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
    
    def _build_in_custom_temp(self):
        """Build using Python's tempfile with custom prefix"""
        with tempfile.TemporaryDirectory(prefix="SFX_", suffix="_build") as temp_dir:
            self._build_in_directory(temp_dir)
    
    def _build_in_directory(self, temp_dir):
        """Build the extractor in the specified directory"""
        # Create the extractor script
        extractor_script = self._generate_extractor_script()
        script_path = os.path.join(temp_dir, "extractor.py")
        
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(extractor_script)
        
        # Copy the ZIP file to temp directory
        zip_dest = os.path.join(temp_dir, "payload.zip")
        shutil.copy2(self.zip_file_path.get(), zip_dest)
        
        # Create config file
        config = {
            'extract_folder': self.extract_folder.get(),
            'run_after_extract': self.run_after_extract.get(),
            'delete_after_run': self.delete_after_run.get(),
            'show_console': self.show_console.get(),
            'require_admin': self.require_admin.get(),
            'inherit_admin': self.inherit_admin.get()
        }
        
        config_path = os.path.join(temp_dir, "config.json")
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        
        # Use PyInstaller to create the EXE
        self._build_with_pyinstaller(temp_dir, script_path, zip_dest, config_path)
    
    def _generate_extractor_script(self):
        """Generate the Python script that will be embedded in the EXE"""
        return '''#!/usr/bin/env python3
"""
Self-Extracting Archive
This script extracts embedded files and optionally runs a program.
"""

import os
import sys
import zipfile
import json
import subprocess
import tempfile
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def show_error(message):
    """Show error message"""
    try:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Extraction Error", message)
        root.destroy()
    except:
        print(f"ERROR: {message}")

def show_info(message):
    """Show info message"""
    try:
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Self-Extracting Archive", message)
        root.destroy()
    except:
        print(f"INFO: {message}")

def main():
    try:
        # Load configuration
        config_path = get_resource_path("config.json")
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        extract_folder = config.get('extract_folder', '.')
        run_after_extract = config.get('run_after_extract', '')
        delete_after_run = config.get('delete_after_run', False)
        show_console = config.get('show_console', True)
        require_admin = config.get('require_admin', False)
        inherit_admin = config.get('inherit_admin', True)
        
        # Determine extraction path
        if extract_folder == '.':
            extract_path = os.getcwd()
        elif extract_folder.startswith('%TEMP%'):
            # Handle Windows temp directory variables
            temp_dir = os.environ.get('TEMP', os.environ.get('TMP', 'C:\\Windows\\Temp'))
            extract_path = extract_folder.replace('%TEMP%', temp_dir)
            extract_path = os.path.expandvars(extract_path)  # Expand any other variables
        elif os.path.isabs(extract_folder):
            extract_path = extract_folder
        else:
            extract_path = os.path.join(os.getcwd(), extract_folder)
        
        # Create extraction directory if it doesn't exist
        os.makedirs(extract_path, exist_ok=True)
        
        # Extract the ZIP file
        zip_path = get_resource_path("payload.zip")
        
        if show_console:
            print(f"Extracting to: {extract_path}")
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        
        if show_console:
            print("Extraction completed successfully!")
        
        # Run the specified file if provided
        if run_after_extract:
            run_path = os.path.join(extract_path, run_after_extract)
            
            if os.path.exists(run_path):
                if show_console:
                    print(f"Running: {run_path}")
                
                # Change to the extraction directory
                original_cwd = os.getcwd()
                os.chdir(extract_path)
                
                try:
                    # Check if we're already running as admin
                    import ctypes
                    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
                    
                    if show_console:
                        print(f"Running: {run_path}")
                        if is_admin:
                            print("Note: Already running with administrator privileges")
                    
                    # Check for UAC elevation patterns (always do this, regardless of console mode)
                    has_uac_elevation = False
                    if run_path.lower().endswith('.bat') or run_path.lower().endswith('.cmd'):
                        try:
                            with open(run_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read().strip()
                                
                                # Check for UAC elevation patterns
                                uac_patterns = ['runas', 'UAC', 'getadmin.vbs', 'ShellExecute', 'cacls.exe', 'exit /B']
                                has_uac_elevation = any(pattern.lower() in content.lower() for pattern in uac_patterns)
                                
                                # Only show debug info if console is enabled
                                if show_console:
                                    print(f"Batch file contents ({len(content)} chars):")
                                    print("-" * 40)
                                    print(content[:500] + ("..." if len(content) > 500 else ""))
                                    print("-" * 40)
                                    
                                    if has_uac_elevation:
                                        print("⚠️  DETECTED: Batch file contains UAC elevation logic")
                                        print("   This may cause the batch file to exit and re-launch with admin privileges")
                                    
                        except Exception as e:
                            if show_console:
                                print(f"Could not read batch file: {e}")
                    
                    # Run the program with appropriate method
                    if run_path.lower().endswith('.bat') or run_path.lower().endswith('.cmd'):
                        # For batch files, try multiple execution methods
                        methods = []
                        
                        if is_admin and inherit_admin:
                            # Method 1: Direct execution with cmd /c (preserves admin)
                            methods.append(("cmd /c (admin)", 
                                          ['cmd', '/c', f'cd /d "{extract_path}" && "{run_path}"']))
                            # Method 2: Start command (opens new window)
                            methods.append(("start /wait (admin)", 
                                          ['cmd', '/c', f'start /wait /d "{extract_path}" "{run_path}"']))
                        elif is_admin and not inherit_admin:
                            # Method 1: Try to run without admin privileges
                            methods.append(("runas without admin", 
                                          ['runas', '/trustlevel:0x20000', f'cmd /c "cd /d \"{extract_path}\" && \"{run_path}\""']))
                        else:
                            # Method 1: Direct execution
                            methods.append(("direct execution", [run_path]))
                            # Method 2: With cmd /c
                            methods.append(("cmd /c", ['cmd', '/c', f'cd /d "{extract_path}" && "{run_path}"']))
                        
                        # Try each method until one works or we run out
                        result = None
                        for method_name, cmd_args in methods:
                            try:
                                if show_console:
                                    print(f"Trying method: {method_name}")
                                    print(f"Command: {' '.join(cmd_args)}")
                                
                                # Special handling for batch files with UAC elevation
                                if has_uac_elevation and show_console:
                                    print("🔄 UAC elevation detected - waiting for elevated process...")
                                
                                result = subprocess.run(cmd_args,
                                                      capture_output=not show_console,
                                                      text=True,
                                                      cwd=extract_path,
                                                      shell=True if 'runas' in cmd_args[0] else False,
                                                      timeout=300)  # 5 minute timeout
                                
                                if show_console:
                                    print(f"Method '{method_name}' completed with exit code: {result.returncode}")
                                
                                # For UAC elevation batch files, exit code 0 might mean it launched elevated process
                                if has_uac_elevation and result.returncode == 0:
                                    if show_console:
                                        print("✅ Batch file with UAC elevation completed (may have launched elevated process)")
                                        print("   Waiting additional time for elevated process to complete...")
                                    
                                    # Wait a bit more for the elevated process to do its work
                                    import time
                                    time.sleep(5)
                                    
                                    # Check if any processes are still running from the batch file
                                    try:
                                        # Look for common processes that might be launched
                                        import psutil
                                        batch_name = os.path.splitext(os.path.basename(run_path))[0]
                                        
                                        if show_console:
                                            print(f"   Checking for processes related to '{batch_name}'...")
                                        
                                        # Wait up to 30 seconds for related processes to complete
                                        for i in range(30):
                                            related_processes = []
                                            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                                                try:
                                                    if proc.info['cmdline']:
                                                        cmdline = ' '.join(proc.info['cmdline']).lower()
                                                        if (batch_name.lower() in cmdline or 
                                                            extract_path.lower() in cmdline or
                                                            'getadmin.vbs' in cmdline):
                                                            related_processes.append(proc.info['name'])
                                                except (psutil.NoSuchProcess, psutil.AccessDenied):
                                                    continue
                                            
                                            if not related_processes:
                                                if show_console and i > 0:
                                                    print(f"   All related processes completed after {i} seconds")
                                                break
                                            elif i == 0 and show_console:
                                                print(f"   Found related processes: {', '.join(set(related_processes))}")
                                            
                                            time.sleep(1)
                                        
                                        if related_processes and show_console:
                                            print(f"   Some processes may still be running: {', '.join(set(related_processes))}")
                                            
                                    except ImportError:
                                        # psutil not available, just wait a fixed time
                                        if show_console:
                                            print("   Waiting 10 seconds for elevated process to complete...")
                                        time.sleep(10)
                                    except Exception as e:
                                        if show_console:
                                            print(f"   Error checking processes: {e}")
                                
                                # If successful or if this is our last method, break
                                if result.returncode == 0 or method_name == methods[-1][0]:
                                    break
                                    
                            except subprocess.TimeoutExpired:
                                if show_console:
                                    print(f"Method '{method_name}' timed out after 5 minutes")
                                continue
                            except Exception as e:
                                if show_console:
                                    print(f"Method '{method_name}' failed: {e}")
                                continue
                    else:
                        # For other executables, run directly
                        if is_admin and not inherit_admin and show_console:
                            print("Note: Running executable with inherited admin privileges")
                        result = subprocess.run([run_path], 
                                              capture_output=not show_console,
                                              text=True,
                                              cwd=extract_path,
                                              timeout=300)
                    
                    if show_console and result.returncode != 0:
                        print(f"Program exited with code: {result.returncode}")
                    elif show_console:
                        print(f"Program completed successfully (exit code: {result.returncode})")
                
                except Exception as e:
                    show_error(f"Failed to run {run_after_extract}:\\n{str(e)}")
                    return
                finally:
                    os.chdir(original_cwd)
                
                # Delete extracted files if requested
                if delete_after_run:
                    if show_console:
                        print("Cleaning up extracted files...")
                    try:
                        shutil.rmtree(extract_path)
                        if show_console:
                            print("Cleanup completed!")
                    except Exception as e:
                        if show_console:
                            print(f"Warning: Could not clean up files: {e}")
            else:
                show_error(f"File to run not found: {run_after_extract}")
        else:
            if not show_console:
                show_info(f"Files extracted successfully to:\\n{extract_path}")
    
    except Exception as e:
        show_error(f"Extraction failed:\\n{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
    
    def _build_with_pyinstaller(self, temp_dir, script_path, zip_path, config_path):
        """Build the EXE using PyInstaller"""
        try:
            import PyInstaller.__main__
        except ImportError:
            raise Exception("PyInstaller is required. Install it with: pip install pyinstaller")
        
        # Create a custom build directory to avoid permission issues
        build_dir = os.path.join(temp_dir, 'build')
        work_dir = os.path.join(temp_dir, 'work')
        os.makedirs(build_dir, exist_ok=True)
        os.makedirs(work_dir, exist_ok=True)
        
        # PyInstaller arguments
        args = [
            '--onefile',  # Create a single executable
            '--windowed' if not self.show_console.get() else '--console',  # Window mode
            '--add-data', f'{zip_path};.',  # Add ZIP file
            '--add-data', f'{config_path};.',  # Add config file
            '--distpath', os.path.dirname(self.output_exe_path.get()),  # Output directory
            '--workpath', work_dir,  # Custom work directory
            '--specpath', temp_dir,  # Spec file location
            '--name', os.path.splitext(os.path.basename(self.output_exe_path.get()))[0],  # EXE name
            '--clean',  # Clean cache
            '--noconfirm',  # Don't ask for confirmation
        ]
        
        # Add icon if specified
        if self.icon_file_path.get() and os.path.exists(self.icon_file_path.get()):
            # Copy icon to temp directory to avoid path issues
            icon_source = self.icon_file_path.get()
            icon_name = os.path.basename(icon_source)
            icon_dest = os.path.join(temp_dir, icon_name)
            
            try:
                # Copy the icon file to temp directory
                shutil.copy2(icon_source, icon_dest)
                
                # Normalize the path for PyInstaller
                icon_path = os.path.normpath(icon_dest)
                
                # Validate it's a proper ICO file
                if not icon_path.lower().endswith('.ico'):
                    raise Exception(f"Icon file must be a .ico file, got: {icon_path}")
                
                # Check file size (ICO files should be reasonable size)
                icon_size = os.path.getsize(icon_path)
                if icon_size > 5 * 1024 * 1024:  # 5MB limit
                    raise Exception(f"Icon file too large: {icon_size} bytes (max 5MB)")
                
                if icon_size < 100:  # Very small files are likely corrupt
                    raise Exception(f"Icon file too small: {icon_size} bytes (likely corrupt)")
                
                args.extend(['--icon', icon_path])
                
                if hasattr(self, 'status_label'):
                    self.status_label.config(text=f"Using icon: {icon_name}")
                    self.root.update()
                    
            except Exception as e:
                # If icon fails, continue without it but warn user
                error_msg = f"Warning: Could not use icon file: {str(e)}"
                if hasattr(self, 'status_label'):
                    self.status_label.config(text=error_msg)
                    self.root.update()
                print(f"Icon Error: {error_msg}")
        
        # Add UPX compression if enabled
        if self.upx_enabled_var.get():
            upx_dir = self.upx_path_var.get()
            if upx_dir and os.path.isdir(upx_dir):
                upx_executable = os.path.join(upx_dir, "upx.exe") if sys.platform == "win32" else os.path.join(upx_dir, "upx")
                if os.path.exists(upx_executable):
                    args.extend(['--upx-dir', upx_dir])
                    if hasattr(self, 'status_label'):
                        self.status_label.config(text="UPX compression enabled.")
                        self.root.update()
                else:
                    error_msg = f"Warning: upx.exe not found in '{upx_dir}'. Continuing without compression."
                    if hasattr(self, 'status_label'):
                        self.status_label.config(text=error_msg)
                        self.root.update()
                    print(f"UPX Error: {error_msg}")
            else:
                error_msg = "Warning: UPX directory not specified or invalid. Continuing without compression."
                if hasattr(self, 'status_label'):
                    self.status_label.config(text=error_msg)
                    self.root.update()
                print(f"UPX Error: {error_msg}")
        
        # Add admin privileges if requested
        if self.require_admin.get():
            # Create a manifest file for admin privileges
            manifest_content = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <assemblyIdentity
    version="1.0.0.0"
    processorArchitecture="*"
    name="SelfExtractingArchive"
    type="win32"
  />
  <description>Self-Extracting Archive</description>
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v2">
    <security>
      <requestedPrivileges xmlns="urn:schemas-microsoft-com:asm.v3">
        <requestedExecutionLevel level="requireAdministrator" uiAccess="false"/>
      </requestedPrivileges>
    </security>
  </trustInfo>
</assembly>'''
            
            manifest_path = os.path.join(temp_dir, 'admin.manifest')
            with open(manifest_path, 'w', encoding='utf-8') as f:
                f.write(manifest_content)
            
            args.extend(['--manifest', manifest_path])
        
        args.append(script_path)  # Script to build
        
        try:
            # Run PyInstaller
            PyInstaller.__main__.run(args)
        except Exception as e:
            error_msg = str(e)
            if "Access is denied" in error_msg or "WinError 5" in error_msg:
                # Provide specific guidance for permission errors
                raise Exception(
                    "Build failed due to permission issues. This is usually caused by:\n\n"
                    "1. Antivirus software blocking PyInstaller\n"
                    "2. Files being locked by another process\n"
                    "3. Insufficient permissions\n\n"
                    "Solutions to try:\n"
                    "• Temporarily disable antivirus real-time protection\n"
                    "• Run this program as Administrator\n"
                    "• Close any programs that might be using the files\n"
                    "• Try building to a different location (like Desktop)\n"
                    "• Add PyInstaller to your antivirus exclusions\n\n"
                    f"Original error: {error_msg}"
                )
            else:
                raise Exception(f"PyInstaller build failed: {error_msg}")

def main():
    root = tk.Tk()
    app = SelfExtractingEXECreator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
