from envirogen import (
    Bot,
    EnviroGenApp,
    Environment,
    Obstacle,
    Plant,
    ScenarioConfig,
)


def test_public_api_imports() -> None:
    env = Environment(width=100, height=100, seed=1)
    bot = env.add_bot(Bot(x=10, y=10))
    plant = env.add_plant(Plant(x=20, y=20))
    obstacle = env.add_obstacle(Obstacle(x=40, y=40, width=10, height=10))

    assert bot.id is not None
    assert plant.id is not None
    assert obstacle.id is not None
    assert ScenarioConfig(name="smoke").name == "smoke"


def test_app_instantiation_does_not_create_tk_root() -> None:
    app = EnviroGenApp(Environment(width=120, height=90, seed=2))

    assert app.root is None
    assert app.env.width == 120

