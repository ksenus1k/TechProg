from abc import ABC, abstractmethod
from core import Dice
class Enemy:
    def __init__(self, name, health, attack, defense=0):
        self.name = name
        self.health = health
        self.max_health = health
        self.attack = attack
        self.defense = defense
    def is_alive(self):
        return self.health > 0
    def show_info(self):
        print(f"Противник: {self.name}")
        print(f"Здоровье: {self.health}")
        print(f"Атака: {self.attack}")
    def roll_damage(self):
        damage = self.attack + Dice().roll(1, 6)
        critical = Dice().chance(0.1)
        if critical:
            damage *= 2
        return damage, critical
    def receive_hit(self, damage):
        actual = min(
            self.health,
            max(1, damage - self.defense)
        )
        self.health -= actual
        return actual
class Goblin(Enemy):
    def __init__(self):
        super().__init__("Гоблин", 50, 10)
class Skeleton(Enemy):
    def __init__(self):
        super().__init__("Скелет", 70, 15, 2)
class Orc(Enemy):
    def __init__(self):
        super().__init__("Орк", 100, 20, 5)
class Dragon(Enemy):
    def __init__(self):
        super().__init__("Древний дракон", 200, 30, 8)
# Factory Method
class EnemyFactory(ABC):
    @abstractmethod
    def create_enemy(self):
        pass
class GoblinFactory(EnemyFactory):
    def create_enemy(self):
        return Goblin()
class SkeletonFactory(EnemyFactory):
    def create_enemy(self):
        return Skeleton()
class OrcFactory(EnemyFactory):
    def create_enemy(self):
        return Orc()
class DragonFactory(EnemyFactory):
    def create_enemy(self):
        return Dragon()
