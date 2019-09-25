from modelservice.games import Period, Game
from modelservice.games import subscribe, register

from .runmodel import step_scenario, save_decision


class SimplCalcPeriod(Period):
    @subscribe
    async def submit_decision(self, operand, **kwargs):
        """
        Receives the operand played and stores as a ``Decision`` then
        steps the model saving the ``Result``. A new ``Period`` is added to
        scenario in preparation for the next decision.
        """
        # Call will prefix the ROOT_TOPIC
        # "world.simpl.sims.simpl-calc.model.period.1.submit_decision"

        for k in kwargs:
            self.session.log.info("submit_decision: Key: {}".format(k))

        await save_decision(self.pk, operand)
        self.session.log.info("submit_decision: saved decision")

        await step_scenario(self.scenario.pk)
        self.session.log.info("submit_decision: stepped scenario")


Game.register('simpl-calc', [
    SimplCalcPeriod,
])
