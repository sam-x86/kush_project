# kush-framework/kush/core/agent_manager.py
"""
Agent manager for Empire-style agents
"""

import time
import uuid
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from colorama import Fore, Style

@dataclass
class Agent:
    name: str
    hostname: str
    user: str
    os: str
    architecture: str
    process_id: int
    listener: str
    first_seen: float = field(default_factory=time.time)
    last_seen: float = field(default_factory=time.time)
    active: bool = True

class AgentManager:
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        
        # Add some mock agents for demonstration
        self._add_mock_agents()
    
    def _add_mock_agents(self):
        """Add mock agents for demonstration"""
        mock_agents = [
            Agent("WIN-AGENT1", "DESKTOP-123", "Administrator", "Windows", "x64", 1234, "http"),
            Agent("LINUX-AGENT1", "ubuntu-server", "root", "Linux", "x64", 5678, "tcp"),
            Agent("MAC-AGENT1", "macbook-pro", "user", "macOS", "x64", 9012, "http"),
        ]
        
        for agent in mock_agents:
            self.agents[agent.name] = agent
    
    def get_agents(self) -> List[Dict[str, Any]]:
        """Get all agents"""
        return [
            {
                'name': agent.name,
                'hostname': agent.hostname,
                'user': agent.user,
                'os': agent.os,
                'architecture': agent.architecture,
                'listener': agent.listener,
                'active': agent.active,
                'first_seen': time.ctime(agent.first_seen),
                'last_seen': time.ctime(agent.last_seen),
            }
            for agent in self.agents.values()
        ]
    
    def get_agent(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Get specific agent"""
        agent = self.agents.get(agent_name)
        if not agent:
            return None
        
        return {
            'name': agent.name,
            'hostname': agent.hostname,
            'user': agent.user,
            'os': agent.os,
            'architecture': agent.architecture,
            'listener': agent.listener,
            'active': agent.active,
            'first_seen': time.ctime(agent.first_seen),
            'last_seen': time.ctime(agent.last_seen),
        }
    
    def execute_command(self, agent_name: str, command: str) -> str:
        """Execute command on agent"""
        agent = self.agents.get(agent_name)
        if not agent:
            return f"{Fore.RED}[-] Agent '{agent_name}' not found{Style.RESET_ALL}"
        
        # Update last seen
        agent.last_seen = time.time()
        
        # Mock command execution with platform-specific responses
        if command.lower() == 'whoami':
            return f"{agent.user}"
        elif command.lower() == 'hostname':
            return f"{agent.hostname}"
        elif command.lower() == 'uname' or command.lower() == 'ver':
            return f"{agent.os}"
        elif command.lower() == 'pwd' or command.lower().startswith('cd '):
            return f"/home/{agent.user}" if agent.os != "Windows" else f"C:\\Users\\{agent.user}"
        elif command.lower() == 'ls' or command.lower() == 'dir':
            return "file1.txt\nfile2.txt\nfolder1"
        elif command.lower() == 'ipconfig' or command.lower() == 'ifconfig':
            return "eth0: 192.168.1.100\nlo: 127.0.0.1"
        else:
            return f"Command '{command}' executed on {agent_name}\nOutput: Mock execution successful"
    
    def upload_file(self, agent_name: str, local_path: str, remote_path: str) -> bool:
        """Upload file to agent"""
        agent = self.agents.get(agent_name)
        if not agent:
            return False
        
        # Update last seen
        agent.last_seen = time.time()
        
        # Mock upload
        print(f"{Fore.CYAN}[*] Uploading {local_path} to {agent_name}:{remote_path}{Style.RESET_ALL}")
        return True
    
    def download_file(self, agent_name: str, remote_path: str) -> Optional[str]:
        """Download file from agent"""
        agent = self.agents.get(agent_name)
        if not agent:
            return None
        
        # Update last seen
        agent.last_seen = time.time()
        
        # Create downloads directory
        downloads_dir = Path("downloads")
        downloads_dir.mkdir(exist_ok=True)
        
        # Mock download
        local_path = f"downloads/{agent_name}_{os.path.basename(remote_path)}"
        print(f"{Fore.CYAN}[*] Downloading {agent_name}:{remote_path} to {local_path}{Style.RESET_ALL}")
        
        # Create a mock downloaded file
        with open(local_path, 'w') as f:
            f.write(f"Mock content downloaded from {agent_name}:{remote_path}")
        
        return local_path
    
    def register_agent(self, agent_data: Dict[str, Any]) -> str:
        """Register a new agent"""
        agent_name = f"{agent_data['os'].upper()}-{str(uuid.uuid4())[:8]}"
        
        agent = Agent(
            name=agent_name,
            hostname=agent_data.get('hostname', 'unknown'),
            user=agent_data.get('user', 'unknown'),
            os=agent_data.get('os', 'unknown'),
            architecture=agent_data.get('architecture', 'x64'),
            process_id=agent_data.get('process_id', 0),
            listener=agent_data.get('listener', 'unknown')
        )
        
        self.agents[agent_name] = agent
        return agent_name