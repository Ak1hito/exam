from datetime import datetime
from pathlib import Path

from django.conf import settings


class RequestMetricsMiddleware:
    total = 0
    status_2xx = 0
    status_4xx = 0
    status_5xx = 0

    def __init__(self, get_response):
        self.get_response = get_response
        self.log_path = Path(settings.BASE_DIR) / "metrics.log"

    def __call__(self, request):
        response = self.get_response(request)
        self.__class__.total += 1

        if 200 <= response.status_code < 300:
            self.__class__.status_2xx += 1
        elif 400 <= response.status_code < 500:
            self.__class__.status_4xx += 1
        elif 500 <= response.status_code < 600:
            self.__class__.status_5xx += 1

        line = (
            f"{datetime.now():%Y-%m-%d %H:%M:%S} "
            f"requests_total={self.total} "
            f"responses_2xx={self.status_2xx} "
            f"responses_4xx={self.status_4xx} "
            f"responses_5xx={self.status_5xx}"
        )
        print(line)
        with self.log_path.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")
        return response
