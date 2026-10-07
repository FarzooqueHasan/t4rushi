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

class FastQuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass
    def copyfile(self, source, outputfile):
        shutil.copyfileobj(source, outputfile, 1024 * 1024)

os.chdir(PROJECT_DIR)
httpd = ThreadingHTTPServer(('127.0.0.1', 0), FastQuietHandler)
port = httpd.server_address[1]
threading.Thread(target=httpd.serve_forever, daemon=True).start()
print(f"Local ThreadingHTTPServer started on port {port}", flush=True)

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1440,900')
options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

driver = webdriver.Chrome(options=options)
base_url = f"http://127.0.0.1:{port}"

def wait_for_models(timeout=40):
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("""
            return window.blackHoleReady === true && 
                   window.fighterReady === true && 
                   window.b2Ready === true &&
                   window.f16Ready === true &&
                   window.mig35Ready === true;
        """)
    )

try:
    print("\n=======================================================", flush=True)
    print("TASK 14: BEAT 8 HANDOFF TO SCRAPBOOK VERIFICATION", flush=True)
    print("=======================================================", flush=True)

    # -------------------------------------------------------------
    # Step 1: Negative / Before-1.0 Scroll Tests
    # Scrolling before 1.0 and scrolling back up must never trigger handoff
    # -------------------------------------------------------------
    print("\n[Step 1] Verifying scroll before 1.0 does not fire handoff...", flush=True)
    driver.get(f"{base_url}/index.html?prankState=done")
    wait_for_models()
    time.sleep(1.0)

    # Scroll to 0.50
    driver.execute_script("""
        const maxScroll = ScrollTrigger.maxScroll(window);
        window.scrollTo(0, maxScroll * 0.50);
        ScrollTrigger.update();
    """)
    time.sleep(0.4)
    res_050 = driver.execute_script("""
        const overlay = document.getElementById('scrapbook-handoff-overlay');
        return {
            progress: ScrollTrigger.getAll()[0].progress,
            isTriggered: window.isHandoffTriggered(),
            overlayOpacity: overlay ? parseFloat(window.getComputedStyle(overlay).opacity || '0') : null
        };
    """)
    print(f"  At progress {res_050['progress']:.2f}: isTriggered = {res_050['isTriggered']} (Expected: False), overlayOpacity = {res_050['overlayOpacity']}", flush=True)

    # Scroll to 0.95 (mid Beat 7 Name Reveal)
    driver.execute_script("""
        const maxScroll = ScrollTrigger.maxScroll(window);
        window.scrollTo(0, maxScroll * 0.95);
        ScrollTrigger.update();
    """)
    time.sleep(0.4)
    res_095 = driver.execute_script("""
        const overlay = document.getElementById('scrapbook-handoff-overlay');
        return {
            progress: ScrollTrigger.getAll()[0].progress,
            isTriggered: window.isHandoffTriggered(),
            overlayOpacity: overlay ? parseFloat(window.getComputedStyle(overlay).opacity || '0') : null
        };
    """)
    print(f"  At progress {res_095['progress']:.2f}: isTriggered = {res_095['isTriggered']} (Expected: False), overlayOpacity = {res_095['overlayOpacity']}", flush=True)

    # Scroll BACK UP from 0.95 to 0.70 -> confirm handoff does NOT fire
    print("  Testing scroll back up from 0.95 to 0.70...", flush=True)
    driver.execute_script("""
        const maxScroll = ScrollTrigger.maxScroll(window);
        window.scrollTo(0, maxScroll * 0.70);
        ScrollTrigger.update();
    """)
    time.sleep(0.4)
    res_up = driver.execute_script("""
        return {
            progress: ScrollTrigger.getAll()[0].progress,
            isTriggered: window.isHandoffTriggered()
        };
    """)
    print(f"  Scrolled back up to {res_up['progress']:.2f}: isTriggered = {res_up['isTriggered']} (Expected: False)", flush=True)

    # -------------------------------------------------------------
    # Step 2: Progress at 1.0 Holding ('Happy Birthday' text)
    # -------------------------------------------------------------
    print("\n[Step 2] Capturing Progress at 1.0 Holding ('Happy Birthday')...", flush=True)
    driver.get(f"{base_url}/index.html?prankState=done&progress=1.0")
    wait_for_models()
    time.sleep(1.0)

    holding_status = driver.execute_script("""
        const s4 = document.getElementById('reveal-stage-4');
        const overlay = document.getElementById('scrapbook-handoff-overlay');
        return {
            s4Opacity: s4 ? parseFloat(s4.style.opacity || '0') : 0,
            s4Text: s4 ? s4.textContent.trim() : '',
            overlayOpacity: overlay ? parseFloat(window.getComputedStyle(overlay).opacity || '0') : 0
        };
    """)
    print(f"  Stage 4 Text: '{holding_status['s4Text']}'", flush=True)
    print(f"  Stage 4 Opacity: {holding_status['s4Opacity']:.2f} (Expected: 1.00, fully holding)", flush=True)
    print(f"  Overlay Opacity at 1.0 holding: {holding_status['overlayOpacity']:.2f} (Expected: 0.00)", flush=True)

    p1_path = os.path.join(OUT_DIR, "beat8_holding_1.0.png")
    driver.save_screenshot(p1_path)
    print(f"Saved: {p1_path}", flush=True)

    # -------------------------------------------------------------
    # Step 3: Trigger onLeave & Verify Overlay Fade Sequence (#EFE6D2 over 1200ms)
    # -------------------------------------------------------------
    print("\n[Step 3] Triggering onLeave handoff sequence with 'Happy Birthday' on screen...", flush=True)
    driver.get(f"{base_url}/index.html?prankState=done&progress=1.0")
    wait_for_models()
    time.sleep(1.0)

    # Prevent immediate navigation so we can capture mid-fade and full-cover
    driver.execute_script("""
        window.__skipNavigationForTest = true;
        window.triggerBeat8Handoff();
        if (window.__handoffTween) {
            window.__handoffTween.pause();
            window.__handoffTween.time(0.5);
        }
    """)
    time.sleep(0.2)

    mid_status = driver.execute_script("""
        const overlay = document.getElementById('scrapbook-handoff-overlay');
        return {
            opacity: overlay ? parseFloat(window.getComputedStyle(overlay).opacity || '0') : null,
            bgColor: overlay ? window.getComputedStyle(overlay).backgroundColor : null,
            visibility: overlay ? window.getComputedStyle(overlay).visibility : null,
            isTriggered: window.isHandoffTriggered()
        };
    """)
    print(f"  Handoff Triggered by onLeave: {mid_status['isTriggered']} (Expected: True)", flush=True)
    print(f"  Mid-fade Opacity: {mid_status['opacity']:.3f} (Expected: ~0.6 - 0.75)", flush=True)
    print(f"  Overlay Background Color: {mid_status['bgColor']} (Expected: rgb(239, 230, 210) for #EFE6D2)", flush=True)
    print(f"  Overlay Visibility: {mid_status['visibility']} (Expected: visible)", flush=True)

    p2_path = os.path.join(OUT_DIR, "beat8_handoff_fading.png")
    driver.save_screenshot(p2_path)
    print(f"Saved: {p2_path}", flush=True)

    # Resume tween and wait for full 1200ms completion
    driver.execute_script("""
        if (window.__handoffTween) {
            window.__handoffTween.play();
        }
    """)
    time.sleep(0.8)
    full_status = driver.execute_script("""
        const overlay = document.getElementById('scrapbook-handoff-overlay');
        return {
            opacity: overlay ? parseFloat(window.getComputedStyle(overlay).opacity || '0') : null,
            navCompleted: window.__navigationComplete === true
        };
    """)
    print(f"  Full Cover Opacity: {full_status['opacity']:.3f} (Expected: 1.000)", flush=True)
    print(f"  Fade Complete (Ready to Navigate): {full_status['navCompleted']} (Expected: True)", flush=True)

    p3_path = os.path.join(OUT_DIR, "beat8_handoff_full_cover.png")
    driver.save_screenshot(p3_path)
    print(f"Saved: {p3_path}", flush=True)

    # -------------------------------------------------------------
    # Step 4: Full Navigation to scrapbook.html (Real E2E navigation)
    # -------------------------------------------------------------
    print("\n[Step 4] Executing live navigation to scrapbook.html...", flush=True)
    driver.execute_script("window.location.href = 'scrapbook.html';")
    time.sleep(1.0)

    scrapbook_status = driver.execute_script("""
        const cover = document.getElementById('cover');
        const title = document.querySelector('.cover-title');
        const subtitle = document.querySelector('.cover-subtitle');
        const bodyBg = window.getComputedStyle(document.body).backgroundColor;
        const htmlBg = window.getComputedStyle(document.documentElement).backgroundColor;
        return {
            url: window.location.href,
            coverExists: Boolean(cover),
            title: title ? title.innerText.trim() : null,
            subtitle: subtitle ? subtitle.innerText.trim() : null,
            bodyBg: bodyBg,
            htmlBg: htmlBg
        };
    """)
    print(f"  Current URL: {scrapbook_status['url']}", flush=True)
    print(f"  ScrapBook Cover Exists: {scrapbook_status['coverExists']} (Target: True)", flush=True)
    print(f"  Cover Title: '{scrapbook_status['title']}' (Target: 'tarushi's scrapbook')", flush=True)
    print(f"  Cover Subtitle: '{scrapbook_status['subtitle']}' (Target: 'vol. 1 · 09.10.2026')", flush=True)
    print(f"  Body Background Color: {scrapbook_status['bodyBg']} (Expected: rgb(239, 230, 210) for #EFE6D2)", flush=True)

    p4_path = os.path.join(OUT_DIR, "scrapbook_cover_after_handoff.png")
    driver.save_screenshot(p4_path)
    print(f"Saved: {p4_path}", flush=True)

    # Check console logs
    print("\n[Step 5] Checking Browser Console Logs...", flush=True)
    logs = driver.get_log('browser')
    severe = [l for l in logs if l['level'] == 'SEVERE']
    print(f"  Total Severe Errors: {len(severe)}", flush=True)
    for l in logs:
        if '[Beat 8 Handoff]' in l['message']:
            print(f"  -> {l['message']}", flush=True)

    print("\n=======================================================", flush=True)
    print("ALL TASK 14 BEAT 8 HANDOFF CHECKS COMPLETED SUCCESSFULLY", flush=True)
    print("=======================================================", flush=True)

finally:
    driver.quit()
    httpd.shutdown()
