import os
from fastapi import Request, HTTPException, status
from constants import X_PROCESS_TIME_KEY
from dotenv import load_dotenv
from utils import get_processing_time
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime, timedelta

env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', '.env')
load_dotenv(dotenv_path=env_path)

RATE_LIMIT_DURATION_MINUTES = os.getenv("RATE_LIMIT_DURATION_MINUTES")
RATE_LIMIT_REQUESTS_COUNT = os.getenv("RATE_LIMIT_REQUESTS_COUNT")

class X_Process_Time_Middleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = datetime.utcnow()
        response = await call_next(request)
        response.headers[X_PROCESS_TIME_KEY] = get_processing_time(start_time)
        return response

class RateLimitingMiddleware(BaseHTTPMiddleware):

    def __init__(self, app):
        self._RATE_LIMIT_DURATION = timedelta(minutes=int(RATE_LIMIT_DURATION_MINUTES))
        self._RATE_LIMIT_REQUESTS = int(RATE_LIMIT_REQUESTS_COUNT)
        super().__init__(app)
        
        self._request_counts = {}

    async def dispatch(self, request, call_next):
        client_ip = request.client.host

        request_count, last_request = self._request_counts.get(client_ip, (0, datetime.min))

        elapsed_time = datetime.utcnow() - last_request

        if elapsed_time > self._RATE_LIMIT_DURATION:
            request_count = 0
        else:
            if request_count > self._RATE_LIMIT_REQUESTS:
                return HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=f"Rate limit exceeded. Please try again later. Number of hits: {request_count}")
            request_count += 1

        self._request_counts[client_ip] = (request_count, datetime.now())

        response = await call_next(request)
        return response