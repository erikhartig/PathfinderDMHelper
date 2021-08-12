import pathlib

BASE_PATH = pathlib.Path(__file__).parent.absolute()
DATA = BASE_PATH / "Data"
PLAYERS = DATA / "players.pkl"
ITEMS = DATA / "items.pkl"
