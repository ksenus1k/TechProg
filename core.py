import random

# Singleton — единственный генератор случайных чисел
class Dice:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._random = random.Random()
        return cls._instance
    def reseed(self, seed):
        self._random.seed(seed)
    def roll(self, minimum, maximum):
        return self._random.randint(minimum, maximum)
    def chance(self, probability):
        return self._random.random() < probability
    def pick(self, options):
        return self._random.choice(options)
    def next_seed(self):
        return self._random.randrange(1_000_000)

class UnknownCodeError(LookupError):
    def __init__(self, category, code):
        super().__init__(
            f"{category} с кодом '{code}' не существует"
        )
