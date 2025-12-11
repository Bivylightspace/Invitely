from sqlalchemy import create_engine
from supabase import create_client, Client
import os 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



URL = os.getenv("https://quuvbchjhlseucxqqgcn.supabase.co")
KEY = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF1dXZiY2hqaGxzZXVjeHFxZ2NuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM5NzgyNDYsImV4cCI6MjA3OTU1NDI0Nn0.9JIrsWl5RmFCTtiLjN6skyI1P0JxLnsRjscwOi54F2k")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)



URL = "sqlite:///./invitation_app.db" 

engine = create_engine(URL, connect_args={"check_same_thread": False})
Session = sessionmaker(autocommit=True, autoflush=False, bind=engine)
Base  = declarative_base()

def get_db():
    db = Session()
    try: 
        yield db
    finally:
        db.close()
