# kush-framework/kush/listeners/tcp_listener.py
"""
TCP listener for Empire-style communication
"""

import socket
import threading
import time
from typing import Optional
from colorama import Fore, Style

class TCPListener:
    def __init__(self, host: str = '0.0.0.0', port: int = 4444):
        self.host = host
        self.port = port
        self.socket: Optional[socket.socket] = None
        self.thread: Optional[threading.Thread] = None
        self.running = False
    
    def start(self):
        """Start TCP listener"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            self.running = True
            
            print(f"{Fore.GREEN}[+] TCP listener started on {self.host}:{self.port}{Style.RESET_ALL}")
            
            while self.running:
                try:
                    client_socket, client_address = self.socket.accept()
                    print(f"{Fore.GREEN}[+] TCP connection from {client_address[0]}:{client_address[1]}{Style.RESET_ALL}")
                    
                    # Handle client in a separate thread
                    client_thread = threading.Thread(
                        target=self._handle_client,
                        args=(client_socket, client_address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except socket.timeout:
                    continue
                except OSError:
                    break
                    
        except Exception as e:
            print(f"{Fore.RED}[-] TCP listener error: {e}{Style.RESET_ALL}")
        finally:
            self.stop()
    
    def _handle_client(self, client_socket: socket.socket, client_address: tuple):
        """Handle individual client connection"""
        try:
            # Send welcome message
            welcome_msg = "Connected to Kush Framework TCP Listener\n"
            client_socket.send(welcome_msg.encode())
            
            while self.running:
                try:
                    # Receive data from client
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    
                    command = data.decode().strip()
                    if command.lower() == 'exit':
                        break
                    
                    # Execute command (mock implementation)
                    response = f"Executed: {command}\nResult: Mock execution successful\n"
                    client_socket.send(response.encode())
                    
                except socket.timeout:
                    continue
                except Exception:
                    break
                    
        except Exception as e:
            print(f"{Fore.RED}[-] Client handler error: {e}{Style.RESET_ALL}")
        finally:
            client_socket.close()
            print(f"{Fore.YELLOW}[-] TCP client disconnected: {client_address[0]}:{client_address[1]}{Style.RESET_ALL}")
    
    def stop(self):
        """Stop TCP listener"""
        self.running = False
        if self.socket:
            self.socket.close()
