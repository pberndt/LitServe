from litserve.api import LitAPI
import csv
from io import StringIO


class CSVEchoAPI(LitAPI):
    """Simple API that echoes CSV input."""

    def setup(self, device):
        pass

    def decode_request(self, request):
        reader = csv.reader(StringIO(request))
        return [row for row in reader]

    def predict(self, rows):
        return rows

    def encode_response(self, output):
        return output
