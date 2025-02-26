import os
from typing import Dict, Any

def get_config() -> Dict[str, Any]:
    config = {
        "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY"),
        "OPENAI_MODEL": os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
        "MAX_TOKENS": int(os.environ.get("MAX_TOKENS", "150")),
        "TEMPERATURE": float(os.environ.get("TEMPERATURE", "0.7")),
    }
    
    return config