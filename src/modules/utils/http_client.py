import requests
import config
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from log import logError

requests.packages.urllib3.disable_warnings()

# Perform a Sync Request and return response details
def do_sync_request(method, url):
    headers = {"User-Agent": config.userAgent}
    proxies = {"http": config.proxy, "https": config.proxy} if config.proxy else None
    response = requests.request(
        method=method,
        url=url,
        proxies=proxies,
        timeout=config.timeout,
        verify=False,
        headers=headers
    )
    parsedData = None
    try:
        parsedData = response.json()
    except Exception as e:
        if config.verbose:
            config.console.print(f"  ❌ Error in Sync HTTP Request [{method}] {url}")
        logError(e, f"Error in Sync HTTP Request [{method}] {url}")
    if config.verbose:
        config.console.print(f"  🆗 Sync HTTP Request completed [{method} - {response.status_code}] {url}")
    return response, parsedData


# Perform an Async Request and return response details
async def do_async_request(method, url, session):
    headers = {"User-Agent": config.userAgent}
    proxy = config.proxy if config.proxy else None
    try:
        response = await session.request(
            method,
            url,
            proxy=proxy,
            timeout=config.timeout,
            allow_redirects=True,
            ssl=False,
            headers=headers
        )

        content = await response.text()
        responseData = {
            "url": url,
            "status_code": response.status,
            "headers": response.headers,
            "content": content,
        }
        if config.verbose:
            config.console.print(f"  🆗 Async HTTP Request completed [{method} - {response.status}] {url}")
        return responseData
    except Exception as e:
        if config.verbose:
            config.console.print(f"  ❌ Error in Async HTTP Request [{method}] {url}")
        logError(e, f"Error in Async HTTP Request [{method}] {url}")
        return None