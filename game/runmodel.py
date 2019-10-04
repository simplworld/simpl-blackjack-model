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


async def step_scenario(scenario_id):
    """
    Step the scenario's current period
    """
    async with games_client as api_session:
        periods = await api_session.periods.filter(scenario=scenario_id,
                                                   ordering='order')
        period_count = len(periods)
        period = periods[period_count - 1]

        action = 'deal'
        period_decisions = await api_session.decisions.filter(period=period.id)
        if len(period_decisions) > 0:
            action = period_decisions[0].data["action"]

        data = {}
        if period_count > 1:
            prev_period = periods[period_count - 2]
            prev_period_results = \
                await api_session.results.filter(period=prev_period.id)
            if len(prev_period_results) > 0:
                data = prev_period_results[0].data["data"]

        # step model
        model = Model()
        data = model.step(action, data)
        data = {"data": data}

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
        await next_period.save()

        return next_period.id
