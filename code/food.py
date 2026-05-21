import random

BOARD_SIZE = 8

# generate ramdom x , y that is not ocuupied by snake 
def random_free_position(ocuupied_positions):
    # loop to antil find a free position
    while True:
        x = random.randint(0, BOARD_SIZE - 1)
        y = random.randint(0, BOARD_SIZE - 1)
        if [x, y] not in ocuupied_positions:
            #flat the list 
            return [x, y]
        else:
            continue



#  Generate `count` new food positions, avoiding snakes and other food.
def spawn_food(snakes_pixel, existing_food, count=1):
    # call random free position many times and flatten the snake list
    flat_snakes = []
    for snake in snakes_pixel:
        flat_snakes.extend(snake)    # add all pixels to the snake list
    
    new_food = []
    for i in range(count):
    # occupied positions for any snake or food call this function
       occupied = flat_snakes + existing_food + new_food
       new_food.append(random_free_position(occupied))
    return new_food 


def check_food_eaten(head, food_list):
    if head in food_list:
        return head
    return None 


if __name__ == "__main__":
    snake = [[0, 0], [1, 0], [2, 0]]
    food = spawn_food([snake], [], count=2)
    print(f"Initial food: {food}")

    # simulate snake etaing food
    head = food[0]
    eaten = check_food_eaten(head, food)
    print(f"Ate: {eaten}")

