import json
from logger import logger
from datetime import datetime
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from exceptions.exceptions import Missing_Params
from constants import JSON_RESPONSE_INDENT, JSON_RESPONSE_SORT_KEYS, JSON_RESPONSE_DEFAULT

def get_processing_time(start_time: datetime = None):
    if not start_time:
        raise Missing_Params

    return str(datetime.utcnow() - start_time)

def send_response(content=None, status_code=None, error_tag=False):
    try:
        if content is None or status_code is None:
            raise Exception("content and status_code must be present")
        
        if error_tag:
            raise Exception(content)
        
        if not isinstance(content, dict):
            content= content.dict()
        
        logger.log(f"SUCCESSFUL: Status Code: {status_code} with Response: {content}")
        
        return JSONResponse(content = json.dumps(content, indent=JSON_RESPONSE_INDENT, sort_keys=JSON_RESPONSE_SORT_KEYS, default=JSON_RESPONSE_DEFAULT), status_code=status_code)
    
    except Exception as e:
        logger.log(content, error_tag=True)
        raise HTTPException(status_code=status_code, detail=str(e))