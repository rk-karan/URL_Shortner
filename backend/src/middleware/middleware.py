import time
from fastapi import Request
from constants import X_PROCESS_TIME_KEY
from utils import get_processing_time
from starlette.middleware.base import BaseHTTPMiddleware

class X_Process_Time_Middleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        response.headers[X_PROCESS_TIME_KEY] = get_processing_time(start_time)
        return response