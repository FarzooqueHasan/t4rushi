import os
import sys
import time
import shutil
import threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"c:\Users\dpset\Desktop\PROJECTS\MBD"
OUT_DIR = os.path.join(PROJECT_DIR, "verification")
PORT = 8103

class FastQuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass
    def copyfile(self, source, outputfile):
        shutil.copyfileobj(source, outputfile, 1024 * 1024)

os.chdir(PROJECT_DIR)
httpd = ThreadingHTTPServer(('127.0.0.1', PORT), FastQuietHandler)
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
    print("TASK 15: BEAT 6 HANGAR ASSEMBLY & PERFORMANCE VERIFICATION", flush=True)
    print("=======================================================", flush=True)

    url = f"http://127.0.0.1:{PORT}/index.html?prankState=done&cam=beat6&progress=0.85"
    print(f"Loading {url}...", flush=True)
    driver.get(url)

    # Wait for all Beat 6 assets to be ready
    WebDriverWait(driver, 60).until(lambda d: d.execute_script(
        "return window.f16Ready === true && window.mig35Ready === true && window.hangarReady === true;"
    ))
    time.sleep(1.5)

    shot_path = os.path.join(OUT_DIR, "beat6_hangar_assembly.png")
    driver.save_screenshot(shot_path)
    print(f"Saved: {shot_path}", flush=True)

    # Retrieve assembly metrics
    hangar_metrics = driver.execute_script("return window.hangarMetrics;")
    renderer_info = driver.execute_script("""
        const r = window.renderer;
        return {
            triangles: r.info.render.triangles,
            lines: r.info.render.lines,
            points: r.info.render.points,
            calls: r.info.render.calls,
            geometries: r.info.memory.geometries,
            textures: r.info.memory.textures
        };
    """)

    # Measure frame render times across 60 frames
    perf_data = driver.execute_async_script("""
        const callback = arguments[arguments.length - 1];
        let frameTimes = [];
        let lastTime = performance.now();
        let frameCount = 0;
        const targetFrames = 60;

        function recordFrame() {
            const now = performance.now();
            frameTimes.push(now - lastTime);
            lastTime = now;
            frameCount++;
            if (frameCount < targetFrames) {
                requestAnimationFrame(recordFrame);
            } else {
                const avg = frameTimes.reduce((a, b) => a + b, 0) / frameTimes.length;
                const min = Math.min(...frameTimes);
                const max = Math.max(...frameTimes);
                callback({
                    avgFrameTimeMs: avg,
                    minFrameTimeMs: min,
                    maxFrameTimeMs: max,
                    approxFps: 1000 / avg
                });
            }
        }
        requestAnimationFrame(recordFrame);
    """)

    print("\n--- Beat 6 Hangar Metrics ---", flush=True)
    print(f"Kept Node Groups: {hangar_metrics['keptGroups']}", flush=True)
    print(f"Total Vertices: {hangar_metrics['vertices']:,}", flush=True)
    print(f"Total Triangles (Geometry): {hangar_metrics['triangles']:,}", flush=True)
    print(f"Scale Factor: {hangar_metrics['scaleFactor']:.6f}", flush=True)
    print(f"Placement Position: {hangar_metrics['position']}", flush=True)

    print("\n--- Renderer Info (Single Frame) ---", flush=True)
    print(f"Triangles Rendered: {renderer_info['triangles']:,}", flush=True)
    print(f"Draw Calls: {renderer_info['calls']}", flush=True)
    print(f"Active Geometries: {renderer_info['geometries']}", flush=True)
    print(f"Active Textures: {renderer_info['textures']}", flush=True)

    print("\n--- Performance Note (60 Frame Benchmark) ---", flush=True)
    print(f"Average Frame Time: {perf_data['avgFrameTimeMs']:.2f} ms", flush=True)
    print(f"Min Frame Time: {perf_data['minFrameTimeMs']:.2f} ms", flush=True)
    print(f"Max Frame Time: {perf_data['maxFrameTimeMs']:.2f} ms", flush=True)
    print(f"Estimated FPS: {perf_data['approxFps']:.1f} fps", flush=True)

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
