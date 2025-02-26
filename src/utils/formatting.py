from rich.panel import Panel
from rich.text import Text
from rich.console import Console
import pyperclip

def format_result_panel(input_text: str, output_text: str) -> Panel:
    try:
        pyperclip.copy(output_text)
        clipboard_msg = "✓ Copied to clipboard"
    except Exception:
        clipboard_msg = "❌ Failed to copy to clipboard"
    
    content = Text()
    content.append("Original:\n", style="dim")
    content.append(f"{input_text}\n\n")
    content.append("Say This Instead ↓\n", style="bold")
    content.append(f"{output_text}\n\n")
    content.append(clipboard_msg, style="dim italic")
    
    return Panel(
        content,
        title="Transformation Result",
        border_style="green"
    )

def format_error_panel(message: str) -> Panel:
    return Panel(
        Text(message, style="bold red"),
        title="Error",
        border_style="red"
    )