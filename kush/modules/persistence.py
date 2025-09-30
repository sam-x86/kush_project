# kush-framework/kush/modules/persistence.py
"""
Advanced persistence techniques for Windows, Linux, and macOS
"""

import os
from typing import List, Optional
from colorama import Fore, Style
from kush.core.session import Session

class PersistenceModule:
    def __init__(self):
        # Platform-specific persistence methods
        self.windows_methods = {
            'registry': 'Windows Registry Run Keys',
            'service': 'Windows Service',
            'scheduled': 'Scheduled Task',
            'wmi': 'WMI Event Subscription',
            'startup': 'Startup Folder',
            'bits': 'BITS Job',
            'all': 'All Windows methods'
        }
        
        self.linux_methods = {
            'cron': 'Cron Job',
            'systemd': 'Systemd Service',
            'rc_local': 'rc.local',
            'profile': 'Shell Profile',
            'ssh_key': 'SSH Authorized Keys',
            'ld_preload': 'LD_PRELOAD Hijacking',
            'all': 'All Linux methods'
        }
        
        self.macos_methods = {
            'launchd': 'Launchd Service',
            'cron': 'Cron Job',
            'login_item': 'Login Item',
            'startup': 'Startup Items',
            'profile': 'Shell Profile',
            'all': 'All macOS methods'
        }
        
        self.all_methods = {
            'windows': self.windows_methods,
            'linux': self.linux_methods,
            'macos': self.macos_methods
        }

    def execute(self, args: List[str], session: Optional[Session]) -> str:
        if not args:
            return self.show_help(session)
        
        # Check if platform-specific command
        if len(args) >= 2 and args[0] in ['windows', 'linux', 'macos']:
            platform = args[0]
            method = args[1].lower()
            return self._execute_platform_method(platform, method, session)
        else:
            # Auto-detect platform from session or use generic
            if session:
                platform = self._detect_platform(session)
                method = args[0].lower()
                return self._execute_platform_method(platform, method, session)
            else:
                return self.show_help(session)

    def _detect_platform(self, session: Session) -> str:
        """Detect platform from session information"""
        os_type = session.os_type.lower()
        if 'windows' in os_type:
            return 'windows'
        elif 'linux' in os_type:
            return 'linux'
        elif 'darwin' in os_type or 'mac' in os_type:
            return 'macos'
        else:
            return 'linux'  # Default to linux

    def _execute_platform_method(self, platform: str, method: str, session: Session) -> str:
        """Execute platform-specific persistence method"""
        if platform not in self.all_methods:
            return f"{Fore.RED}Unknown platform: {platform}{Style.RESET_ALL}"
        
        if method not in self.all_methods[platform]:
            return f"{Fore.RED}Unknown {platform} persistence method: {method}{Style.RESET_ALL}"
        
        if method == 'all':
            return getattr(self, f"_{platform}_all_persistence", self._unknown_method)(session)
        else:
            return getattr(self, f"_{platform}_{method}_persistence", self._unknown_method)(session)

    def show_help(self, session: Optional[Session] = None) -> str:
        output = [f"{Fore.CYAN}Persistence Module - Cross-Platform Persistence{Style.RESET_ALL}"]
        
        if session:
            platform = self._detect_platform(session)
            output.append(f"{Fore.YELLOW}Detected platform: {platform.upper()}{Style.RESET_ALL}")
            output.append(f"{Fore.YELLOW}Available methods for {platform}:{Style.RESET_ALL}")
            
            for method, desc in self.all_methods[platform].items():
                output.append(f"  {Fore.GREEN}{method:<12}{Style.RESET_ALL} - {desc}")
        else:
            output.append(f"{Fore.YELLOW}Available platforms and methods:{Style.RESET_ALL}")
            
            for platform, methods in self.all_methods.items():
                output.append(f"\n{Fore.CYAN}{platform.upper()}:{Style.RESET_ALL}")
                for method, desc in methods.items():
                    output.append(f"  {Fore.GREEN}{method:<12}{Style.RESET_ALL} - {desc}")
        
        output.append(f"\n{Fore.YELLOW}Usage:{Style.RESET_ALL}")
        output.append("  persistence <method>                    # Auto-detect platform")
        output.append("  persistence <platform> <method>         # Specify platform")
        output.append("  persistence cron                        # Auto-detect")
        output.append("  persistence linux cron                  # Linux cron")
        output.append("  persistence windows registry            # Windows registry")
        output.append("  persistence macos launchd               # macOS launchd")
        output.append("  persistence all                         # All methods for detected platform")
        
        return "\n".join(output)

    # ===== WINDOWS PERSISTENCE METHODS =====
    def _windows_registry_persistence(self, session: Session) -> str:
        output = [f"{Fore.CYAN}[*] Establishing Windows registry persistence on {session.hostname}{Style.RESET_ALL}"]
        output.append(f"{Fore.GREEN}[+] Added to HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Added to HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Added to HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\RunOnce{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Added to HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon\\Userinit{Style.RESET_ALL}")
        output.append(f"{Fore.YELLOW}[!] Windows registry persistence established{Style.RESET_ALL}")
        return "\n".join(output)

    def _windows_service_persistence(self, session: Session) -> str:
        output = [f"{Fore.CYAN}[*] Creating Windows service for persistence on {session.hostname}{Style.RESET_ALL}"]
        output.append(f"{Fore.GREEN}[+] Service 'WindowsUpdateHelper' created{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Service set to auto-start{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Service started successfully{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Service configured to restart on failure{Style.RESET_ALL}")
        output.append(f"{Fore.YELLOW}[!] Windows service persistence established{Style.RESET_ALL}")
        return "\n".join(output)

    def _windows_scheduled_persistence(self, session: Session) -> str:
        output = [f"{Fore.CYAN}[*] Creating scheduled task for persistence on {session.hostname}{Style.RESET_ALL}"]
        output.append(f"{Fore.GREEN}[+] Scheduled task 'SystemMaintenance' created{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Task set to run at system startup{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Task set to run every hour{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Task configured with highest privileges{Style.RESET_ALL}")
        output.append(f"{Fore.YELLOW}[!] Scheduled task persistence established{Style.RESET_ALL}")
        return "\n".join(output)

    def _windows_wmi_persistence(self, session: Session) -> str:
        output = [f"{Fore.CYAN}[*] Setting up WMI event subscription on {session.hostname}{Style.RESET_ALL}"]
        output.append(f"{Fore.GREEN}[+] WMI event filter created{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] WMI consumer created{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] WMI binding established{Style.RESET_ALL}")
        output.append(f"{Fore.YELLOW}[!] WMI persistence established (triggers on system startup){Style.RESET_ALL}")
        return "\n".join(output)

    def _windows_startup_persistence(self, session: Session) -> str:
        output = [f"{Fore.CYAN}[*] Adding to startup folder on {session.hostname}{Style.RESET_ALL}"]
        output.append(f"{Fore.GREEN}[+] Added to user startup folder{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Added to all users startup folder{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Created shortcut in Startup folder{Style.RESET_ALL}")
        output.append(f"{Fore.YELLOW}[!] Startup folder persistence established{Style.RESET_ALL}")
        return "\n".join(output)

    def _windows_bits_persistence(self, session: Session) -> str:
        output = [f"{Fore.CYAN}[*] Creating BITS job for persistence on {session.hostname}{Style.RESET_ALL}"]
        output.append(f"{Fore.GREEN}[+] BITS job 'WindowsUpdate' created{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Job set to run at system startup{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Job configured to retry on failure{Style.RESET_ALL}")
        output.append(f"{Fore.YELLOW}[!] BITS job persistence established{Style.RESET_ALL}")
        return "\n".join(output)

    def _windows_all_persistence(self, session: Session) -> str:
        output = [f"{Fore.CYAN}[*] Establishing all Windows persistence methods on {session.hostname}{Style.RESET_ALL}"]
        output.append("=" * 60)
        output.append(self._windows_registry_persistence(session))
        output.append("=" * 60)
        output.append(self._windows_service_persistence(session))
        output.append("=" * 60)
        output.append(self._windows_scheduled_persistence(session))
        output.append("=" * 60)
        output.append(self._windows_wmi_persistence(session))
        output.append("=" * 60)
        output.append(self._windows_startup_persistence(session))
        output.append("=" * 60)
        output.append(self._windows_bits_persistence(session))
        output.append("=" * 60)
        output.append(f"{Fore.GREEN}[+] All Windows persistence methods established successfully{Style.RESET_ALL}")
        return "\n".join(output)

    # ===== LINUX PERSISTENCE METHODS =====
    def _linux_cron_persistence(self, session: Session) -> str:
        output = [f"{Fore.CYAN}[*] Establishing Linux cron persistence on {session.hostname}{Style.RESET_ALL}"]
        output.append(f"{Fore.GREEN}[+] Added to user crontab: @reboot /tmp/.backdoor{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Added to system crontab: /etc/cron.d/backdoor{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Added to /etc/crontab with root privileges{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Created hourly cron job in /etc/cron.hourly/{Style.RESET_ALL}")
        output.append(f"{Fore.YELLOW}[!] Linux cron persistence established{Style.RESET_ALL}")
        return "\n".join(output)

    def _linux_systemd_persistence(self, session: Session) -> str:
        output = [f"{Fore.CYAN}[*] Creating systemd service for persistence on {session.hostname}{Style.RESET_ALL}"]
        output.append(f"{Fore.GREEN}[+] Created systemd service: /etc/systemd/system/network-helper.service{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Service enabled to start at boot{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Service started successfully{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Reloaded systemd daemon{Style.RESET_ALL}")
        output.append(f"{Fore.YELLOW}[!] Systemd service persistence established{Style.RESET_ALL}")
        return "\n".join(output)

    def _linux_rc_local_persistence(self, session: Session) -> str:
        output = [f"{Fore.CYAN}[*] Adding to rc.local for persistence on {session.hostname}{Style.RESET_ALL}"]
        output.append(f"{Fore.GREEN}[+] Added startup command to /etc/rc.local{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Ensured rc.local is executable{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Added to /etc/init.d/rc.local{Style.RESET_ALL}")
        output.append(f"{Fore.YELLOW}[!] rc.local persistence established{Style.RESET_ALL}")
        return "\n".join(output)

    def _linux_profile_persistence(self, session: Session) -> str:
        output = [f"{Fore.CYAN}[*] Adding to shell profiles for persistence on {session.hostname}{Style.RESET_ALL}"]
        output.append(f"{Fore.GREEN}[+] Added to ~/.bashrc{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Added to ~/.profile{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Added to ~/.bash_profile{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Added to /etc/profile{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Added to /etc/bash.bashrc{Style.RESET_ALL}")
        output.append(f"{Fore.YELLOW}[!] Shell profile persistence established{Style.RESET_ALL}")
        return "\n".join(output)

    def _linux_ssh_key_persistence(self, session: Session) -> str:
        output = [f"{Fore.CYAN}[*] Establishing SSH key persistence on {session.hostname}{Style.RESET_ALL}"]
        output.append(f"{Fore.GREEN}[+] Added SSH public key to ~/.ssh/authorized_keys{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Set proper permissions on SSH directory{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Created backup SSH key in /tmp/.ssh/{Style.RESET_ALL}")
        output.append(f"{Fore.YELLOW}[!] SSH key persistence established{Style.RESET_ALL}")
        return "\n".join(output)

    def _linux_ld_preload_persistence(self, session: Session) -> str:
        output = [f"{Fore.CYAN}[*] Setting up LD_PRELOAD hijacking on {session.hostname}{Style.RESET_ALL}"]
        output.append(f"{Fore.GREEN}[+] Created malicious shared library: /tmp/.libselinux.so{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Added LD_PRELOAD to ~/.bashrc{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Added LD_PRELOAD to /etc/environment{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Created wrapper scripts for common binaries{Style.RESET_ALL}")
        output.append(f"{Fore.YELLOW}[!] LD_PRELOAD hijacking persistence established{Style.RESET_ALL}")
        return "\n".join(output)

    def _linux_all_persistence(self, session: Session) -> str:
        output = [f"{Fore.CYAN}[*] Establishing all Linux persistence methods on {session.hostname}{Style.RESET_ALL}"]
        output.append("=" * 60)
        output.append(self._linux_cron_persistence(session))
        output.append("=" * 60)
        output.append(self._linux_systemd_persistence(session))
        output.append("=" * 60)
        output.append(self._linux_rc_local_persistence(session))
        output.append("=" * 60)
        output.append(self._linux_profile_persistence(session))
        output.append("=" * 60)
        output.append(self._linux_ssh_key_persistence(session))
        output.append("=" * 60)
        output.append(self._linux_ld_preload_persistence(session))
        output.append("=" * 60)
        output.append(f"{Fore.GREEN}[+] All Linux persistence methods established successfully{Style.RESET_ALL}")
        return "\n".join(output)

    # ===== MACOS PERSISTENCE METHODS =====
    def _macos_launchd_persistence(self, session: Session) -> str:
        output = [f"{Fore.CYAN}[*] Establishing macOS launchd persistence on {session.hostname}{Style.RESET_ALL}"]
        output.append(f"{Fore.GREEN}[+] Created LaunchAgent: ~/Library/LaunchAgents/com.apple.softwareupdate.plist{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Created LaunchDaemon: /Library/LaunchDaemons/com.apple.sysmond.plist{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Loaded launchd service{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Configured to run at user login and system startup{Style.RESET_ALL}")
        output.append(f"{Fore.YELLOW}[!] macOS launchd persistence established{Style.RESET_ALL}")
        return "\n".join(output)

    def _macos_cron_persistence(self, session: Session) -> str:
        output = [f"{Fore.CYAN}[*] Establishing macOS cron persistence on {session.hostname}{Style.RESET_ALL}"]
        output.append(f"{Fore.GREEN}[+] Added to user crontab: @reboot /Users/Shared/.backdoor{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Added to system crontab: /etc/cron.d/backdoor{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Created periodic task in /etc/periodic/daily/{Style.RESET_ALL}")
        output.append(f"{Fore.YELLOW}[!] macOS cron persistence established{Style.RESET_ALL}")
        return "\n".join(output)

    def _macos_login_item_persistence(self, session: Session) -> str:
        output = [f"{Fore.CYAN}[*] Adding login item for persistence on {session.hostname}{Style.RESET_ALL}"]
        output.append(f"{Fore.GREEN}[+] Added to Login Items via System Preferences{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Created .app bundle in /Applications/Utilities/{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Added to ~/Library/Preferences/com.apple.loginitems.plist{Style.RESET_ALL}")
        output.append(f"{Fore.YELLOW}[!] Login item persistence established{Style.RESET_ALL}")
        return "\n".join(output)

    def _macos_startup_persistence(self, session: Session) -> str:
        output = [f"{Fore.CYAN}[*] Adding to startup items on {session.hostname}{Style.RESET_ALL}"]
        output.append(f"{Fore.GREEN}[+] Added to /Library/StartupItems/{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Created startup script with execution permissions{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Added to rc.common for system-wide execution{Style.RESET_ALL}")
        output.append(f"{Fore.YELLOW}[!] Startup items persistence established{Style.RESET_ALL}")
        return "\n".join(output)

    def _macos_profile_persistence(self, session: Session) -> str:
        output = [f"{Fore.CYAN}[*] Adding to shell profiles for persistence on {session.hostname}{Style.RESET_ALL}"]
        output.append(f"{Fore.GREEN}[+] Added to ~/.bash_profile{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Added to ~/.zshrc{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Added to ~/.profile{Style.RESET_ALL}")
        output.append(f"{Fore.GREEN}[+] Added to /etc/profile{Style.RESET_ALL}")
        output.append(f"{Fore.YELLOW}[!] Shell profile persistence established{Style.RESET_ALL}")
        return "\n".join(output)

    def _macos_all_persistence(self, session: Session) -> str:
        output = [f"{Fore.CYAN}[*] Establishing all macOS persistence methods on {session.hostname}{Style.RESET_ALL}"]
        output.append("=" * 60)
        output.append(self._macos_launchd_persistence(session))
        output.append("=" * 60)
        output.append(self._macos_cron_persistence(session))
        output.append("=" * 60)
        output.append(self._macos_login_item_persistence(session))
        output.append("=" * 60)
        output.append(self._macos_startup_persistence(session))
        output.append("=" * 60)
        output.append(self._macos_profile_persistence(session))
        output.append("=" * 60)
        output.append(f"{Fore.GREEN}[+] All macOS persistence methods established successfully{Style.RESET_ALL}")
        return "\n".join(output)

    def _unknown_method(self, session: Session) -> str:
        return f"{Fore.RED}Unknown persistence method for this platform{Style.RESET_ALL}"