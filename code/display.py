from sense_hat import SenseHat
import time

sense = SenseHat()

#constants - colors
GREEN = (0, 255, 0)
PURPLE = (160, 32, 240)
FOOD = (255,255, 0)

def draw_state(state):
    """"Render the full game state on the led matrix"""
    sense.clear()
     # draw the green snake in the inicial state
    for pixel in state['snakes']['green']['pixels']:
        x, y = pixel[0], pixel[1]
        sense.set_pixel(x, y, GREEN)

# 3 draw snake puprple same patter
    for pixel in state['snakes']['purple']['pixels']:
        x, y = pixel[0], pixel[1]
        sense.set_pixel(x, y, PURPLE)

    # draw food
    for pixel in state['food']:
        x, y = pixel[0], pixel[1]
        sense.set_pixel(x, y, FOOD)


# test 
if __name__ == "__main__":
    state = {
        "snakes": {
            "green":  {"pixels": [[0,0], [1,0], [2,0]]},
            "purple": {"pixels": [[7,7], [6,7], [5,7]]},
        },
        "food": [[1,1], [6,6]],
    }
    draw_state(state)
    time.sleep(5)
    sense.clear()