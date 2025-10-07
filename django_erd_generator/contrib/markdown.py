from typing import Any, Dict, List


class Table:
    def __init__(self, data: List[Dict[str, Any]] = []):
        self.data = data
        if len(self.data) == 0 or not self.data:
            return
        self.headers = list(data[0].keys())

    @property
    def headers(self) -> str:
        return "\n".join(
            [
                f"| {' | '.join(self._headers)} |",
                f"| {' | '.join(['---' for _ in self._headers])} | ",
            ]
        )

    @headers.setter
    def headers(self, headers: List[str]) -> None:
        self._headers = headers

    @property
    def body(self) -> str:
        return "\n".join(
            f"| {' | '.join([str(x) for x in i.values()])} |" for i in self.data
        )

    def __str__(self) -> str:
        return "\n".join([self.headers, self.body])
