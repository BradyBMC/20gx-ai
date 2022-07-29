import melee
import pickle

# Returns port of targeted character
def has_character(console: melee.Console, character: melee.Character) -> int:
    gamestate = console.step()
    if gamestate is None:
        return False
    for i in range(1,3):
        if character == gamestate.players[i].character:
            return i
    return -1

def player_data(gamestate):
    player = gamestate.players[1].controller_state
    return

def convert_dataset(character: melee.Character=melee.Character.CPTFALCON) -> None:

    console = melee.Console(is_dolphin=False, path="/Users/bchan/Slippi/Game_20220722T142744.slp")
    console.connect()

    

    data = []
    while True:
        gamestate = console.step()
        # step() returns None when the file ends
        if gamestate is None:
            break
        frame = {}
        # Each frame has character data and controller data
        # Character data is location, velocity, hitstun

        p1 = player_data(gamestate)
        print(gamestate.players[2].character == character)
        break

'''
count = 0
stick_pos = {}
while True:
    gamestate = console.step()
    # step() returns None when the file ends
    if gamestate is None:
        break
    # print(gamestate.players[1].controller_state)
    temp = gamestate.players[1].controller_state
    player = gamestate.players[1]
    print(player)
    pressed = []
    for x in temp.button:
        if temp.button[x] is True:
            pressed.append(x)
    if len(pressed) >= 1:
        print(gamestate.players[1].position.x, gamestate.players[1].position.y, pressed)
    # print(type(temp.main_stick))
    r = (round(temp.main_stick[0], 2), round(temp.main_stick[1], 2))
    if r not in stick_pos:
        stick_pos[r] = 1
    else:
        stick_pos[r] += 1
    count += 1
    break
print(stick_pos)
print(count)
'''

if __name__ == '__main__':
    convert_dataset()