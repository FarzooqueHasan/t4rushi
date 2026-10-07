import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

print("=== TASK 8: VERIFYING SCRAPBOOK FOUNDATION & FLIGHT LOG SPREAD ===")

# 1. Verify Assets Directory
assets_dir = r"c:\Users\dpset\Desktop\PROJECTS\MBD\assets\scrapbook"
expected_files = {"flight-b2-top.jpg", "flight-fighter-top.jpg", "flight-fighter-side.jpg"}

actual_files = set(os.listdir(assets_dir))
print(f"\n1. Assets Directory Listing ({assets_dir}):")
for f in sorted(actual_files):
    size = os.path.getsize(os.path.join(assets_dir, f))
    print(f"  - {f}: {size:,} bytes")

assert actual_files == expected_files, f"Asset directory mismatch! Expected {expected_files}, found {actual_files}"
print("  ✓ Directory contains ONLY the three specified files.")

total_size = sum(os.path.getsize(os.path.join(assets_dir, f)) for f in actual_files)
max_allowed = 1.5 * 1024 * 1024 # 1.5 MB
print(f"  Total size: {total_size:,} bytes ({total_size / (1024 * 1024):.2f} MB)")
assert total_size < max_allowed, f"Total size exceeds 1.5 MB limit: {total_size} bytes"
print(f"  ✓ Combined image size is well under 1.5 MB limit.")

# 2. Browser Verification (Selenium Headless Chrome)
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--allow-file-access-from-files')
options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

out_dir = r"c:\Users\dpset\Desktop\PROJECTS\MBD\verification"
url = "file:///c:/Users/dpset/Desktop/PROJECTS/MBD/scrapbook.html"

# Desktop Test at 1440x900
print("\n2. Desktop Viewport Test (1440x900):")
driver = webdriver.Chrome(options=options)
driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {
    "width": 1440,
    "height": 900,
    "deviceScaleFactor": 1,
    "mobile": False
})
driver.get(url)
time.sleep(1.0)

# Check console errors on cover
logs = driver.get_log('browser')
errors = [log for log in logs if log['level'] in ('SEVERE', 'ERROR')]
print(f"  Console errors: {len(errors)}")
if errors:
    for err in errors:
        print(f"    ! {err['message']}")
assert len(errors) == 0, "Console errors detected on page load!"
print("  ✓ Zero console errors on load.")

# Screenshot 1: Desktop Cover
cover_desktop_path = os.path.join(out_dir, "scrapbook_cover_desktop_1440x900.png")
driver.save_screenshot(cover_desktop_path)
print(f"  ✓ Captured: scrapbook_cover_desktop_1440x900.png")

# Scroll to Flight Log and reveal
driver.execute_script("document.getElementById('flight-log').scrollIntoView({behavior: 'instant'});")
time.sleep(1.5) # Wait for IntersectionObserver (20% visibility) + 120ms sibling staggers + 600ms ease-out

# Verify all spread-items are revealed
revealed_count = driver.execute_script("return document.querySelectorAll('.spread-item.is-revealed').length;")
total_items = driver.execute_script("return document.querySelectorAll('.spread-item').length;")
print(f"  Flight Log items revealed: {revealed_count}/{total_items}")
assert revealed_count == total_items, f"Not all items revealed! {revealed_count}/{total_items}"

# Check console errors after scroll
logs_after = driver.get_log('browser')
errors_after = [log for log in logs_after if log['level'] in ('SEVERE', 'ERROR')]
assert len(errors_after) == 0, "Console errors detected after scroll!"
print("  ✓ Zero console errors after reveal.")

# Screenshot 2: Desktop Flight Log Fully Revealed
flight_log_desktop_path = os.path.join(out_dir, "scrapbook_flight_log_desktop_1440x900.png")
driver.save_screenshot(flight_log_desktop_path)
print(f"  ✓ Captured: scrapbook_flight_log_desktop_1440x900.png")

driver.quit()

# 3. Mobile Viewport Test (390x844)
print("\n3. Mobile Viewport Test (390x844):")
driver_mobile = webdriver.Chrome(options=options)
driver_mobile.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {
    "width": 390,
    "height": 844,
    "deviceScaleFactor": 1,
    "mobile": True
})
driver_mobile.get(url)
time.sleep(1.0)

# Screenshot 3: Mobile Cover
cover_mobile_path = os.path.join(out_dir, "scrapbook_cover_mobile_390x844.png")
driver_mobile.save_screenshot(cover_mobile_path)
print(f"  ✓ Captured: scrapbook_cover_mobile_390x844.png")

# Scroll through Flight Log on mobile to reveal items
driver_mobile.execute_script("document.getElementById('flight-log').scrollIntoView({behavior: 'instant'});")
time.sleep(1.2)

# Screenshot 4: Mobile Flight Log
flight_log_mobile_path = os.path.join(out_dir, "scrapbook_flight_log_mobile_390x844.png")
driver_mobile.save_screenshot(flight_log_mobile_path)
print(f"  ✓ Captured: scrapbook_flight_log_mobile_390x844.png")

# Check console errors on mobile
mob_logs = driver_mobile.get_log('browser')
mob_errors = [log for log in mob_logs if log['level'] in ('SEVERE', 'ERROR')]
assert len(mob_errors) == 0, "Console errors detected on mobile!"
print("  ✓ Zero console errors on mobile.")

driver_mobile.quit()

print("\n=== TASK 8 VERIFICATION COMPLETE ===")
