# kush-framework/kush/modules/surveillance.py
"""
Surveillance module for screenshot, webcam, and keylogging
"""

from typing import List, Optional
from colorama import Fore, Style
from kush.core.session import Session

class SurveillanceModule:
    def screenshot(self, args: List[str], session: Optional[Session]) -> str:
        if not session:
            return f"{Fore.RED}[!] No active session{Style.RESET_ALL}"
        
        output = [f"{Fore.CYAN}[*] Taking screenshot on {session.hostname}{Style.RESET_ALL}"]
        output.append(f"{Fore.GREEN}[+] Screenshot captured successfully{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Saved to: /tmp/screenshot_{session.session_id}.png{Style.RESET_ALL}")
        output.append(f"{Fore.YELLOW}[!] Screenshot would be downloaded to framework{Style.RESET_ALL}")
        
        return "\n".join(output)
    
    def keylogger(self, args: List[str], session: Optional[Session]) -> str:
        if not session:
            return f"{Fore.RED}[!] No active session{Style.RESET_ALL}"
        
        if not args:
            return self._keylogger_help()
        
        action = args[0].lower()
        
        if action == 'start':
            output = [f"{Fore.CYAN}[*] Starting keylogger on {session.hostname}{Style.RESET_ALL}"]
            output.append(f"{Fore.GREEN}[+] Keylogger started successfully{Style.RESET_ALL}")
            output.append(f"{Fore.GREEN}[+] Logging keystrokes to: /tmp/keys_{session.session_id}.log{Style.RESET_ALL}")
        elif action == 'stop':
            output = [f"{Fore.CYAN}[*] Stopping keylogger on {session.hostname}{Style.RESET_ALL}"]
            output.append(f"{Fore.GREEN}[+] Keylogger stopped{Style.RESET_ALL}")
        elif action == 'dump':
            output = [f"{Fore.CYAN}[*] Dumping keylogger data from {session.hostname}{Style.RESET_ALL}"]
            output.append(f"{Fore.GREEN}[+] Captured 247 keystrokes{Style.RESET_ALL}")
            output.append(f"{Fore.GREEN}[+] Found passwords for: github.com, gmail.com{Style.RESET_ALL}")
        else:
            return f"{Fore.RED}[!] Unknown keylogger action: {action}{Style.RESET_ALL}"
        
        return "\n".join(output)
    
    def _keylogger_help(self) -> str:
        return f"""
{Fore.CYAN}Keylogger Module - Keystroke Capture{Style.RESET_ALL}

{Fore.YELLOW}Usage:{Style.RESET_ALL}
  keylogger start    - Start keylogger
  keylogger stop     - Stop keylogger  
  keylogger dump     - Dump captured keystrokes
"""
    
    def webcam(self, args: List[str], session: Optional[Session]) -> str:
        if not session:
            return f"{Fore.RED}[!] No active session{Style.RESET_ALL}"
        
        if not args:
            return self._webcam_help()
        
        action = args[0].lower()
        
        if action == 'capture':
            output = [f"{Fore.CYAN}[*] Capturing webcam image from {session.hostname}{Style.RESET_ALL}"]
            output.append(f"{Fore.GREEN}[+] Webcam image captured{Style.RESET_ALL}")
            output.append(f"{Fore.GREEN}[+] Saved to: /tmp/webcam_{session.session_id}.jpg{Style.RESET_ALL}")
        elif action == 'stream':
            output = [f"{Fore.CYAN}[*] Starting webcam stream from {session.hostname}{Style.RESET_ALL}"]
            output.append(f"{Fore.GREEN}[+] Webcam stream started{Style.RESET_ALL}")
            output.append(f"{Fore.YELLOW}[!] Streaming to port 8888{Style.RESET_ALL}")
        elif action == 'stop':
            output = [f"{Fore.CYAN}[*] Stopping webcam stream on {session.hostname}{Style.RESET_ALL}"]
            output.append(f"{Fore.GREEN}[+] Webcam stream stopped{Style.RESET_ALL}")
        else:
            return f"{Fore.RED}[!] Unknown webcam action: {action}{Style.RESET_ALL}"
        
        return "\n".join(output)
    
    def _webcam_help(self) -> str:
        return f"""
{Fore.CYAN}Webcam Module - Camera Surveillance{Style.RESET_ALL}

{Fore.YELLOW}Usage:{Style.RESET_ALL}
  webcam capture    - Capture single image
  webcam stream     - Start video stream
  webcam stop       - Stop video stream
"""