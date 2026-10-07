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
# 1. External Links Verification
# -----------------------------------------------------------------------------
print("\n=== STEP 1: VERIFYING ALL EXTERNAL LINKS ===", flush=True)
links_to_verify = [
    ("Spotify Tap-Through", "https://open.spotify.com/user/314ipmyt62uzmajordk4fg3pwrmi"),
    ("F16-C Falcon (Carlos.Maciel)", "https://sketchfab.com/3d-models/f16-c-falcon-4bc2ff75dc584af2afd0aa6bd8b79015"),
    ("MiG-35 (bohmerang)", "https://sketchfab.com/3d-models/mig-35-fighter-jet-free-1dcea306e8a14ed4ab4d11a819cb6676"),
    ("MiG-21 Bison (OUTPISTON)", "https://sketchfab.com/3d-models/mig-21-bison-f60f84227a954e3293e5ccb016c2de3f"),
    ("Black Hole (NestaEric)", "https://sketchfab.com/3d-models/black-hole-e410da98b1e5445eae2acafaaa53587d"),
    ("Centrale Markthal (Jungle Jim)", "https://sketchfab.com/3d-models/centrale-markthal-amsterdam-interiorexterior-a11dee950272459b935ecb469730e6bc")
]

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

link_results = {}
for name, url in links_to_verify:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12, context=ctx) as resp:
            status = resp.status
            link_results[name] = {"url": url, "status": status, "ok": status == 200}
            print(f"  [OK] {name}: HTTP {status}", flush=True)
    except Exception as e:
        link_results[name] = {"url": url, "status": str(e), "ok": False}
        print(f"  [FAIL] {name}: {e}", flush=True)

# -----------------------------------------------------------------------------
# 2. Desktop (1440x900) Continuous Take Pass
# -----------------------------------------------------------------------------
print("\n=== STEP 2: DESKTOP (1440x900) FULL CONTINUOUS PASS ===", flush=True)
desk_options = Options()
desk_options.add_argument('--headless')
desk_options.add_argument('--disable-gpu')
desk_options.add_argument('--window-size=1440,900')
driver_desk = webdriver.Chrome(options=desk_options)

try:
    print("Cold loading index.html on Desktop...", flush=True)
    driver_desk.get(f"{base_url}/index.html")
    time.sleep(1.0)
    
    # Capture initial prank
    driver_desk.save_screenshot(os.path.join(OUT_DIR, "desktop_00_prank_initial.png"))
    
    # Wait for 3D assets to preload in background
    WebDriverWait(driver_desk, 60).until(lambda d: d.execute_script("""
        return window.blackHoleReady === true && 
               window.fighterReady === true && 
               window.b2Ready === true && 
               window.f16Ready === true && 
               window.mig35Ready === true && 
               window.hangarReady === true;
    """))
    print("All models loaded.", flush=True)

    # Trigger prank hold completion programmatically
    driver_desk.execute_script("window.prankAPI.triggerTransition();")
    time.sleep(3.0) # allow grayscale, punchline, and burn dissolve to play
    
    # Verify prank layer is removed
    prank_removed = driver_desk.execute_script("return document.getElementById('prank-layer') === null;")
    print("Prank layer cleanly removed from DOM:", prank_removed, flush=True)
    driver_desk.save_screenshot(os.path.join(OUT_DIR, "desktop_01_beat1_revealed.png"))

    # Continuous scroll through all beats
    scroll_checkpoints = [
        ("beat1", 0.04, "desktop_02_scroll_beat1.png"),
        ("beat2", 0.15, "desktop_03_scroll_beat2_warp.png"),
        ("beat3", 0.30, "desktop_04_scroll_beat3_cloud.png"),
        ("beat4", 0.50, "desktop_05_scroll_beat4_b2.png"),
        ("beat5", 0.65, "desktop_06_scroll_beat5_mig21.png"),
        ("beat6", 0.85, "desktop_07_scroll_beat6_hangar.png"),
        ("beat7", 0.95, "desktop_08_scroll_beat7_name.png"),
        ("beat8", 1.00, "desktop_09_scroll_beat8_hold.png")
    ]

    for bname, p, fname in scroll_checkpoints:
        # Scroll using lenis or direct ScrollTrigger
        driver_desk.execute_script("""
            const p = arguments[0];
            const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
            window.scrollTo(0, p * maxScroll);
            if (window.lenis) window.lenis.scrollTo(p * maxScroll, { immediate: true });
        """, p)
        time.sleep(0.5)
        driver_desk.save_screenshot(os.path.join(OUT_DIR, fname))
        print(f"  [Scrolled] {bname} (p={p}) -> {fname}", flush=True)

    # Trigger Beat 8 onLeave handoff
    print("Triggering Beat 8 handoff scroll to bottom...", flush=True)
    driver_desk.execute_script("""
        window.__skipNavigationForTest = true;
        window.triggerBeat8Handoff();
    """)
    time.sleep(1.5)
    
    overlay_opacity = driver_desk.execute_script("""
        const el = document.getElementById('scrapbook-handoff-overlay');
        return el ? parseFloat(window.getComputedStyle(el).opacity) : 0;
    """)
    print("Beat 8 Handoff overlay opacity:", overlay_opacity, flush=True)
    driver_desk.save_screenshot(os.path.join(OUT_DIR, "desktop_10_handoff_overlay.png"))

    # Cold load scrapbook.html directly
    print("\nCold loading scrapbook.html on Desktop...", flush=True)
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
    print("Scrapbook Spreads & Attribution verification:", scrapbook_dom, flush=True)

