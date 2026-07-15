from seed import seed
from api.db.db import session_local
from api.v1.model import User, Event, Invitation 


def test_seed_creates_expected_data():
    
    seed()

    db = session_local()

    try:
        users = db.query(User).all()
        events = db.query(Event).all()
        invitations = db.query(Invitation).all()

        # Assertions
        assert len(users) == 1
        assert users[0].email == "stephen@gmail.com"

        assert len(events) == 1
        assert events[0].title == "Wedding Party"

        assert len(invitations) == 5

    finally:
        db.close()
