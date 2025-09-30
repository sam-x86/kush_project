# kush-framework/kush/listeners/http_listener.py
"""
HTTP listener for Empire-style communication
"""

import http.server
import socketserver
import threading
import json
from typing import Optional
from colorama import Fore, Style

class HTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<h1>Kush Framework HTTP Listener</h1>")
        elif self.path.startswith('/agent'):
            self.send_response(200)
            self.send_header('Content-type', 'application/octet-stream')
            self.end_headers()
            # In a real implementation, this would serve the actual agent
            self.wfile.write(b"Mock agent binary content")
        else:
            self.send_error(404, "File not found")
    
    def do_POST(self):
        """Handle POST requests - agent checkin"""
        if self.path == '/checkin':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode())
                print(f"{Fore.GREEN}[+] Agent checkin from {self.client_address[0]}: {data}{Style.RESET_ALL}")
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"status": "ok", "task": None}
                self.wfile.write(json.dumps(response).encode())
            except Exception as e:
                self.send_error(500, f"Error: {e}")
        else:
            self.send_error(404, "Endpoint not found")
    
    def log_message(self, format, *args):
        """Override to suppress normal HTTP logs"""
        # Uncomment for debugging
        # print(f"[HTTP] {format % args}")
        pass

class HTTPListener:
    def __init__(self, host: str = '0.0.0.0', port: int = 8080):
        self.host = host
        self.port = port
        self.server: Optional[socketserver.TCPServer] = None
        self.thread: Optional[threading.Thread] = None
        self.running = False
    
    def start(self):
        """Start HTTP listener"""
        try:
            self.server = socketserver.TCPServer((self.host, self.port), HTTPHandler)
            self.running = True
            
            print(f"{Fore.GREEN}[+] HTTP listener started on {self.host}:{self.port}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*] Endpoints:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*]   GET  /agent.*    - Serve agent payloads{Style.RESET_ALL}")
            print(f"{Fore.CYAN}[*]   POST /checkin    - Agent checkin{Style.RESET_ALL}")
            
            # Run in a thread to avoid blocking
            self.thread = threading.Thread(target=self.server.serve_forever)
            self.thread.daemon = True
            self.thread.start()
            
        except Exception as e:
            print(f"{Fore.RED}[-] HTTP listener error: {e}{Style.RESET_ALL}")
            self.running = False
    
    def stop(self):
        """Stop HTTP listener"""
        self.running = False
        if self.server:
            self.server.shutdown()
            self.server.server_close()
