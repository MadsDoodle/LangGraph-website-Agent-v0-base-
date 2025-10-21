# =============================================================================
# FILESYSTEM TOOLS MODULE
# =============================================================================
# This module provides secure file operations for the web builder agent.
# Maps to: Core utilities used by the coder agent to interact with the filesystem
# while maintaining security boundaries within the project root directory.

import pathlib
# Maps to: filesystem path operations for cross-platform compatibility
import subprocess
# Maps to: running shell commands for project setup and execution
from typing import Tuple
# Maps to: type hints for function return values (returncode, stdout, stderr)

from langchain_core.tools import tool
# Maps to: decorator for creating LangChain tools that can be used by AI agents

# PROJECT_ROOT will be set dynamically with a serial ID
PROJECT_ROOT = None


def get_next_serial_id() -> int:
    """Finds the next available serial ID by checking existing project directories."""
    base_path = pathlib.Path.cwd()
    existing_dirs = [d for d in base_path.glob("generated_project_*") if d.is_dir()]
    
    if not existing_dirs:
        return 1
    
    # Extract serial IDs from existing directories
    serial_ids = []
    for d in existing_dirs:
        try:
            # Extract number from "generated_project_X" format
            serial_id = int(d.name.split("_")[-1])
            serial_ids.append(serial_id)
        except (ValueError, IndexError):
            continue
    
    return max(serial_ids) + 1 if serial_ids else 1


# safe_path_for_project maps to: security function that prevents path traversal attacks
# It ensures all file operations stay within the designated PROJECT_ROOT directory
def safe_path_for_project(path: str) -> pathlib.Path:
    if PROJECT_ROOT is None:
        raise RuntimeError("PROJECT_ROOT not initialized. Call init_project_root() first.")
    
    p = (PROJECT_ROOT / path).resolve()
    if PROJECT_ROOT.resolve() not in p.parents and PROJECT_ROOT.resolve() != p.parent and PROJECT_ROOT.resolve() != p:
        raise ValueError("Attempt to write outside project root")
    return p


@tool
# write_file maps to: LangChain tool for creating/modifying files in the project
# Used by the coder agent to implement the actual file changes
def write_file(path: str, content: str) -> str:
    """Writes content to a file at the specified path within the project root."""
    p = safe_path_for_project(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)
    return f"WROTE:{p}"


@tool
# read_file maps to: LangChain tool for reading existing files in the project
# Used by the coder agent to understand current file contents before making changes
def read_file(path: str) -> str:
    """Reads content from a file at the specified path within the project root."""
    p = safe_path_for_project(path)
    if not p.exists():
        return ""
    with open(p, "r", encoding="utf-8") as f:
        return f.read()


@tool
# get_current_directory maps to: LangChain tool for getting project root path
# Used by the coder agent to understand the working directory context
def get_current_directory() -> str:
    """Returns the current working directory."""
    if PROJECT_ROOT is None:
        raise RuntimeError("PROJECT_ROOT not initialized. Call init_project_root() first.")
    return str(PROJECT_ROOT)


@tool
# list_files maps to: LangChain tool for listing files in project directory
# Used by the coder agent to see what files exist and plan file operations
def list_files(directory: str = ".") -> str:
    """Lists all files in the specified directory within the project root."""
    p = safe_path_for_project(directory)
    if not p.is_dir():
        return f"ERROR: {p} is not a directory"
    files = [str(f.relative_to(PROJECT_ROOT)) for f in p.glob("**/*") if f.is_file()]
    return "\n".join(files) if files else "No files found."

@tool
# run_cmd maps to: LangChain tool for executing shell commands
# Used by the coder agent to run build commands, install dependencies, etc.
def run_cmd(cmd: str, cwd: str = None, timeout: int = 30) -> Tuple[int, str, str]:
    """Runs a shell command in the specified directory and returns the result."""
    cwd_dir = safe_path_for_project(cwd) if cwd else PROJECT_ROOT
    res = subprocess.run(cmd, shell=True, cwd=str(cwd_dir), capture_output=True, text=True, timeout=timeout)
    return res.returncode, res.stdout, res.stderr


# init_project_root maps to: initialization function for setting up the project directory
# Called once to ensure the project root directory exists before any file operations
def init_project_root():
    """Initializes a new project root directory with a unique serial ID."""
    global PROJECT_ROOT
    
    serial_id = get_next_serial_id()
    PROJECT_ROOT = pathlib.Path.cwd() / f"generated_project_{serial_id}"
    PROJECT_ROOT.mkdir(parents=True, exist_ok=True)
    
    return str(PROJECT_ROOT)