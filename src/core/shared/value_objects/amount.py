
class Amount:
    'Represents a decimal value with a fixed precision.'

    def __init__(self, value: float, precision: int = 2):
        self.value = round(value, precision)
        self.precision = precision

    def __str__(self) -> str:
        return f'{self.value:.{self.precision}f}'

    def __add__(self, other: 'Amount') -> 'Amount':
        if not isinstance(other, Amount):
            raise TypeError('Can only add Decimal to Decimal')
        return Amount(self.value + other.value, max(self.precision, other.precision))
