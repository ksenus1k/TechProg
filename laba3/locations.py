from abc import ABC, abstractmethod
from enemies import (
    GoblinFactory,
    SkeletonFactory,
    OrcFactory,
    DragonFactory
)
# Abstract Factory
class LocationFactory(ABC):
    @abstractmethod
    def create_enemy(self):
        pass
    @abstractmethod
    def create_reward(self, registry):
        pass
class ForestFactory(LocationFactory):
    def create_enemy(self):
        return GoblinFactory().create_enemy()
    def create_reward(self, registry):
        return registry.create("amulet")
class DungeonFactory(LocationFactory):
    def create_enemy(self):
        return SkeletonFactory().create_enemy()
    def create_reward(self, registry):
        return registry.create("magic_sword")
class CastleFactory(LocationFactory):
    def create_enemy(self):
        return OrcFactory().create_enemy()
    def create_reward(self, registry):
        return registry.create("armor")
class DragonLairFactory(LocationFactory):
    def create_enemy(self):
        return DragonFactory().create_enemy()
    def create_reward(self, registry):
        return registry.create("dragon_sword")
class Expedition:
    def __init__(self, name, factory):
        self.name = name
        self.factory = factory
    def start(self, hero, registry):
        from combat import Battle, Outcome
        print(f"\nЭкспедиция: {self.name}")
        enemy = self.factory.create_enemy()
        enemy.show_info()
        report = Battle(hero, enemy).run()
        if report.outcome == Outcome.VICTORY:
            from core import Dice
            gold = Dice().roll(10, 30)
            experience = 15
            if isinstance(self.factory, DragonLairFactory):
                gold = 100
                experience = 50
            hero.gold += gold
            hero.add_experience(experience)
            reward = self.factory.create_reward(registry)
            hero.add_item(reward)
            print("\nНАГРАДЫ")
            print("Золото:", gold)
            print("Опыт:", experience)
            print("Предмет:", reward.name)
        return report
