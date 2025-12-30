from abc import ABC, abstractmethod
from typing import List, Dict


class BaseParser(ABC):

    @abstractmethod
    def parse(self, text: str) -> List[Dict]:
        """
        Returns a list of sections/articles with:
        - section_id
        - section_title
        - text
        """
        pass
