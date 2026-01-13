import random
from pages.base_page import BasePage

class ProductPage(BasePage):
    def select_random_variants(self):
        """Select random variants from both standard selects and custom listboxes"""
        try:
            self.page.wait_for_load_state("domcontentloaded")
            self.page.wait_for_timeout(1000)
            
            # Handle custom listbox variants (like size, color selectors)
            self._select_listbox_variants()
            
            # Handle standard select dropdowns (if any)
            self._select_standard_dropdowns()
            
        except Exception as e:
            print(f"Error in select_random_variants: {e}")
    
    def _select_listbox_variants(self):
        """Handle custom eBay listbox components"""
        try:
            # Find all listbox buttons (the custom dropdowns)
            listbox_buttons = self.page.locator("button[aria-haspopup='listbox']").all()
            print(f"Found {len(listbox_buttons)} listbox components")
            
            for idx, button in enumerate(listbox_buttons):
                try:
                    if not button.is_visible():
                        continue
                    
                    # Get the button text to see what this is for
                    button_label = button.locator(".btn__label").inner_text() if button.locator(".btn__label").count() > 0 else ""
                    button_text = button.locator(".btn__text").inner_text() if button.locator(".btn__text").count() > 0 else ""
                    
                    print(f"Listbox {idx}: label='{button_label}', current='{button_text}'")
                    
                    # Skip if it's quantity
                    skip_keywords = ['quantity', 'qty', 'amount']
                    if any(keyword in button_label.lower() for keyword in skip_keywords):
                        print(f"Listbox {idx}: Skipping quantity selector")
                        continue
                    
                    # Skip if already selected (not "Select")
                    if button_text.lower() != "select" and button_text.strip():
                        print(f"Listbox {idx}: Already selected, skipping")
                        continue
                    
                    # Click button to open the listbox
                    button.click()
                    self.page.wait_for_timeout(500)
                    
                    # Get the listbox ID from aria-controls
                    listbox_id = button.get_attribute("aria-controls")
                    
                    if listbox_id:
                        # Find all valid options in the opened listbox
                        listbox = self.page.locator(f"#{listbox_id}")
                        options = listbox.locator("div[role='option']").all()
                        
                        valid_options = []
                        for option in options:
                            # Skip disabled options
                            is_disabled = option.get_attribute("aria-disabled") == "true"
                            if is_disabled:
                                continue
                            
                            # Get option text
                            option_text = option.locator(".listbox__value").inner_text().strip()
                            
                            # Skip placeholder and out of stock options
                            if "select" in option_text.lower() or "out of stock" in option_text.lower():
                                continue
                            
                            if option_text:
                                valid_options.append({
                                    'element': option,
                                    'text': option_text
                                })
                        
                        print(f"Listbox {idx}: Found {len(valid_options)} valid options")
                        
                        # Select a random valid option
                        if valid_options:
                            chosen = random.choice(valid_options)
                            print(f"Listbox {idx}: Selecting '{chosen['text']}'")
                            chosen['element'].click()
                            self.page.wait_for_timeout(500)
                        else:
                            print(f"Listbox {idx}: No valid options, closing")
                            # Close the listbox by clicking the button again
                            button.click()
                            self.page.wait_for_timeout(300)
                    
                except Exception as e:
                    print(f"Listbox {idx}: Error - {e}")
                    # Try to close any open listbox
                    try:
                        self.page.keyboard.press("Escape")
                    except:
                        pass
                    continue
                    
        except Exception as e:
            print(f"Error in _select_listbox_variants: {e}")
    
    def _select_standard_dropdowns(self):
        """Handle standard HTML select dropdowns"""
        try:
            all_selects = self.page.locator("select:not([hidden])").all()
            print(f"Found {len(all_selects)} standard select elements")
            
            for idx, select in enumerate(all_selects):
                try:
                    if not select.is_visible():
                        continue
                    
                    aria_label = select.get_attribute("aria-label") or ""
                    
                    # Skip quantity selectors
                    skip_keywords = ['quantity', 'qty', 'amount']
                    if any(keyword in aria_label.lower() for keyword in skip_keywords):
                        continue
                    
                    # Get valid options
                    valid_options = []
                    options = select.locator("option").all()
                    
                    for option in options:
                        if option.get_attribute("disabled"):
                            continue
                        value = option.get_attribute("value") or ""
                        text = option.inner_text().strip()
                        
                        if value and value not in ["-1", "0", ""] and text:
                            if "select" not in text.lower():
                                valid_options.append({'value': value, 'text': text})
                    
                    if valid_options:
                        chosen = random.choice(valid_options)
                        print(f"Select {idx}: Selecting '{chosen['text']}'")
                        select.select_option(value=chosen['value'])
                        self.page.wait_for_timeout(500)
                        
                except Exception as e:
                    print(f"Select {idx}: Error - {e}")
                    continue
                    
        except Exception as e:
            print(f"Error in _select_standard_dropdowns: {e}")

    def add_to_cart(self):
        """Add item to cart, selecting variants if needed"""
        try:
            print(f"Processing product page: {self.page.url}")
            
            # Wait for page to load
            self.page.wait_for_load_state("domcontentloaded")
            self.page.wait_for_timeout(1500)
            
            # Check if variants need to be selected
            listbox_count = self.page.locator("button[aria-haspopup='listbox']").count()
            select_count = self.page.locator("select:not([hidden])").count()
            print(f"Found {listbox_count} listbox components and {select_count} select elements")
            
            if listbox_count > 0 or select_count > 0:
                print("Selecting variants...")
                self.select_random_variants()
            else:
                print("No variants to select")
            
            # Wait a bit for any updates
            self.page.wait_for_timeout(1000)
            
            # Try to find and click "Add to cart" button
            print("Looking for 'Add to cart' button...")
            
            add_to_cart_selectors = [
                "a:has-text('Add to cart')",
                "button:has-text('Add to cart')",
                "a.ux-call-to-action--primary:has-text('Add')",
                "a[href*='addToCart']",
                "#atcBtn_btn",
                "a.btn--primary:has-text('Add')",
            ]
            
            button_clicked = False
            for selector in add_to_cart_selectors:
                try:
                    button = self.page.locator(selector).first
                    if button.count() > 0 and button.is_visible():
                        button_text = button.inner_text()
                        print(f"Found button: text='{button_text}'")
                        button.click(timeout=5000)
                        button_clicked = True
                        print("Successfully clicked 'Add to cart' button")
                        break
                except:
                    continue
            
            if not button_clicked:
                print("ERROR: Could not find 'Add to cart' button")
                self.page.screenshot(path="debug_no_add_to_cart.png")
                raise Exception("Could not find 'Add to cart' button")
            
            # Wait for cart action to complete
            self.page.wait_for_timeout(2000)
            
        except Exception as e:
            print(f"Error adding to cart: {e}")
            self.page.screenshot(path=f"error_add_to_cart.png")
            raise