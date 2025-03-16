import asyncio
import time

from scrapybara import Scrapybara
from undetected_playwright.async_api import async_playwright

# loading in .env file
import os
from dotenv import load_dotenv

# loading API key from .env file
load_dotenv()
SCRAPYBARA_API_KEY = os.getenv("SCRAPYBARA_API_KEY")

async def get_scrapybara_browser():
    client = Scrapybara(api_key=SCRAPYBARA_API_KEY)
    instance = client.start_browser()
    return instance

async def retrieve_menu_items(instance, start_url: str) -> list[dict]:
    """
    :args:
    instance: the scrapybara instance to use
    url: the initial url to navigate to

    :desc:
    this function navigates to {url}. then, it will collect the detailed
    data for each menu item in the store and return it.

    (hint: click a menu item, open dev tools -> network tab -> filter for
            "https://www.doordash.com/graphql/itemPage?operation=itemPage")

    one way to do this is to scroll through the page and click on each menu
    item.

    determine the most efficient way to collect this data.

    :returns:
    a list of menu items on the page, represented as dictionaries
    """
    menu_items = []

    # start timer
    start_time = time.time()

    cdp_url = instance.get_cdp_url().cdp_url
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(cdp_url)
        page = await browser.new_page()

        await page.goto(start_url)

        # browser automation ...
        """
        1. Wait for page to be fully loaded
        """
        await page.wait_for_load_state("networkidle")
        print("page is loaded")

        # in case store is closed
        await page.keyboard.press("Escape")

        """
        2. Set address to San Francisco, CA
        """
        # click -> data-testid="addressTextButton"
        # await page.wait_for_selector('[data-testid="addressTextButton"]', state="visible")
        await page.locator('[data-testid="addressTextButton"]').click()
        await page.screenshot(path=f"screenshots/address_step_1.png")
        print("step 1")

        # input San Francisco, CA -> data-testid="AddressAutocompleteField"
        # await page.wait_for_selector('[data-testid="AddressAutocompleteField"]', state="visible")
        await page.get_by_test_id("AddressAutocompleteField").first.fill("San Francisco, CA")
        await page.screenshot(path=f"screenshots/address_step_2.png")
        print("step 2")

        # select -> data-testid="AddressAutocompleteSuggestion-0"
        await page.wait_for_selector('[data-testid="AddressAutocompleteSuggestion-0"]', state="visible")
        await page.locator('[data-testid="AddressAutocompleteSuggestion-0"]').click()
        await page.screenshot(path=f"screenshots/address_step_3.png")
        print("step 3")

        # click -> data-anchor-id="AddressEditSave"
        # await page.wait_for_selector('[data-anchor-id="AddressEditSave"]', state="visible")
        await page.locator('[data-anchor-id="AddressEditSave"]').click()
        await page.screenshot(path=f"screenshots/address_step_4.png")
        print("step 4")

        print("set up address")
        
        """
        3. Set up response listener
        """
        # handler
        async def response_handler(response):            
            if response.request.url == "https://www.doordash.com/graphql/itemPage?operation=itemPage":
                json_data = await response.json()
                menu_items.append(json_data)

        # listener for responses
        page.on("response", response_handler)

        print("set up listener")

        """
        4. Find menu items and click (tentative)
        """
        seen_items = set()
        item_count = 0

        # in case store is closed
        await page.keyboard.press("Escape")

        while True:
            # find menu items in current frame
            items = await page.locator('[data-anchor-id="MenuItem"]').all()
            print(len(items))

            # process found menu item
            for item in items:
                if item and item not in seen_items:
                    seen_items.add(item)
                    await item.click()

                    print(f"found item: {item_count}")
                    await page.screenshot(path=f"screenshots/menu_item_{item_count}.png")

                    # close modal w/ ESC key
                    await page.keyboard.press("Escape")
                    item_count += 1
                    await page.screenshot(path=f"screenshots/checkpoint.png")

            # update scroll
            current_scroll = await page.evaluate("window.scrollY + window.innerHeight")
            total_scroll_height = await page.evaluate("document.body.scrollHeight")

            # scroll down to lazy load more menu items
            await page.evaluate(f"window.scrollBy(0, {current_scroll})")
            print(current_scroll)

            # if we reach bottom
            if current_scroll >= total_scroll_height:
                break

        # all found menu items
        menu_items = list(seen_items)
        print(f"\n found menu items:\n{len(menu_items)}")

        # track time taken
        total_time = time.time() - start_time
        print(f"total execution time: {total_time:.2f} seconds")

        await browser.close()
    
    print(menu_items)
    return menu_items



async def main():
    instance = await get_scrapybara_browser()

    try:
        await retrieve_menu_items(
            instance,
            "https://www.doordash.com/store/panda-express-san-francisco-980938/12722988/?event_type=autocomplete&pickup=false",
        )
    finally:
        # Be sure to close the browser instance after you're done!
        instance.stop()


if __name__ == "__main__":
    asyncio.run(main())