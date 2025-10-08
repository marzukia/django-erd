"""
Git utilities for ERD generation.

This module provides functions for extracting git repository information
that can be included in generated documentation for version tracking
and correlation with codebase changes.
"""

import subprocess


def get_git_commit() -> str:
    """
    Get the current git commit hash.

    Executes 'git rev-parse HEAD' to retrieve the full SHA hash of the
    current commit. This is useful for including version information
    in generated documentation to correlate docs with specific code states.

    Returns:
        String containing the full commit hash

    Raises:
        subprocess.CalledProcessError: If git command fails (e.g., not in a git repo)

    Example:
        >>> commit = get_git_commit()
        >>> print(f"Generated from commit: {commit}")
    """
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()
