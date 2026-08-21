from __future__ import annotations
import json
from abc import ABC, abstractmethod
from typing import Any


class InventorySource(ABC):
    """Abstract source of a guild inventory tree."""

    @abstractmethod
    def root(self) -> Any:
        """Return the root of the world tree."""


    @abstractmethod
    def version(self) -> int | str:
        """Return the source version; a missing JSON version defaults to 1."""
        raise NotImplementedError


class JSONInventorySource(InventorySource):
    """Load an inventory from a JSON file.

    You may assume that grading files follow the documented inventory schema.
    Full schema validation is not required.
    """

    def __init__(self, path: str):
        # TODO: Load the JSON object and cache its version (default 1).
        with open(path, "r") as file:
            self._root = json.load(file)
        self._version = self._root.get("version", 1)

    def root(self) -> Any:
        # TODO: Return the loaded root object.
        return self._root

    def version(self) -> int | str:
        # TODO: Return the cached version.
        return self._version
