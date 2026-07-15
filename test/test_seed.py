import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from seed import Event, Invitation, User, seed
from api.db.db import session_local


def test_seed_creates_expected_data():
    seed()

    db = session_local()
    try:
        users = db.query(User).all()
        events = db.query(Event).all()
        invitations = db.query(Invitation).all()

        assert len(users) == 1
        assert users[0].email == "stephen@gmail.com"

        assert len(events) == 1
        assert events[0].title == "Wedding Party"

        assert len(invitations) == 5
    finally:
        db.close()
