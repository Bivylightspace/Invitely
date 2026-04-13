from fastapi import FastAPI, Depends, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession    
from api.v1.routes import api_version_one    
from api.db.database import get_async_db, check_database_connection
from api.utils.responses import success_response

 
app = FastAPI()  
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
        message="API is healthy and database connection is successful." if db_ok else "API is healthy but database connection failed.",
        data={"database_connection": db_ok}
    )
    