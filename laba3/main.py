from core import Dice
from combat import Outcome
from heroes import (
    HeroBuilder,
    WarriorPreset,
    MagePreset,
    ArcherPreset
)
from enemies import (
    GoblinFactory,
    SkeletonFactory,
    OrcFactory,
    DragonFactory
)
from items import create_item_registry
from locations import (
    ForestFactory,
    DungeonFactory,
    CastleFactory,
    DragonLairFactory,
    Expedition
)
# Демонстрация всех паттернов
def demonstrate_patterns():
    print("ДЕМОНСТРАЦИЯ ПАТТЕРНОВ")
    # Singleton
    print("\n1. Singleton")
    dice1 = Dice()
    dice2 = Dice()
    print("Один экземпляр:", dice1 is dice2)
    dice1.reseed(42)
    first = dice1.roll(1, 20)
    dice2.reseed(42)
    second = dice2.roll(1, 20)
    print("Повторяемый бросок:", first == second)
    # Builder
    print("\n2. Builder")
    hero = (
        HeroBuilder()
        .set_name("Артур")
        .set_class("Воин")
        .set_health(150)
        .set_attack(25)
        .set_defense(15)
        .build()
    )
    hero.show_info()
    # Factory Method
    print("\n3. Factory Method")
    factories = [
        GoblinFactory(),
        SkeletonFactory(),
        OrcFactory(),
        DragonFactory()
    ]
    for factory in factories:
        enemy = factory.create_enemy()
        print("Создан противник:", enemy.name)
    # Abstract Factory
    print("\n4. Abstract Factory")
    registry = create_item_registry()
    locations = [
        ("Лес", ForestFactory()),
        ("Подземелье", DungeonFactory()),
        ("Замок", CastleFactory())
    ]
    for name, factory in locations:
        enemy = factory.create_enemy()
        reward = factory.create_reward(registry)
        print(
            f"{name}: противник {enemy.name}, "
            f"награда {reward.name}"
        )
    # Prototype
    print("\n5. Prototype")
    sword1 = registry.create("sword")
    sword2 = registry.create("sword")
    sword2.enchant("Острое", 5)
    print("Первый предмет:", sword1.name, sword1.power)
    print("Копия:", sword2.name, sword2.power)
    print("Разные объекты:", sword1 is not sword2)
    print("\nВсе пять паттернов продемонстрированы!")
# Выбор героя
def create_hero():
    print("\nСОЗДАНИЕ ГЕРОЯ")
    name = input("Введите имя героя: ").strip()
    if not name:
        name = "Артур"
    print("\nВыберите класс:")
    print("1. Воин")
    print("2. Маг")
    print("3. Лучник")
    choice = input("Ваш выбор: ").strip()
    presets = {
        "1": WarriorPreset(),
        "2": MagePreset(),
        "3": ArcherPreset()
    }
    preset = presets.get(choice, WarriorPreset())
    hero = preset.create(name)
    print("\nГерой создан!")
    hero.show_info()
    return hero
# Главная игра
def start_game():
    print("RPG ПРИКЛЮЧЕНИЕ")
    hero = create_hero()
    registry = create_item_registry()
    # Начальное снаряжение
    hero.add_item(registry.create("sword"))
    expeditions = {
        "1": Expedition("Мистический лес", ForestFactory()),
        "2": Expedition("Подземелье", DungeonFactory()),
        "3": Expedition("Заброшенный замок", CastleFactory()),
        "4": Expedition("Логово дракона", DragonLairFactory())
    }
    dragon_defeated = False
    while hero.health > 0:
        print("\nГЛАВНОЕ МЕНЮ")
        print("1. Экспедиция в лес")
        print("2. Экспедиция в подземелье")
        print("3. Экспедиция в замок")
        print("4. Сражение с драконом")
        print("5. Характеристики героя")
        print("6. Инвентарь")
        print("7. Экипировать предмет")
        print("8. Восстановить здоровье (20 золота)")
        print("9. Зачаровать предмет (15 золота)")
        print("0. Выход")
        choice = input("\nВыберите действие: ").strip()
        if choice in expeditions:
            if choice == "4" and dragon_defeated:
                print("Дракон уже побеждён!")
                continue
            report = expeditions[choice].start(
                hero, registry
            )
            if choice == "4" and report.outcome == Outcome.VICTORY:
                dragon_defeated = True
                print("\nПОЗДРАВЛЯЕМ!")
                print("Вы победили древнего дракона!")
                print("Главная цель игры выполнена!")
        elif choice == "5":
            hero.show_info()
        elif choice == "6":
            hero.show_inventory()
        elif choice == "7":
            hero.show_inventory()
            try:
                number = int(
                    input("Номер предмета: ")
                )
                hero.equip(number - 1)
            except ValueError:
                print("Введите число.")
        elif choice == "8":
            if hero.health == hero.max_health:
                print("Здоровье уже полное!")
            elif hero.gold >= 20:
                hero.gold -= 20
                hero.heal()
            else:
                print("Недостаточно золота.")
        elif choice == "9":
            if hero.gold < 15:
                print("Недостаточно золота.")
                continue
            hero.show_inventory()
            try:
                number = int(
                    input("Номер предмета: ")
                )
                if 1 <= number <= len(hero.inventory):
                    item = hero.inventory[number - 1]
                    item.enchant("Магическое", 5)
                    hero.gold -= 15
                    print("Предмет зачарован!")
                else:
                    print("Неверный номер.")
            except ValueError:
                print("Введите число.")
        elif choice == "0":
            print("\nСпасибо за игру!")
            break
        else:
            print("Неверная команда.")
    if hero.health <= 0:
        print("\nИГРА ОКОНЧЕНА!")
        print("Герой потерял всё здоровье.")
# Точка входа
if __name__ == "__main__":
    demonstrate_patterns()
    start_game()

