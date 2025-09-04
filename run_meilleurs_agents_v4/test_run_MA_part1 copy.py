from playwright.async_api import async_playwright
import asyncio, random

async def human_scrape():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
            headless=False
        )
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("https://www.meilleursagents.com/prix-immobilier/")

        # Pause pour “observer”
        await asyncio.sleep(random.uniform(2, 5))

        # Trouver l’input
        input_box = page.locator("input[name='q']")
        await input_box.wait_for(state="visible")

        # Simuler mouvement souris vers l’input
        box = await input_box.bounding_box()
        await page.mouse.move(box['x'] + box['width']/2, box['y'] + box['height']/2, steps=15)
        await asyncio.sleep(random.uniform(0.5, 1.5))
        await page.mouse.click(box['x'] + box['width']/2, box['y'] + box['height']/2)

        # Typing humain
        city = "Paris (75000)"
        for char in city:
            await page.keyboard.type(char, delay=random.randint(50, 120))
        await page.keyboard.press("Enter")

        # Scroll naturel
        for _ in range(random.randint(3, 7)):
            await page.evaluate(f"window.scrollBy(0, {random.randint(100,300)})")
            await asyncio.sleep(random.uniform(0.5, 1.5))

        # Pause finale
        await asyncio.sleep(random.uniform(3, 6))
        await browser.close()

asyncio.run(human_scrape())
