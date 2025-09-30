# kush-framework/kush/core/engine.py
"""
Kush Framework Engine - Empire-inspired design
"""

import cmd
import os
import sys
import threading
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from colorama import Fore, Style

from kush.core.listener_manager import ListenerManager
from kush.core.stager_manager import StagerManager
from kush.core.agent_manager import AgentManager
from kush.core.module_manager import ModuleManager
from kush.core.session_manager import SessionManager

@dataclass
class FrameworkState:
    current_listener: Optional[str] = None
    current_agent: Optional[str] = None
    current_module: Optional[str] = None

class KushEngine(cmd.Cmd):
    """Main Kush Framework engine with Empire-style interface"""
    
    intro = f"""
{Fore.CYAN}Kush Framework v3.0{Style.RESET_ALL} - {Fore.YELLOW}Empire-inspired Penetration Testing{Style.RESET_ALL}

Type {Fore.GREEN}help{Style.RESET_ALL} for available commands
Type {Fore.GREEN}list{Style.RESET_ALL} to see available modules/listeners/stagers
"""
    
    prompt = f'{Fore.GREEN}(Kush){Style.RESET_ALL} > '
    
    def __init__(self):
        super().__init__()
        self.state = FrameworkState()
        self.session_manager = SessionManager()
        self.listener_manager = ListenerManager()
        self.module_manager = ModuleManager() 
        self.stager_manager = StagerManager()
        self.agent_manager = AgentManager()
        
        # Start background services
        self._start_services()
    
    def _start_services(self):
        """Start background framework services"""
        # Session monitor
        def session_monitor():
            while True:
                self.session_manager.cleanup_sessions()
                time.sleep(30)
        
        threading.Thread(target=session_monitor, daemon=True).start()
    
    # ===== LISTENER COMMANDS =====
    def do_listeners(self, args):
        """List all available listeners"""
        listeners = self.listener_manager.get_listeners()
        if not listeners:
            print(f"{Fore.YELLOW}[!] No listeners available{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}Available Listeners:{Style.RESET_ALL}")
        for listener in listeners:
            print(f"  {Fore.GREEN}{listener['name']:<15}{Style.RESET_ALL} - {listener['description']}")
    
    def do_uselistener(self, listener_name):
        """Use a specific listener: uselistener <name>"""
        if not listener_name:
            print(f"{Fore.RED}[-] Usage: uselistener <listener_name>{Style.RESET_ALL}")
            self.do_listeners("")
            return
        
        listener = self.listener_manager.get_listener(listener_name)
        if not listener:
            print(f"{Fore.RED}[-] Listener '{listener_name}' not found{Style.RESET_ALL}")
            self.do_listeners("")
            return
        
        self.state.current_listener = listener_name
        self.prompt = f'{Fore.GREEN}(Kush: {listener_name}){Style.RESET_ALL} > '
        print(f"{Fore.GREEN}[+] Using listener: {listener_name}{Style.RESET_ALL}")
        
        # Show listener options
        self._show_listener_options(listener)
    
    def _show_listener_options(self, listener):
        """Show listener configuration options"""
        print(f"\n{Fore.CYAN}Listener Options:{Style.RESET_ALL}")
        for option in listener.get('options', []):
            required = " (required)" if option.get('required') else ""
            value = self.listener_manager.get_option(listener['name'], option['name'])
            current = f" [current: {value}]" if value else ""
            print(f"  {Fore.YELLOW}{option['name']:<15}{Style.RESET_ALL} - {option['description']}{required}{current}")
    
    def do_set(self, args):
        """Set listener option: set <option> <value>"""
        if not self.state.current_listener:
            print(f"{Fore.RED}[-] No listener selected. Use 'uselistener' first.{Style.RESET_ALL}")
            return
        
        parts = args.split()
        if len(parts) != 2:
            print(f"{Fore.RED}[-] Usage: set <option> <value>{Style.RESET_ALL}")
            return
        
        option, value = parts
        success = self.listener_manager.set_option(self.state.current_listener, option, value)
        if success:
            print(f"{Fore.GREEN}[+] Set {option} = {value}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[-] Failed to set option{Style.RESET_ALL}")
    
    def do_info(self, args):
        """Show information about current listener/module"""
        if self.state.current_listener:
            listener = self.listener_manager.get_listener(self.state.current_listener)
            if listener:
                print(f"\n{Fore.CYAN}Listener: {listener['name']}{Style.RESET_ALL}")
                print(f"  Description: {listener['description']}")
                print(f"  Author: {listener.get('author', 'Unknown')}")
                print(f"  Options:")
                for option in listener.get('options', []):
                    current_value = self.listener_manager.get_option(self.state.current_listener, option['name'])
                    print(f"    {option['name']} = {current_value or option.get('default', '')} - {option['description']}")
    
    def do_start(self, args):
        """Start the current listener"""
        if not self.state.current_listener:
            print(f"{Fore.RED}[-] No listener selected. Use 'uselistener' first.{Style.RESET_ALL}")
            return
        
        success = self.listener_manager.start_listener(self.state.current_listener)
        if success:
            print(f"{Fore.GREEN}[+] Listener '{self.state.current_listener}' started{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[-] Failed to start listener{Style.RESET_ALL}")
    
    def do_stop(self, args):
        """Stop the current listener"""
        if not self.state.current_listener:
            print(f"{Fore.RED}[-] No listener selected.{Style.RESET_ALL}")
            return
        
        success = self.listener_manager.stop_listener(self.state.current_listener)
        if success:
            print(f"{Fore.GREEN}[+] Listener '{self.state.current_listener}' stopped{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[-] Failed to stop listener{Style.RESET_ALL}")
    
    # ===== STAGER COMMANDS =====
    def do_stagers(self, args):
        """List all available stagers"""
        stagers = self.stager_manager.get_stagers()
        if not stagers:
            print(f"{Fore.YELLOW}[!] No stagers available{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}Available Stagers:{Style.RESET_ALL}")
        for stager in stagers:
            print(f"  {Fore.GREEN}{stager['name']:<20}{Style.RESET_ALL} - {stager['description']}")
    
    def do_usestager(self, stager_name):
        """Use a specific stager: usestager <name>"""
        if not stager_name:
            print(f"{Fore.RED}[-] Usage: usestager <stager_name>{Style.RESET_ALL}")
            self.do_stagers("")
            return
        
        stager = self.stager_manager.get_stager(stager_name)
        if not stager:
            print(f"{Fore.RED}[-] Stager '{stager_name}' not found{Style.RESET_ALL}")
            self.do_stagers("")
            return
        
        self.state.current_module = stager_name
        self.prompt = f'{Fore.GREEN}(Kush: {stager_name}){Style.RESET_ALL} > '
        print(f"{Fore.GREEN}[+] Using stager: {stager_name}{Style.RESET_ALL}")
        
        # Show stager options
        self._show_stager_options(stager)
    
    def _show_stager_options(self, stager):
        """Show stager configuration options"""
        print(f"\n{Fore.CYAN}Stager Options:{Style.RESET_ALL}")
        for option in stager.get('options', []):
            required = " (required)" if option.get('required') else ""
            value = self.stager_manager.get_option(stager['name'], option['name'])
            current = f" [current: {value}]" if value else ""
            print(f"  {Fore.YELLOW}{option['name']:<15}{Style.RESET_ALL} - {option['description']}{required}{current}")
    
    def do_generate(self, args):
        """Generate a stager with current options"""
        if not self.state.current_module:
            print(f"{Fore.RED}[-] No stager selected. Use 'usestager' first.{Style.RESET_ALL}")
            return
        
        stager_path = self.stager_manager.generate_stager(self.state.current_module)
        if stager_path:
            print(f"{Fore.GREEN}[+] Stager generated: {stager_path}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[!] Execute this on the target to get an agent{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[-] Failed to generate stager{Style.RESET_ALL}")
    
    # ===== AGENT COMMANDS =====
    def do_agents(self, args):
        """List all active agents"""
        agents = self.agent_manager.get_agents()
        if not agents:
            print(f"{Fore.YELLOW}[!] No active agents{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}Active Agents ({len(agents)}):{Style.RESET_ALL}")
        for agent in agents:
            status = f"{Fore.GREEN}Active{Style.RESET_ALL}" if agent['active'] else f"{Fore.RED}Dead{Style.RESET_ALL}"
            print(f"  {Fore.GREEN}{agent['name']:<15}{Style.RESET_ALL} - {agent['hostname']} ({agent['user']}@{agent['os']}) [{status}]")
    
    def do_interact(self, agent_name):
        """Interact with an agent: interact <agent_name>"""
        if not agent_name:
            print(f"{Fore.RED}[-] Usage: interact <agent_name>{Style.RESET_ALL}")
            self.do_agents("")
            return
        
        agent = self.agent_manager.get_agent(agent_name)
        if not agent:
            print(f"{Fore.RED}[-] Agent '{agent_name}' not found{Style.RESET_ALL}")
            return
        
        self.state.current_agent = agent_name
        self.prompt = f'{Fore.GREEN}(Kush: {agent_name}){Style.RESET_ALL} > '
        print(f"{Fore.GREEN}[+] Interacting with agent: {agent_name}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Type 'back' to return to main menu{Style.RESET_ALL}")
    
    def do_shell(self, command):
        """Execute shell command on current agent: shell <command>"""
        if not self.state.current_agent:
            print(f"{Fore.RED}[-] No agent selected. Use 'interact' first.{Style.RESET_ALL}")
            return
        
        if not command:
            print(f"{Fore.RED}[-] Usage: shell <command>{Style.RESET_ALL}")
            return
        
        result = self.agent_manager.execute_command(self.state.current_agent, command)
        print(result)
    
    def do_upload(self, args):
        """Upload file to agent: upload <local_path> <remote_path>"""
        if not self.state.current_agent:
            print(f"{Fore.RED}[-] No agent selected. Use 'interact' first.{Style.RESET_ALL}")
            return
        
        parts = args.split()
        if len(parts) != 2:
            print(f"{Fore.RED}[-] Usage: upload <local_path> <remote_path>{Style.RESET_ALL}")
            return
        
        local_path, remote_path = parts
        success = self.agent_manager.upload_file(self.state.current_agent, local_path, remote_path)
        if success:
            print(f"{Fore.GREEN}[+] File uploaded successfully{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[-] File upload failed{Style.RESET_ALL}")
    
    def do_download(self, remote_path):
        """Download file from agent: download <remote_path>"""
        if not self.state.current_agent:
            print(f"{Fore.RED}[-] No agent selected. Use 'interact' first.{Style.RESET_ALL}")
            return
        
        if not remote_path:
            print(f"{Fore.RED}[-] Usage: download <remote_path>{Style.RESET_ALL}")
            return
        
        local_path = self.agent_manager.download_file(self.state.current_agent, remote_path)
        if local_path:
            print(f"{Fore.GREEN}[+] File downloaded: {local_path}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[-] File download failed{Style.RESET_ALL}")
    
    def do_back(self, args):
        """Return to main menu"""
        self.state.current_listener = None
        self.state.current_agent = None
        self.state.current_module = None
        self.prompt = f'{Fore.GREEN}(Kush){Style.RESET_ALL} > '
        print(f"{Fore.GREEN}[+] Returned to main menu{Style.RESET_ALL}")
    
    # ===== MODULE COMMANDS =====
    def do_modules(self, args):
        """List all available modules"""
        modules = self.module_manager.get_modules()
        if not modules:
            print(f"{Fore.YELLOW}[!] No modules available{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.CYAN}Available Modules:{Style.RESET_ALL}")
        for category, module_list in modules.items():
            print(f"\n{Fore.YELLOW}{category}:{Style.RESET_ALL}")
            for module in module_list:
                print(f"  {Fore.GREEN}{module['name']:<25}{Style.RESET_ALL} - {module['description']}")
    
    def do_usemodule(self, module_name):
        """Use a specific module: usemodule <name>"""
        if not module_name:
            print(f"{Fore.RED}[-] Usage: usemodule <module_name>{Style.RESET_ALL}")
            self.do_modules("")
            return
        
        module = self.module_manager.get_module(module_name)
        if not module:
            print(f"{Fore.RED}[-] Module '{module_name}' not found{Style.RESET_ALL}")
            self.do_modules("")
            return
        
        self.state.current_module = module_name
        self.prompt = f'{Fore.GREEN}(Kush: {module_name}){Style.RESET_ALL} > '
        print(f"{Fore.GREEN}[+] Using module: {module_name}{Style.RESET_ALL}")
        
        # Show module options
        self._show_module_options(module)
    
    def _show_module_options(self, module):
        """Show module configuration options"""
        print(f"\n{Fore.CYAN}Module Options:{Style.RESET_ALL}")
        for option in module.get('options', []):
            required = " (required)" if option.get('required') else ""
            print(f"  {Fore.YELLOW}{option['name']:<15}{Style.RESET_ALL} - {option['description']}{required}")
    
    def do_run(self, args):
        """Execute the current module"""
        if not self.state.current_module:
            print(f"{Fore.RED}[-] No module selected. Use 'usemodule' first.{Style.RESET_ALL}")
            return
        
        if not self.state.current_agent:
            print(f"{Fore.RED}[-] No agent selected. Use 'interact' first.{Style.RESET_ALL}")
            return
        
        result = self.module_manager.execute_module(self.state.current_module, self.state.current_agent)
        print(result)
    
    # ===== FRAMEWORK COMMANDS =====
    def do_help(self, args):
        """Show help menu"""
        help_text = f"""
{Fore.CYAN}Kush Framework v3.0 - Empire-inspired Commands{Style.RESET_ALL}

{Fore.YELLOW}Listener Management:{Style.RESET_ALL}
  {Fore.GREEN}listeners{Style.RESET_ALL}                    - List available listeners
  {Fore.GREEN}uselistener <name>{Style.RESET_ALL}          - Use a specific listener
  {Fore.GREEN}set <option> <value>{Style.RESET_ALL}        - Set listener option
  {Fore.GREEN}info{Style.RESET_ALL}                        - Show listener info
  {Fore.GREEN}start{Style.RESET_ALL}                       - Start listener
  {Fore.GREEN}stop{Style.RESET_ALL}                        - Stop listener

{Fore.YELLOW}Stager Management:{Style.RESET_ALL}
  {Fore.GREEN}stagers{Style.RESET_ALL}                     - List available stagers
  {Fore.GREEN}usestager <name>{Style.RESET_ALL}           - Use a specific stager
  {Fore.GREEN}set <option> <value>{Style.RESET_ALL}        - Set stager option
  {Fore.GREEN}generate{Style.RESET_ALL}                    - Generate stager

{Fore.YELLOW}Agent Management:{Style.RESET_ALL}
  {Fore.GREEN}agents{Style.RESET_ALL}                      - List active agents
  {Fore.GREEN}interact <agent>{Style.RESET_ALL}           - Interact with agent
  {Fore.GREEN}shell <command>{Style.RESET_ALL}            - Execute command on agent
  {Fore.GREEN}upload <local> <remote>{Style.RESET_ALL}    - Upload file to agent
  {Fore.GREEN}download <remote>{Style.RESET_ALL}          - Download file from agent
  {Fore.GREEN}back{Style.RESET_ALL}                       - Return to main menu

{Fore.YELLOW}Module Management:{Style.RESET_ALL}
  {Fore.GREEN}modules{Style.RESET_ALL}                     - List available modules
  {Fore.GREEN}usemodule <name>{Style.RESET_ALL}           - Use a specific module
  {Fore.GREEN}run{Style.RESET_ALL}                        - Execute module on agent

{Fore.YELLOW}Framework:{Style.RESET_ALL}
  {Fore.GREEN}help{Style.RESET_ALL}                        - Show this help
  {Fore.GREEN}exit{Style.RESET_ALL}                       - Exit framework
  {Fore.GREEN}reset{Style.RESET_ALL}                      - Reset framework
  {Fore.GREEN}version{Style.RESET_ALL}                    - Show version

{Fore.CYAN}Examples:{Style.RESET_ALL}
  uselistener http
  set Host 0.0.0.0
  set Port 8080
  start
  
  usestager windows_dropper
  set Listener http
  generate
  
  interact WIN-AGENT1
  shell whoami
  usemodule mimikatz
  run
"""
        print(help_text)
    
    def do_exit(self, args):
        """Exit the framework"""
        print(f"{Fore.YELLOW}[!] Shutting down Kush Framework...{Style.RESET_ALL}")
        self.listener_manager.stop_all_listeners()
        return True
    
    def do_quit(self, args):
        """Exit the framework"""
        return self.do_exit(args)
    
    def do_reset(self, args):
        """Reset the framework"""
        print(f"{Fore.YELLOW}[!] Resetting framework state...{Style.RESET_ALL}")
        self.state = FrameworkState()
        self.prompt = f'{Fore.GREEN}(Kush){Style.RESET_ALL} > '
        print(f"{Fore.GREEN}[+] Framework reset{Style.RESET_ALL}")
    
    def do_version(self, args):
        """Show framework version"""
        print(f"{Fore.CYAN}Kush Framework v3.0 - Empire-inspired Penetration Testing{Style.RESET_ALL}")
    
    # ===== OVERRIDE CMD METHODS =====
    def emptyline(self):
        """Do nothing on empty line"""
        pass
    
    def default(self, line):
        """Handle unknown commands"""
        print(f"{Fore.RED}[-] Unknown command: {line}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[!] Type 'help' for available commands{Style.RESET_ALL}")
    
    def precmd(self, line):
        """Process command before execution"""
        if line.strip() == 'EOF':
            return 'exit'
        return line