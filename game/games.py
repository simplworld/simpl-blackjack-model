import asyncio

from modelservice.games import Scenario, Game
from modelservice.games import register
from modelservice.simpl import games_client
from .model import Model


class BlackjackScenario(Scenario):
    @register
    async def deal_new_game(self, **kwargs):
        """
        Deal a new game to the user
        """
        self.session.log.info("deal_new_game: {}".format(self.pk))

        async with games_client as api_session:
            # Delete all existing Periods
            await api_session.bulk.periods.delete(scenario=self.pk)
            self.session.log.info("Deleted bulk periods!!!!")

            await asyncio.sleep(0.5)
            self.session.log.info("Woke from sleep!!!!")

            # Create a new initial period
            new_period = await api_session.periods.create(
                {"scenario": self.pk, "order": 1, "data": {}}
            )

            return new_period.id

    @register
    async def submit_decision(self, action, **kwargs):
        """
        Receives the operand played and stores as a ``Decision`` then
        steps the model saving the ``Result``. A new ``Period`` is added to
        scenario in preparation for the next decision.
        """
        # Call will prefix the ROOT_TOPIC
        # "world.simpl.sims.blackjack.model.scenario.1.submit_decision"

        # Log our decision
        self.session.log.info("submit_decision: '{}'".format(action))

        scenario_id = self.pk

        # Get last period
        async with games_client as api_session:
            periods = await api_session.periods.filter(
                scenario=scenario_id, ordering="order"
            )
            period_count = len(periods)
            last_period = periods[period_count - 1]

        # periods = self.periods.all()
        # periods = list(periods)
        # last_period = periods[-1]

        # Save our decision
        async with games_client as api_session:
            await api_session.decisions.create(
                {
                    "period": last_period.pk,
                    "name": action,
                    "data": {"action": action},
                    "role": None,
                }
            )
        self.session.log.info("submit_decision: saved decision")

        async with games_client as api_session:
            periods = await api_session.periods.filter(
                scenario=scenario_id, ordering="order"
            )
            period_count = len(periods)
            period = periods[period_count - 1]

            print("Period")
            print(period)

            if action is None:
                action = "deal"

            data = {}
            if period_count > 1:
                prev_period = periods[period_count - 2]

                prev_period_results = await api_session.results.filter(
                    period=prev_period.pk
                )
                if len(prev_period_results) > 0:
                    data = prev_period_results[0].data["data"]

            model = Model()
            data = model.step(action, data)
            data = {"data": data}

            # step model
            result = await api_session.results.create(
                {"period": period.pk, "name": "results", "data": data, "role": None}
            )

            # prepare for next step by adding a new period
            next_period_order = period.order + 1
            next_period = await api_session.periods.create(
                {"scenario": scenario_id, "order": next_period_order, "data": {}}
            )

        self.session.log.info("submit_decision: stepped scenario")


Game.register("blackjack", [BlackjackScenario])