finally:
    driver_desk.quit()

# -----------------------------------------------------------------------------
# 3. Mobile (390x844) Continuous Take Pass & Telemetry
# -----------------------------------------------------------------------------
print("\n=== STEP 3: MOBILE (390x844) FULL CONTINUOUS PASS & TELEMETRY ===", flush=True)
mobile_options = Options()
mobile_options.add_argument('--headless')
mobile_options.add_argument('--disable-gpu')
mobile_options.add_argument('--window-size=390,844')
driver_mob = webdriver.Chrome(options=mobile_options)

try:
    driver_mob.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {
        "width": 390,
        "height": 844,
        "deviceScaleFactor": 2.5,
        "mobile": True
    })
    driver_mob.execute_cdp_cmd("Emulation.setTouchEmulationEnabled", {
        "enabled": True,
        "maxTouchPoints": 5
    })

    print("Cold loading index.html on Mobile...", flush=True)
    driver_mob.get(f"{base_url}/index.html")
    time.sleep(1.0)
    driver_mob.save_screenshot(os.path.join(OUT_DIR, "mobile_00_prank_initial.png"))

    WebDriverWait(driver_mob, 60).until(lambda d: d.execute_script("""
        return window.blackHoleReady === true && 
               window.fighterReady === true && 
               window.b2Ready === true && 
               window.f16Ready === true && 
               window.mig35Ready === true && 
               window.hangarReady === true;
    """))

    # Touch hold button transition
    driver_mob.execute_script("window.prankAPI.triggerTransition();")
    time.sleep(3.0)
    driver_mob.save_screenshot(os.path.join(OUT_DIR, "mobile_01_beat1_revealed.png"))

    # Continuous scroll across all beats on mobile
    for bname, p, fname in scroll_checkpoints:
        driver_mob.execute_script("""
            const p = arguments[0];
            const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
            window.scrollTo(0, p * maxScroll);
            if (window.lenis) window.lenis.scrollTo(p * maxScroll, { immediate: true });
        """, p)
        time.sleep(0.5)
        driver_mob.save_screenshot(os.path.join(OUT_DIR, f"mobile_{fname}"))
        print(f"  [Mobile Scrolled] {bname} (p={p}) -> mobile_{fname}", flush=True)

    # Cold load scrapbook.html directly on mobile
    print("\nCold loading scrapbook.html on Mobile...", flush=True)
    driver_mob.get(f"{base_url}/scrapbook.html")
    time.sleep(1.0)
    driver_mob.save_screenshot(os.path.join(OUT_DIR, "mobile_11_scrapbook_cold_load.png"))

    # -------------------------------------------------------------------------
    # 4. Final Telemetry Verification under 4x CPU Throttling
    # -------------------------------------------------------------------------
    print("\n=== STEP 4: FINAL TELEMETRY CHECK UNDER 4X CPU THROTTLING ===", flush=True)
    driver_mob.get(f"{base_url}/index.html?prankState=done")
    WebDriverWait(driver_mob, 60).until(lambda d: d.execute_script("""
        return window.blackHoleReady === true && 
               window.fighterReady === true && 
               window.b2Ready === true && 
               window.f16Ready === true && 
               window.mig35Ready === true && 
               window.hangarReady === true;
    """))

    driver_mob.execute_cdp_cmd("Emulation.setCPUThrottlingRate", {"rate": 4})
    print("Applied 4x CPU slowdown.", flush=True)

    measure_script = """
        window.__measureResult = null;
        const times = [];
        let last = performance.now();
        let count = 0;
        const maxFrames = 40;

        function loop(now) {
            const delta = now - last;
            last = now;
            times.push(delta);
            count++;
            if (count < maxFrames) {
                requestAnimationFrame(loop);
            } else {
                const sample = times.slice(3);
                const sum = sample.reduce((a, b) => a + b, 0);
                const avg = sum / sample.length;
                const min = Math.min(...sample);
                const max = Math.max(...sample);
                const fps = 1000 / avg;
                window.__measureResult = {
                    sampleCount: sample.length,
                    avgMs: Number(avg.toFixed(2)),
                    minMs: Number(min.toFixed(2)),
                    maxMs: Number(max.toFixed(2)),
                    fps: Number(fps.toFixed(1))
                };
            }
        }
        requestAnimationFrame(loop);
    """

    beats_to_profile = [
        ("Beat 1 (Black Hole)", "beat1", 0.04),
        ("Beat 3 (Cloud Layer & Fog)", "beat3", 0.23),
        ("Beat 6 (Hangar + Escort Jets)", "beat6", 0.85)
    ]

    telemetry_summary = {}
    for name, cam, prog in beats_to_profile:
        driver_mob.execute_script("window.setTestCamera(arguments[0], arguments[1]);", cam, prog)
        time.sleep(0.8)
        driver_mob.execute_script(measure_script)
        res = None
        for _ in range(40):
            time.sleep(0.3)
            res = driver_mob.execute_script("return window.__measureResult;")
            if res is not None:
                break
        telemetry_summary[name] = res
        print(f"Final Telemetry for {name}: {res}", flush=True)

    # Save full summary
    with open(os.path.join(OUT_DIR, "final_ship_telemetry.json"), "w") as f:
        json.dump({
            "externalLinks": link_results,
            "scrapbookDOM": scrapbook_dom,
            "telemetry": telemetry_summary
        }, f, indent=2)
    print(f"\nSaved final ship telemetry to {os.path.join(OUT_DIR, 'final_ship_telemetry.json')}", flush=True)

finally:
    driver_mob.quit()
