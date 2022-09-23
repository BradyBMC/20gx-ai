import melee
import pickle
import numpy as np

#----------------------------------------------------------------------------

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
    '''
    position = (
                np.array(player.position.x, dtype=float),
                np.array(player.position.y, dtype=float)
               )
    '''
    position = [player.position.x, player.position.y]
    return position
    '''
    velocity = [
        player.speed_air_x_self,
        player.speed_ground_x_self,
        player.speed_x_attack,
        player.speed_y_attack,
        player.speed_y_self
    ]
    return [position, velocity, player.facing]
    '''

#----------------------------------------------------------------------------

'''
Process game data and controller inputs from slp -> pkl
Returns 0 if it DOESN'T work and 1 if it does
'''
def convert_dataset(
                    agent: melee.Character=melee.Character.CPTFALCON,
                    adversary: melee.Character=melee.Character.FOX,
                    match: bool=True,
                    train_path: str='Game_20220803T133857.slp',
                    pkl_path: str=None,
                    count: int=None
) -> None:

    # assert train_path is not None
    # assert pkl_path is not None
    
    console = melee.Console(is_dolphin=False, path=train_path)
    console.connect()

    if match is True:
        agent_port = has_character(console, agent)
        adversary_port = has_character(console, adversary, agent_port)
        if agent_port == -1 or adversary_port == -1:
            print('ERROR character not found in slp file')
            return 0

    # Need to change how name will be generated
    f = open(pkl_path + '/data' + str(count) + '.pkl', 'wb')
    # f = open('data.pkl', 'wb')

    data = []
    while True:
        gamestate = console.step()
        # step() returns None when the file ends
        if gamestate is None:
            break

        # Each frame has game data and controller data
        #frame = {}
        frame = []

        # Visible game data for 1 frame
        agent_data = gamedata(gamestate.players[agent_port])
        adversary_data = gamedata(gamestate.players[adversary_port])
        # frame.append(agent_data)
        # frame.append(adversary_data)
        frame.append([agent_data[0], agent_data[1],
                      adversary_data[0], adversary_data[1]])
        
        
        # frame['Gamedata'] = [agent_data, adversary_data]

        # All controller data for 1 frame
        controller = gamestate.players[agent_port].controller_state
        
        count = 0
        pressed = []
        for button in controller.button:
            count += 1
            if controller.button[button] is True:
                pressed.append(float(1))
            else:
                pressed.append(float(0))
            if count == 6:
                break
        # Missing L/R half press for light shield. Dpad missing bc Luigi and Samus = Cringe

        control_stick = [float(round(controller.main_stick[0], 2)), float(round(controller.main_stick[1], 2))]
        c_stick = [float(round(controller.c_stick[0], 2)), float(round(controller.c_stick[1], 2))]
        # inputs = [control_stick, c_stick, pressed]
        inputs = control_stick + c_stick + pressed

        # frame['Controller'] = inputs
        frame.append(inputs)

        data.append(frame)

    pickle.dump(data, f)
    f.close()
    
    return 1

#----------------------------------------------------------------------------

if __name__ == '__main__':
    convert_dataset()