from typing import List, Tuple, Dict

# Map layouts (grid coordinates)
MAPS = {
    "Forest": {
        "path": [(0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), 
                (5, 4), (5, 5), (5, 6), (5, 7), 
                (6, 7), (7, 7), (8, 7), (9, 7), (10, 7),
                (10, 6), (10, 5), (10, 4), (10, 3), (10, 2),
                (11, 2), (12, 2), (13, 2), (14, 2), (15, 2),
                (15, 3), (15, 4), (15, 5), (15, 6), (15, 7),
                (16, 7), (17, 7), (18, 7), (19, 7)],
        "description": "A winding forest path with many turns"
    },
    "Ice Kingdom": {
        "path": [(17,0),(17,3),(14,3),(14,2),(2,2),(2,10),(5,10),(5,7),(13,7),(13,13),(16,13),(16,10),(9,10),(9,13),(0,13)],
        "description": "A frozen kingdom with slippery paths"
    },
    "Flame Desert": {
        "path": [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2),
                (4, 3), (4, 4), (4, 5), (4, 6),
                (5, 6), (6, 6), (7, 6), (8, 6), (9, 6),
                (9, 5), (9, 4), (9, 3), (9, 2),
                (10, 2), (11, 2), (12, 2), (13, 2),
                (13, 3), (13, 4), (13, 5), (13, 6),
                (14, 6), (15, 6), (16, 6), (17, 6), (18, 6), (19, 6)],
        "description": "A scorching desert with winding paths"
    }
}

# Difficulty settings
DIFFICULTY_SETTINGS = {
    "Easy": {
        "enemy_health_multiplier": 0.8,
        "enemy_speed_multiplier": 0.8,
        "enemy_reward_multiplier": 1.2,
        "starting_gold": 150,
        "starting_lives": 15,
        "wave_size_multiplier": 0.8
    },
    "Medium": {
        "enemy_health_multiplier": 1.0,
        "enemy_speed_multiplier": 1.0,
        "enemy_reward_multiplier": 1.0,
        "starting_gold": 100,
        "starting_lives": 10,
        "wave_size_multiplier": 1.0
    },
    "Hard": {
        "enemy_health_multiplier": 1.3,
        "enemy_speed_multiplier": 1.2,
        "enemy_reward_multiplier": 0.8,
        "starting_gold": 75,
        "starting_lives": 8,
        "wave_size_multiplier": 1.2
    },
    "Hell": {
        "enemy_health_multiplier": 1.8,
        "enemy_speed_multiplier": 1.5,
        "enemy_reward_multiplier": 0.6,
        "starting_gold": 50,
        "starting_lives": 5,
        "wave_size_multiplier": 1.5
    }
}

def get_map_path(map_name: str) -> List[Tuple[int, int]]:
    """Get the path for a specific map."""
    if map_name not in MAPS:
        raise ValueError(f"Map '{map_name}' not found")
    return MAPS[map_name]["path"]

def get_map_description(map_name: str) -> str:
    """Get the description for a specific map."""
    if map_name not in MAPS:
        raise ValueError(f"Map '{map_name}' not found")
    return MAPS[map_name]["description"]

def get_difficulty_settings(difficulty: str) -> Dict:
    """Get the settings for a specific difficulty level."""
    if difficulty not in DIFFICULTY_SETTINGS:
        raise ValueError(f"Difficulty '{difficulty}' not found")
    return DIFFICULTY_SETTINGS[difficulty] 
