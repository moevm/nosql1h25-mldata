"""
Структура для хранения фильтров отображения датасетов на главной странице.
"""
from typing import Optional


class FilterValues:
    """
    Структура для хранения фильтров отображения датасетов на главной странице.
    """

    def __init__(self, name: str,
                 size_from: Optional[int], size_to: Optional[int],
                 row_size_from: Optional[int], row_size_to: Optional[int],
                 column_size_from: Optional[int], column_size_to: Optional[int]):
        self.name: str = name.strip()

        self.size_from: Optional[int] = size_from
        self.size_to: Optional[int] = size_to

        self.row_size_from: Optional[int] = row_size_from
        self.row_size_to: Optional[int] = row_size_to

        self.column_size_from: Optional[int] = column_size_from
        self.column_size_to: Optional[int] = column_size_to
