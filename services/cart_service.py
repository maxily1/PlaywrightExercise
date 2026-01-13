import allure
from allure_commons.types import AttachmentType
from pages.product_page import ProductPage
from pages.cart_page import CartPage
import json

@allure.step("Adding items to cart")  # ← Fixed: removed {len(urls)}
def addItemsToCart(page, urls: list[str]):
    """
    Add multiple items to shopping cart
    
    :param page: Playwright page object
    :param urls: List of product URLs to add
    """
    
    # Log the count inside the function instead
    allure.dynamic.title(f"Adding {len(urls)} items to cart")
    
    product_page = ProductPage(page)
    
    # Attach items to be added
    allure.attach(
        json.dumps({"items_to_add": len(urls), "urls": urls}, indent=2),
        name="Items to Add",
        attachment_type=AttachmentType.JSON
    )
    
    added_items = []
    failed_items = []
    
    for idx, url in enumerate(urls, 1):
        with allure.step(f"Adding item {idx}/{len(urls)}"):
            try:
                allure.attach(url, name=f"Item {idx} URL", attachment_type=AttachmentType.TEXT)
                
                with allure.step(f"Navigating to product page"):
                    page.goto(url)
                    page.wait_for_load_state("domcontentloaded")
                
                # Screenshot before adding
                allure.attach(
                    page.screenshot(full_page=True),
                    name=f"Item_{idx}_Product_Page",
                    attachment_type=AttachmentType.PNG
                )
                
                with allure.step("Adding item to cart"):
                    product_page.add_to_cart()
                
                # Screenshot after adding
                allure.attach(
                    page.screenshot(full_page=True),
                    name=f"Item_{idx}_Added_Confirmation",
                    attachment_type=AttachmentType.PNG
                )
                
                added_items.append({"index": idx, "url": url, "status": "success"})
                
            except Exception as e:
                error_msg = f"Failed to add item {idx}: {str(e)}"
                allure.attach(
                    error_msg,
                    name=f"Item_{idx}_Error",
                    attachment_type=AttachmentType.TEXT
                )
                
                # Screenshot on error
                allure.attach(
                    page.screenshot(full_page=True),
                    name=f"Item_{idx}_Error_Screenshot",
                    attachment_type=AttachmentType.PNG
                )
                
                failed_items.append({"index": idx, "url": url, "error": str(e)})
                raise  # Re-raise to fail the test
    
    # Summary of additions
    summary = {
        "total_items": len(urls),
        "successfully_added": len(added_items),
        "failed": len(failed_items),
        "added_items": added_items,
        "failed_items": failed_items
    }
    
    allure.attach(
        json.dumps(summary, indent=2),
        name="Add to Cart Summary",
        attachment_type=AttachmentType.JSON
    )

@allure.step("Verifying cart total does not exceed budget")
def assertCartTotalNotExceeds(page, budget_per_item: int, items_count: int):
    """
    Verify that cart total is within budget
    
    :param page: Playwright page object
    :param budget_per_item: Maximum price per item
    :param items_count: Number of items in cart
    """
    cart_page = CartPage(page)
    
    with allure.step("Opening shopping cart"):
        cart_page.open()
    
    # Screenshot of cart
    allure.attach(
        page.screenshot(full_page=True),
        name="Shopping_Cart_Full_View",
        attachment_type=AttachmentType.PNG
    )
    
    with allure.step("Extracting cart total"):
        total = cart_page.get_total()
    
    max_allowed = budget_per_item * items_count
    
    # Create detailed verification report
    verification_data = {
        "cart_total": f"{total} ILS",
        "budget_per_item": f"{budget_per_item} ILS",
        "number_of_items": items_count,
        "max_allowed_total": f"{max_allowed} ILS",
        "within_budget": total <= max_allowed,
        "difference": f"{max_allowed - total} ILS" if total <= max_allowed else f"-{total - max_allowed} ILS (OVER BUDGET)"
    }
    
    allure.attach(
        json.dumps(verification_data, indent=2),
        name="Budget Verification Details",
        attachment_type=AttachmentType.JSON
    )
    
    # Add dynamic description
    allure.dynamic.description(
        f"Cart Total: {total} ILS\n"
        f"Budget Threshold: {max_allowed} ILS\n"
        f"Items: {items_count}\n"
        f"Status: {'✓ PASS' if total <= max_allowed else '✗ FAIL'}"
    )
    
    # Attach final verification screenshot
    allure.attach(
        page.screenshot(full_page=True),
        name="Final_Cart_Verification",
        attachment_type=AttachmentType.PNG
    )
    
    # Assertion with detailed message
    assert total <= max_allowed, (
        f"\n{'='*50}\n"
        f"BUDGET EXCEEDED!\n"
        f"{'='*50}\n"
        f"Cart Total: {total} ILS\n"
        f"Max Allowed: {max_allowed} ILS ({budget_per_item} ILS × {items_count} items)\n"
        f"Over Budget By: {total - max_allowed} ILS\n"
        f"{'='*50}"
    )
    
    allure.attach(
        "✓ Cart total is within budget",
        name="Verification Result",
        attachment_type=AttachmentType.TEXT
    )