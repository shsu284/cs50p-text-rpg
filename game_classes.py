class Character:
    """Base class representing a combatant in the game."""

    def __init__(self, name, hp, attack_power):
        """Initialize character name, current/max health, and attack power."""
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack_power = attack_power

    def is_alive(self):
        """Return True if the character still has health points remaining."""
        return self.hp > 0

    def attack(self, target):
        """Deal damage to target equal to attack_power, floored at 0 HP."""
        target.hp -= self.attack_power
        target.hp = max(target.hp, 0)


class Player(Character):
    """Represent the player hero with health, attack power, and an inventory."""

    def __init__(self, name):
        """Initialize the player with default stats and an empty inventory."""
        super().__init__(name, hp=100, attack_power=15)
        self.inventory = []

    def add_item(self, item):
        """Append an item to the player's inventory and print confirmation."""
        self.inventory.append(item)
        print(f"Congratulations! A {item.name} has been added to your inventory!")

    def heal(self, amount):
        """Restore player health up to max_hp."""
        self.hp += amount
        self.hp = min(self.hp, self.max_hp)

    def remove_item(self, item):
        """Remove an item from the player's inventory if present."""
        if item in self.inventory:
            self.inventory.remove(item)

    def show_inventory(self):
        """Return the inventory list, or a message if it is empty."""
        if not self.inventory:
            return "Your inventory is empty."
        return self.inventory


class Item:
    """Represent a game item such as a healing potion."""

    def __init__(self, name, item_type, value):
        """Initialize item name, type, and numeric effect value."""
        self.name = name
        self.item_type = item_type
        self.value = value

    def __str__(self):
        """Return the item's display name."""
        return self.name