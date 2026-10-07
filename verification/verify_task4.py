import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')
options.add_argument('--allow-file-access-from-files')
options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

driver = webdriver.Chrome(options=options)
url_base = 'file:///c:/Users/dpset/Desktop/PROJECTS/MBD'
out_dir = r'c:\Users\dpset\Desktop\PROJECTS\MBD\verification'

print("=== TASK 4: VERIFYING B2 BOMBER IMPORT, CLEANUP, ORIENTATION & PLACEMENT ===")

# 1. Orientation Renders
print("\n--- 1. Capturing Standalone Orientation Renders ---")
for view, filename in [('top', 'b2_orientation_top.png'), ('side', 'b2_orientation_side.png')]:
    url = f"{url_base}/b2-orientation-test.html?view={view}"
    driver.get(url)
    WebDriverWait(driver, 15).until(lambda d: d.execute_script("return window.b2ModelReady === true;"))
    time.sleep(0.5)
    save_path = os.path.join(out_dir, filename)
    driver.save_screenshot(save_path)
    print(f"Saved {filename}")

# 2. Post-Placement Beat 4 Renders
print("\n--- 2. Capturing Beat 4 Post-Placement Renders in index.html ---")
placement_views = [
    ('beat4_front', 'b2_beat4_front.png'),
    ('beat4_three_quarter', 'b2_beat4_three_quarter.png')
]

for cam, filename in placement_views:
    url = f"{url_base}/index.html?prankState=done&cam={cam}"
    driver.get(url)
    WebDriverWait(driver, 15).until(lambda d: d.execute_script("return window.b2Ready === true;"))
    time.sleep(0.5)
    save_path = os.path.join(out_dir, filename)
    driver.save_screenshot(save_path)
    print(f"Saved {filename}")

# 3. Scene Graph and Console Inspection
print("\n--- 3. Scene Graph & DOM Inspection ---")
verification_script = """
const scene = window.__debugScene || (function() {
  // Find scene in Three.js objects or traverse
  let s = null;
  if (window.b2Aircraft && window.b2Aircraft.parent) {
    s = window.b2Aircraft.parent;
  }
  return s;
})();

const results = {
  b2Present: !!window.b2Aircraft,
  b2Position: window.b2Aircraft ? {
    x: window.b2Aircraft.position.x,
    y: window.b2Aircraft.position.y,
    z: window.b2Aircraft.position.z
  } : null,
  b2RotationZDeg: window.b2Aircraft ? THREE.MathUtils.radToDeg(window.b2Aircraft.rotation.z).toFixed(1) : null,
  b2Scale: window.b2Aircraft ? {
    x: window.b2Aircraft.scale.x.toFixed(4),
    y: window.b2Aircraft.scale.y.toFixed(4),
    z: window.b2Aircraft.scale.z.toFixed(4)
  } : null,
  placeholderBox4Present: scene ? !!scene.getObjectByName('placeholder_box_beat_4') : false,
  baseplatePresent: scene ? !!scene.getObjectByName('Baseplate1') : false,
  spawnPresent: scene ? !!scene.getObjectByName('Spawnlocation1') : false
};

return results;
"""
scene_check = driver.execute_script(verification_script)
print("Scene Check Results:")
for k, v in scene_check.items():
    print(f"  {k}: {v}")

print("\n--- 4. Browser Console Logs ---")
console_logs = driver.get_log('browser')
for entry in console_logs:
    msg = entry['message']
    if any(tag in msg for tag in ['[Beat 4]', '[B2 Loader]', 'Roblox', 'Wingspan']):
        print(f"  [{entry['level']}] {msg}")

driver.quit()
print("\n=== TASK 4 VERIFICATION COMPLETE ===")
