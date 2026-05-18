import time 
import logging

logger = logging.getLogger(__name__)

class PerformanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        end_time = time.time()
        response_time = end_time - start_time
        logger.info(f"API Request | Method: {request.method} | Path: {request.path} | Duration: {response_time:.3f}s | Response Size: {len(response.content)} bytes")
        return response

