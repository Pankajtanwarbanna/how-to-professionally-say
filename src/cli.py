import argparse
import sys
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.theme import Theme
from dotenv import load_dotenv
import pyperclip

from src.client import OpenAIClient
from src.config import get_config
from src.utils.formatting import format_result_panel, format_error_panel

custom_theme = Theme({
    "info": "dim cyan",
    "input": "green",
    "output": "bold blue",
    "error": "bold red",
})

console = Console(theme=custom_theme)

class HowToProfessionallySayCLI:
    def __init__(self):
        self.console = console
        load_dotenv()  # Loading environment variables from .env file
        
        config = get_config()
        
        try:
            self.openai_client = OpenAIClient(api_key=config.get("OPENAI_API_KEY"))
        except ValueError as e:
            self.console.print(Panel(
                "[error]OpenAI API key not found. Please set the OPENAI_API_KEY environment variable "
                "or create a .env file with OPENAI_API_KEY=your_api_key[/error]",
                title="Error",
                border_style="red"
            ))
            sys.exit(1)
    
    def parse_arguments(self) -> argparse.Namespace:
        parser = argparse.ArgumentParser(
            description="Transform casual text into professional workplace language"
        )
        
        parser.add_argument(
            "--input", "-i",
            type=str,
            help="Casual text to transform (if not provided, interactive mode will be used)"
        )
        
        return parser.parse_args()
    
    def display_header(self):
        self.console.print(Panel(
            "[bold]How To Professionally Say[/bold]\n"
            "Transform casual text into professional workplace language",
            border_style="cyan"
        ))
    
    def get_input_text(self, args: argparse.Namespace) -> str:
        if args.input:
            return args.input
        
        self.console.print()
        return Prompt.ask("[input]Drop your unfiltered message here")
    
    def display_result(self, input_text: str, professional_text: str):
        self.console.print()
        self.console.print(format_result_panel(input_text, professional_text))
    
    def run(self):
        self.display_header()
        args = self.parse_arguments()
        
        input_text = self.get_input_text(args)
        
        if not input_text:
            self.console.print("[error]No input provided. Exiting.[/error]")
            return
        
        with self.console.status("[info]Adding corporate sugar-coating...[/info]"):
            professional_text = self.openai_client.get_professional_response(input_text)
        
        if professional_text:
            self.display_result(input_text, professional_text)
        else:
            self.console.print("[error]Failed to transform text. Please try again.[/error]")