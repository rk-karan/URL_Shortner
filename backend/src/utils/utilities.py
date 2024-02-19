from logger import logger
import json
import time
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from exceptions.exceptions import Missing_Params

def get_processing_time(start_time):
    if not start_time:
        raise Missing_Params

    return str(time.time() - start_time)

def send_response(content=None, status_code=None, error_tag=False):
    try:
        if content is None or status_code is None:
            raise Exception("content and status_code must be present")
        
        if error_tag:
            raise Exception(content)
        
        if not isinstance(content, dict):
            content= content.dict()
        
        logger.log(f"SUCCESSFUL: Status Code: {status_code} with Response: {content}")
        
        return JSONResponse(content = json.dumps(content, indent=4, sort_keys=True, default=str), status_code=status_code)
    
    except Exception as e:
        logger.log(content, error_tag=True)
        raise HTTPException(status_code=status_code, detail=str(e))