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

import sys
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

print("=== TASK 7: VERIFYING BEAT 7 NAME REVEAL FOUR STAGES ===")

stages_test = [
    (0.78, 'name_reveal_stage1_0.78.png', 'Stage 1: Phi with strikethrough & caption'),
    (0.82, 'name_reveal_stage2_0.82.png', 'Stage 2: taNushi with strikethrough & caption'),
    (0.845, 'name_reveal_stage3_0.845.png', 'Stage 3: Tarushi with soft glow & caption'),
    (0.87, 'name_reveal_stage4_0.87.png', 'Stage 4: Happy Birthday large scale')
]

for progress, filename, desc in stages_test:
    url = f"{url_base}/index.html?prankState=done&progress={progress}"
    driver.get(url)
    WebDriverWait(driver, 15).until(lambda d: d.execute_script("return window.fighterReady === true && window.b2Ready === true && typeof window.getNameRevealState === 'function';"))
    time.sleep(0.5)

    state = driver.execute_script("return window.getNameRevealState();")
    save_path = os.path.join(out_dir, filename)
    driver.save_screenshot(save_path)
    print(f"\n--- Progress {progress}: {desc} ---")
    print(f"  Saved screenshot: {filename}")
    print(f"  Stage 1 (Φ) Opacity: {state['stage1']:.4f}, Strike transform: {state['strike1']}")
    print(f"  Stage 2 (taNushi) Opacity: {state['stage2']:.4f}, Strike transform: {state['strike2']}")
    print(f"  Stage 3 (Tarushi) Opacity: {state['stage3']:.4f}")
    print(f"  Stage 4 (Happy Birthday) Opacity: {state['stage4']:.4f}")

# Verification of non-overlapping transitions
print("\n--- Verifying Non-Overlap In-Between Stages ---")
test_transitions = [0.74, 0.788, 0.789, 0.828, 0.829, 0.858, 0.859, 0.875]
for p in test_transitions:
    url = f"{url_base}/index.html?prankState=done&progress={p}"
    driver.get(url)
    time.sleep(0.2)
    state = driver.execute_script("return window.getNameRevealState();")
    print(f"Progress {p:0.3f} -> S1:{state['stage1']:.2f}, S2:{state['stage2']:.2f}, S3:{state['stage3']:.2f}, S4:{state['stage4']:.2f}")

driver.quit()
print("\n=== TASK 7 VERIFICATION COMPLETE ===")
