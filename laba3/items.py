import copy
from core import UnknownCodeError
# Игровой предмет
class Item:
    def __init__(self, name, power, rarity, item_type):
        self.name = name
        self.power = power
        self.rarity = rarity
        self.item_type = item_type
        self.enchantments = []
    # Prototype
    def clone(self):
        return copy.deepcopy(self)
    def enchant(self, name, bonus):
        self.enchantments.append((name, bonus))
        self.power += bonus
        return self
    def show_info(self):
        print(f"Предмет: {self.name}")
        print(f"Тип: {self.item_type}")
        print(f"Сила: {self.power}")
        print(f"Редкость: {self.rarity}")
        if self.enchantments:
            for name, bonus in self.enchantments:
                print(f"Зачарование: {name} (+{bonus})")

# Каталог прототипов
class ItemRegistry:
    def __init__(self):
        self.items = {}
    def register(self, code, item):
        self.items[code] = item.clone()
    def create(self, code):
        if code not in self.items:
            raise UnknownCodeError("Предмет", code)
        return self.items[code].clone()

def create_item_registry():
    registry = ItemRegistry()
    registry.register(
        "sword",
        Item("Железный меч", 10, "Обычный", "Оружие")
    )
    registry.register(
        "magic_sword",
        Item("Магический меч", 20, "Редкий", "Оружие")
    )
    registry.register(
        "armor",
        Item("Рыцарская броня", 8, "Редкий", "Броня")
    )
    registry.register(
        "amulet",
        Item("Лесной амулет", 5, "Обычный", "Амулет")
    )
    registry.register(
        "dragon_sword",
        Item("Клинок дракона", 35, "Легендарный", "Оружие")
    )
    return registry
