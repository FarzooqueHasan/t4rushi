import os
import sys
import time
import shutil
import threading
import json
import urllib.request
import ssl
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"c:\Users\dpset\Desktop\PROJECTS\MBD"
OUT_DIR = os.path.join(PROJECT_DIR, "verification", "output_task19")
os.makedirs(OUT_DIR, exist_ok=True)

class FastQuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass
    def copyfile(self, source, outputfile):
        try:
            shutil.copyfileobj(source, outputfile, 1024 * 1024)
        except Exception:
            pass

os.chdir(PROJECT_DIR)
httpd = ThreadingHTTPServer(('127.0.0.1', 0), FastQuietHandler)
port = httpd.server_address[1]
threading.Thread(target=httpd.serve_forever, daemon=True).start()
print(f"Local ThreadingHTTPServer started on port {port}", flush=True)

base_url = f"http://127.0.0.1:{port}"

# -----------------------------------------------------------------------------
# 1. Performance Telemetry (Beat 1, Beat 3, Beat 6) under 4x CPU throttle
# -----------------------------------------------------------------------------
print("\n=== STEP 1: PERFORMANCE TELEMETRY UNDER 4x CPU THROTTLE ===", flush=True)

opts = Options()
opts.add_argument('--headless')
opts.add_argument('--disable-gpu')
opts.add_argument('--window-size=1440,900')
driver_telem = webdriver.Chrome(options=opts)

telemetry_results = {}
try:
    print("Loading assets for telemetry profiling...", flush=True)
    driver_telem.get(f"{base_url}/index.html")
    WebDriverWait(driver_telem, 45).until(lambda d: d.execute_script("""
        return window.blackHoleReady === true && 
               window.fighterReady === true && 
               window.b2Ready === true && 
               window.f16Ready === true && 
               window.mig35Ready === true && 
               window.hangarReady === true;
    """))
    print("Assets loaded. Applying 4x CPU throttling...", flush=True)
    driver_telem.execute_cdp_cmd("Emulation.setCPUThrottlingRate", {"rate": 4})
    
    beats_to_profile = [
        ("beat1", "beat1", 0.04),
        ("beat3", "beat3", 0.23),
        ("beat6", "beat6", 0.85)
    ]
    
    measure_script = """
    const callback = arguments[0];
    const times = [];
    let count = 0;
    let last = performance.now();
    function tick() {
        const now = performance.now();
        times.push(now - last);
        last = now;
        count++;
        if (count < 30) {
            requestAnimationFrame(tick);
        } else {
            const info = window.renderer ? window.renderer.info.render : {};
            callback({
                samples: times.slice(5),
                triangles: info.triangles || 0,
                calls: info.calls || 0
            });
        }
    }
    requestAnimationFrame(tick);
    """
    
    for b_key, cam, prog in beats_to_profile:
        driver_telem.execute_script("window.setTestCamera(arguments[0], arguments[1]);", cam, prog)
        time.sleep(1.0)
        res = driver_telem.execute_async_script(measure_script)
        s = res['samples']
        avg_ms = sum(s) / len(s)
        fps = 1000.0 / avg_ms if avg_ms > 0 else 0
        t_data = {
            "cam": cam,
            "avg_ms": round(avg_ms, 2),
            "fps": round(fps, 1),
            "triangles": res['triangles'],
            "calls": res['calls'],
            "samples_count": len(s)
        }
        telemetry_results[b_key] = t_data
        print(f"  [{b_key.upper()}] Frame Time: {t_data['avg_ms']} ms ({t_data['fps']} fps) | Triangles: {t_data['triangles']} | Calls: {t_data['calls']}", flush=True)

    driver_telem.execute_cdp_cmd("Emulation.setCPUThrottlingRate", {"rate": 1})
finally:
    driver_telem.quit()

# -----------------------------------------------------------------------------
# 2. Desktop Continuous Scroll Pass (1440x900)
# -----------------------------------------------------------------------------
print("\n=== STEP 2: DESKTOP (1440x900) FULL CONTINUOUS PASS ===", flush=True)
desk_opts = Options()
desk_opts.add_argument('--headless')
desk_opts.add_argument('--disable-gpu')
desk_opts.add_argument('--window-size=1440,900')
driver_desk = webdriver.Chrome(options=desk_opts)

