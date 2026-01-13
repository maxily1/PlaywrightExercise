import pytest
import allure
from playwright.sync_api import sync_playwright
from allure_commons.types import AttachmentType

@pytest.fixture(scope="function")
def page(request):
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=False, slow_mo=100)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            locale='en-US',
            timezone_id='Asia/Jerusalem'
        )
        
        # Enable tracing for detailed debugging
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        
        page = context.new_page()
        
        # Attach browser info to Allure
        allure.dynamic.parameter("Browser", "Microsoft Edge")
        allure.dynamic.parameter("Viewport", "1920x1080")
        
        yield page
        
        # On test failure, attach trace and screenshot
        if request.node.rep_call.failed if hasattr(request.node, 'rep_call') else False:
            allure.attach(
                page.screenshot(full_page=True),
                name="Failure Screenshot",
                attachment_type=AttachmentType.PNG
            )
            
            # Save and attach trace
            trace_path = f"trace_{request.node.name}.zip"
            context.tracing.stop(path=trace_path)
            allure.attach.file(
                trace_path,
                name="Playwright Trace",
                attachment_type=AttachmentType.ZIP
            )
        else:
            context.tracing.stop()
        
        browser.close()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test result for use in fixture"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

def pytest_configure(config):
    config.addinivalue_line("markers", "e2e: mark test as end-to-end")
    
    # Set Allure report metadata
    allure.dynamic.feature("E2E Shopping Flow")
    allure.dynamic.suite("eBay Automation Tests")