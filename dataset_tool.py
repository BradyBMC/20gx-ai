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

#----------------------------------------------------------------------------

'''
Copies ingame character data and returns as list
May need to restructure how data is saved
'''
def gamedata(player: melee.GameState.players) -> list:
    position = player.position
    velocity = [
        player.speed_air_x_self,
        player.speed_ground_x_self,
        player.speed_x_attack,
        player.speed_y_attack,
        player.speed_y_self
    ]
    return [position, velocity, player.facing]

#----------------------------------------------------------------------------

'''
Process game data and controller inputs from slp -> pkl
'''
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

    f = open('data.pkl', 'wb')

    data = []
    while True:
        gamestate = console.step()
        # step() returns None when the file ends
        if gamestate is None:
            break

        # Each frame has game data and controller data
        frame = {}

        # Visible game data for 1 frame
        agent_data = gamedata(gamestate.players[agent_port])
        adversary_data = gamedata(gamestate.players[adversary_port])
        frame['Gamedata'] = [agent_data, adversary_data]

        # All controller data for 1 frame
        controller = gamestate.players[agent_port].controller_state
        pressed = []
        for button in controller.button:
            if controller.button[button] is True:
                pressed.append(button)
        control_stick = (round(controller.main_stick[0], 2), round(controller.main_stick[1], 2))
        c_stick = (round(controller.c_stick[0], 2), round(controller.c_stick[1], 2))
        inputs = [control_stick, c_stick, pressed]
        frame['Controller'] = inputs
        # Missing L/R half press for light shield. Dpad missing bc Luigi and Samus = Cringe

        data.append(frame)

    pickle.dump(data, f)
    f.close()

#----------------------------------------------------------------------------

if __name__ == '__main__':
    convert_dataset()