from pytocl.driver import Driver
from pytocl.car import State, Command
import pickle
import base

class MyDriver(Driver):
    # Override the `drive` method to create your own driver
    ...
    def drive(self, carstate: State) -> Command:
        # Interesting stuff
        # print(carstate)

        sensor = base.MySensorModel()
        sensor.setCarState(carstate)


        driver = base.HeuristicDriver()
        recievedAct = driver.control(sensor)

        # print(">>>Decided Move: ", recievedAct.toString())

        # print(">>>For State: \n", carstate)

        command = Command()
        command.accelerator = recievedAct.accelerate
        command.brake = recievedAct.brake
        command.gear = recievedAct.gear
        command.steering = recievedAct.steering
        command.focus = recievedAct.focus
        command.clutch = recievedAct.clutch

        return command
