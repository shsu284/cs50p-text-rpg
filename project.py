import json
from game_classes import Player, Character, Item
from pathlib import Path


def main():
    print("==================================================")
    print("       WELCOME TO THE CS50P TEXT-RPG!             ")
    print("==================================================")

    loaded_save = False

    start_index = 0

    health_potion = Item("Health Potion", "heal", 25)

    goblins = [
        Character("Goblin Soldier", hp=30, attack_power=8),
        Character("Goblin Knight", hp=35, attack_power=10),
        Character("Goblin Boss", hp=50, attack_power=12),
    ]

    all_defeated = True

    if check_save_file():
        with open("savegame.json", "r") as f:
            data = json.load(f)

        if validate_save_data(data):
            hero = Player(data["name"])
            hero.hp = data["hp"]
            hero.attack_power = data["attack_power"]
            start_index = data["next_enemy_index"]
            for item_name in data["inventory"]:
                if item_name == health_potion.name:
                    hero.add_item(
                        Item(
                            health_potion.name,
                            health_potion.item_type,
                            health_potion.value,
                        )
                    )
            loaded_save = True
            print(f"\nWelcome back, {hero.name}!")

        else:
            print("\nSave file data is invalid. Starting a new game ...")

    if not loaded_save:
        # 1. Introduction and Player creation
        name = get_player_name()
        hero = Player(name)
        print(f"\nWelcome to the world, {hero.name}!")

        # 2. Weapon selection
        choose_weapon(hero)

    # 4. Main game loop for battles
    for index, goblin in enumerate(goblins[start_index:], start=start_index):
        if not hero.is_alive():
            all_defeated = False
            break

        handle_combat(hero, goblin)
        handle_potion(hero, health_potion)

        if hero.is_alive():
            save_game(hero, index + 1)
            answer = input(
                "\nPress Enter to proceed to the next battle (or 'q' to quit): "
            )

            if answer.lower() == "q":
                all_defeated = False
                break

    # End of game message
    print("\n" + "=" * 50)
    if hero.is_alive() and all_defeated:
        print("Congratulations! You defeated all the goblins and won the game!")
    elif hero.is_alive() and not all_defeated:
        print("See you soon hero!!!")
    else:
        print("You were defeated in battle... Game Over!")
    print("=" * 50)


def get_player_name():
    """Asks for the player's name and validates it."""
    while True:
        name = input("What is the name of your Hero? Enter here: ").strip()
        if name:
            return name
        print("Name not accepted. Try again.")


def choose_weapon(player):
    """Lets the player choose a starting weapon."""
    print("\n--------------------------------------------------")
    print("Choose your starting class / weapon:")
    print("[1] Axe (High damage, slower)")
    print("[2] Dagger (Medium damage, agile)")
    print("[3] Bow (Ranged combat)")
    print("--------------------------------------------------")

    while True:
        choice = input("Your choice (1-3): ").strip()
        if choice == "1":
            player.attack_power = 20
            print("You chose the Axe! (Attack: 20)")
            break
        elif choice == "2":
            player.attack_power = 15
            print("You chose the Dagger! (Attack: 15)")
            break
        elif choice == "3":
            player.attack_power = 18
            print("You chose the Bow! (Attack: 18)")
            break
        else:
            print("Please choose 1, 2, or 3.")


def handle_combat(player, enemy):
    """Handles the turn-based combat between player and enemy."""
    print("\n--------------------------------------------------")
    print(f"A wild {enemy.name} appears!")
    print("Ready... Steady... Fight!")
    print("--------------------------------------------------")

    while enemy.hp > 0 and player.is_alive():
        player.attack(enemy)

        if enemy.is_alive():
            enemy.attack(player)

        # Clean and readable health status output
        print(
            f"-> Your health: {player.hp}/{player.max_hp}  |  {enemy.name}'s health: {enemy.hp}/{enemy.max_hp}"
        )

    print("--------------------------------------------------")


def handle_potion(player, potion):
    if not player.is_alive():
        return

    has_potion = any(item.name == potion.name for item in player.inventory)

    if not has_potion:
        print("Nice job. You have defeated the enemy!!!")
        new_potion = Item(potion.name, potion.item_type, potion.value)
        player.add_item(new_potion)
        print("--------------------------------------------------")

    potion_in_inventory = next(
        (item for item in player.inventory if item.name == potion.name),
        None,
    )

    if potion_in_inventory is not None:
        while True:
            decision = input(
                "Do you want to use the health potion? Type 'Yes', else 'No': "
            ).lower()
            if decision == "yes":
                player.heal(potion.value)
                player.inventory.remove(potion_in_inventory)
                print(f"You used the potion! Current HP: {player.hp}")
                print("--------------------------------------------------")
                break
            elif decision == "no":
                print("Potion kept in inventory.")
                print("--------------------------------------------------")
                break
            else:
                print("Wrong input. Please type 'Yes' or 'No'.")
                print("--------------------------------------------------")


def handle_inventory(player):

    inventory = player.show_inventory()

    if not inventory:
        print("Your inventory is empty.")
    else:
        print(f"Current Inventory: {inventory}")


def save_game(player, next_enemy_index):
    """Saves the game state to a JSON file (File I/O requirement)."""
    data = {
        "name": player.name,
        "hp": player.hp,
        "attack_power": player.attack_power,
        "inventory": [item.name for item in player.inventory],
        "next_enemy_index": next_enemy_index,
    }
    with open("savegame.json", "w") as f:
        json.dump(data, f, indent=4)
    print("\n[Game state saved to 'savegame.json']")


def check_save_file() -> bool:
    """Return True if savegame.json exists and contains valid JSON, else False."""
    save_path = Path("savegame.json")

    if not save_path.exists():
        return False

    try:
        with save_path.open("r", encoding="utf-8") as f:
            json.load(f)
        return True
    except (json.JSONDecodeError, OSError):
        return False


def validate_save_data(data):

    required_keys = ["name", "hp", "attack_power", "inventory", "next_enemy_index"]

    if type(data) is not dict:
        return False

    for key in required_keys:
        if key not in data:
            return False

    if type(data["name"]) is not str or data["name"].strip() == "":
        return False

    if type(data["hp"]) is not int or data["hp"] < 1:
        return False

    if type(data["attack_power"]) is not int or data["attack_power"] <= 0:
        return False

    if type(data["inventory"]) is not list:
        return False

    for item in data["inventory"]:
        if type(item) is not str:
            return False

    if (
        type(data["next_enemy_index"]) is not int
        or not 0 <= data["next_enemy_index"] <= 3
    ):
        return False

    return True


if __name__ == "__main__":
    main()
