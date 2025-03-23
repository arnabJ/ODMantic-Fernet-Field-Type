import os
from pathlib import Path
from typing import Optional, Union
from dotenv import load_dotenv

# Cache for loaded .env files to avoid multiple loads
_ENV_LOADED = False


def load_environment(env_file: Optional[Union[str, Path]] = None):
    """
    Load environment variables from a .env file.

    Args:
        env_file: Path to .env file. If None, tries to find .env in current
                  or parent directories.
    """
    global _ENV_LOADED

    if _ENV_LOADED and env_file is None:
        return

    if env_file:
        load_dotenv(env_file)
    else:
        # Try to find .env in current directory or parent directories
        current_dir = Path.cwd()
        max_levels = 3  # Limit how far up we look

        for _ in range(max_levels):
            if (current_dir / ".env").exists():
                load_dotenv(current_dir / ".env")
                break
            # Move to parent directory
            parent = current_dir.parent
            if parent == current_dir:  # Reached root
                break
            current_dir = parent

    _ENV_LOADED = True


def get_env_value(name: str, default: Optional[str] = None) -> Optional[str]:
    """
    Get an environment variable value, loading .env if not already loaded.

    Args:
        name: Name of the environment variable
        default: Default value if not found

    Returns:
        The environment variable value or default if not found
    """
    if not _ENV_LOADED:
        load_environment()

    return os.environ.get(name, default)
