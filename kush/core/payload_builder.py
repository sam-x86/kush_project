# kush-framework/kush/core/payload_builder.py
"""
Payload builder for cross-platform payload generation
"""

import os
from pathlib import Path
from typing import Optional
from colorama import Fore, Style

from kush.payloads.windows import WindowsPayload
from kush.payloads.linux import LinuxPayload
from kush.payloads.macos import MacOSPayload

class PayloadBuilder:
    def __init__(self, output_dir: str = "payloads"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.generators = {
            'windows': WindowsPayload(),
            'linux': LinuxPayload(),
            'macos': MacOSPayload()
        }
    
    def build(self, target: str, lhost: str, lport: str, 
              output_name: Optional[str] = None, **kwargs) -> str:
        if target not in self.generators:
            return f"{Fore.RED}[-] Unknown target: {target}{Style.RESET_ALL}"
        
        try:
            generator = self.generators[target]
            
            if not output_name:
                output_name = f"kush_{target}_{lhost}_{lport}"
            
            result = generator.generate(
                lhost=lhost,
                lport=lport,
                output_name=output_name,
                output_dir=self.output_dir,
                **kwargs
            )
            
            return f"{Fore.GREEN}[+] Payload built: {result}{Style.RESET_ALL}"
            
        except Exception as e:
            return f"{Fore.RED}[-] Build failed: {e}{Style.RESET_ALL}"
    
    def list_payloads(self) -> str:
        payloads = list(self.output_dir.glob("*"))
        if not payloads:
            return f"{Fore.YELLOW}[*] No payloads generated{Style.RESET_ALL}"
        
        output = [f"{Fore.CYAN}[*] Generated payloads:{Style.RESET_ALL}"]
        for payload in payloads:
            size = payload.stat().st_size if payload.exists() else 0
            output.append(f"  {payload.name} ({size} bytes)")
        
        return "\n".join(output)