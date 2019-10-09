import djclick as click

from modelservice.simpl import games_client
from modelservice.utils.asyncio import coro

from ...runmodel import step_scenario, save_decision


@click.command()
@click.option('--scenario_id', '-s', type=int, help='Scenario.id')
@click.option('--decision', '-d', default=0, type=int,
              help='Integer to add to current total. (defaults to 0)')
@coro
async def command(scenario_id, decision):
    """
    Add decision to current scenario period, step the model and save result
    """
    if scenario_id is None:
        click.secho("ERROR: scenario_id must specified", fg='red')
        return

    async with games_client as api_session:
        game = await api_session.games.get(slug='simpl-blackjack')

        # periods are returned in order
        periods = await api_session.periods.filter(scenario=scenario_id,
                                                   ordering='order')
        period_count = len(periods)
        period = periods[period_count - 1]

        # add submitted decision to current period
        await save_decision(period.id, decision)

        # calculate new total
        await step_scenario(scenario_id)
