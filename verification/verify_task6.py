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

print("=== TASK 6: VERIFYING SCROLL-DRIVEN AIRCRAFT OPACITY RESOLUTION ===")

# Test cases:
# B2 (Beat 4): progress 0.37 (edges only), 0.40 (partway), 0.42 (fully solid)
# Fighter jet (Beat 5): progress 0.49 (edges only), 0.52 (partway), 0.55 (fully solid)
shots = [
    ('beat4_front', 0.37, 'b2_progress_0.37.png'),
    ('beat4_front', 0.40, 'b2_progress_0.40.png'),
    ('beat4_front', 0.42, 'b2_progress_0.42.png'),
    ('beat5_front', 0.49, 'fighter_progress_0.49.png'),
    ('beat5_front', 0.52, 'fighter_progress_0.52.png'),
    ('beat5_front', 0.55, 'fighter_progress_0.55.png'),
]

for cam, progress, filename in shots:
    url = f"{url_base}/index.html?prankState=done&cam={cam}&progress={progress}"
    driver.get(url)
    WebDriverWait(driver, 15).until(lambda d: d.execute_script("return window.fighterReady === true && window.b2Ready === true;"))
    time.sleep(0.5)

    opacities = driver.execute_script("return window.getAircraftOpacities ? window.getAircraftOpacities() : null;")
    save_path = os.path.join(out_dir, filename)
    driver.save_screenshot(save_path)
    print(f"Captured {filename} at progress={progress}: B2 opacity={opacities['b2Opacity']:.4f}, Fighter opacity={opacities['fighterOpacity']:.4f}")

driver.quit()
print("\n=== TASK 6 VERIFICATION COMPLETE ===")
