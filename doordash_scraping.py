import asyncio
import time
import os
import math
from dotenv import load_dotenv

from scrapybara import Scrapybara
from undetected_playwright.async_api import async_playwright

# loading in .env file
load_dotenv()
SCRAPYBARA_API_KEY = os.getenv("SCRAPYBARA_API_KEY")

async def get_scrapybara_browser():
    client = Scrapybara(api_key=SCRAPYBARA_API_KEY)
    instance = client.start_browser()
    return instance

async def setup_address(page):
    """
    1. Setup Address
    """
    # click -> data-testid="addressTextButton"
    # await page.wait_for_selector('[data-testid="addressTextButton"]', state="visible")
    await page.locator('[data-testid="addressTextButton"]').click()
    await page.screenshot(path=f"screenshots/checkpoint.png")
    print("step 1")

    # input San Francisco, CA -> data-testid="AddressAutocompleteField"
    # await page.wait_for_selector('[data-testid="AddressAutocompleteField"]', state="visible")
    await page.get_by_test_id("AddressAutocompleteField").first.fill("San Francisco, CA")
    await page.screenshot(path=f"screenshots/checkpoint.png")
    print("step 2")

    # select -> data-testid="AddressAutocompleteSuggestion-0"
    await page.screenshot(path=f"screenshots/checkpoint.png")
    # await page.wait_for_selector('[data-testid="AddressAutocompleteSuggestion-0"]', state="visible")
    # await page.locator('[data-testid="AddressAutocompleteSuggestion-0"]').click()
    await page.keyboard.press("Enter")
    await page.screenshot(path=f"screenshots/checkpoint.png")
    print("step 3")

    # click -> data-anchor-id="AddressEditSave"
    # await page.wait_for_selector('[data-anchor-id="AddressEditSave"]', state="visible")
    await page.locator('[data-anchor-id="AddressEditSave"]').click()
    await page.screenshot(path=f"screenshots/checkpoint.png")
    print("step 4")

    # escape you are outside this area modal
    # await page.screenshot(path=f"screenshots/checkpoint.png")
    await page.wait_for_timeout(1500)
    await page.keyboard.press("Escape")
    await page.screenshot(path=f"screenshots/checkpoint.png")
    print("step 5")

    print("ADDRESS SETUP COMPLETE")

async def process_section(page, section_id, start_y, seen_items):
    """
    3. Process Menu Items
    """
    print(f"starting to process section: {section_id}")
    await page.evaluate(f"window.scrollTo(0, {start_y})")
    await page.wait_for_timeout(1500)
    await page.screenshot(path=f"screenshots/checkpoint.png")
    print("scrolled to correct section")
    
    # find menu items
    items = await page.locator('[data-anchor-id="MenuItem"]').all()
    print(f"found {len(items)} items in section {section_id}")
    
    item_count = 0
    for item in items:
        try:
            item_name = await item.text_content()
            if item_name and item_name not in seen_items:
                await item.click()
                await page.screenshot(path=f"screenshots/section_{section_id}_item_{item_count}.png")

                # Close modal with ESC key
                await page.keyboard.press("Escape")
                await page.wait_for_timeout(500)
                item_count += 1
        except Exception as e:
            print(f"Viewport {section_id}: Error processing item: {e}")
    
    print(f"FINISHED PROCESSING SECTION: {section_id}")

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
    seen_items = set()

    # start timer
    start_time = time.time()

    cdp_url = instance.get_cdp_url().cdp_url
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(cdp_url)
        page = await browser.new_page()
        
        # load page
        await page.goto(start_url)
        await page.wait_for_load_state("networkidle")
        print("page loaded")
        
        # set up address
        await setup_address(page)
        
        # get section dimensions
        total_height = await page.evaluate("document.body.scrollHeight")
        viewport_height = await page.evaluate("window.innerHeight")
        sections = math.ceil(total_height / viewport_height)
        print(f"section height: {viewport_height}px / total height: {total_height}px, ")
        print(f"dividing page into {sections} sections")

        # set up response listener
        async def response_handler(response):            
            if response.request.url == "https://www.doordash.com/graphql/itemPage?operation=itemPage":
                try:
                    json_data = await response.json()
                    item_name = json_data["data"]["itemPage"]["itemHeader"]["name"]
                    if item_name not in seen_items:
                        print(item_name)
                        seen_items.add(item_name)
                        menu_items.append(json_data)
                except:
                    print(f"Failed to parse JSON response")

        # set up listener
        page.on("response", response_handler)
        print(f"set up listener")
        
        # process sections
        print("starting to process sections")
        
        for i in range(sections):
            start_y = i * viewport_height
            await process_section(page, i, start_y, seen_items)
        
        # track time taken
        total_time = time.time() - start_time
        print(f"total execution time: {total_time:.2f} seconds")
    
    print(f"Total unique menu items found: {len(menu_items)}")
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