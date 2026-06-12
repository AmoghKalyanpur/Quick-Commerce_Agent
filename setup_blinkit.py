import os
from playwright.sync_api import sync_playwright

def run_persistent_setup():
    print("🚀 Launching Permanent Profile Canvas for Blinkit...")
    
    # Define a clean local directory path for your browser session storage profile
    profile_dir = "./blinkit_profile"
    
    with sync_playwright() as p:
        # Launch a persistent context wrapper that records ALL storage automatically
        context = p.chromium.launch_persistent_context(
            user_data_dir=profile_dir,
            headless=False,
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            permissions=["geolocation"],
            geolocation={"latitude": 19.0760, "longitude": 72.8777}
        )
        
        page = context.pages[0] if context.pages else context.new_page()
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("🌐 Navigating to Blinkit Marketplace...")
        page.goto("https://blinkit.com")
        
        print("\n🔒 ACTION REQUIRED FOR PERMANENT HANDSHAKE:")
        print("1. Click 'Login' or 'Select Address' on the top panel grid view.")
        print("2. Enter your mobile phone number and complete the OTP verification.")
        print("3. Explicitly select your 'Home' address so the delivery coordinates freeze active.")
        print("4. Once you see your main logged-in dashboard panel, return here.\n")
        
        input("⏳ Press [Enter] inside this terminal window ONLY after you are completely logged in...")
        
        print("✅ Permanent profile sync state completed successfully!")
        context.close()

if __name__ == "__main__":
    run_persistent_setup()