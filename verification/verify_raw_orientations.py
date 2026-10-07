import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--allow-file-access-from-files')
options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

driver = webdriver.Chrome(options=options)
driver.set_window_size(1280, 800)

base_url = 'file:///c:/Users/dpset/Desktop/PROJECTS/MBD/formation-orientation-test.html'
out_dir = r'c:\Users\dpset\Desktop\PROJECTS\MBD\verification'

tests = [
    ('f16', 'top', 'raw', 'f16_raw_top.png'),
    ('f16', 'side', 'raw', 'f16_raw_side.png'),
    ('f16', 'top', 'normalized', 'f16_normalized_top.png'),
    ('f16', 'side', 'normalized', 'f16_normalized_side.png'),
    ('mig35', 'top', 'raw', 'mig35_raw_top.png'),
    ('mig35', 'side', 'raw', 'mig35_raw_side.png'),
    ('mig35', 'top', 'normalized', 'mig35_normalized_top.png'),
    ('mig35', 'side', 'normalized', 'mig35_normalized_side.png'),
]

for model, view, stage, fname in tests:
    url = f"{base_url}?model={model}&view={view}&stage={stage}"
    driver.get(url)
    WebDriverWait(driver, 10).until(lambda d: d.execute_script("return window.modelReady === true;"))
    time.sleep(0.5)
    save_path = os.path.join(out_dir, fname)
    driver.save_screenshot(save_path)
    data = driver.execute_script("return window.modelData;")
    print(f"Captured {fname}: {data}")

driver.quit()
