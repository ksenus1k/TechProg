from dataclasses import dataclass
from enum import Enum
from core import Dice
class Side(Enum):
    HERO = "Герой"
    ENEMY = "Противник"
class EventType(Enum):
    HIT = "Удар"
    CRITICAL_HIT = "Критический удар"
    DEATH = "Победа над участником"
class Outcome(Enum):
    VICTORY = "Победа"
    DEFEAT = "Поражение"
@dataclass(frozen=True)
class Hit:
    damage: int
    critical: bool
@dataclass(frozen=True)
class BattleEvent:
    round: int
    event_type: EventType
    source: Side
    target: Side
    damage: int
    health_after: int
@dataclass(frozen=True)
class BattleReport:
    hero_name: str
    enemy_name: str
    outcome: Outcome
    events: tuple
class Battle:
    def __init__(self, hero, enemy):
        self.hero = hero
        self.enemy = enemy
        self.events = []
        self.round_number = 0
    def hero_hit(self):
        dice = Dice()
        damage = self.hero.attack + dice.roll(1, 6)
        critical = dice.chance(0.2)
        if critical:
            damage *= 2
        return Hit(damage, critical)
    def enemy_hit(self):
        damage, critical = self.enemy.roll_damage()
        return Hit(damage, critical)
    def strike(self, attacker, defender, source, target, hit):
        if target == Side.HERO:
            damage = max(1, hit.damage - defender.defense)
        else:
            damage = max(1, hit.damage - defender.defense)
        actual = min(defender.health, damage)
        defender.health -= actual
        event_type = (
            EventType.CRITICAL_HIT
            if hit.critical
            else EventType.HIT
        )
        event = BattleEvent(
            self.round_number,
            event_type,
            source,
            target,
            actual,
            defender.health
        )
        self.events.append(event)
        print(
            f"{source.value} наносит {actual} урона. "
            f"Здоровье цели: {defender.health}"
        )
        if defender.health <= 0:
            self.events.append(
                BattleEvent(
                    self.round_number,
                    EventType.DEATH,
                    source,
                    target,
                    0,
                    0
                )
            )
    def run(self):
        print("\nНАЧАЛО БОЯ")
        print(self.hero.name, "против", self.enemy.name)
        while self.hero.health > 0 and self.enemy.health > 0:
            self.round_number += 1
            print(f"\nРаунд {self.round_number}")
            self.strike(
                self.hero,
                self.enemy,
                Side.HERO,
                Side.ENEMY,
                self.hero_hit()
            )
            if self.enemy.health <= 0:
                break
            self.strike(
                self.enemy,
                self.hero,
                Side.ENEMY,
                Side.HERO,
                self.enemy_hit()
            )
        outcome = (
            Outcome.VICTORY
            if self.hero.health > 0
            else Outcome.DEFEAT
        )
        report = BattleReport(
            self.hero.name,
            self.enemy.name,
            outcome,
            tuple(self.events)
        )
        print("\nРезультат боя:", report.outcome.value)
        print("Всего событий:", len(report.events))
        return report
