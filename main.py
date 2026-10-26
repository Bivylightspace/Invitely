from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from api.db.database import check_database_connection, get_async_db
from api.utils.responses import success_response
from api.v1.routes import api_version_one

app = FastAPI()

origins = [
    "https://inviteme.name.ng",
    "https://www.inviteme.name.ng",
    "http://localhost:3000",
]

# Regex to match your specific Vercel project deployment subdomains
vercel_regex = r"^https://inviteme(-[a-zA-Z0-9-]+)?\.vercel\.app$"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=vercel_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_version_one)


@app.get("/")
def home():
    return {"message": "Hello from Invitely!"}


@app.get("/health")
async def health(db: AsyncSession = Depends(get_async_db)):
    """Health check: verifies app is running and database connection is available."""
    db_ok = await check_database_connection(db)
    return success_response(
        status_code=200,
        message=(
            "API is healthy and database connection is successful."
            if db_ok
            else "API is healthy but database connection failed."
        ),
        data={"database_connection": db_ok},
    )
