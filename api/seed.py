from app.database import SessionLocal, engine
from app import models
from datetime import datetime

# Create tables (only needed once)
models.Base.metadata.create_all(bind=engine)

def seed():
    db = SessionLocal()

    try:
        #  one user
        user = models.User(
            name="Stephen",
            email="Stephen@.com",
            password="password123"  
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        #  Create one event
        event = models.Event(
            title="Wedding_Party",
            description="Stephen Wedding celebration",
            date=datetime(2026, 1, 10),
            owner_id=user.id
        )
        db.add(event)
        db.commit()
        db.refresh(event)

        #  five invitations
        invitations = [
            models.Invitation(
                email=f"guest{i}@example.com",
                event_id=event.id,
                status="pending"
            )
            for i in range(1, 6)
        ]

        db.add_all(invitations)
        db.commit()

        print("successfully!")

    except Exception as e:
        db.rollback()
        print("failed:", e)

    finally:
        db.close()


if __name__ == "__main__":
    seed()
