from db import engine
from models import Base

def init():
    print("⏳ Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully")

if __name__ == "__main__":
    init()
