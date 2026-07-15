from sqlalchemy import create_engine
from sqlalchemy.future import select  
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base 
from api.utils.config import settings
import os                            
from urllib.parse import quote_plus  

# Inside your get_db_url function:
DB_HOST = settings.DB_HOST 
DB_PORT = settings.DB_PORT                
DB_USER = settings.DB_USER
DB_PASSWORD = quote_plus(settings.DB_PASSWORD)          
DB_NAME = settings.DB_NAME
DB_TYPE = settings.DB_TYPE
                              
def get_db_url(test_mode: bool = False):
    if DB_TYPE == "sqlite" or test_mode or os.environ.get("TESTING"):
        BASE_PATH = "sqlite:///./test.db"
        return BASE_PATH

    elif DB_TYPE == "postgresql":
        return f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# **Synchronous Engine (for legacy code)**
if os.environ.get("TESTING"):
    sync_engine = create_engine(get_db_url(test_mode=True))
else:
    sync_engine = create_engine(
        get_db_url(),
        echo=settings.DB_ECHO,
        pool_pre_ping=settings.DB_POOL_PRE_PING,  
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW, 
    )

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=sync_engine
)
db_session = scoped_session(SessionLocal)

# **Asynchronous Engine (for new async code)**
if os.environ.get("TESTING"):
    async_engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:", echo=settings.DB_ECHO
    )
else:
    async_engine = create_async_engine(
        get_db_url().replace("postgresql://", "postgresql+asyncpg://"),
        echo=settings.DB_ECHO,
        pool_pre_ping=settings.DB_POOL_PRE_PING,
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW,
    )

async_session_factory = async_sessionmaker(
    bind=async_engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()
# **Legacy (Sync) Database Dependency**


def get_db():
    db = db_session()
    try:
        yield db 
    finally:
        db.close()

# **New (Async) Database Dependency**


async def get_async_db():
    async with async_session_factory() as session:
        try:
            yield session 
        finally:
            await session.close()


async def check_database_connection(db: AsyncSession):
    try:
        await db.execute(select(1))
        return True
    except Exception as e:
        print(f"Error checking database connection: {e}")
        return False