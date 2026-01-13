# eBay E2E Automation Testing

This is an automated testing project for eBay's shopping flow. It searches for products, filters by price (including shipping), adds items to cart, and verifies the total doesn't exceed a budget.

## What This Does

The test performs a complete shopping journey:

1. Opens eBay
2. Searches for a product (like "shoes")
3. Filters results to only show items under a certain price
4. **Important:** Also checks shipping costs - skips items where item price + shipping exceeds the budget
5. Collects 5 products that fit the budget
6. Opens each product page
7. Selects random variants (size, color, etc.) if needed
8. Adds each item to the shopping cart
9. Opens the cart and verifies the total is within budget

Everything is logged with detailed screenshots and data in an Allure report.

## Tech Stack

- **Python 3.13** - Programming language
- **Playwright** - Browser automation (uses Microsoft Edge)
- **Pytest** - Test framework
- **Allure** - Fancy HTML reports with screenshots

## Project Structure
```
PlaywrightExercise/
├── pages/               # Page Object Model - each page has its own class
│   ├── base_page.py
│   ├── cart_page.py
│   ├── product_page.py
│   ├── search_page.py
│   └── login_page.py
├── services/            # Business logic layer
│   ├── auth_service.py
│   ├── cart_service.py
│   └── search_service.py
├── tests/               # The actual tests
│   └── test_e2e_flow.py
├── utils/               # Helper functions
│   ├── price_utils.py
│   └── screenshot_helper.py
├── data/                # Test data
│   └── test_data.json
└── conftest.py          # Pytest configuration
```

## Setup

### 1. Install Python packages
```bash
pip install -r requirements.txt
```

### 2. Install the browser

Playwright needs to download Microsoft Edge (or Chromium):
```bash
playwright install msedge
```

## Configuration

Edit `data/test_data.json` to change what you're searching for:
```json
{
  "auth": {
    "mode": "guest"
  },
  "search": {
    "query": "shoes",
    "max_price": 1000,
    "limit": 5
  }
}
```

- `query` - What to search for
- `max_price` - Maximum price per item (including shipping) in ILS
- `limit` - How many items to add to cart

## Running the Tests

### Run the test
```bash
pytest
```

This will:
- Open Microsoft Edge (not headless, so you can watch)
- Run through the entire flow
- Save results to `allure-results/` folder

### View the report
```bash
allure serve allure-results
```

This opens your browser with a beautiful HTML report showing:
- Every step that was executed
- Screenshots at each stage
- Detailed data (prices, URLs, etc.)
- Error screenshots if something failed

## Key Features

### Smart Price Filtering

The test doesn't just look at item prices - it calculates **item price + shipping** and only selects items where the total is under budget. This prevents surprises at checkout.

### Handles eBay's Complex UI

eBay has different layouts and custom dropdown components. The code handles:
- Custom listbox dropdowns (not standard HTML selects)
- Multiple variant options (size, color, etc.)
- Out-of-stock options
- Different product page layouts

### Detailed Reporting

Every action is logged with:
- Screenshots before and after each step
- JSON data of what was found/selected
- Error details with screenshots if something fails
- Full browser trace on failures

## Known Issues

- **CAPTCHA**: If eBay shows a CAPTCHA (especially when opening the cart), you need to solve it manually. Can't automate around that.
- **Rate Limiting**: Running the test too many times in a row might trigger eBay's anti-bot measures.

## Design Decisions

- **Page Object Model (POM)**: Each page has its own class with methods for interacting with it. Makes the code cleaner and easier to maintain.
- **Service Layer**: Business logic is separated from page interactions. The test itself is just high-level steps.
- **Data-Driven**: Test data comes from JSON, not hardcoded.
- **Guest Mode**: Runs without login by default (less likely to trigger security measures).

## Notes

- The browser runs in **non-headless mode** by default so you can see what's happening
- Screenshots are saved both to `screenshots/` folder and embedded in the Allure report
- The test budget is **per item**, not total. With max_price=1000 and 5 items, the budget is 5000 ILS total.

## Troubleshooting

**Test fails on "Add to cart":**
- eBay's product pages vary. Some buttons are different. Check the error screenshot in the report.

**Can't find items under budget:**
- Try increasing `max_price` or changing the search query
