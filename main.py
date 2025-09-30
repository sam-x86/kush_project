#!/usr/bin/env python3
"""
Kush Framework - Empire-inspired Penetration Testing Framework
"""

import sys
import os
import argparse
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Configure logging before imports
from kush.utils.logging import setup_logging
setup_logging()

try:
    from kush.core.engine import KushEngine
    from kush.utils.helpers import display_banner, setup_tab_completion, setup_directories
    from colorama import Fore, Style, init as colorama_init
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("🔧 Please install dependencies: pip install -r requirements.txt")
    sys.exit(1)

def main():
    """Main entry point"""
    colorama_init()
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Kush Framework')
    parser.add_argument('--reset', action='store_true', help='Reset framework')
    parser.add_argument('--setup', action='store_true', help='Run setup')
    args = parser.parse_args()
    
    # Setup environment
    setup_directories()
    
    if args.reset:
        print(f"{Fore.YELLOW}[!] Reset functionality would be implemented here{Style.RESET_ALL}")
    
    if args.setup:
        print(f"{Fore.YELLOW}[!] Setup functionality would be implemented here{Style.RESET_ALL}")
    
    display_banner()
    
    try:
        # Initialize and start engine
        engine = KushEngine()
        
        print(f"\n{Fore.GREEN}🚀 Kush Framework v3.0 (Empire-inspired){Style.RESET_ALL}")
        print(f"{Fore.CYAN}💡 Type 'help' for available commands{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}🔗 Modular architecture with stagers and agents{Style.RESET_ALL}")
        
        # Main command loop
        engine.cmdloop()
                
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Exiting Kush Framework{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Failed to start Kush Framework: {e}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == '__main__':
    main()