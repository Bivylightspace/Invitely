from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

from api.db.db import engine, session_local

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    events = relationship("Event", back_populates="owner", cascade="all, delete-orphan")


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(String(500), nullable=True)
    date = Column(DateTime, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="events")
    invitations = relationship("Invitation", back_populates="event", cascade="all, delete-orphan")


class Invitation(Base):
    __tablename__ = "invitations"

    id = Column(Integer, primary_key=True)
    email = Column(String(100), nullable=False)
    status = Column(String(20), nullable=False, default="pending")
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)

    event = relationship("Event", back_populates="invitations")


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def seed():
    db = session_local()

    try:
        db.query(Invitation).delete()
        db.query(Event).delete()
        db.query(User).delete()
        db.commit()

        user = User(
            name="Stephen",
            email="stephen@gmail.com",
            password="password123",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        event = Event(
            title="Wedding Party",
            description="Stephen wedding celebration",
            date=datetime(2026, 1, 10),
            owner_id=user.id,
        )
        db.add(event)
        db.commit()
        db.refresh(event)

        invitations = [
            Invitation(email=f"guest{i}@example.com", status="pending", event_id=event.id)
            for i in range(1, 6)
        ]

        db.add_all(invitations)
        db.commit()

    except Exception as exc:
        db.rollback()
        raise RuntimeError(f"Seed failed: {exc}") from exc

    finally:
        db.close()


if __name__ == "__main__":
    seed()
