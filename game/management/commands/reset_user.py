import djclick as click

from modelservice.simpl.sync import games_client


def echo(text, value):
    click.echo(click.style(text, fg="green") + "{0}".format(value))


@click.command()
@click.option("--pk", help="Simpl API User PK")
@click.option("--email", help="Simpl API User Email")
def command(pk, email):
    """
    Reset a user by PK or Email address
    This will remove the User's Scenarios from the one default Run
    and create new empty Scenarios and Periods for them.
    """
    if not pk and not email:
        click.secho(
            "ERROR: You must provide a --pk or --email to find the user", fg="red"
        )
        return

    echo("Resetting game: ", "Blackjack")

    # Get or create the Game
    game = games_client.games.get_or_create(name="Blackjack", slug="blackjack")
    echo("getting or creating game: ", game.name)

    # Get or create the Run
    run = games_client.runs.get_or_create(game=game.id, name="default")
    echo("getting or creating run: ", run.name)

    # Find the user
    if pk:
        user = games_client.users.get(pk=pk)
    else:
        user = games_client.users.get(email=email)

    # Get the RunUser
    run_user = games_client.runusers.get(user=user.id)

    # Reset each RunUser
    for s in games_client.scenarios.filter(runuser=run_user.id):
        games_client.scenarios.delete(s.id)

    new_scenario = games_client.scenarios.get_or_create(
        runuser=run_user.id, name="Scenario 1"
    )

    games_client.periods.create({"scenario": new_scenario.id, "order": 1})

    echo("Completed reseting user: ", user.email)
