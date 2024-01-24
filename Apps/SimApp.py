
from Apps.App import App
from Sim.Simulation import Simulation


class SimApp(App):
    """
    Class for delegating a simulation to a bot.
    """

    def run(self):
        """
        Runs the sim
        """
        Simulation(self._service_provider).run()
