# kush-framework/kush/core/listener_manager.py
"""
Listener manager for Empire-style listeners
"""

import threading
import time
from typing import Dict, List, Optional, Any
from colorama import Fore, Style

class ListenerManager:
    def __init__(self):
        self.listeners: Dict[str, Any] = {}
        self.active_listeners: Dict[str, Any] = {}
        self.listener_options: Dict[str, Dict[str, Any]] = {}
        
        # Load built-in listeners
        self._load_builtin_listeners()
    
    def _load_builtin_listeners(self):
        """Load built-in listeners"""
        # HTTP Listener
        self.listeners['http'] = {
            'name': 'http',
            'description': 'HTTP listener for agent communication',
            'author': 'Kush Team',
            'options': [
                {'name': 'Host', 'description': 'Listener host', 'required': True, 'default': '0.0.0.0'},
                {'name': 'Port', 'description': 'Listener port', 'required': True, 'default': '8080'},
                {'name': 'Name', 'description': 'Listener name', 'required': False, 'default': 'http'},
            ]
        }
        
        # TCP Listener
        self.listeners['tcp'] = {
            'name': 'tcp',
            'description': 'TCP listener for agent communication',
            'author': 'Kush Team',
            'options': [
                {'name': 'Host', 'description': 'Listener host', 'required': True, 'default': '0.0.0.0'},
                {'name': 'Port', 'description': 'Listener port', 'required': True, 'default': '4444'},
                {'name': 'Name', 'description': 'Listener name', 'required': False, 'default': 'tcp'},
            ]
        }
        
        # Initialize options
        for listener_name in self.listeners:
            self.listener_options[listener_name] = {}
            for option in self.listeners[listener_name]['options']:
                self.listener_options[listener_name][option['name']] = option.get('default', '')
    
    def get_listeners(self) -> List[Dict[str, Any]]:
        """Get all available listeners"""
        return list(self.listeners.values())
    
    def get_listener(self, listener_name: str) -> Optional[Dict[str, Any]]:
        """Get specific listener"""
        return self.listeners.get(listener_name)
    
    def set_option(self, listener_name: str, option: str, value: str) -> bool:
        """Set listener option"""
        if listener_name not in self.listener_options:
            return False
        
        self.listener_options[listener_name][option] = value
        return True
    
    def get_option(self, listener_name: str, option: str) -> Optional[str]:
        """Get listener option value"""
        if listener_name not in self.listener_options:
            return None
        return self.listener_options[listener_name].get(option)
    
    def start_listener(self, listener_name: str) -> bool:
        """Start a listener"""
        if listener_name not in self.listeners:
            return False
        
        # Get listener options
        options = self.listener_options[listener_name]
        host = options.get('Host', '0.0.0.0')
        port = options.get('Port', '8080')
        
        try:
            if listener_name == 'http':
                from kush.listeners.http_listener import HTTPListener
                listener = HTTPListener(host, int(port))
            elif listener_name == 'tcp':
                from kush.listeners.tcp_listener import TCPListener
                listener = TCPListener(host, int(port))
            else:
                return False
            
            # Start listener in thread
            thread = threading.Thread(target=listener.start, daemon=True)
            thread.start()
            
            self.active_listeners[listener_name] = {
                'listener': listener,
                'thread': thread,
                'options': options
            }
            
            print(f"{Fore.GREEN}[+] {listener_name.upper()} listener started on {host}:{port}{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}[-] Failed to start listener: {e}{Style.RESET_ALL}")
            return False
    
    def stop_listener(self, listener_name: str) -> bool:
        """Stop a listener"""
        if listener_name not in self.active_listeners:
            return False
        
        try:
            listener_info = self.active_listeners[listener_name]
            listener_info['listener'].stop()
            del self.active_listeners[listener_name]
            print(f"{Fore.GREEN}[+] Listener '{listener_name}' stopped{Style.RESET_ALL}")
            return True
        except Exception as e:
            print(f"{Fore.RED}[-] Failed to stop listener: {e}{Style.RESET_ALL}")
            return False
    
    def stop_all_listeners(self):
        """Stop all active listeners"""
        for listener_name in list(self.active_listeners.keys()):
            self.stop_listener(listener_name)