"""
Структура для хранения фильтров отображения датасетов на главной странице.
"""
from typing import Optional
from datetime import datetime


class FilterValues:
    """
    Структура для хранения фильтров отображения датасетов на главной странице.
    """

    def __init__(self, name: str,
                 size_from: Optional[float], size_to: Optional[float],
                 row_size_from: Optional[int], row_size_to: Optional[int],
                 column_size_from: Optional[int], column_size_to: Optional[int],
                 creation_date_from: Optional[datetime], creation_date_to: Optional[datetime],
                 modify_date_from: Optional[datetime], modify_date_to: Optional[datetime]):

        self.name: str = name.strip()

        self.size_from: Optional[float] = size_from
        self.size_to: Optional[float] = size_to

        self.row_size_from: Optional[int] = row_size_from
        self.row_size_to: Optional[int] = row_size_to

        self.column_size_from: Optional[int] = column_size_from
        self.column_size_to: Optional[int] = column_size_to

        self.creation_date_from: Optional[datetime] = creation_date_from
        self.creation_date_to: Optional[datetime] = creation_date_to

        self.modify_date_from: Optional[datetime] = modify_date_from
        self.modify_date_to: Optional[datetime] = modify_date_to
