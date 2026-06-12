import os
import json
import time
import re
from openai import OpenAI
from playwright.sync_api import sync_playwright

# Initialize explicit GROQ client configuration engine
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

def query_groq_json(prompt: str) -> dict:
    """Helper to get clean, reliable raw JSON dictionaries from Llama."""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an elite quick-commerce automation controller. Respond ONLY with a valid, raw JSON object. Do not include markdown code blocks or introductory text."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0  
        )
        clean_str = response.choices[0].message.content.strip()
        clean_str = re.sub(r"^```json\s*|^```\s*|\s*```$", "", clean_str, flags=re.IGNORECASE).strip()
        return json.loads(clean_str)
    except Exception as e:
        print(f"⚠️ Groq inference error: {str(e)}")
        return {}

def run_interactive_agent():
    print("\n========================================================")
    print("🤖 COGNITIVE MULTI-ITEM COMMERCE CONTEXT AGENT")
    print("========================================================")
    
    user_instruction = input("\n💬 What would you like to order today?\n> ")
    if not user_instruction.strip():
        print("❌ Empty order intent string. Exiting...")
        return

    profile_dir = "./blinkit_profile"
    if not os.path.exists(profile_dir):
        print("❌ System session footprint directory missing! Please run 'python setup_blinkit.py' first.")
        return

    # -----------------------------------------------------------------
    # NODE 1: Smart Intent & Property Parser
    # -----------------------------------------------------------------
    print("\n⚡ Parsing Complex Natural Language Intent via Llama...")
    planner_prompt = f"""
    Analyze the user's shopping request and break it down into a structured JSON list of items to search for.
    For each item, extract the best search keyword string, the desired quantity count, and any special preference modifiers like 'cheapest' or 'smallest'.
    
    User Request: '{user_instruction}'
    
    Return ONLY a raw JSON dictionary structured exactly like this:
    {{
        "items": [
            {{"keyword": "redbull can", "quantity": 1, "preference": "none"}},
            {{"keyword": "thumbs up bottle", "quantity": 1, "preference": "smallest"}}
        ]
    }}
    """
    intent_data = query_groq_json(planner_prompt)
    search_manifest = intent_data.get("items", [])
    
    if not search_manifest:
        print("❌ Llama failed to parse a valid manifest array. Exiting...")
        return
        
    print("\n📋 Generated Smart Order Manifest:")
    for item in search_manifest:
        print(f"  • Search: '{item['keyword']}' | Qty: {item['quantity']} | Preference: {item['preference']}")
    
    proceed = input("\n❓ Does this manifest look correct? Ready to launch automation canvas? (y/n): ")
    if proceed.lower() not in ['y', 'yes']:
        print("🛑 Order pipeline execution cancelled by operator.")
        return

    # -----------------------------------------------------------------
    # NODE 2: Automated Browser Session Mount
    # -----------------------------------------------------------------
    with sync_playwright() as p:
        print("\n🌐 Initializing browser canvas via Shared Persistent Profile data...")
        context = p.chromium.launch_persistent_context(
            user_data_dir=profile_dir,
            headless=False,
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        
        page = context.pages[0] if context.pages else context.new_page()
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        base_protocol = "https://"
        base_domain = "blinkit.com"
        
        # --- INITIAL HOMEPAGE LANDING FOR VISUAL TRACE ---
        print("🌐 Opening Blinkit Homepage to demonstrate active authenticated session context...")
        page.goto(f"{base_protocol}{base_domain}")
        page.wait_for_load_state("domcontentloaded")
        print("⏳ Staying on homepage for 3 seconds for visual trace capture...")
        page.wait_for_timeout(3000)
        
        # -----------------------------------------------------------------
        # NODE 3, 4 & 5: Sequential URL Routing Cart Injection Loop
        # -----------------------------------------------------------------
        for item_idx, item in enumerate(search_manifest):
            keyword = item["keyword"]
            print(f"\n🔄 [Processing Item {item_idx + 1}/{len(search_manifest)}]: '{keyword}'")
            
            encoded_keyword = keyword.replace(" ", "%20")
            search_url = f"{base_protocol}{base_domain}/s/?q={encoded_keyword}"
            page.goto(search_url)
            
            try:
                page.locator("text='ADD'").first.wait_for(state="visible", timeout=8000)
                print("✅ Catalog grid items rendered successfully.")
            except Exception:
                print("⚠️ Search layout loading delayed. Moving to safety fallback timing...")
                page.wait_for_timeout(4000)
                
            print("🕵️ Locating the primary target row 'ADD' switch...")
            add_buttons = page.locator("text='ADD'").all()
            
            if not add_buttons:
                print(f"❌ Could not find an active 'ADD' button for '{keyword}'. Skipping item...")
                continue
                
            try:
                target_btn = add_buttons[0]
                target_btn.scroll_into_view_if_needed()
                target_btn.click(force=True)
                print(f"➕ Successfully added '{keyword}' to your checkout basket!")
            except Exception as e:
                print(f"❌ Failed to click injection button for '{keyword}': {str(e)}")
                
            page.wait_for_timeout(3000)

        # -----------------------------------------------------------------
        # NODE 6: Trigger Checkout Slide Drawer Panel
        # -----------------------------------------------------------------
        print("\n📋 All manifest loops complete. Triggering top-right checkout cart drawer...")
        cart_selectors = [
            page.locator("text='My Cart'").first,
            page.locator("div:has-text('item')").last,
            page.locator("div[class*='cart']").first
        ]
        
        action_success = False
        for i, cart_btn in enumerate(cart_selectors):
            try:
                if cart_btn.is_visible(timeout=2000):
                    cart_btn.click(force=True)
                    print(f"🛒 Drawer opened via UI element branch [{i}].")
                    action_success = True
                    break
            except Exception:
                continue
                
        if not action_success:
            page.click("header >> div", position={"x": 1180, "y": 30})
            
        page.wait_for_timeout(4000) 
        
        # -----------------------------------------------------------------
        # NODE 7: Optimized Human-In-The-Loop Security Gate Location
        # -----------------------------------------------------------------
        print("\n========================================================")
        print("🚨 COGNITIVE COMMERCE AGENT CHECKOUT SECURITY GATE")
        print("========================================================")
        print("🔒 The browser is currently parked directly at your open basket review panel.")
        print("🟢 Verify your item rows, delivery address, and subtotal metrics on screen now.")
        
        # FIXED: Input confirmation gate executed BEFORE navigating to the sensitive gateway
        confirmation = input("\n❓ Is everything you mention proper? Would you like to confirm? (Type CONFIRM to place order):\n> ")
        
        if confirmation.strip() == "CONFIRM":
            print("\n🚀 UNLEASHING AUTOMATED CHECKOUT SUBMISSION MATRIX...")
            
            try:
                payment_gate_btn = page.locator("text='Proceed To Pay'").first
                payment_gate_btn.scroll_into_view_if_needed()
                payment_gate_btn.click(force=True)
                print("✅ Dispatched execution loop straight to gateway frame.")
            except Exception as e:
                print(f"❌ Failed to click checkout button: {str(e)}")
                context.close()
                return
                
            print("⏳ Loading checkout layout parameters...")
            page.wait_for_timeout(5000)
            
            # --- NODE 8: Unified Direct Payment Interaction (Zero-Delay Session Execution) ---
            if page.locator("iframe#payment_widget").is_visible(timeout=1500):
                pay_context = page.frame_locator("iframe#payment_widget")
            else:
                pay_context = page
                
            try:
                cash_selectors = [
                    pay_context.locator("text='Cash on Delivery'"),
                    pay_context.locator("div[title='Cash']"),
                    pay_context.locator("text='Cash'").first
                ]
                
                for selector in cash_selectors:
                    if selector.is_visible(timeout=1500):
                        selector.scroll_into_view_if_needed()
                        selector.click(force=True)
                        print(f"💵 Expanded Cash option accordion container layout.")
                        break
                
                page.wait_for_timeout(1500)
                
                cod_sub_triggers = [
                    pay_context.locator("text='Pay on Delivery'"),
                    pay_context.locator("button:has-text('Cash')"),
                    pay_context.locator("role=button[name*='Cash']")
                ]
                for trigger in cod_sub_triggers:
                    if trigger.is_visible(timeout=1000):
                        trigger.click(force=True)
                        break
            except Exception as e:
                print(f"⚠️ Cash drawer toggle skipped: {str(e)}")

            # --- NODE 9: Final Rapid Transaction Click ---
            final_pay_selectors = [
                page.locator("button:has-text('Pay Now')"),
                page.locator("text='Pay Now'"),
                pay_context.locator("button:has-text('Place Order')"),
                pay_context.locator("button:has-text('Pay')")
            ]
            
            pay_triggered = False
            for idx, selector in enumerate(final_pay_selectors):
                try:
                    if selector.is_visible(timeout=1500):
                        print(f"🎯 Matching checkout locator triggered via rule strategy [{idx}].")
                        selector.scroll_into_view_if_needed()
                        selector.click(force=True)
                        print("✅ Final order transaction sent live!")
                        pay_triggered = True
                        break
                except Exception:
                    continue
                    
            if not pay_triggered:
                try:
                    page.locator("button:not([disabled])").last.click(force=True)
                    print("✅ Alternative bottom matrix panel button clicked.")
                    pay_triggered = True
                except Exception as e:
                    print(f"❌ Final step click interaction bypassed: {str(e)}")
                    
            if pay_triggered:
                print("⏳ Order sent! Holding browser window open for 10 seconds to capture success validation screen...")
                page.wait_for_timeout(10000)
        else:
            print("\n🛑 Order held safely. Final submission blocked by operator request.")
            
        input("\n🏁 Session complete. Press [Enter] inside this terminal to close the workspace window...")
        context.close()

if __name__ == "__main__":
    run_interactive_agent()