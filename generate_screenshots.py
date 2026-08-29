import asyncio
from playwrite.async_api import async_playwright
import os

urls = [
    ("http://localhost:8080/ServletDemo/index.html", "screenshot_index.png"),
    ("http://localhost:8080/ServletDemo/hello", "screenshot_hello.png"),
    ("http://localhost:8080/ServletDemo/date", "screenshot_date.png"),
    ("http://localhost:8080/ServletDemo/welcome?username=Rahul", "screenshot_welcome.png"),
]

async def capture():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1024, "height": 768})
        for url, fname in urls:
            await page.goto(url)
            await page.wait_for_timeout(500)
            await page.screenshot(path=fname)
            print(f"Saved {fname}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture())