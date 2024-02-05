from logger import logger
import json
from fastapi.responses import JSONResponse
from fastapi import HTTPException

def send_response(content=None, status_code=None, error_tag=False):
    try:
        if content is None or status_code is None:
            raise Exception("content and status_code must be present")
        
        if error_tag:
            raise Exception(content)
    
        logger.log(f"SUCCESSFUL: Status Code: {status_code} with Response: {content}")
        
        if isinstance(content, dict):
            return JSONResponse(content=json.dumps(content), status_code=status_code)
        
        return JSONResponse(content = json.dumps(content.dict(), indent=4, sort_keys=True, default=str), status_code=status_code)
    except Exception as e:
        detail = f"Some error has occurred. Status Code: {status_code} with Response: {content} and Error: {e}"
        logger.log(detail, error_tag=True)
        raise HTTPException(status_code=status_code, detail=detail)