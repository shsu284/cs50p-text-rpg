# CS50P Text RPG

#### Video Demo: [VIDEO URL WILL BE ADDED HERE]

#### Description:

CS50P Text RPG is a simple text-based role-playing game developed in Python as my final project for Harvard's CS50's Introduction to Programming with Python.

The objective of the game is to create a hero, choose a weapon and defeat three goblins in turn-based combat. Each enemy has different health and attack power, making the battles progressively more challenging.

At the beginning of the game, the player enters a character name and chooses a weapon. Each weapon has its own attack power, which determines how much damage the player can inflict on enemies. During combat, the player and the enemy take turns attacking each other. The player's health decreases when attacked, and the battle continues until either the player or the enemy is defeated.

The game also includes an inventory system and health potions. After defeating an enemy, the player receives a health potion that can restore health. The player can decide whether to use the potion immediately or keep it in the inventory for later. This adds a small element of resource management to the game.

Another important feature is the save and load system. The game stores the player's progress in a JSON file called `savegame.json`. This includes the character's name, current health, attack power, inventory and the index of the next enemy. When the game is started again, it checks whether a valid save file exists. If one is available, the player can continue from the previous progress instead of starting a new game. The program also checks the save data to ensure that it contains the expected information and valid values.

### Project Files

The project consists of three main Python files:

- **project.py:** Contains the main function and the game's main logic. It handles the game flow, weapon selection, combat, inventory interactions, saving and loading, and validation of save data.
- **game_classes.py:** Contains the `Player`, `Character` and `Item` classes. These classes represent the main objects in the game and organize their attributes and related methods.
- **test_project.py:** Contains automated tests written with pytest. The tests check the save-data validation, save-file checking and game-state saving functions. They cover valid data, invalid data and different file conditions.

The project uses Python's built-in `json` module to store game progress and `pathlib` to work with file paths. Pytest is used for automated testing.

### Design Decisions and Learning Experience

One of the main design decisions was to separate the game's classes from its main logic. This makes the code easier to organize and allows the different game objects to manage their own attributes and behavior.

JSON was chosen for saving progress because it provides a straightforward way to store Python data in a readable file. Since JSON data must be converted back into Python objects when loading a game, the program reconstructs the player's inventory and restores the saved attributes.

Developing this project helped me practise several concepts from CS50P, including functions, classes, object-oriented programming, exception handling, file operations, JSON serialization, type validation and automated testing.

The project combines these concepts into a playable program rather than isolated exercises.