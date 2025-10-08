"""
Markdown table generation utilities.

This module provides classes for generating properly formatted Markdown tables
from structured data. It's primarily used for creating data dictionary documentation
with consistent formatting and proper alignment.
"""

from typing import Any, Dict, List


class Table:
    """
    Generates Markdown tables from structured data.

    This class takes a list of dictionaries and converts them into a properly
    formatted Markdown table with headers and aligned columns. It's designed
    for creating documentation tables in data dictionaries.

    Attributes:
        data: List of dictionaries representing table rows
        headers: List of column header names

    Example:
        >>> data = [
        ...     {'name': 'John', 'age': 30},
        ...     {'name': 'Jane', 'age': 25}
        ... ]
        >>> table = Table(data)
        >>> print(table)
    """

    def __init__(self, data: List[Dict[str, Any]] = None):
        """
        Initialize the table with data.

        Args:
            data: List of dictionaries where each dict represents a table row.
                 Keys become column headers, values become cell content.
        """
        self.data = data or []
        if len(self.data) == 0 or not self.data:
            return
        self.headers = list(data[0].keys())

    @property
    def headers(self) -> str:
        """
        Generate the Markdown table header section.

        Creates the header row and separator row for the Markdown table,
        properly formatted with pipe separators and alignment indicators.

        Returns:
            String containing the formatted header and separator rows
        """
        return "\n".join(
            [
                f"| {' | '.join(self._headers)} |",
                f"| {' | '.join(['---' for _ in self._headers])} | ",
            ]
        )

    @headers.setter
    def headers(self, headers: List[str]) -> None:
        """
        Set the table headers.

        Args:
            headers: List of column header names
        """
        self._headers = headers

    @property
    def body(self) -> str:
        """
        Generate the Markdown table body content.

        Creates the data rows for the Markdown table, converting all values
        to strings and properly formatting them with pipe separators.

        Returns:
            String containing all data rows formatted for Markdown
        """
        return "\n".join(
            f"| {' | '.join([str(x) for x in i.values()])} |" for i in self.data
        )

    def __str__(self) -> str:
        """
        Generate the complete Markdown table.

        Combines headers and body to create a complete Markdown table
        with proper formatting and alignment.

        Returns:
            Complete Markdown table as a string
        """
        return "\n".join([self.headers, self.body])
