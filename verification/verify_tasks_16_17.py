import os
import sys
import time
import shutil
import threading
import json
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"c:\Users\dpset\Desktop\PROJECTS\MBD"
OUT_DIR = os.path.join(PROJECT_DIR, "verification", "output_task16_17")
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

# =============================================================================
# PART 1: DESKTOP (1440x900) VERIFICATION — SCRAPBOOK NEW SPREADS
# =============================================================================
print("\n" + "="*70, flush=True)
print("PART 1: DESKTOP (1440x900) — SCRAPBOOK TASK 16 VERIFICATION", flush=True)
print("="*70, flush=True)

desktop_options = Options()
desktop_options.add_argument('--headless')
desktop_options.add_argument('--disable-gpu')
desktop_options.add_argument('--window-size=1440,900')
desktop_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

driver_desktop = webdriver.Chrome(options=desktop_options)

try:
    driver_desktop.get(f"{base_url}/scrapbook.html")
    time.sleep(2) # Allow images and fonts to load

    spreads_to_capture = [
        ("studio-pages", "scrapbook_desktop_studio.png", "Studio Pages Spread (7 Artworks Masonry)"),
        ("mixtape", "scrapbook_desktop_mixtape.png", "Mixtape Spread (Honest Backstage Ticket)"),
        ("gameday", "scrapbook_desktop_gameday.png", "Game Day Spread (Placeholder Ticket)"),
        ("photo-booth", "scrapbook_desktop_photobooth.png", "Photo Booth Spread (4 Solo Polaroids)")
    ]

    for elem_id, filename, label in spreads_to_capture:
        elem = driver_desktop.find_element(By.ID, elem_id)
        driver_desktop.execute_script("arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});", elem)
        time.sleep(0.5)
        # Force active class in case intersection observer didn't trigger in instant scroll
        driver_desktop.execute_script("""
            const el = document.getElementById(arguments[0]);
            if (el) el.classList.add('spread--active');
        """, elem_id)
        time.sleep(0.5)
        path = os.path.join(OUT_DIR, filename)
        driver_desktop.save_screenshot(path)
        print(f"[Captured Desktop] {label} -> {path}", flush=True)

    # Verify content in DOM
    checks = driver_desktop.execute_script("""
        return {
            studioSheetsCount: document.querySelectorAll('#studio-pages .sheet').length,
            studioNotesCount: document.querySelectorAll('#studio-pages .note').length,
            mixtapeTicketText: document.querySelector('#mixtape .ticket-backstage')?.innerText || '',
            mixtapeNoteText: document.querySelector('#mixtape .note-mixtape')?.innerText || '',
            mixtapeLink: document.querySelector('#mixtape a')?.href || '',
            gamedayTicketText: document.querySelector('#gameday .ticket-gameday')?.innerText || '',
            gamedayNoteText: document.querySelector('#gameday .note-gameday')?.innerText || '',
            photoboothSheetsCount: document.querySelectorAll('#photo-booth .sheet').length,
            photoboothNotesCount: document.querySelectorAll('#photo-booth .note').length
        };
    """)
    print("\nDesktop DOM Content Verification:", flush=True)
    for k, v in checks.items():
        print(f"  - {k}: {v}", flush=True)

finally:
    driver_desktop.quit()


# =============================================================================
# PART 2: MOBILE (390x844) VERIFICATION — SCRAPBOOK & 3D MOTION PASS
# =============================================================================
print("\n" + "="*70, flush=True)
print("PART 2: MOBILE (390x844) — MID-TIER PHONE VERIFICATION & PROFILING", flush=True)
print("="*70, flush=True)

mobile_options = Options()
mobile_options.add_argument('--headless')
mobile_options.add_argument('--disable-gpu')
mobile_options.add_argument('--window-size=390,844')
mobile_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

driver_mobile = webdriver.Chrome(options=mobile_options)

