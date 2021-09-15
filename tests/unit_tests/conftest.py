import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

from Core import player
from Core.player import set_engine


# from Core import misc
# from Core.misc import set_engine


@pytest.fixture()
def session():
    if os.path.exists("test.db"):
        os.remove("test.db")
    engine = create_engine('sqlite:///test.db', connect_args={"check_same_thread": False}, poolclass=StaticPool,
                           echo=True)
    set_engine(engine)
    return player.Session
