from colorama import Fore, Style
from rich.console import Console
from rich.table import Table
import json
from datetime import datetime

console = Console()

def print_info(message):
    console.print(f"[bold blue][*][/bold blue] {message}")

def print_success(message):
    console.print(f"[bold green][+][/bold green] {message}")

def print_error(message):
    console.print(f"[bold red][-][/bold red] {message}")

def print_warning(message):
    console.print(f"[bold yellow][!][/bold yellow] {message}")

def create_table(title, columns, rows):
    table = Table(title=title)
    for column in columns:
        table.add_column(column, style="cyan")
    for row in rows:
        table.add_row(*row)
    console.print(table)

def save_results(data, filename=None):
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"darkice_report_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print_success(f"Результаты сохранены в {filename}")