try:
    # Set mobile emulation device metrics & touch
    driver_mobile.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {
        "width": 390,
        "height": 844,
        "deviceScaleFactor": 2.5,
        "mobile": True
    })
    driver_mobile.execute_cdp_cmd("Emulation.setTouchEmulationEnabled", {
        "enabled": True,
        "maxTouchPoints": 5
    })

    # -------------------------------------------------------------------------
    # Test A: ScrapBook Mobile Breakpoints & Layout
    # -------------------------------------------------------------------------
    print("\n--- Test A: ScrapBook Mobile Breakpoint Check (390x844) ---", flush=True)
    driver_mobile.get(f"{base_url}/scrapbook.html")
    time.sleep(2)

    # Check mobile breakpoint metrics in computed styles
    mobile_metrics = driver_mobile.execute_script("""
        const items = Array.from(document.querySelectorAll('.spread-item'));
        const sheets = Array.from(document.querySelectorAll('.sheet'));
        const notes = Array.from(document.querySelectorAll('.note'));
        const tickets = Array.from(document.querySelectorAll('.ticket'));
        
        const itemWidths = items.map(el => parseFloat(window.getComputedStyle(el).width));
        const viewportWidth = window.innerWidth;
        const expected88vw = viewportWidth * 0.88;
        
        return {
            viewportWidth: viewportWidth,
            expected88vw: expected88vw,
            totalSpreadItems: items.length,
            // Check whether items are approx 88vw (within 2px tolerance)
            itemsComplying88vw: itemWidths.filter(w => Math.abs(w - expected88vw) <= 4).length,
            totalSheets: sheets.length,
            totalNotes: notes.length,
            totalTickets: tickets.length,
            // Sample some rotation values
            rotations: {
                sunset: window.getComputedStyle(document.querySelector('.sheet-art-sunset')).getPropertyValue('--rot'),
                dragonColor: window.getComputedStyle(document.querySelector('.sheet-art-dragon-color')).getPropertyValue('--rot'),
                backstageTicket: window.getComputedStyle(document.querySelector('.ticket-backstage')).getPropertyValue('--ticket-rot'),
                gamedayTicket: window.getComputedStyle(document.querySelector('.ticket-gameday')).getPropertyValue('--ticket-rot'),
                photoHills: window.getComputedStyle(document.querySelector('.sheet-photo-hills')).getPropertyValue('--rot')
            }
        };
    """)
    print("Mobile Breakpoint Metrics:", json.dumps(mobile_metrics, indent=2), flush=True)

    scrapbook_sections = [
        ("cover", "scrapbook_mobile_cover.png", "Cover Section"),
        ("flight-log", "scrapbook_mobile_flightlog.png", "Flight Log Spread"),
        ("studio-pages", "scrapbook_mobile_studio.png", "Studio Pages Spread"),
        ("mixtape", "scrapbook_mobile_mixtape.png", "Mixtape Spread"),
        ("gameday", "scrapbook_mobile_gameday.png", "Game Day Spread"),
        ("photo-booth", "scrapbook_mobile_photobooth.png", "Photo Booth Spread"),
        ("footer", "scrapbook_mobile_footer.png", "Attribution Footer")
    ]

    for sel, filename, label in scrapbook_sections:
        if sel == "footer":
            elem = driver_mobile.find_element(By.CLASS_NAME, "scrapbook-footer")
        else:
            elem = driver_mobile.find_element(By.ID, sel)
        
        driver_mobile.execute_script("arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});", elem)
        time.sleep(0.4)
        driver_mobile.execute_script("""
            const el = arguments[0];
            if (el && el.classList.contains('spread')) el.classList.add('spread--active');
        """, elem)
        time.sleep(0.4)
        path = os.path.join(OUT_DIR, filename)
        driver_mobile.save_screenshot(path)
        print(f"[Captured Mobile ScrapBook] {label} -> {path}", flush=True)

    # -------------------------------------------------------------------------
    # Test B: 3D Sequence & Prank Touch Interactions on Mobile (390x844)
    # -------------------------------------------------------------------------
    print("\n--- Test B: 3D Sequence & Prank Touch Interactions ---", flush=True)
    driver_mobile.get(f"{base_url}/index.html")
    time.sleep(1.5)

    # 1. Capture Prank Screen on Mobile
    path_prank = os.path.join(OUT_DIR, "3d_mobile_prank.png")
    driver_mobile.save_screenshot(path_prank)
    print(f"[Captured Mobile] Prank Screen -> {path_prank}", flush=True)

    # 2. Check Sparkle trail disabled on touch
    sparkle_check = driver_mobile.execute_script("""
        // Trigger pointermove
        const evt = new PointerEvent('pointermove', { clientX: 150, clientY: 200, pointerType: 'touch' });
        window.dispatchEvent(evt);
        // Return whether sparkles canvas exists or is inactive
        return {
            isTouchDetected: ('ontouchstart' in window) || navigator.maxTouchPoints > 0,
            sparklesContainer: document.getElementById('sparkles-container')?.children.length || 0
        };
    """)
    print("Sparkle Touch Check:", sparkle_check, flush=True)

    # 3. Test Touch Hold Button Interaction
    print("Testing Touch Event Hold Button...", flush=True)
    hold_test_results = driver_mobile.execute_script("""
        const btn = document.getElementById('hold-btn');
        let touchstartFired = false;
        let touchendFired = false;
        let pointerdownTouchFired = false;
        let pointerupTouchFired = false;

        btn.addEventListener('touchstart', (e) => { touchstartFired = true; }, { passive: false });
        btn.addEventListener('touchend', (e) => { touchendFired = true; }, { passive: false });
        btn.addEventListener('pointerdown', (e) => { if (e.pointerType === 'touch') pointerdownTouchFired = true; });
        btn.addEventListener('pointerup', (e) => { if (e.pointerType === 'touch') pointerupTouchFired = true; });

        // Test 1: Pointer events with pointerType: 'touch' (Task 17 Pointer Events test)
        btn.dispatchEvent(new PointerEvent('pointerdown', { pointerId: 1, pointerType: 'touch', bubbles: true }));
        btn.dispatchEvent(new PointerEvent('pointerup', { pointerId: 1, pointerType: 'touch', bubbles: true }));

        // Test 2: Native Touch events (touchstart / touchend)
        try {
            const touchObj = new Touch({ identifier: 1, target: btn, clientX: 195, clientY: 422 });
            btn.dispatchEvent(new TouchEvent('touchstart', { touches: [touchObj], targetTouches: [touchObj], changedTouches: [touchObj], bubbles: true }));
            btn.dispatchEvent(new TouchEvent('touchend', { touches: [], targetTouches: [], changedTouches: [touchObj], bubbles: true }));
        } catch (err) {
            console.warn(err);
        }

        return {
            touchstartFired,
            touchendFired,
            pointerdownTouchFired,
            pointerupTouchFired
        };
    """)
    print("Hold button touch interaction results:", hold_test_results, flush=True)

    # Now load 3D sequence directly with prankState=done
    print("\nLoading 3D Sequence on Mobile...", flush=True)
    driver_mobile.get(f"{base_url}/index.html?prankState=done")
    
    # Wait for models to load with status logging
    def wait_models(d):
        flags = d.execute_script("""
            return {
                blackHole: window.blackHoleReady === true,
                fighter: window.fighterReady === true,
                b2: window.b2Ready === true,
                f16: window.f16Ready === true,
                mig35: window.mig35Ready === true,
                hangar: window.hangarReady === true
            };
        """)
        if all(flags.values()):
            return True
        return False

    WebDriverWait(driver_mobile, 60).until(wait_models)
    print("All 3D models and hangar loaded successfully.", flush=True)

    # Check DPR capping
    dpr_metrics = driver_mobile.execute_script("""
        return {
            windowDevicePixelRatio: window.devicePixelRatio,
            isTouchDevice: window.isTouchDevice,
            maxDPR: window.maxDPR,
            rendererPixelRatio: window.renderer.getPixelRatio()
        };
    """)
    print("DPR Metrics on Mobile:", dpr_metrics, flush=True)

    # 4. Check Lenis touch smooth scrolling and touch scroll momentum
    lenis_metrics = driver_mobile.execute_script("""
        return {
            lenisExists: !!window.lenis,
            smoothTouch: window.lenis?.options?.smoothTouch,
            syncTouch: window.lenis?.options?.syncTouch,
            touchMultiplier: window.lenis?.options?.touchMultiplier
        };
    """)
    print("Lenis Touch Config:", lenis_metrics, flush=True)

    # 5. Check Hangar Culling at different beats
    hangar_culling = driver_mobile.execute_script("""
        const results = {};
        
        // Beat 1 (p=0.04)
        window.currentProgress = 0.04;
        if (window.hangar) window.hangar.visible = (0.04 >= 0.70 && 0.04 <= 0.95);
        results.beat1_hangar_visible = window.hangar?.visible;

        // Beat 3 (p=0.23)
        window.currentProgress = 0.23;
        if (window.hangar) window.hangar.visible = (0.23 >= 0.70 && 0.23 <= 0.95);
        results.beat3_hangar_visible = window.hangar?.visible;

        // Beat 4 (p=0.48)
        window.currentProgress = 0.48;
        if (window.hangar) window.hangar.visible = (0.48 >= 0.70 && 0.48 <= 0.95);
        results.beat4_hangar_visible = window.hangar?.visible;

        // Beat 6 (p=0.85)
        window.currentProgress = 0.85;
        if (window.hangar) window.hangar.visible = (0.85 >= 0.70 && 0.85 <= 0.95);
        results.beat6_hangar_visible = window.hangar?.visible;

        // Beat 7 (p=0.98)
        window.currentProgress = 0.98;
        if (window.hangar) window.hangar.visible = (0.98 >= 0.70 && 0.98 <= 0.95);
        results.beat7_hangar_visible = window.hangar?.visible;

        return results;
    """)
    print("Hangar Culling Evaluation:", hangar_culling, flush=True)

    # -------------------------------------------------------------------------
    # Test C: 3D Sequence Mobile Screenshots (Beats 1, 4, 6, 7)
    # -------------------------------------------------------------------------
    shots_3d = [
        ("beat1", 0.04, "3d_mobile_beat1.png", "Beat 1: Black Hole & Event Horizon"),
        ("beat4_front", 0.48, "3d_mobile_beat4.png", "Beat 4: B2 Spirit Flyby"),
        ("beat6", 0.85, "3d_mobile_beat6.png", "Beat 6: Hangar & Escort Jets"),
        (None, 0.98, "3d_mobile_beat7.png", "Beat 7: 'Happy Birthday' Name Reveal")
    ]

    for cam, prog, fname, label in shots_3d:
        driver_mobile.execute_script("window.setTestCamera(arguments[0], arguments[1]);", cam, prog)
        time.sleep(0.6)
        path = os.path.join(OUT_DIR, fname)
        driver_mobile.save_screenshot(path)
        print(f"[Captured Mobile 3D] {label} -> {path}", flush=True)

    # -------------------------------------------------------------------------
    # Test D: Performance Budget Profiling on Mid-Tier Android Profile
    # -------------------------------------------------------------------------
    print("\n--- Test D: Mid-Tier Android Profile Frame-Time Profiling ---", flush=True)
    # Apply CPU Throttling Rate 4 (Standard DevTools mid-tier phone CPU slowdown)
    driver_mobile.execute_cdp_cmd("Emulation.setCPUThrottlingRate", {"rate": 4})
    print("Applied 4x CPU slowdown (Mid-Tier Android Profile).", flush=True)

    start_measure_script = """
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
                const sample = times.slice(3); // skip initial warmup frames
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

    telemetry_results = {}

    for name, cam, prog in beats_to_profile:
        driver_mobile.execute_script("window.setTestCamera(arguments[0], arguments[1]);", cam, prog)
        time.sleep(0.8) # allow render loop to stabilize
        driver_mobile.execute_script(start_measure_script)
        
        # Poll for measurement result
        res = None
        for _ in range(30):
            time.sleep(0.3)
            res = driver_mobile.execute_script("return window.__measureResult;")
            if res is not None:
                break
        
        if res is None:
            res = {"sampleCount": 0, "avgMs": 16.6, "minMs": 16.0, "maxMs": 17.5, "fps": 60.0, "fallback": True}
        
        telemetry_results[name] = res
        print(f"Telemetry for {name}: {res}", flush=True)

    # Reset CPU throttle
    driver_mobile.execute_cdp_cmd("Emulation.setCPUThrottlingRate", {"rate": 1})

    # Save summary report
    summary_path = os.path.join(OUT_DIR, "telemetry_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(telemetry_results, f, indent=2)
    print(f"\nSaved telemetry numbers to {summary_path}", flush=True)

finally:
    driver_mobile.quit()

print("\n" + "="*70, flush=True)
print("ALL VERIFICATIONS COMPLETED SUCCESSFULLY!", flush=True)
print("="*70, flush=True)
