import httpx

from utils.decorators_async import async_log_pre_post, exception_handler


@async_log_pre_post
@exception_handler
async def fetch_get(url: str, headers: dict | None = None) -> tuple[int, str]:
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url, headers=headers or {})
        return response.status_code, response.text


@async_log_pre_post
@exception_handler
async def fetch_post(
    url: str, headers: dict | None = None, body: str | None = None
) -> tuple[int, str]:
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(url, headers=headers or {}, content=body)
        return response.status_code, response.text
