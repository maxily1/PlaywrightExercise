from utils.price_utils import parse_price
from pages.base_page import BasePage
import allure
from allure_commons.types import AttachmentType

class SearchPage(BasePage):
    def search(self, query: str):
        allure.attach(f"Search query: {query}", name="Query", attachment_type=AttachmentType.TEXT)
        search_bar = self.page.locator("input[aria-label='Search for anything']")
        search_bar.fill(query)
        self.page.keyboard.press("Enter")
        self.page.wait_for_load_state("networkidle")

    def apply_max_price_filter(self, max_price: int):
        """Apply max price filter using the sidebar filter"""
        try:
            allure.attach(f"Max price: {max_price} ILS", name="Price Filter", attachment_type=AttachmentType.TEXT)
            
            # Wait for the price filter section to load
            self.page.wait_for_selector("input[aria-label*='Maximum Value']", timeout=10000)
            
            # Fill the max price input
            max_price_input = self.page.locator("input[aria-label*='Maximum Value']")
            max_price_input.fill(str(max_price))
            
            # Press Tab to move focus away and enable the button
            self.page.keyboard.press("Tab")
            
            # Wait for button to become enabled
            self.page.wait_for_timeout(500)
            
            # Click the submit button
            submit_button = self.page.locator("button[aria-label='Submit price range']")
            submit_button.click()
            
            # Wait for results to update
            self.page.wait_for_load_state("networkidle")
            
            allure.attach(
                self.page.screenshot(full_page=True),
                name="After Price Filter Applied",
                attachment_type=AttachmentType.PNG
            )
            
        except Exception as e:
            allure.attach(f"Error applying price filter: {str(e)}", 
                         name="Filter Error", 
                         attachment_type=AttachmentType.TEXT)
            print(f"Could not apply price filter via UI: {e}")
            print("Falling back to URL-based filtering...")
            current_url = self.page.url
            if "_udhi=" not in current_url:
                separator = "&" if "?" in current_url else "?"
                new_url = f"{current_url}{separator}_udhi={max_price}"
                self.page.goto(new_url)
                self.page.wait_for_load_state("networkidle")

    def collect_item_urls_under_price(self, max_price: int, limit: int):
        urls = []
        page_count = 0
        max_pages = 5
        
        collected_items_details = []
        
        while len(urls) < limit and page_count < max_pages:
            page_count += 1
            
            try:
                self.page.wait_for_selector("li.s-card", timeout=10000)
            except:
                print(f"No items found on page {page_count}")
                break
            
            items = self.page.locator("li.s-card").all()
            print(f"Found {len(items)} items on page {page_count}")

            for item in items:
                if len(urls) >= limit:
                    break
                
                try:
                    # Get item price
                    price_locator = item.locator(".s-card__price").first
                    
                    if price_locator.count() > 0 and price_locator.is_visible():
                        price_text = price_locator.inner_text()
                        item_price = parse_price(price_text)
                        
                        if not item_price:
                            continue
                        
                        # Get shipping cost
                        shipping_price = 0
                        try:
                            shipping_locator = item.locator("span:has-text('delivery'), span:has-text('shipping')").first
                            if shipping_locator.count() > 0:
                                shipping_text = shipping_locator.inner_text()
                                shipping_price = parse_price(shipping_text)
                                
                                if not shipping_price:
                                    if "free" in shipping_text.lower():
                                        shipping_price = 0
                                    else:
                                        shipping_price = 0
                        except Exception as e:
                            shipping_price = 0
                        
                        # Calculate total price
                        total_price = item_price + shipping_price
                        
                        print(f"Item price: {item_price}, Shipping: {shipping_price}, Total: {total_price}")
                        
                        if total_price <= max_price:
                            # Get the link
                            all_links = item.locator("a[href*='/itm/']").all()
                            
                            for link in all_links:
                                url = link.get_attribute("href")
                                
                                if url and "/itm/" in url:
                                    if url.startswith("http"):
                                        clean_url = url.split("?")[0]
                                        
                                        if self._is_valid_ebay_url(clean_url) and clean_url not in urls:
                                            print(f"✓ Adding: {clean_url} (item: {item_price}, shipping: {shipping_price}, total: {total_price})")
                                            urls.append(clean_url)
                                            
                                            collected_items_details.append({
                                                "url": clean_url,
                                                "item_price": item_price,
                                                "shipping_price": shipping_price,
                                                "total_price": total_price
                                            })
                                            break
                        else:
                            print(f"✗ Skipping: total price {total_price} exceeds budget {max_price}")
                            
                except Exception as e:
                    print(f"Error processing item: {e}")
                    continue

            # Paging Logic
            if len(urls) < limit:
                try:
                    next_btn = self.page.locator("a.pagination__next")
                    
                    if next_btn.count() > 0 and next_btn.is_visible():
                        is_disabled = next_btn.get_attribute("aria-disabled")
                        if is_disabled != "true":
                            print(f"Going to next page...")
                            next_btn.click()
                            self.page.wait_for_load_state("networkidle")
                        else:
                            print("Next button is disabled")
                            break
                    else:
                        print("No next button found")
                        break
                except Exception as e:
                    print(f"Pagination error: {e}")
                    break
        
        print(f"Collected {len(urls)} URLs total")
        
        # Attach collected items details to Allure
        import json
        allure.attach(
            json.dumps(collected_items_details, indent=2),
            name="Collected Items Details",
            attachment_type=AttachmentType.JSON
        )
        
        return urls

    def _is_valid_ebay_url(self, url: str) -> bool:
        """Validate that the URL is a real eBay item URL"""
        import re
        
        if "www.ebay.com" not in url:
            return False
        
        match = re.search(r'/itm/(\d+)', url)
        if not match:
            return False
        
        item_id = match.group(1)
        
        invalid_ids = ['123456', '000000', '111111', '999999']
        if item_id in invalid_ids:
            return False
        
        if len(item_id) < 10:
            return False
        
        return True