try:
    print("Cold loading index.html on Desktop...", flush=True)
    driver_desk.get(f"{base_url}/index.html")
    time.sleep(1.0)
    driver_desk.save_screenshot(os.path.join(OUT_DIR, "desktop_00_prank_initial.png"))
    
    WebDriverWait(driver_desk, 40).until(lambda d: d.execute_script("""
        return window.blackHoleReady === true && 
               window.fighterReady === true && 
               window.b2Ready === true && 
               window.f16Ready === true && 
               window.mig35Ready === true && 
               window.hangarReady === true;
    """))
    
    # Trigger prank hold transition
    driver_desk.execute_script("window.prankAPI.triggerTransition();")
    time.sleep(3.0)
    driver_desk.save_screenshot(os.path.join(OUT_DIR, "desktop_01_beat1_revealed.png"))
    
    # Prevent auto-navigation when scrolling reaches Beat 8
    driver_desk.execute_script("window.__skipNavigationForTest = true;")
    
    # Scroll through each beat using window.scrollToBeat
    beats = [
        (1, "desktop_02_scroll_beat1.png"),
        (2, "desktop_03_scroll_beat2_warp.png"),
        (3, "desktop_04_scroll_beat3_cloud.png"),
        (4, "desktop_05_scroll_beat4_b2.png"),
        (5, "desktop_06_scroll_beat5_mig21.png"),
        (6, "desktop_07_scroll_beat6_hangar.png"),
        (7, "desktop_08_scroll_beat7_name.png"),
        (8, "desktop_09_scroll_beat8_hold.png")
    ]
    
    for b_id, fname in beats:
        driver_desk.execute_script(f"window.scrollToBeat({b_id}, true);")
        if b_id == 5:
            # At Beat 5 station (p=0.5893 to 0.617), nudge scroll slightly into beat range so MiG-21 body resolves
            driver_desk.execute_script("""
                const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
                window.lenis.scrollTo(0.617 * maxScroll, { immediate: true });
            """)
        time.sleep(1.2)
        driver_desk.save_screenshot(os.path.join(OUT_DIR, fname))
        info = driver_desk.execute_script("""
            return {
                scrollY: window.scrollY,
                camPos: window.camera ? [window.camera.position.x.toFixed(1), window.camera.position.y.toFixed(1), window.camera.position.z.toFixed(1)] : null,
                b2Vis: window.b2Aircraft ? window.b2Aircraft.visible : false,
                fighterVis: window.fighterJet ? window.fighterJet.visible : false,
                hangarVis: window.hangar ? window.hangar.visible : false
            };
        """)
        print(f"  [Desktop Beat {b_id}] Cam: {info['camPos']} | B2: {info['b2Vis']}, MiG: {info['fighterVis']}, Hangar: {info['hangarVis']} -> {fname}", flush=True)

    # Trigger Beat 8 onLeave handoff overlay
    print("Triggering Beat 8 handoff overlay...", flush=True)
    driver_desk.execute_script("window.triggerBeat8Handoff();")
    time.sleep(1.5)
    driver_desk.save_screenshot(os.path.join(OUT_DIR, "desktop_10_handoff_overlay.png"))
    
    # Cold load scrapbook.html on Desktop
    print("Cold loading scrapbook.html on Desktop...", flush=True)
    driver_desk.get(f"{base_url}/scrapbook.html")
    time.sleep(1.0)
    driver_desk.save_screenshot(os.path.join(OUT_DIR, "desktop_11_scrapbook_cold_load.png"))
    
    # Check all spreads and attribution footer lines on scrapbook
    scrapbook_dom = driver_desk.execute_script("""
        return {
            cover: !!document.getElementById('cover'),
            flightLog: !!document.getElementById('flight-log'),
            studio: !!document.getElementById('studio-pages'),
            mixtape: !!document.getElementById('mixtape'),
            gameday: !!document.getElementById('game-day'),
            photobooth: !!document.getElementById('photo-booth'),
            attributionCount: document.querySelectorAll('.attribution-line').length
        };
    """)
    print("Desktop Scrapbook DOM Validation:", scrapbook_dom, flush=True)
finally:
    driver_desk.quit()

# -----------------------------------------------------------------------------
# 3. Mobile Continuous Scroll Pass (390x844)
# -----------------------------------------------------------------------------
print("\n=== STEP 3: MOBILE (390x844) FULL CONTINUOUS PASS ===", flush=True)
mob_opts = Options()
mob_opts.add_argument('--headless')
mob_opts.add_argument('--disable-gpu')
mob_opts.add_argument('--window-size=390,844')
driver_mob = webdriver.Chrome(options=mob_opts)

try:
    print("Cold loading index.html on Mobile...", flush=True)
    driver_mob.get(f"{base_url}/index.html")
    time.sleep(1.0)
    driver_mob.save_screenshot(os.path.join(OUT_DIR, "mobile_00_prank_initial.png"))
    
    WebDriverWait(driver_mob, 45).until(lambda d: d.execute_script("""
        return window.blackHoleReady === true && 
               window.fighterReady === true && 
               window.b2Ready === true && 
               window.f16Ready === true && 
               window.mig35Ready === true && 
               window.hangarReady === true;
    """))
    
    driver_mob.execute_script("window.prankAPI.triggerTransition();")
    time.sleep(3.0)
    driver_mob.save_screenshot(os.path.join(OUT_DIR, "mobile_01_beat1_revealed.png"))
    
    driver_mob.execute_script("window.__skipNavigationForTest = true;")
    
    for b_id, fname in beats:
        driver_mob.execute_script(f"window.scrollToBeat({b_id}, true);")
        if b_id == 5:
            driver_mob.execute_script("""
                const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
                window.lenis.scrollTo(0.617 * maxScroll, { immediate: true });
            """)
        time.sleep(1.2)
        mob_fname = fname.replace("desktop_", "mobile_")
        driver_mob.save_screenshot(os.path.join(OUT_DIR, mob_fname))
        print(f"  [Mobile Beat {b_id}] -> {mob_fname}", flush=True)

    # Trigger handoff overlay on Mobile
    driver_mob.execute_script("window.triggerBeat8Handoff();")
    time.sleep(1.5)
    driver_mob.save_screenshot(os.path.join(OUT_DIR, "mobile_10_handoff_overlay.png"))

    # Cold load scrapbook.html on Mobile
    print("Cold loading scrapbook.html on Mobile...", flush=True)
    driver_mob.get(f"{base_url}/scrapbook.html")
    time.sleep(1.0)
    driver_mob.save_screenshot(os.path.join(OUT_DIR, "mobile_11_scrapbook_cold_load.png"))
finally:
    driver_mob.quit()

# Save final report JSON
report_file = os.path.join(OUT_DIR, "final_ship_telemetry.json")
with open(report_file, "w") as f:
    json.dump({
        "telemetry": telemetry_results,
        "verified_time": time.ctime()
    }, f, indent=2)

print("\n=== SHIP READINESS HARNESS COMPLETE ===", flush=True)
