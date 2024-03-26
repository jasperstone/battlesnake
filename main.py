# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing
import sys
import copy

# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "Team16",  # TODO: Your Battlesnake Username
        "color": "#B3A369",  # TODO: Choose color
        "head": "bee",  # TODO: Choose head
        "tail": "ion",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")

def manhattan_distance(a, b):
    return abs(a["x"] - b["x"]) + abs(a["y"] - b["y"])

def get_food_count(head, food):
    radius = 3
    food_count = 0
    for bite in food:
        if abs(head["x"] - bite["x"]) <= radius and abs(head["y"] - bite["y"]) <= radius:
            food_count += 1
    return food_count

def normalize(x, min, max):
    return (x - min)/(max - min)

def snake_eval_function(snake, game_state):
    normalized_length = normalize(snake["length"], 0, 121)
    normalized_health = normalize(snake["health"], 0, 100)

    food_count = get_food_count(snake["head"], game_state["board"]["food"])
    normalized_food_count = normalize(food_count, 0, 23)

    possible_moves = ["up", "down", "left", "right"]
    safe_moves = get_safe_moves(possible_moves, snake["body"], game_state["board"])
    normalized_safe_moves = normalize(len(safe_moves), 0, 3)

    value = normalized_length + normalized_health + normalized_food_count + normalized_safe_moves
    return value

def eval_function(game_state):
    me = game_state["you"]
    my_heuristic = snake_eval_function(me, game_state)

    them = game_state["board"]["snakes"][0]
    their_heuristic = snake_eval_function(them, game_state)

    return my_heuristic - their_heuristic

def process_move(game_state, move, maximizingPlayer):
    snake = get_current_snake(game_state, maximizingPlayer)
    next_head = get_next(snake["head"], move)
    if next_head in game_state["board"]["food"]:
        snake["length"] += 1
        snake["health"] = 100
        snake["body"].insert(0, next_head)
        snake["head"] = next_head
        game_state["board"]["food"].remove(next_head)
    else:
        snake["health"] -= 1
        snake["body"].insert(0, next_head)
        snake["body"].pop()
        snake["head"] = next_head
    return game_state

def get_current_snake(game_state, maximizingPlayer):
    if maximizingPlayer:
        return game_state["you"]
    else:
        return game_state["board"]["snakes"][0]

def minimax(game_state, depth, maximizingPlayer):
    possible_moves = ["up", "down", "left", "right"]
    
    snake = get_current_snake(game_state, maximizingPlayer)
    safe_moves = get_safe_moves(possible_moves, snake["body"], game_state["board"])

    if depth == 0 or len(safe_moves) == 0:
        return (eval_function(game_state), random.choice(possible_moves))
    if maximizingPlayer:
        value = -sys.maxsize
        best_move = None
        for guess in safe_moves:
            new_state = process_move(copy.deepcopy(game_state), guess, maximizingPlayer)
            minimax_value, _ = minimax(new_state, depth - 1, False)
            if minimax_value > value:
                value = minimax_value
                best_move = guess
        return (value, best_move)
    else:
        value = sys.maxsize
        best_move = None
        for guess in safe_moves:
            new_state = process_move(copy.deepcopy(game_state), guess, maximizingPlayer)
            minimax_value, _ = minimax(new_state, depth - 1, True)
            if minimax_value < value:
                value = minimax_value
                best_move = guess
        return (value, best_move)

def get_next(current_head, next_move):
    """
    return the coordinate of the head if our snake goes that way
    """
    MOVE_LOOKUP = {"left":-1, "right": 1, "up": 1, "down":-1}
    # Copy first
    future_head = current_head.copy()

    if next_move in ["left", "right"]:
        # X-axis
        future_head["x"] = current_head["x"] + MOVE_LOOKUP[next_move]
    elif next_move in ["up", "down"]:
        future_head["y"] = current_head["y"] + MOVE_LOOKUP[next_move]

    return future_head

def avoid_walls(future_head, board_width, board_height):
    result = True

    x = int(future_head["x"])
    y = int(future_head["y"])

    if x < 0 or y < 0 or x >= board_width or y >= board_height:
        result = False

    return result

def avoid_snakes(future_head, snake_bodies):
    for snake in snake_bodies:
        if future_head in snake["body"][:-1]:
            return False
    return True

# adapted from https://github.com/altersaddle/untimely-neglected-wearable
def get_safe_moves(possible_moves, body, board):
    safe_moves = []
    for guess in possible_moves:
        guess_coord = get_next(body[0], guess)
        if avoid_walls(guess_coord, board["width"], board["height"]) and avoid_snakes(guess_coord, board["snakes"]) and guess_coord not in body[:-1]:
            safe_moves.append(guess)
        elif len(body) > 1 and guess_coord == body[-1] and guess_coord not in body[:-1]:
           # The tail is also a safe place to go... unless there is a non-tail segment there too
           safe_moves.append(guess)
    return safe_moves

# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    value, next_move = minimax(game_state, 5, True)

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server
    port = "8000"
    for i in range(len(sys.argv) - 1):
        if sys.argv[i] == '--port':
            port = sys.argv[i+1]

    run_server({"info": info, "start": start, "move": move, "end": end, "port": port})
