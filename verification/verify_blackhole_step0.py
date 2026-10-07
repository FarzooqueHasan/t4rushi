import os
import sys
import time
import json
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"c:\Users\dpset\Desktop\PROJECTS\MBD"
OUT_DIR = os.path.join(PROJECT_DIR, "verification")
PORT = 8095

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
    url = f"http://127.0.0.1:{PORT}/test-blackhole-step0.html"
    driver.get(url)
    WebDriverWait(driver, 20).until(lambda d: d.execute_script("return window.step0Ready === true;"))
    time.sleep(1.0)

    screenshot_path = os.path.join(OUT_DIR, "blackhole_step0_loader_check.png")
    driver.save_screenshot(screenshot_path)
    print(f"Saved Step 0 screenshot: {screenshot_path}")

    report = driver.execute_script("return window.loadReport;")
    print("\n[Step 0 Load Report]")
    print(f"Loaded: {report['loaded']}")
    print(f"Error: {report['error']}")
    print(f"Warnings ({len(report['warnings'])}):")
    for w in report['warnings']:
        print(f"  WARN: {w}")
    print(f"Mesh count: {report['meshCount']}")
    print(f"Materials ({len(report['materials'])}):")
    for m in report['materials']:
        print(f"  Mesh: {m['meshName']}, MatType: {m['matType']}, MatName: {m['matName']}, hasMap: {m['hasMap']}, hasEmissiveMap: {m['hasEmissiveMap']}")

    logs = driver.get_log('browser')
    print("\n[Browser Console Logs]")
    for l in logs:
        print(f"  [{l['level']}] {l['message']}")

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
