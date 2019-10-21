import djclick as click

from modelservice.simpl.sync import games_client


def echo(text, value):
    click.echo(click.style(text, fg="green") + "{0}".format(value))


def delete_default_run(games_client):
    """ Delete default Run """
    echo("Resetting the Blackjack game default run...", " done")
    game = games_client.games.get_or_create(slug="blackjack")
    runs = games_client.runs.filter(game=game.id)
    for run in runs:
        if run.name == "default":
            games_client.runs.delete(run.id)


@click.command()
@click.option(
    "--reset",
    default=False,
    is_flag=True,
    help="Delete default game run and recreate it from scratch",
)
def command(reset):
    """
    Create and initialize Blackjack game.
    Create a "default" Blackjack run.
    Set the run phase to "Play".
    Add 1 player "demo@example.com" with password "demo"
    Add a scenario and period 1 for each player.
    """

    # Handle resetting the game
    if reset:
        if click.confirm(
            "Are you sure you want to delete the default game run and recreate from scratch?"
        ):
            delete_default_run(games_client)

    # Create a Game
    game = games_client.games.get_or_create(name="Blackjack", slug="blackjack")
    echo("getting or creating game: ", game.name)

    # Create game Phases ("Play")
    play_phase = games_client.phases.get_or_create(game=game.id, name="Play", order=1)
    echo("getting or creating phase: ", play_phase.name)

    run = games_client.runs.get_or_create(game=game.id, name="default")
    echo("getting or creating run: ", run.name)

    # Set run to phase
    run.phase = phase.id
    run.save()
    echo("setting run to phase: ", phase.name)

    player = games_client.users.get_or_create(
        password="demo",
        first_name="Blackjack",
        last_name="Demo",
        email="demo@example.com",
    )
    echo("getting or creating user: ", player.email)

    runuser = games_client.runusers.get_or_create(
        user=player.id, run=run.id, leader=True
    )

    scenario = games_client.scenarios.get_or_create(
        runuser=runuser.id, name="Scenario 1"
    )
    click.echo(
        "getting or creating runuser {} scenario: {}".format(runuser.id, scenario.id)
    )

    period = games_client.periods.get_or_create(scenario=scenario.id, order=1)
    click.echo(
        "getting or creating runuser {} period 1 for scenario: {}".format(
            runuser.id, scenario.id
        )
    )
    echo("Completed setting up run: id=", run.id)
