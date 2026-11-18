import unittest
from core import Dice, UnknownCodeError
from heroes import HeroBuilder
from enemies import GoblinFactory, DragonFactory
from items import create_item_registry
from locations import ForestFactory
class TestPatterns(unittest.TestCase):
    def test_singleton(self):
        self.assertIs(Dice(), Dice())
    def test_dice_reseed(self):
        dice = Dice()
        dice.reseed(42)
        first = dice.roll(1, 100)
        dice.reseed(42)
        second = dice.roll(1, 100)
        self.assertEqual(first, second)
    def test_builder(self):
        hero = (
            HeroBuilder()
            .set_name("Тест")
            .set_health(150)
            .set_attack(25)
            .build()
        )
        self.assertEqual(hero.name, "Тест")
        self.assertEqual(hero.max_health, 150)
        self.assertEqual(hero.attack, 25)
    def test_factory_method(self):
        goblin = GoblinFactory().create_enemy()
        dragon = DragonFactory().create_enemy()
        self.assertEqual(goblin.name, "Гоблин")
        self.assertEqual(dragon.name, "Древний дракон")
        self.assertIsNot(goblin, GoblinFactory().create_enemy())
    def test_abstract_factory(self):
        registry = create_item_registry()
        factory = ForestFactory()
        enemy = factory.create_enemy()
        reward = factory.create_reward(registry)
        self.assertEqual(enemy.name, "Гоблин")
        self.assertEqual(reward.name, "Лесной амулет")
    def test_prototype(self):
        registry = create_item_registry()
        first = registry.create("sword")
        second = registry.create("sword")
        second.enchant("Магическое", 5)
        self.assertIsNot(first, second)
        self.assertEqual(first.power, 10)
        self.assertEqual(second.power, 15)
    def test_unknown_item(self):
        registry = create_item_registry()
        with self.assertRaises(UnknownCodeError):
            registry.create("unknown")
if __name__ == "__main__":
    unittest.main()
