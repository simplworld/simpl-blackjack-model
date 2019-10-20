import uuid

from modelservice.games import Period, Game
from modelservice.games import subscribe
from modelservice.simpl import games_client
from .model import Model


class BlackjackPeriod(Period):
    @subscribe
    async def submit_decision(self, action, **kwargs):
        """
        Receives the operand played and stores as a ``Decision`` then
        steps the model saving the ``Result``. A new ``Period`` is added to
        scenario in preparation for the next decision.
        """
        # Call will prefix the ROOT_TOPIC
        # "world.simpl.sims.blackjack.model.period.1.submit_decision"

        # Log our decision
        self.session.log.info("submit_decision: '{}'".format(action))

        # Save our decision
        async with games_client as api_session:
            await api_session.decisions.create(
                {
                    "period": self.pk,
                    "name": action,
                    "data": {"action": action},
                    "role": None,
                }
            )
        self.session.log.info("submit_decision: saved decision")

        scenario_id = self.scenario.pk

        # Get last period
        periods = self.scenario.periods.all()

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

                # if prev_period.results.all():
                #    data = prev_period.results.all()[0].json.get("data")
                #    print("Period Data")
                #    print(data)
                prev_period_results = await api_session.results.filter(
                    period=prev_period.pk
                )
                if len(prev_period_results) > 0:
                    data = prev_period_results[0].data["data"]

            model = Model()
            data = model.step(action, data)
            data = {"data": data}

            if not action == "new":
                # step model
                result = await api_session.results.create(
                    {"period": period.pk, "name": "results", "data": data, "role": None}
                )

                # prepare for next step by adding a new period
                next_period_order = period.order + 1
                next_period = await api_session.periods.create(
                    {"scenario": scenario_id, "order": next_period_order, "data": {}}
                )

            if action == "new":
                old_scenario = await api_session.scenarios.filter(id=scenario_id)
                runuser = old_scenario[0].runuser
                new_scenario = await api_session.scenarios.create(
                    {"runuser": runuser, "name": "Scenario {}".format(uuid.uuid4())}
                )

                new_period_for_new_scenario = await api_session.periods.create(
                    {"scenario": new_scenario.id, "order": 1, "data": {}}
                )

                result = await api_session.results.create(
                    {
                        "period": new_period_for_new_scenario.id,
                        "name": "results",
                        "data": data,
                        "role": None,
                    }
                )

                next_period = await api_session.periods.create(
                    {"scenario": new_scenario.id, "order": 2, "data": {}}
                )

        self.session.log.info("submit_decision: stepped scenario")


Game.register("blackjack", [BlackjackPeriod])
