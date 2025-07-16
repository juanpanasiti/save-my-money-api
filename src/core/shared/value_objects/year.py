
class Year:
    def __init__(self, year: int):
        if not isinstance(year, int):
            raise TypeError('Year must be an integer')
        if year < 0:
            raise ValueError('Year cannot be negative')
        self.value = year

    def __eq__(self, other):
        if not isinstance(other, Year):
            raise TypeError('Comparison must be with another Year instance')
        return self.value == other.value

    def __repr__(self):
        return f'Year({self.value})'

    def is_leap_year(self) -> bool:
        'Check if the year is a leap year.'
        return (self.value % 4 == 0 and self.value % 100 != 0) or (self.value % 400 == 0)
