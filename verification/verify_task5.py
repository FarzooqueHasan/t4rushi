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

print("=== TASK 5: VERIFYING ESCORT FIGHTER JET GEOMETRY, SCALE, MATERIALS & PLACEMENT ===")

# 1. Post-Placement Beat 5 Renders in index.html
print("\n--- 1. Capturing Beat 5 Post-Placement Renders in index.html ---")
placement_views = [
    ('beat5_front', 'fighter_beat5_front.png'),
    ('beat5_three_quarter', 'fighter_beat5_three_quarter.png')
]

for cam, filename in placement_views:
    url = f"{url_base}/index.html?prankState=done&cam={cam}"
    driver.get(url)
    WebDriverWait(driver, 15).until(lambda d: d.execute_script("return window.fighterReady === true && window.b2Ready === true;"))
    time.sleep(0.5)
    save_path = os.path.join(out_dir, filename)
    driver.save_screenshot(save_path)
    print(f"Saved {filename}")

# 2. Scene Graph and Console Inspection
print("\n--- 2. Scene Graph & Model Inspection ---")
verification_script = """
const scene = window.__debugScene;

const jet = window.fighterJet;
let jetData = null;
if (jet) {
  const box = new THREE.Box3().setFromObject(jet);
  const size = new THREE.Vector3();
  box.getSize(size);
  jetData = {
    position: { x: jet.position.x, y: jet.position.y, z: jet.position.z },
    rotationYDeg: THREE.MathUtils.radToDeg(jet.rotation.y).toFixed(1),
    rotationZDeg: THREE.MathUtils.radToDeg(jet.rotation.z).toFixed(1),
    scale: { x: jet.scale.x.toFixed(5), y: jet.scale.y.toFixed(5), z: jet.scale.z.toFixed(5) },
    worldSpanX: size.x.toFixed(2),
    worldSpanY: size.y.toFixed(2),
    worldSpanZ: size.z.toFixed(2)
  };
}

return {
  fighterJetPresent: !!jet,
  fighterJetData: jetData,
  placeholderBox5Present: scene ? !!scene.getObjectByName('placeholder_box_beat_5') : false,
  placeholderBox4Present: scene ? !!scene.getObjectByName('placeholder_box_beat_4') : false,
  b2Present: scene ? !!scene.getObjectByName('B2_Bomber') : false
};
"""
scene_check = driver.execute_script(verification_script)
print("Scene Check Results:")
for k, v in scene_check.items():
    print(f"  {k}: {v}")

print("\n--- 3. Browser Console Logs ---")
console_logs = driver.get_log('browser')
for entry in console_logs:
    msg = entry['message']
    if any(tag in msg for tag in ['[Beat 5]', '[Fighter Jet]', '[Beat 4]', '[B2 Loader]']):
        print(f"  [{entry['level']}] {msg}")

driver.quit()
print("\n=== TASK 5 VERIFICATION COMPLETE ===")
