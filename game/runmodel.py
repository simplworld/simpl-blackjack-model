from modelservice.simpl import games_client
from .model import Model


async def save_decision(period_id, decision):
    # add decision to period
    async with games_client as api_session:
        decision = await api_session.decisions.get_or_create(
            period=period_id,
            name='decision',
            data={"operand": decision},
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

        operand = 0.0
        period_decisions = await api_session.decisions.filter(period=period.id)
        if len(period_decisions) > 0:
            operand = float(period_decisions[0].data["operand"])

        prev_total = 0.0
        if period_count > 1:
            prev_period = periods[period_count - 2]
            prev_period_results = \
                await api_session.results.filter(period=prev_period.id)
            if len(prev_period_results) > 0:
                prev_total = float(prev_period_results[0].data["total"])

        # step model
        model = Model()
        total = model.step(operand, prev_total)
        data = {"total": total}

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
