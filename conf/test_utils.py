class RequestIDFilter:
    """Mock filter for tests that provides dummy values for all log record fields"""

    def filter(self, record):
        record.request_id = "test-request-id"
        record.client = "127.0.0.1"
        record.path = "/test/"
        record.user_id = "anonymous"
        record.status_code = 200
        record.response_time = 0.0
        return True


def mock_request_id(get_response):
    """Test utility to mock request ID generation"""

    def middleware(request):
        request.id = "test-request-id"
        return get_response(request)

    return middleware


# Test configuration
RequestIDMiddleware = mock_request_id
