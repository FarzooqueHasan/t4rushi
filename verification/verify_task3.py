import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')
options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

driver = webdriver.Chrome(options=options)
url_base = 'file:///c:/Users/dpset/Desktop/PROJECTS/MBD/index.html'
out_dir = r'c:\Users\dpset\Desktop\PROJECTS\MBD\verification'

# 1. State Captures
checks = [
    ('idle', 'prank_idle.png'),
    ('hold50', 'prank_mid_hold.png'),
    ('punchline', 'prank_punchline_desaturated.png'),
    ('burn50', 'prank_mid_burn.png'),
    ('done', 'prank_handoff_beat01.png'),
]

print("=== PART 1: CAPTURING 5 VERIFICATION SCREENSHOTS ===")
for state, filename in checks:
    driver.get(f'{url_base}?prankState={state}')
    time.sleep(1.0)
    
    # Check DOM
    elem = driver.execute_script("return document.getElementById('prank-layer');")
    exists = elem is not None
    print(f"State '{state}': #prank-layer in DOM = {exists}")
    
    save_path = os.path.join(out_dir, filename)
    driver.save_screenshot(save_path)
    print(f"Saved: {filename}")

# 2. Live Interactive End-to-End Test
print("\n=== PART 2: LIVE INTERACTIVE END-TO-END TIMING VERIFICATION ===")
driver.get(url_base)
time.sleep(1.0)

# Check idle state
print("Live: Page loaded. Sparkle and hold button active.")
hold_btn = driver.find_element(By.ID, "hold-btn")

# Simulate pointerdown on hold button
t0 = time.time()
actions = ActionChains(driver)
actions.click_and_hold(hold_btn).perform()
print("Live: Pointer down on hold button...")

# Hold for 1250ms (duration is 1200ms)
time.sleep(1.25)
actions.release().perform()
print(f"Live: Released after {(time.time() - t0):.2f}s")

# Wait through: desaturation (400ms) + punchline hold (1200ms) + burn (800ms) + buffer (300ms) = 2.7s
time.sleep(2.7)

# Verify element tree removal
prank_after = driver.execute_script("return document.getElementById('prank-layer');")
canvas_after = driver.execute_script("return document.getElementById('burn-canvas');")
webgl_canvas = driver.execute_script("return document.getElementById('webgl-canvas');")
scroll_top = driver.execute_script("return window.pageYOffset || document.documentElement.scrollTop;")

print(f"Live: After sequence completion:")
print(f" - #prank-layer in DOM: {prank_after is not None} (Expected: False)")
print(f" - #burn-canvas in DOM: {canvas_after is not None} (Expected: False)")
print(f" - #webgl-canvas in DOM: {webgl_canvas is not None} (Expected: True)")
print(f" - Scroll Position: {scroll_top} (Expected: 0, Beat 1 active)")

print("\n=== BROWSER CONSOLE LOGS ===")
for entry in driver.get_log('browser'):
    print(f"[{entry['level']}] {entry['message']}")

driver.quit()
print("\nVerification complete!")
