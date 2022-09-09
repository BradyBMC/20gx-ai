from tensorflow import keras
from keras.models import load_model
import melee
import numpy as np
from sklearn.preprocessing import MinMaxScaler


model = load_model('40-0.0000-0.0000-0.0001-0.0002.hdf5')
print('Model Loaded!')

console = melee.Console(path="/Users/bchan/Library/Application Support/Slippi Launcher/netplay/Slippi Dolphin.app")

controller = melee.Controller(console=console, port=1)
controller_human = melee.Controller(console=console,
                                    port=2,
                                    type=melee.ControllerType.GCN_ADAPTER)

console.run()
console.connect()

controller.connect()
controller_human.connect()

scaler = MinMaxScaler(feature_range=(0,1))
sample = list()
timestep = 48

while True:
    gamestate = console.step()
    # Press buttons on controller based on the GameState
    if gamestate.menu_state in [melee.enums.Menu.IN_GAME, melee.enums.Menu.SUDDEN_DEATH]:
        agent_port = 1
        player_port = 2
        agent = gamestate.players[agent_port]
        player = gamestate.players[player_port]
        agent_pos = [agent.position.x, agent.position.y]
        player_pos = [player.position.x, player.position.y]
        pos = [agent.position.x, agent.position.y,
                player.position.x, player.position.y]

        trans = None
        if len(sample) < timestep:
            sample = [pos for i in range(timestep)]
        else:
            sample = sample[1:] + [pos]
        trans = scaler.fit_transform(sample)
        trans = np.array(trans)
        trans = trans.reshape((1, trans.shape[0], trans.shape[1]))
        assert trans is not None, 'trans is None'
        print(model.predict(trans, verbose=0))
    else:
    # Selects character and stage
        melee.MenuHelper.menu_helper_simple(gamestate,
                                            controller,
                                            melee.Character.CPTFALCON,
                                            melee.Stage.BATTLEFIELD,
                                            "",
                                            autostart=True,
                                            swag=False)