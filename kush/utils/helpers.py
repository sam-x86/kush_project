# kush-framework/kush/utils/helpers.py
"""
Enhanced helper functions with advanced tab completion
"""

import readline
import os
import glob
from pathlib import Path
from colorama import Fore, Style

def display_banner():
    """Display Kush Framework banner"""
    banner = f"""
{Fore.RED}

██╗  ██╗██╗   ██╗███████╗██╗  ██╗
 ██║ ██╔╝██║   ██║██╔════╝██║  ██║
 █████╔╝ ██║   ██║███████╗███████║
 ██╔═██╗ ██║   ██║╚════██║██╔══██║
 ██║  ██╗╚██████╔╝███████║██║  ██║
 ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝                                                                                           __/ |
                                                                                         |___/ 
{Style.RESET_ALL}
{Fore.CYAN}        Version 3.0.0 - Empire-inspired Penetration Testing Framework{Style.RESET_ALL}
{Fore.YELLOW}    Modular Architecture | Stagers & Agents | Professional Workflow{Style.RESET_ALL}
{Fore.GREEN}           Powered by DeepSeek AI | Educational Use Only{Style.RESET_ALL}
"""
    print(banner)

class KushCompleter:
    def __init__(self):
        self.commands = {
            # Listener management
            'listeners': [],
            'uselistener': ['http', 'tcp'],
            'set': [],
            'info': [],
            'start': [],
            'stop': [],
            
            # Stager management
            'stagers': [],
            'usestager': ['windows_dropper', 'linux_dropper', 'macos_dropper', 'windows_macro', 'powershell'],
            'generate': [],
            
            # Agent management
            'agents': [],
            'interact': [],
            'shell': [],
            'upload': [],
            'download': [],
            'back': [],
            
            # Module management
            'modules': [],
            'usemodule': ['mimikatz', 'keylogger', 'screenshot', 'persistence_scheduled_task', 'persistence_service', 
                         'persistence_registry', 'bypassuac', 'getsystem', 'recon_host', 'recon_network', 'recon_users', 'psexec'],
            'run': [],
            
            # Framework
            'help': [],
            'exit': [],
            'quit': [],
            'reset': [],
            'version': [],
        }
        
        # Build command list for basic completion
        self.flat_commands = list(self.commands.keys())

    def complete(self, text, state):
        """Tab completion function"""
        buffer = readline.get_line_buffer()
        words = buffer.split()
        
        if not words:
            options = [cmd for cmd in self.flat_commands if cmd.startswith(text)]
        else:
            if len(words) == 1:
                # First word - complete command names
                options = [cmd for cmd in self.flat_commands if cmd.startswith(text)]
            else:
                # Subsequent words - complete based on command
                command = words[0]
                if command in self.commands:
                    options = [opt for opt in self.commands[command] if opt.startswith(text)]
                else:
                    options = []
        
        if state < len(options):
            return options[state]
        else:
            return None

def setup_tab_completion():
    """Setup advanced tab completion"""
    completer = KushCompleter()
    readline.set_completer(completer.complete)
    
    # Tab completion settings
    readline.parse_and_bind("tab: complete")
    readline.set_completer_delims(' \t\n`~!@#$%^&*()-=+[{]}\\|;:\'",<>?')
    
    # Load history if exists
    history_file = os.path.expanduser('~/.kush_history')
    try:
        readline.read_history_file(history_file)
    except FileNotFoundError:
        pass
    
    # Save history on exit
    import atexit
    atexit.register(readline.write_history_file, history_file)

def setup_directories():
    """Create necessary directories"""
    directories = ['stagers', 'downloads', 'logs', 'data']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"{Fore.GREEN}[+] Created directory: {directory}{Style.RESET_ALL}")

def print_success(message: str):
    """Print success message"""
    print(f"{Fore.GREEN}[+] {message}{Style.RESET_ALL}")

def print_error(message: str):
    """Print error message"""
    print(f"{Fore.RED}[-] {message}{Style.RESET_ALL}")

def print_warning(message: str):
    """Print warning message"""
    print(f"{Fore.YELLOW}[!] {message}{Style.RESET_ALL}")

def print_info(message: str):
    """Print info message"""
    print(f"{Fore.CYAN}[*] {message}{Style.RESET_ALL}")