class Month:
    def __init__(self, month: int):
        if not (1 <= month <= 12):
            raise ValueError('Month must be between 1 and 12')
        self.value = month

    def __str__(self):
        return f'{self.value:02d}'

    def __eq__(self, other):
        if not isinstance(other, Month):
            raise TypeError('Comparison must be with another Month instance')
        return self.value == other.value

    def next(self):
        'Get the next month, wrapping around to January if necessary.'
        return Month(1) if self.value == 12 else Month(self.value + 1)

    def previous(self):
        'Get the previous month, wrapping around to December if necessary.'
        return Month(12) if self.value == 1 else Month(self.value - 1)
