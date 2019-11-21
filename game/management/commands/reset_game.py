import djclick as click

from modelservice.simpl.sync import games_client


def echo(text, value):
    click.echo(click.style(text, fg="green") + "{0}".format(value))


@click.command()
def command():
    """
    Reset the entire game.
    This will remove all RunUser Scenarios from the one default Run
    and create new empty Scenarios and Periods for them.
    """
    echo("Resetting game: ", "Simpl Blackjack")

    # Create a Game
    game = games_client.games.get_or_create(name="Simpl Blackjack", slug="simpl-blackjack")
    echo("getting or creating game: ", game.name)

    # Create game Phases ("Play")
    play_phase = games_client.phases.get_or_create(game=game.id, name="Play", order=1)
    echo("getting or creating phase: ", play_phase.name)

    run = games_client.runs.get_or_create(game=game.id, name="default")
    echo("getting or creating run: ", run.name)

    # Reset each RunUser
    for ruser in games_client.runusers.filter(run=run.id):
        echo("  resetting runuser: ", ruser.id)

        for s in games_client.scenarios.filter(runuser=ruser.id):
            games_client.scenarios.delete(s.id)

        new_scenario = games_client.scenarios.get_or_create(
            runuser=ruser.id, name="Scenario 1"
        )

        games_client.periods.create({"scenario": new_scenario.id, "order": 1})

    echo("Completed reseting game: ", game.slug)
