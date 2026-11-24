import json
from game_classes import Item, Player
from project import check_save_file, save_game, validate_save_data


def valid_save_payload():
    return {
        "name": "Aria",
        "hp": 85,
        "attack_power": 20,
        "inventory": ["Health Potion"],
        "next_enemy_index": 1,
    }


# --- Tests for validate_save_data() ---


def test_validate_save_data_valid():
    assert validate_save_data(valid_save_payload()) is True


def test_validate_save_data_missing_key():
    data = valid_save_payload()
    del data["next_enemy_index"]
    assert validate_save_data(data) is False


def test_validate_save_data_invalid_values():
    bad_name = {**valid_save_payload(), "name": "   "}
    zero_hp = {**valid_save_payload(), "hp": 0}
    negative_attack = {**valid_save_payload(), "attack_power": -5}
    bad_inventory = {**valid_save_payload(), "inventory": ["Health Potion", 123]}
    out_of_range_index = {**valid_save_payload(), "next_enemy_index": 4}
    non_dict = ["not", "a", "dict"]

    for payload in [
        bad_name,
        zero_hp,
        negative_attack,
        bad_inventory,
        out_of_range_index,
        non_dict,
    ]:
        assert validate_save_data(payload) is False


# --- Tests for check_save_file() ---


def test_check_save_file_missing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert check_save_file() is False


def test_check_save_file_corrupt_json(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    save_file = tmp_path / "savegame.json"
    save_file.write_text("{not valid json", encoding="utf-8")
    assert check_save_file() is False


def test_check_save_file_valid_json(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    save_file = tmp_path / "savegame.json"
    save_file.write_text(json.dumps(valid_save_payload()), encoding="utf-8")
    assert check_save_file() is True


# --- Tests for save_game() ---


def test_save_game_writes_expected_state(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    hero = Player("Thorin")
    hero.hp = 70
    hero.attack_power = 20
    hero.add_item(Item("Health Potion", "heal", 25))

    save_game(hero, 2)

    saved_path = tmp_path / "savegame.json"
    assert saved_path.exists()

    with saved_path.open("r", encoding="utf-8") as f:
        saved_data = json.load(f)

    assert saved_data == {
        "name": "Thorin",
        "hp": 70,
        "attack_power": 20,
        "inventory": ["Health Potion"],
        "next_enemy_index": 2,
    }
    assert validate_save_data(saved_data) is True