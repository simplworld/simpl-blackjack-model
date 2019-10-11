from modelservice.simpl import games_client
from .model import Model


async def save_decision(period_id, decision):
    # add decision to period
    async with games_client as api_session:
        decision = await api_session.decisions.get_or_create(
            period=period_id,
            name='decision',
            data={"action": decision},
            defaults={"role": None}
        )
        return decision


async def step_scenario(scenario_id, action=None):
    """
    Step the scenario's current period
    """
    async with games_client as api_session:
        periods = await api_session.periods.filter(scenario=scenario_id,
                                                   ordering='order')
        period_count = len(periods)
        period = periods[period_count - 1]

        if action is None:
            action = 'deal'

        data = {}
        if period_count > 1:
            prev_period = periods[period_count - 2]
            prev_period_results = \
                await api_session.results.filter(period=prev_period.id)
            if len(prev_period_results) > 0:
                data = prev_period_results[0].data["data"]

        model = Model()
        data = model.step(action, data)
        data = {"data": data}

        if not action == 'new':
            # step model
            result = await api_session.results.get_or_create(
                period=period.id,
                name='results',
                data=data,
                defaults={"role": None}
            )

            # prepare for next step by adding a new period
            next_period_order = period.order + 1
            next_period = await api_session.periods.get_or_create(
                scenario=scenario_id,
                order=next_period_order,
            )

        if action == 'new':
            old_scenario = await api_session.scenarios.filter(id=scenario_id)
            runuser = old_scenario[0].runuser
            new_scenario = await api_session.scenarios.get_or_create(
                runuser=runuser,
                name='Scenario {}'.format(scenario_id + 1),
            )

            new_period_for_new_scenario = await api_session.periods.get_or_create(
                scenario=new_scenario.id,
                order=1,
            )

            result = await api_session.results.get_or_create(
                period=new_period_for_new_scenario.id,
                name='results',
                data=data,
                defaults={"role": None}
            )

            next_period = await api_session.periods.get_or_create(
                scenario=new_scenario.id,
                order=2
            )

        await next_period.save()

        return next_period.id

