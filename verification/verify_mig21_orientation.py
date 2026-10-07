import os
import sys
import time
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"c:\Users\dpset\Desktop\PROJECTS\MBD"
OUT_DIR = os.path.join(PROJECT_DIR, "verification")
PORT = 8096

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

os.chdir(PROJECT_DIR)
httpd = HTTPServer(('127.0.0.1', PORT), QuietHandler)
server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
server_thread.start()

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1440,900')
options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

driver = webdriver.Chrome(options=options)
try:
    print("\n=======================================================")
    print("MIG-21 BISON: RAW ORIENTATION CHECK")
    print("=======================================================")

    # 1. Raw Top View
    url_raw_top = f"http://127.0.0.1:{PORT}/formation-orientation-test.html?model=mig21&stage=raw&view=top"
    driver.get(url_raw_top)
    WebDriverWait(driver, 20).until(lambda d: d.execute_script("return window.modelReady === true;"))
    time.sleep(1.0)
    raw_top_path = os.path.join(OUT_DIR, "mig21_raw_top.png")
    driver.save_screenshot(raw_top_path)
    print(f"Saved: {raw_top_path}")

    # 2. Raw Side View
    url_raw_side = f"http://127.0.0.1:{PORT}/formation-orientation-test.html?model=mig21&stage=raw&view=side"
    driver.get(url_raw_side)
    WebDriverWait(driver, 20).until(lambda d: d.execute_script("return window.modelReady === true;"))
    time.sleep(1.0)
    raw_side_path = os.path.join(OUT_DIR, "mig21_raw_side.png")
    driver.save_screenshot(raw_side_path)
    print(f"Saved: {raw_side_path}")

    data_raw = driver.execute_script("return window.modelData;")
    print(f"Raw Size: X={data_raw['rawSize']['x']:.2f}, Y={data_raw['rawSize']['y']:.2f}, Z={data_raw['rawSize']['z']:.2f}")

    # 3. Normalized Top View
    url_norm_top = f"http://127.0.0.1:{PORT}/formation-orientation-test.html?model=mig21&stage=normalized&view=top"
    driver.get(url_norm_top)
    WebDriverWait(driver, 20).until(lambda d: d.execute_script("return window.modelReady === true;"))
    time.sleep(1.0)
    norm_top_path = os.path.join(OUT_DIR, "mig21_normalized_top.png")
    driver.save_screenshot(norm_top_path)
    print(f"Saved: {norm_top_path}")

    # 4. Normalized Side View
    url_norm_side = f"http://127.0.0.1:{PORT}/formation-orientation-test.html?model=mig21&stage=normalized&view=side"
    driver.get(url_norm_side)
    WebDriverWait(driver, 20).until(lambda d: d.execute_script("return window.modelReady === true;"))
    time.sleep(1.0)
    norm_side_path = os.path.join(OUT_DIR, "mig21_normalized_side.png")
    driver.save_screenshot(norm_side_path)
    print(f"Saved: {norm_side_path}")

    data_norm = driver.execute_script("return window.modelData;")
    print(f"Normalized Bounds: X={data_norm['finalSize']['x']:.2f} (Wingspan), Y={data_norm['finalSize']['y']:.2f} (Height), Z={data_norm['finalSize']['z']:.2f} (Length)")

finally:
    try:
        driver.quit()
    except Exception:
        pass
    try:
        httpd.server_close()
    except Exception:
        pass
    os._exit(0)
