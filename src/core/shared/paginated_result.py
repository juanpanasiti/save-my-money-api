from typing import Generic, List, TypeVar

T = TypeVar('T')


class PaginatedResult(Generic[T]):
    def __init__(self, items: List[T], total_items: int, total_pages, page: int, page_size: int):
        self.items = items
        self.total_items = total_items  # Total number of items
        self.total_pages = total_pages  # Total number of pages
        self.page = page  # Current page number
        self.page_size = page_size  # Number of items per page

    @property
    def has_next(self) -> bool:
        'Check if there is a next page.'
        return self.page < self.total_pages
    
    @property
    def has_previous(self) -> bool:
        'Check if there is a previous page.'
        return self.page > 1
