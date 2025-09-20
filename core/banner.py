from colorama import Fore, Style

def show_banner():
    banner = f"""
{Fore.RED}
██████╗  █████╗ ██████╗ ██╗  ██╗██╗ ██████╗███████╗
██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝██║██╔════╝██╔════╝
██║  ██║███████║██████╔╝█████╔╝ ██║██║     █████╗  
██║  ██║██╔══██║██╔══██╗██╔═██╗ ██║██║     ██╔══╝  
██████╔╝██║  ██║██║  ██║██║  ██╗██║╚██████╗███████╗
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝ ╚═════╝╚══════╝
{Style.RESET_ALL}
{Fore.CYAN}DarkIce OSINT Framework v1.0{Style.RESET_ALL}
{Fore.YELLOW}Created by Cyber Brothers{Style.RESET_ALL}
"""
    print(banner)