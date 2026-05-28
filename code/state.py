def make_waiting_state():
    """Returns a fresh game state dict, ready to start a new match."""
    return {
        "game_status": "waiting",
        "winner": None,
        "win_reason": None,
        "victory_shown": False,
        "tick_count": 0,
        "players":{},
        "hands":{},
        "snakes": {
            "green": {
                "pixels":  [[0,0], [1,0], [2,0]],
                "score": 0,
                "direction": "RIGHT",       
                "powerPillActive": False,
                "turboActive": False
            },
            "purple": {
                "pixels":[[7, 7], [6, 7], [5, 7]],
                "score": 0,
                "direction": "LEFT",
                "powerPillActive": False,
                "turboActive": False
            }
        },
        "food":[[1, 1], [6, 6]],
        "pending_cards": {
            "green": [],
            "purple": []
            
        }
    }
if __name__ == "__main__":
    import json
    state = make_waiting_state()
    print(json.dumps(state, indent=2))