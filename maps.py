from typing import List, Tuple, Dict

# Map layouts (grid coordinates)
MAPS = {
    "Forest": {
        "path": [(0,2),(1,2),(2,2),(2,3),(2,4),(2,5),(2,6),
                 (2,7),(2,8),(2,9),(2,10),(2,11),(2,12),(3,12),
                 (4,12),(4,12),(4,11),(4,10),(4,9),(4,8),(4,7),(4,6)
            ,(4,5),(4,4),(4,3),(4,2),(4,1),(5,1),(6,1),(7,1),(8,1)
            ,(9,1),(10,1),(11,1),(12,1),(13,1),(14,1),(15,1),(16,1),(17,1)
            ,(18,1),(19,1),(20,1),(20,2),(20,3),(20,4),(19,4),(18,4),(17,4),(16,4)
            ,(15,4),(14,4),(13,4),(12,4),(11,4),(10,4),(9,4),(8,4),(7,4),(7,5),(7,6)
            ,(7,7),(7,8),(7,9),(7,10),(8,10),(9,10),(10,10),(11,10),(11,9),(11,8),(11,7)
            ,(12,7),(13,7),(14,7),(14,8),(14,9),(14,10),(15,10),(16,10),(17,10),(18,10)
            ,(19,10),(20,10)],
        "description": "A winding forest path with many turns"
    },
    "Ice Kingdom": {
        "path": [(17,0),(17,1),(17,2),(17,3),(16,3),(15,3),(14,3),(14,2),(13,2),(12,2)
            ,(11,2),(10,2),(9,2),(8,2),(7,2),(6,2),(5,2),(4,2),(3,2),(2,2),(2,3),(2,4)
            ,(2,5),(2,6),(2,7),(2,8),(2,9),(2,10),(3,10),(4,10),(5,10),(5,9),(5,8),(5,7)
            ,(6,7),(7,7),(8,7),(9,7),(10,7),(11,7),(12,7),(13,7),(13,8),(13,9),(13,10)
            ,(13,11),(13,12),(13,13),(14,13),(15,13),(16,13),(16,12),(16,11),(16,10)
            ,(15,10),(14,10),(13,10),(12,10),(11,10),(10,10),(9,10),(9,11),(9,12)
            ,(9,13),(8,13),(7,13),(6,13),(5,13),(4,13),(3,13),(2,13),(1,13),(0,13)],
        "description": "A frozen kingdom with slippery paths"
    },
    "Flame Desert": {
        "path": [(0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(5,2),(5,3),(5,4),(4,4),(3,4)
            ,(2,4),(2,5),(2,6),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7),(8,7),(8,6),(8,5)
            ,(8,4),(8,3),(8,2),(9,2),(10,2),(11,2),(11,3),(11,4),(11,5),(11,6),(12,6)
            ,(13,6),(13,5),(13,4),(13,3),(13,2),(13,1),(14,1),(15,1),(16,1),(16,2)
            ,(16,3),(16,4),(16,5),(16,6),(16,7),(16,8),(16,9),(16,10),(15,10),(14,10)
            ,(14,9),(14,8),(13,8),(12,8),(11,8),(10,8),(10,9),(10,10),(9,10),(8,10),(7,10)
            ,(6,10),(5,10),(4,10),(3,10),(2,10),(2,11),(2,12),(2,13),(3,13),(4,13),(5,13)
            ,(6,13),(7,13),(8,13),(9,13),(10,13),(11,13),(12,13),(13,13),(14,13),(15,13)
            ,(16,13),(17,13),(18,13),(19,13),(20,13)],
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
