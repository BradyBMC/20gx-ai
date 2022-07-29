import melee
import pickle

'''
Returns port of specific character and -1 if not found
Skip checking for specific port
'''
def has_character(
                    console: melee.Console,
                    character: melee.Character,
                    skip: int=-1
) -> int:

    gamestate = console.step()
    if gamestate is None:
        return False
    for i in range(1,3):
        if character == gamestate.players[i].character and i != skip:
            return i
    return -1

def convert_dataset(
                    agent: melee.Character=melee.Character.CPTFALCON,
                    adversary: melee.Character=melee.Character.FOX,
                    match: bool=True
) -> None:

    console = melee.Console(is_dolphin=False, path="/Users/bchan/Slippi/Game_20220727T191324.slp")
    console.connect()

    if match is True:
        agent_port = has_character(console, agent)
        adversary_port = has_character(console, adversary, agent_port)
        if agent_port == -1 or adversary_port == -1:
            print('ERROR character not found in slp file')
            return

    f = open('data.pkl', 'w')

    data = []
    while True:
        gamestate = console.step()
        # step() returns None when the file ends
        if gamestate is None:
            break
        frame = {}
        # Each frame has character data and controller data
        break

    pickle.dump(data, f)
    f.close()

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