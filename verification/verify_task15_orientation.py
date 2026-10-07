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
PORT = 8098

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
    print("TASK 15: HANGAR ORIENTATION VERIFICATION (3/4 EXTERIOR & DOWN AXIS)", flush=True)
    print("=======================================================", flush=True)

    # 1. 3/4 Exterior View
    url_3q = f"http://127.0.0.1:{PORT}/test-hangar-orientation.html?view=three_quarter"
    print(f"Loading {url_3q}...", flush=True)
    driver.get(url_3q)
    WebDriverWait(driver, 60).until(lambda d: d.execute_script("return window.modelReady === true;"))
    time.sleep(1.0)

    shot_3q = os.path.join(OUT_DIR, "hangar_orientation_three_quarter.png")
    driver.save_screenshot(shot_3q)
    print(f"Saved: {shot_3q}", flush=True)

    data = driver.execute_script("return window.hangarData;")
    print("\n--- Hangar Assembly Metrics ---", flush=True)
    print(f"Kept Groups Count: {data['keptGroupCount']}", flush=True)
    print(f"Mesh Count: {data['meshCount']}", flush=True)
    print(f"Total Vertices: {data['vertexCount']:,} (Expected: ~156k)", flush=True)
    print(f"Total Triangles: {data['triangleCount']:,}", flush=True)
    print(f"Raw Span: X={data['rawSpan'][0]:.2f}, Y={data['rawSpan'][1]:.2f}, Z={data['rawSpan'][2]:.2f}", flush=True)
    print(f"Raw Center: X={data['rawCenter'][0]:.2f}, Y={data['rawCenter'][1]:.2f}, Z={data['rawCenter'][2]:.2f}", flush=True)
    print(f"Scale Factor: {data['scaleFactor']:.6f} (90.0 / {data['rawSpan'][0]:.2f})", flush=True)
    print(f"Scaled Span: X={data['scaledSpan'][0]:.2f}, Y={data['scaledSpan'][1]:.2f}, Z={data['scaledSpan'][2]:.2f}", flush=True)

    # 2. Down Long Axis View
    url_axis = f"http://127.0.0.1:{PORT}/test-hangar-orientation.html?view=down_axis"
    print(f"\nLoading {url_axis}...", flush=True)
    driver.get(url_axis)
    WebDriverWait(driver, 60).until(lambda d: d.execute_script("return window.modelReady === true;"))
    time.sleep(1.0)

    shot_axis = os.path.join(OUT_DIR, "hangar_orientation_down_axis.png")
    driver.save_screenshot(shot_axis)
    print(f"Saved: {shot_axis}", flush=True)

    # Check console logs
    logs = driver.get_log('browser')
    errs = [l for l in logs if l['level'] in ('SEVERE', 'ERROR')]
    if errs:
        print("\nConsole errors:", flush=True)
        for err in errs:
            print(f"  [{err['level']}] {err['message']}", flush=True)
    else:
        print("\nNo console errors encountered.", flush=True)

except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    driver.quit()
    httpd.shutdown()
