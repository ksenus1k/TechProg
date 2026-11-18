from abc import ABC, abstractmethod
class Hero:
    def __init__(
        self, name, hero_class, health, attack, defense
    ):
        self.name = name
        self.hero_class = hero_class
        self.health = health
        self.max_health = health
        self.base_attack = attack
        self.base_defense = defense
        self.level = 1
        self.experience = 0
        self.gold = 0
        self.inventory = []
        self.equipment = {
            "Оружие": None,
            "Броня": None,
            "Амулет": None
        }
    @property
    def attack(self):
        bonus = sum(
            item.power
            for kind, item in self.equipment.items()
            if item is not None
            and kind in ("Оружие", "Амулет")
        )
        return self.base_attack + bonus
    @property
    def defense(self):
        armor = self.equipment["Броня"]
        return self.base_defense + (
            armor.power if armor else 0
        )
    def show_info(self):
        print("\nГЕРОЙ")
        print("Имя:", self.name)
        print("Класс:", self.hero_class)
        print("Уровень:", self.level)
        print("Здоровье:", self.health, "/", self.max_health)
        print("Атака:", self.attack)
        print("Защита:", self.defense)
        print("Опыт:", self.experience)
        print("Золото:", self.gold)
    def add_experience(self, amount):
        self.experience += amount
        while self.experience >= self.level * 30:
            self.experience -= self.level * 30
            self.level += 1
            self.max_health += 20
            self.health = self.max_health
            self.base_attack += 4
            self.base_defense += 2
            print("\nНОВЫЙ УРОВЕНЬ!")
            print("Текущий уровень:", self.level)
    def heal(self):
        self.health = self.max_health
        print("Здоровье восстановлено!")
    def add_item(self, item):
        self.inventory.append(item)
    def equip(self, index):
        if index < 0 or index >= len(self.inventory):
            print("Такого предмета нет.")
            return
        item = self.inventory[index]
        kind = item.item_type
        if kind not in self.equipment:
            print("Этот предмет нельзя экипировать.")
            return
        old_item = self.equipment[kind]
        self.equipment[kind] = item
        self.inventory.pop(index)
        if old_item is not None:
            self.inventory.append(old_item)
        print("Экипирован предмет:", item.name)
    def show_inventory(self):
        print("\nИНВЕНТАРЬ")
        if not self.inventory:
            print("Инвентарь пуст.")
        for index, item in enumerate(self.inventory, 1):
            print(f"{index}. {item.name} — сила {item.power}")
        print("\nЭкипировка:")
        for kind, item in self.equipment.items():
            name = item.name if item else "Нет"
            print(f"{kind}: {name}")
# Builder
class HeroBuilder:
    def __init__(self):
        self.name = "Герой"
        self.hero_class = "Воин"
        self.health = 100
        self.attack = 10
        self.defense = 5
    def set_name(self, name):
        self.name = name
        return self
    def set_class(self, hero_class):
        self.hero_class = hero_class
        return self
    def set_health(self, health):
        self.health = health
        return self
    def set_attack(self, attack):
        self.attack = attack
        return self
    def set_defense(self, defense):
        self.defense = defense
        return self
    def build(self):
        return Hero(
            self.name,
            self.hero_class,
            self.health,
            self.attack,
            self.defense
        )
# Разные варианты создания героя
class HeroPreset(ABC):
    @abstractmethod
    def create(self, name):
        pass
class WarriorPreset(HeroPreset):
    def create(self, name):
        return (
            HeroBuilder()
            .set_name(name)
            .set_class("Воин")
            .set_health(150)
            .set_attack(25)
            .set_defense(15)
            .build()
        )
class MagePreset(HeroPreset):
    def create(self, name):
        return (
            HeroBuilder()
            .set_name(name)
            .set_class("Маг")
            .set_health(100)
            .set_attack(35)
            .set_defense(7)
            .build()
        )
class ArcherPreset(HeroPreset):
    def create(self, name):
        return (
            HeroBuilder()
            .set_name(name)
            .set_class("Лучник")
            .set_health(120)
            .set_attack(30)
            .set_defense(10)
            .build()
        )
