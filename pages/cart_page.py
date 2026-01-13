from utils.price_utils import parse_price
from pages.base_page import BasePage

class CartPage(BasePage):
    def open(self):
        self.page.goto("https://cart.ebay.com")
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_timeout(2000)  # Wait for cart to fully load

    def get_total(self):
        """Get the cart subtotal (item + shipping total)"""
        try:
            # Wait for cart summary to load
            self.page.wait_for_selector(".cartsummary", timeout=10000)
            
            # Get the subtotal (this includes items + shipping)
            subtotal_element = self.page.locator("[data-test-id='SUBTOTAL']")
            
            if subtotal_element.count() > 0 and subtotal_element.is_visible():
                subtotal_text = subtotal_element.inner_text()
                total = parse_price(subtotal_text)
                
                if total:
                    print(f"Cart subtotal: {total} ILS")
                    return total
            
            # Fallback: try other selectors
            print("Primary selector failed, trying alternatives...")
            
            alternative_selectors = [
                ".total-row [data-test-id='SUBTOTAL']",
                "div.total-row .val-col",
                ".cart-summary-line-item .total-row",
            ]
            
            for selector in alternative_selectors:
                try:
                    element = self.page.locator(selector).last  # Get last total row
                    if element.count() > 0:
                        text = element.inner_text()
                        total = parse_price(text)
                        if total:
                            print(f"Found total via '{selector}': {total}")
                            return total
                except:
                    continue
            
            # If still not found, take screenshot and raise error
            print("ERROR: Could not find cart total")
            self.page.screenshot(path="debug_cart_total_not_found.png")
            raise Exception("Could not find cart total on page")
            
        except Exception as e:
            print(f"Error getting cart total: {e}")
            self.page.screenshot(path="error_cart_total.png")
            raise
    
    def get_item_count(self):
        """Get the number of items in cart"""
        try:
            # Look for "Item (X)" text
            item_count_element = self.page.locator("[data-test-id='ITEM_TOTAL']")
            if item_count_element.count() > 0:
                # This will give us the item price, but we can count items differently
                pass
            
            # Alternative: count cart items
            cart_items = self.page.locator(".cart-bucket .item-container").count()
            return cart_items if cart_items > 0 else 1
        except:
            return 1  # Default to 1 if can't determine