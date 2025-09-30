# kush-framework/kush/core/module_manager.py
"""
Module manager for Empire-style modules
"""

from typing import Dict, List, Optional, Any
from colorama import Fore, Style

class ModuleManager:
    def __init__(self):
        self.modules: Dict[str, Dict[str, Any]] = {}
        
        # Load built-in modules
        self._load_builtin_modules()
    
    def _load_builtin_modules(self):
        """Load built-in modules"""
        
        # Collection Modules
        self.modules['mimikatz'] = {
            'name': 'mimikatz',
            'description': 'Dump credentials using Mimikatz',
            'author': 'Kush Team',
            'category': 'collection',
            'options': [
                {'name': 'Agent', 'description': 'Agent to run module on', 'required': True},
            ]
        }
        
        self.modules['keylogger'] = {
            'name': 'keylogger',
            'description': 'Capture keystrokes from target',
            'author': 'Kush Team',
            'category': 'collection',
            'options': [
                {'name': 'Agent', 'description': 'Agent to run module on', 'required': True},
                {'name': 'Duration', 'description': 'Duration in seconds', 'required': False, 'default': '60'},
            ]
        }
        
        self.modules['screenshot'] = {
            'name': 'screenshot',
            'description': 'Take screenshot of target desktop',
            'author': 'Kush Team',
            'category': 'collection',
            'options': [
                {'name': 'Agent', 'description': 'Agent to run module on', 'required': True},
            ]
        }
        
        # Persistence Modules
        self.modules['persistence_scheduled_task'] = {
            'name': 'persistence_scheduled_task',
            'description': 'Establish persistence via scheduled task',
            'author': 'Kush Team',
            'category': 'persistence',
            'options': [
                {'name': 'Agent', 'description': 'Agent to run module on', 'required': True},
                {'name': 'TaskName', 'description': 'Name of scheduled task', 'required': False, 'default': 'WindowsUpdate'},
            ]
        }
        
        self.modules['persistence_service'] = {
            'name': 'persistence_service',
            'description': 'Establish persistence via Windows service',
            'author': 'Kush Team',
            'category': 'persistence',
            'options': [
                {'name': 'Agent', 'description': 'Agent to run module on', 'required': True},
                {'name': 'ServiceName', 'description': 'Name of service', 'required': False, 'default': 'WindowsUpdate'},
            ]
        }
        
        self.modules['persistence_registry'] = {
            'name': 'persistence_registry',
            'description': 'Establish persistence via registry run keys',
            'author': 'Kush Team',
            'category': 'persistence',
            'options': [
                {'name': 'Agent', 'description': 'Agent to run module on', 'required': True},
                {'name': 'KeyName', 'description': 'Registry key name', 'required': False, 'default': 'WindowsUpdate'},
            ]
        }
        
        # Privilege Escalation Modules
        self.modules['bypassuac'] = {
            'name': 'bypassuac',
            'description': 'Bypass User Account Control',
            'author': 'Kush Team',
            'category': 'privesc',
            'options': [
                {'name': 'Agent', 'description': 'Agent to run module on', 'required': True},
            ]
        }
        
        self.modules['getsystem'] = {
            'name': 'getsystem',
            'description': 'Attempt to get SYSTEM privileges',
            'author': 'Kush Team',
            'category': 'privesc',
            'options': [
                {'name': 'Agent', 'description': 'Agent to run module on', 'required': True},
            ]
        }
        
        # Reconnaissance Modules
        self.modules['recon_host'] = {
            'name': 'recon_host',
            'description': 'Gather host information',
            'author': 'Kush Team',
            'category': 'recon',
            'options': [
                {'name': 'Agent', 'description': 'Agent to run module on', 'required': True},
            ]
        }
        
        self.modules['recon_network'] = {
            'name': 'recon_network',
            'description': 'Gather network information',
            'author': 'Kush Team',
            'category': 'recon',
            'options': [
                {'name': 'Agent', 'description': 'Agent to run module on', 'required': True},
            ]
        }
        
        self.modules['recon_users'] = {
            'name': 'recon_users',
            'description': 'Enumerate users on target',
            'author': 'Kush Team',
            'category': 'recon',
            'options': [
                {'name': 'Agent', 'description': 'Agent to run module on', 'required': True},
            ]
        }
        
        # Lateral Movement Modules
        self.modules['psexec'] = {
            'name': 'psexec',
            'description': 'Execute commands on remote systems via PSExec',
            'author': 'Kush Team',
            'category': 'lateral',
            'options': [
                {'name': 'Agent', 'description': 'Agent to run module on', 'required': True},
                {'name': 'ComputerName', 'description': 'Target computer name', 'required': True},
            ]
        }
    
    def get_modules(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get all modules organized by category"""
        categories = {}
        for module in self.modules.values():
            category = module['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(module)
        
        return categories
    
    def get_module(self, module_name: str) -> Optional[Dict[str, Any]]:
        """Get specific module"""
        return self.modules.get(module_name)
    
    def execute_module(self, module_name: str, agent_name: str) -> str:
        """Execute module on agent"""
        module = self.modules.get(module_name)
        if not module:
            return f"{Fore.RED}[-] Module '{module_name}' not found{Style.RESET_ALL}"
        
        # Mock module execution with detailed output
        output = [f"{Fore.CYAN}[*] Executing {module_name} on {agent_name}{Style.RESET_ALL}"]
        
        if module_name == 'mimikatz':
            output.append(f"{Fore.GREEN}[+] Mimikatz output:{Style.RESET_ALL}")
            output.append("  .#####.   mimikatz 2.2.0 (x64) #19041 Sep 18 2020 19:18:29")
            output.append("  .## ^ ##.  \"A La Vie, A L'Amour\" - (oe.eo)")
            output.append("  ## / \\ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )")
            output.append("  ## \\ / ##       > https://blog.gentilkiwi.com/mimikatz")
            output.append("  '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )")
            output.append("   '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/")
            output.append("")
            output.append("  Authentication Id : 0 ; 996 (00000000:000003e4)")
            output.append("  Session           : Service from 0")
            output.append("  User Name         : NETWORK SERVICE")
            output.append("  Domain            : NT AUTHORITY")
            output.append("  Logon Server      : (null)")
            output.append("  Logon Time        : 9/29/2025 7:38:44 PM")
            output.append("  SID               : S-1-5-20")
            output.append("")
            output.append("  msv :")
            output.append("   [00000003] Primary")
            output.append("   * Username : Administrator")
            output.append("   * Domain   : CONTOSO")
            output.append("   * NTLM     : 8846f7eaee8fb117ad06bdd830b7586c")
            output.append("   * SHA1     : 28a6b0448ba5b7e5c6c5c5c5c5c5c5c5c5c5c5c5c")
            output.append("   * DPAPI    : 5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c5c")
        
        elif module_name == 'keylogger':
            output.append(f"{Fore.GREEN}[+] Keylogger started for 60 seconds{Style.RESET_ALL}")
            output.append(f"{Fore.YELLOW}[!] Capturing keystrokes from {agent_name}{Style.RESET_ALL}")
            output.append(f"{Fore.GREEN}[+] Keylogger running in background...{Style.RESET_ALL}")
        
        elif module_name == 'screenshot':
            output.append(f"{Fore.GREEN}[+] Taking screenshot from {agent_name}{Style.RESET_ALL}")
            output.append(f"{Fore.GREEN}[+] Screenshot saved to: /tmp/screenshot_{agent_name}.png{Style.RESET_ALL}")
            output.append(f"{Fore.YELLOW}[!] Use 'download' to retrieve the screenshot{Style.RESET_ALL}")
        
        elif module_name == 'persistence_scheduled_task':
            output.append(f"{Fore.GREEN}[+] Creating scheduled task for persistence{Style.RESET_ALL}")
            output.append(f"{Fore.GREEN}[+] Scheduled task 'WindowsUpdate' created{Style.RESET_ALL}")
            output.append(f"{Fore.GREEN}[+] Task configured to run at system startup{Style.RESET_ALL}")
            output.append(f"{Fore.GREEN}[+] Persistence established on {agent_name}{Style.RESET_ALL}")
        
        elif module_name == 'persistence_service':
            output.append(f"{Fore.GREEN}[+] Creating Windows service for persistence{Style.RESET_ALL}")
            output.append(f"{Fore.GREEN}[+] Service 'WindowsUpdate' created{Style.RESET_ALL}")
            output.append(f"{Fore.GREEN}[+] Service set to auto-start{Style.RESET_ALL}")
            output.append(f"{Fore.GREEN}[+] Persistence established on {agent_name}{Style.RESET_ALL}")
        
        elif module_name == 'persistence_registry':
            output.append(f"{Fore.GREEN}[+] Adding registry run key for persistence{Style.RESET_ALL}")
            output.append(f"{Fore.GREEN}[+] Registry key 'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\WindowsUpdate' created{Style.RESET_ALL}")
            output.append(f"{Fore.GREEN}[+] Persistence established on {agent_name}{Style.RESET_ALL}")
        
        elif module_name == 'bypassuac':
            output.append(f"{Fore.GREEN}[+] Attempting UAC bypass on {agent_name}{Style.RESET_ALL}")
            output.append(f"{Fore.GREEN}[+] UAC bypass successful!{Style.RESET_ALL}")
            output.append(f"{Fore.GREEN}[+] Now running with elevated privileges{Style.RESET_ALL}")
        
        elif module_name == 'getsystem':
            output.append(f"{Fore.GREEN}[+] Attempting to get SYSTEM privileges on {agent_name}{Style.RESET_ALL}")
            output.append(f"{Fore.GREEN}[+] Got SYSTEM privileges!{Style.RESET_ALL}")
        
        elif module_name == 'recon_host':
            output.append(f"{Fore.GREEN}[+] Host reconnaissance on {agent_name}:{Style.RESET_ALL}")
            output.append("  OS: Windows 10 Enterprise Build 19041")
            output.append("  Architecture: x64")
            output.append("  Domain: CONTOSO")
            output.append("  Logged in users: Administrator, SYSTEM")
            output.append("  UAC Status: Enabled")
            output.append("  Antivirus: Windows Defender")
        
        elif module_name == 'recon_network':
            output.append(f"{Fore.GREEN}[+] Network reconnaissance on {agent_name}:{Style.RESET_ALL}")
            output.append("  IP Address: 192.168.1.100")
            output.append("  Subnet: 255.255.255.0")
            output.append("  Gateway: 192.168.1.1")
            output.append("  DNS: 8.8.8.8, 8.8.4.4")
            output.append("  Open ports: 80, 443, 445, 3389, 5985")
            output.append("  Network shares: \\\\192.168.1.10\\Share1, \\\\192.168.1.20\\Data")
        
        elif module_name == 'recon_users':
            output.append(f"{Fore.GREEN}[+] User enumeration on {agent_name}:{Style.RESET_ALL}")
            output.append("  Administrator (S-1-5-21-...-500)")
            output.append("  Guest (S-1-5-21-...-501)")
            output.append("  DefaultAccount (S-1-5-21-...-503)")
            output.append("  WDAGUtilityAccount (S-1-5-21-...-504)")
            output.append("  User (S-1-5-21-...-1001)")
        
        elif module_name == 'psexec':
            output.append(f"{Fore.GREEN}[+] Attempting PSExec on target{Style.RESET_ALL}")
            output.append(f"{Fore.GREEN}[+] Connected to remote system{Style.RESET_ALL}")
            output.append(f"{Fore.GREEN}[+] Service created and started{Style.RESET_ALL}")
            output.append(f"{Fore.GREEN}[+] Command executed successfully{Style.RESET_ALL}")
        
        else:
            output.append(f"{Fore.GREEN}[+] Module {module_name} executed successfully{Style.RESET_ALL}")
        
        output.append(f"{Fore.CYAN}[*] Module execution completed{Style.RESET_ALL}")
        return "\n".join(output)