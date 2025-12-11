from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any


def success_response(
    status_code:int,
     message: str,
     data: Optional[dict] = None
) :

 return JSONResponse( 
    status_code=status_code,
    content={
        "status": "success",
         "status_code": status_code,
         "message": message,
        "data": data 
        }
    )
 
 def auth_responses(
     status_code: int,
     message: str,
     access_token: str,
     refresh_token: str,
     data: Optional[dict] = None
     
 ) :
     
  return JSONResponse(
    status_code=status_code,
     content={
         "status": "success",
         "status_code": status_code,
         "message": message,
         "access_token": access_token,
         "refresh_token": refresh_token,
         "data": data 
        }
  )
  
def fail_response(
    status_code: int,
    message: str,
    data: Optional[Dict] = None
):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "fail",
            "status_code": status_code,
            "message": message,
            "data": data 
        }
    )  