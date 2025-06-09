from io import StringIO
import csv
from fastapi import Response

from litserve.api import LitAPI


class CSVEchoAPI(LitAPI):
    def setup(self, device):
        self.model = lambda rows: rows

    def decode_request(self, request: str):
        return list(csv.reader(StringIO(request)))

    def predict(self, rows):
        return self.model(rows)

    def encode_response(self, output) -> Response:
        buf = StringIO()
        csv.writer(buf).writerows(output)
        return Response(content=buf.getvalue(), media_type="text/csv")
