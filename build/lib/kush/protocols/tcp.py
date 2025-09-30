# kush-framework/kush/protocols/tcp.py
"""
Enhanced TCP protocol with better session handling
"""

import socket
import threading
import json
import select
from typing import Optional
from colorama import Fore, Style

from kush.core.session import Session, SessionManager, SessionType

class TCPListener:
    def __init__(self, host: str, port: int, session_manager: SessionManager):
        self.host = host
        self.port = port
        self.session_manager = session_manager
        self.socket: Optional[socket.socket] = None
        self.running = False
    
    def start(self):
        """Start TCP listener"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            self.socket.settimeout(1.0)  # Non-blocking with timeout
            self.running = True
            
            print(f"{Fore.GREEN}[+] TCP listener started on {self.host}:{self.port}{Style.RESET_ALL}")
            
            while self.running:
                try:
                    client_socket, client_address = self.socket.accept()
                    
                    # Create session
                    session = self.session_manager.create_session(
                        client_address, 
                        SessionType.TCP, 
                        client_socket
                    )
                    
                    print(f"{Fore.GREEN}[+] New TCP connection from {client_address[0]}:{client_address[1]} - Session {session.session_id}{Style.RESET_ALL}")
                    
                    # Start session handler
                    thread = threading.Thread(
                        target=self._handle_session,
                        args=(session,),
                        daemon=True
                    )
                    thread.start()
                    
                except socket.timeout:
                    continue
                except OSError:
                    break
                except Exception as e:
                    if self.running:
                        print(f"{Fore.RED}[-] TCP accept error: {e}{Style.RESET_ALL}")
                    
        except Exception as e:
            print(f"{Fore.RED}[-] TCP listener error: {e}{Style.RESET_ALL}")
        finally:
            self.stop()
    
    def stop(self):
        """Stop TCP listener"""
        self.running = False
        if self.socket:
            self.socket.close()
    
    def _handle_session(self, session: Session):
        """Handle TCP session"""
        try:
            # Send welcome message
            welcome_msg = {"type": "welcome", "message": "Connected to Kush Framework"}
            self._reliable_send(session.connection, welcome_msg)
            
            # Main session loop
            while self.running and session.connection:
                try:
                    command = self._reliable_recv(session.connection, timeout=1.0)
                    if command:
                        # Update session activity
                        session.update_activity()
                        
                        if command.get('type') == 'system_info':
                            self.session_manager.update_session_info(session.session_id, command.get('data', {}))
                            print(f"{Fore.CYAN}[*] Session {session.session_id} - {command.get('data', {}).get('hostname', 'unknown')} ({command.get('data', {}).get('user', 'unknown')}@{command.get('data', {}).get('os', 'unknown')}){Style.RESET_ALL}")
                        else:
                            # Execute command and send result
                            result = self._execute_command(command, session)
                            self._reliable_send(session.connection, result)
                        
                except socket.timeout:
                    continue
                except Exception as e:
                    break
                    
        except Exception as e:
            print(f"{Fore.RED}[-] TCP session {session.session_id} error: {e}{Style.RESET_ALL}")
        finally:
            if session.session_id in self.session_manager.sessions:
                self.session_manager.remove_session(session.session_id)
            if session.connection:
                session.connection.close()
            print(f"{Fore.YELLOW}[-] TCP session {session.session_id} disconnected{Style.RESET_ALL}")
    
    def _reliable_send(self, sock: socket.socket, data):
        """Reliable data sending with error handling"""
        try:
            json_data = json.dumps(data).encode('utf-8')
            length = str(len(json_data)).encode().ljust(16)
            sock.sendall(length + json_data)
            return True
        except Exception as e:
            return False
    
    def _reliable_recv(self, sock: socket.socket, timeout=10.0):
        """Reliable data receiving with error handling"""
        try:
            sock.settimeout(timeout)
            
            # Receive length header
            raw_length = b""
            while len(raw_length) < 16:
                chunk = sock.recv(16 - len(raw_length))
                if not chunk:
                    return None
                raw_length += chunk
            
            try:
                length = int(raw_length.decode().strip())
            except ValueError:
                return None
            
            # Receive JSON data
            json_data = b""
            while len(json_data) < length:
                chunk = sock.recv(min(4096, length - len(json_data)))
                if not chunk:
                    break
                json_data += chunk
            
            if len(json_data) != length:
                return None
                
            return json.loads(json_data.decode('utf-8'))
            
        except socket.timeout:
            return None
        except Exception:
            return None
    
    def _execute_command(self, command, session: Session):
        """Execute command on session"""
        if isinstance(command, dict) and command.get('type') == 'command':
            cmd_data = command.get('data', '')
            if cmd_data == "exit":
                return {"type": "result", "data": "EXIT"}
            else:
                # Simulate command execution
                return {"type": "result", "data": f"Command executed: {cmd_data}"}
        else:
            return {"type": "error", "data": "Invalid command format"}