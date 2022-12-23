from mapek.Monitor import Monitor
from subject.PositionSensor import PositionSensor


def run_simulation():
    monitor = Monitor()
    sensor = PositionSensor()

    sensor.register(monitor)
    sensor.read_data()

if __name__ == '__main__':
    run_simulation()