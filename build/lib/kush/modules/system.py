# kush-framework/kush/modules/system.py
"""
System information module
"""

from typing import List, Optional
from colorama import Fore, Style
from kush.core.session import Session

class SystemModule:
    def sysinfo(self, args: List[str], session: Optional[Session]) -> str:
        if not session:
            return f"{Fore.RED}[!] No active session{Style.RESET_ALL}"
        
        output = [f"{Fore.CYAN}[*] System Information for {session.hostname}{Style.RESET_ALL}"]
        output.append(f"  {Fore.YELLOW}Hostname:{Style.RESET_ALL} {session.hostname}")
        output.append(f"  {Fore.YELLOW}OS:{Style.RESET_ALL} {session.os_type}")
        output.append(f"  {Fore.YELLOW}User:{Style.RESET_ALL} {session.user}")
        output.append(f"  {Fore.YELLOW}Architecture:{Style.RESET_ALL} x86_64")
        output.append(f"  {Fore.YELLOW}CPU Cores:{Style.RESET_ALL} 4")
        output.append(f"  {Fore.YELLOW}Memory:{Style.RESET_ALL} 8GB")
        output.append(f"  {Fore.YELLOW}Uptime:{Style.RESET_ALL} 2 days, 5 hours")
        output.append(f"  {Fore.YELLOW}Antivirus:{Style.RESET_ALL} Windows Defender")
        
        return "\n".join(output)
    
    def processes(self, args: List[str], session: Optional[Session]) -> str:
        if not session:
            return f"{Fore.RED}[!] No active session{Style.RESET_ALL}"
        
        output = [f"{Fore.CYAN}[*] Running Processes on {session.hostname}{Style.RESET_ALL}"]
        output.append(f"{Fore.GREEN}PID     Name                     User{Style.RESET_ALL}")
        output.append(f"1234    explorer.exe           {session.user}")
        output.append(f"5678    chrome.exe             {session.user}")
        output.append(f"9012    notepad.exe            {session.user}")
        output.append(f"3456    kush_agent.exe         {session.user}")
        output.append(f"7890    svchost.exe            SYSTEM")
        output.append(f"{Fore.YELLOW}[!] Total processes: 56{Style.RESET_ALL}")
        
        return "\n".join(output)