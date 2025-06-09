from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient

from litserve import LitServer
from litserve.utils import wrap_litserve_start
from litserve.test_examples import CSVEchoAPI


import pytest


@pytest.mark.asyncio
async def test_csv_with_encodings():
    server = LitServer(CSVEchoAPI(), accelerator="cpu")
    with wrap_litserve_start(server) as server:
        async with LifespanManager(server.app) as manager, AsyncClient(
            transport=ASGITransport(app=manager.app), base_url="http://test"
        ) as ac:
            csv_data = "a,b\nc,d\n"
            resp = await ac.post(
                "/predict",
                content=csv_data.encode("utf-8"),
                headers={"Content-Type": "text/csv; charset=utf-8"},
            )
            assert resp.json() == [["a", "b"], ["c", "d"]]

            csv_data_iso = "ä,ö\nü,ß\n".encode("iso-8859-15")
            resp = await ac.post(
                "/predict",
                content=csv_data_iso,
                headers={"Content-Type": "text/csv; charset=iso-8859-15"},
            )
            assert resp.json() == [["ä", "ö"], ["ü", "ß"]]
