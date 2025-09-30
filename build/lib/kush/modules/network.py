# kush-framework/kush/modules/network.py
"""
Network module
"""

from typing import List, Optional
from kush.core.session import Session

class NetworkModule:
    def ifconfig(self, args: List[str], session: Optional[Session]) -> str:
        if not session:
            return "[-] No active session"
        return "[+] Network interfaces"
    
    def netstat(self, args: List[str], session: Optional[Session]) -> str:
        if not session:
            return "[-] No active session"
        return "[+] Network connections"
    
    def portscan(self, args: List[str], session: Optional[Session]) -> str:
        if not session:
            return "[-] No active session"
        return "[+] Port scan"
