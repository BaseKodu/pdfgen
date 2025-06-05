import subprocess
import json
import os
from pathlib import Path


class JSXConverter:
    def __init__(self, node_script_path="convertors/jsx-converter.js"):
        self.node_script_path = node_script_path
        
    def convert(self, jsx_string:str, context=None):
        """
        Convert JSX string to HTML using Node.js
        
        Args:
            jsx_string (str): JSX template string
            context (dict): Variables to pass to the JSX template
            
        Returns:
            str: Converted HTML string
        """
        if context is None:
            context = {}
            
        try:
            # Escape quotes in JSX string for shell
            jsx_escaped = jsx_string.replace('"', '\\"').replace("'", "\\'")
            context_json = json.dumps(context)
            
            # Call Node.js script
            result = subprocess.run([
                'node', 
                self.node_script_path, 
                jsx_escaped, 
                context_json
            ], capture_output=True, text=True, check=True)
            
            return result.stdout.strip()
            
        except subprocess.CalledProcessError as e:
            raise Exception(f"JSX conversion failed: {e.stderr}")
        except FileNotFoundError:
            raise Exception("Node.js not found. Please install Node.js")
