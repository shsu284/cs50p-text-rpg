class Character:  # Used to initialize the characters
    def __init__(self, name, hp, attack_power):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack_power = attack_power

    def is_alive(self):  # Used to check if character is still alive
        """Checks if the character is still alive"""
        return self.hp > 0

    def attack(self, target):  # Used when a character attack a nother one
        """Deducts health points from the target equal to the attack power"""
        target.hp -= self.attack_power
        target.hp = max(target.hp, 0)


class Player(Character):
    def __init__(self, name):
        super().__init__(name, hp=100, attack_power=15)  # Gives the player stats
        self.inventory = []  # and a inventory

    def add_item(self, item):
        """Adds an item to the inventory."""
        self.inventory.append(item)  # adds item to the inventory
        print(f"Congratualations a {item.name} has been added to your inventory!")

    def heal(self, amount):
        """Heals the player, but up to a maximum of the starting HP."""
        self.hp += amount
        self.hp = min(self.hp, self.max_hp)

    def remove_item(self, item):
        """Entfernt ein Item aus dem Inventar, falls es vorhanden ist."""
        if item in self.inventory:
            self.inventory.remove(item)

    def show_inventory(self):
        """Returns the inventory or indicates that it is empty."""

        if not self.inventory:
            return "Your inventory is empty."
        return self.inventory


class Item:
    def __init__(self, name, item_type, value):
        self.name = name
        self.item_type = item_type
        self.value = value

    def __str__(self):
        return self.name
