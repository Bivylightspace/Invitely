from api.db.db import session_local, engine
import models # type: ignore
from datetime import datetime



models.Base.metadata.create_all(bind=engine)


def seed():
    db = session_local()

    try:
        
        db.query(models.Invitation).delete()
        db.query(models.Event).delete()
        db.query(models.User).delete()
        db.commit()

        user = models.User(
            name="Stephen",
            email="stephen@gmail.com",
            password="password123"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
 
        # Create one event
        event = models.Event(
            title="Wedding Party",
            description="Stephen wedding celebration",
            date=datetime(2026, 1, 10),
            owner_id=user.id
        )
        db.add(event)
        db.commit()
        db.refresh(event)

        # Create five invitations
        invitations = [
            models.Invitation(
                email=f"guest{i}@example.com",
                status="pending",
                event_id=event.id
            )
            for i in range(1, 6)
        ]

        db.add_all(invitations)
        db.commit()

        print("Seed completed successfully!")

    except Exception as e:
        db.rollback()
        print("Seed failed:", e)

    finally:
        db.close()


if __name__ == "__main__":
    seed()
