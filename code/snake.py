# Logical code 

#constants - board size and directon deltas

BOARD_SIZE = 8

DELTAS = {
    "UP": (-0, -1),
    "DOWN": (0, 1),
    "LEFT": (-1, 0),
    "RIGHT": (1, 0),
}

def make_snake(start_x, start_y, length=3):
    """Creates a horizontal snake starting at start_x, start_y."""
    snake = []
    for i in range(length):
        snake.append([start_x + i, start_y])
    return snake


def move_snake(snake, direction):
    """Move the snake one step in the given direction. Returns new snake list."""
    # Get current head
    head = snake[-1]

    # Get delta for the direction
    dx, dy = DELTAS[direction]

    # Calculate new head with wrap-around
    new_head = [(head[0] + dx) % BOARD_SIZE, (head[1] + dy) % BOARD_SIZE]

    # build new snake
    new_snake = snake[1:]+ [new_head]
    return new_snake

# grow snake
def grow_snake(snake, direction):
    head = snake[-1]
    dx, dy = DELTAS [direction]
    new_head = [(head[0] + dx) % BOARD_SIZE, (head[1] + dy) % BOARD_SIZE]
    new_snake = snake + [new_head]
    return new_snake
    

# test for the moviments 
if __name__ == "__main__":
    snake = make_snake(0,0)
    print(f"Initial snake: {snake}")

    snake = move_snake(snake, "RIGHT")
    print(f"Move right: {snake}")

    snake = move_snake(snake, "DOWN")
    print(f"Move down: {snake}")
    
    snake = grow_snake(snake, "RIGHT")
    print(f"After grow: {snake}")