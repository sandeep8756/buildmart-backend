import httpx

from utils.common import parse_json_response


async def fetch_get(url: str, headers: dict | None = None) -> tuple[int, str]:
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url, headers=headers or {})
        return response.status_code, response.text


async def fetch_post(
    url: str, headers: dict | None = None, body: str | None = None
) -> tuple[int, str]:
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(url, headers=headers or {}, content=body)
        return response.status_code, response.text


async def fetch_json_get(url: str, headers: dict | None = None) -> tuple[int, dict]:
    status, raw = await fetch_get(url, headers)
    return status, parse_json_response(raw)
