import time
from playwright.sync_api import sync_playwright

def run():
    print("🚀 Launching Native Stealth Manual Verification Canvas...")
    with sync_playwright() as p:
        # Launch standard Chromium instance
        browser = p.chromium.launch(headless=False)
        
        # Configure the context with native automation masking parameters
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720},
            permissions=["geolocation"],
            geolocation={"latitude": 19.0760, "longitude": 72.8777}
        )
        
        page = context.new_page()
        
        # Native Script Injection: This completely overwrites the automation flag in the browser's runtime memory
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("🌐 Navigating to target environment...")
        page.goto("https://www.swiggy.com/instamart")
        
        print("\n🔒 ACTION REQUIRED:")
        print("1. Click 'Sign In' or 'Login'.")
        print("2. Pass your mobile phone verification via OTP.")
        print("3. Explicitly select your target Home/Work Delivery Address.")
        print("4. Return to this terminal once you are looking at your active logged-in dashboard.\n")
        
        input("⏳ Press [Enter] inside this terminal window ONLY after address selection is complete...")
        context.storage_state(path="swiggy_session.json")
        print("✅ Active profile tokens successfully exported -> swiggy_session.json")
        browser.close()

if __name__ == "__main__":
    run()