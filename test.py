import melee

console = melee.Console(path="/Users/bchan/Library/Application Support/Slippi Launcher/netplay/Slippi Dolphin.app")

controller = melee.Controller(console=console, port=1)
controller_human = melee.Controller(console=console,
                                    port=2,
                                    type=melee.ControllerType.GCN_ADAPTER)

console.run()
console.connect()

controller.connect()
controller_human.connect()

while True:
    gamestate = console.step()
    # Press buttons on your controller based on the GameState here!
    if gamestate.menu_state in [melee.enums.Menu.IN_GAME, melee.enums.Menu.SUDDEN_DEATH]:
        if gamestate.distance <= 30:
            controller.press_button(melee.enums.Button.BUTTON_X)
            controller.tilt_analog(melee.enums.Button.BUTTON_MAIN, 0, 0.5)
    else:
        melee.MenuHelper.menu_helper_simple(gamestate,
                                            controller,
                                            melee.Character.CPTFALCON,
                                            melee.Stage.BATTLEFIELD,
                                            "",
                                            autostart=True,
                                            swag=False)