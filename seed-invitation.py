import random

from api.db.db import SessionLocal
from api.v1.models import User, Event, Invitation

NUMBER_OF_INVITATIONS = 100
MIN_INVITEES = 1
MAX_INVITEES = 10


def seed_invitations():
    db = SessionLocal()

    users = db.query(User).all()
    events = db.query(Event).all()

    if len(users) < MAX_INVITEES:
        print(" Not enough users to generate varied invitations.")
        return

    if not events:
        print(" No events found.")
        return

    for i in range(NUMBER_OF_INVITATIONS):

        inviter = random.choice(users)
        event = random.choice(events)

        number_of_invitees = random.randint(MIN_INVITEES, MAX_INVITEES)
        
        possible_invitees = [u for u in users if u.id != inviter.id]

        invitees = random.sample(
            possible_invitees,
            k=min(number_of_invitees, len(possible_invitees))
        )

        invitation = Invitation(
            event_id=event.id,
            invitation_id=inviter.id,
        )

        db.add(invitation)
        db.flush()  

        invitation.invitees.extend(invitees)

    db.commit()
    db.close()

    print(f"Successfully created {NUMBER_OF_INVITATIONS} invitations.")


if __name__ == "__main__":
    seed_invitations()