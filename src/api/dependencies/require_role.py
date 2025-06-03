import jwt 
import os
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()

def require_role(require_role: str):
    async def role_checker(credentials: HTTPAuthorizationCredentials = Depends(security)):
        token = credentials.credentials
        try:
            payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
            user_role = payload.get("role")
            
            if user_role != require_role:
                raise HTTPException(status_code=403, detail=f"User doesn`t have required role: {require_role}")
            
            return {"role": user_role}
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
    return role_checker