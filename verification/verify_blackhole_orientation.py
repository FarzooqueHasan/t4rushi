import os
import sys
import time
import shutil
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"c:\Users\dpset\Desktop\PROJECTS\MBD"
OUT_DIR = os.path.join(PROJECT_DIR, "verification")
PORT = 8097

class FastQuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass
    def copyfile(self, source, outputfile):
        shutil.copyfileobj(source, outputfile, 1024 * 1024)

os.chdir(PROJECT_DIR)
httpd = HTTPServer(('127.0.0.1', PORT), FastQuietHandler)
server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
server_thread.start()

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1440,900')
options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

driver = webdriver.Chrome(options=options)
try:
    print("\n=======================================================", flush=True)
    print("BLACK HOLE: ORIENTATION CHECK AT BEAT 1 CAMERA", flush=True)
    print("=======================================================", flush=True)

    url = f"http://127.0.0.1:{PORT}/test-blackhole-orientation.html"
    driver.get(url)
    WebDriverWait(driver, 45).until(lambda d: d.execute_script("return window.testReady === true;"))
    time.sleep(1.0)

    screenshot_path = os.path.join(OUT_DIR, "blackhole_orientation_check.png")
    driver.save_screenshot(screenshot_path)
    print(f"Saved: {screenshot_path}", flush=True)

    data = driver.execute_script("return window.testData;")
    print(f"Raw Kept Size: X={data['rawSize']['x']:.1f}, Y={data['rawSize']['y']:.1f}, Z={data['rawSize']['z']:.1f}", flush=True)
    print(f"Widest Span: {data['widestSpan']:.1f}", flush=True)
    print(f"Scale Factor: {data['scaleFactor']:.6f}", flush=True)
    print(f"Final Scaled Size: X={data['finalSize']['x']:.2f}, Y={data['finalSize']['y']:.2f}, Z={data['finalSize']['z']:.2f}", flush=True)
    print(f"Planet Excluded: {data['planetExcluded']}", flush=True)

except Exception as e:
    import traceback
    traceback.print_exc()

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
