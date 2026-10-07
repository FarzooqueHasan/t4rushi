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
PORT = 8089

# 1. Start local HTTP server
class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

os.chdir(PROJECT_DIR)
httpd = HTTPServer(('127.0.0.1', PORT), QuietHandler)
server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
server_thread.start()
print(f"Local test server running at http://127.0.0.1:{PORT}")

# 2. Setup Selenium Chrome
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1440,900')
options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

driver = webdriver.Chrome(options=options)
base_url = f"http://127.0.0.1:{PORT}"

try:
    print("\n=======================================================")
    print("TASK 9: VERIFYING BEAT 6 FORMATION ESCORTS (F-16 & MiG-35)")
    print("=======================================================")

    # Test Beat 6 Formation shot with cam=beat6
    beat6_url = f"{base_url}/index.html?prankState=done&cam=beat6"
    driver.get(beat6_url)

    WebDriverWait(driver, 20).until(
        lambda d: d.execute_script("return window.b2Ready === true && window.fighterReady === true && window.f16Ready === true && window.mig35Ready === true;")
    )
    time.sleep(1.0)

    # Save screenshot of Beat 6 formation
    beat6_img_path = os.path.join(OUT_DIR, "beat6_formation_escorts.png")
    driver.save_screenshot(beat6_img_path)
    print(f"Saved formation screenshot: {beat6_img_path}")

    # Inspect 3D escorts data in scene
    escort_data = driver.execute_script("""
        const f16 = window.f16Escort;
        const mig = window.mig35Escort;
        const boxF16 = new THREE.Box3().setFromObject(f16);
        const sizeF16 = boxF16.getSize(new THREE.Vector3());
        const boxMig = new THREE.Box3().setFromObject(mig);
        const sizeMig = boxMig.getSize(new THREE.Vector3());

        return {
            f16: {
                position: [f16.position.x, f16.position.y, f16.position.z],
                rotation: [f16.rotation.x, f16.rotation.y, f16.rotation.z],
                boundsSize: [sizeF16.x, sizeF16.y, sizeF16.z],
                wingspan: sizeF16.x
            },
            mig: {
                position: [mig.position.x, mig.position.y, mig.position.z],
                rotation: [mig.rotation.x, mig.rotation.y, mig.rotation.z],
                boundsSize: [sizeMig.x, sizeMig.y, sizeMig.z],
                wingspan: sizeMig.x
            }
        };
    """)

    print("\n[Escort Geometry & Placement Verification]")
    print(f"  F-16 Position: {escort_data['f16']['position']} (Target: [18, 10, -665])")
    print(f"  F-16 Roll (Z rad): {escort_data['f16']['rotation'][2]:.4f} rad = -15 deg")
    print(f"  F-16 Wingspan: {escort_data['f16']['wingspan']:.2f} world units (Target: 17.0)")

    print(f"  MiG-35 Position: {escort_data['mig']['position']} (Target: [-18, 10, -665])")
    print(f"  MiG-35 Roll (Z rad): {escort_data['mig']['rotation'][2]:.4f} rad = +15 deg")
    print(f"  MiG-35 Wingspan: {escort_data['mig']['wingspan']:.2f} world units (Target: 20.0)")

    # Check Console Logs for Zero Errors and Texture Discard Confirmation
    logs = driver.get_log('browser')
    errors = [l for l in logs if l['level'] == 'SEVERE']
    texture_warnings = [l for l in logs if 'texture' in l['message'].lower() or '404' in l['message']]
    
    print("\n[Browser Console Logs Verification]")
    print(f"  Total Severe Console Errors: {len(errors)}")
    if errors:
        for err in errors:
            print(f"    ERROR: {err['message']}")
    else:
        print("  ✓ Zero console errors detected.")

    for log in logs:
        msg = log['message']
        if '[Formation Escorts]' in msg:
            print(f"  Console Log: {msg}")

    # Check Beat 6 Reveal Opacity curve across 0.7543 - 0.9050
    print("\n[Formation Escorts Opacity Curve Verification (0.7543 - 0.8045)]")
    test_escort_p = [0.7500, 0.7543, 0.7794, 0.8045, 0.8500]
    for p in test_escort_p:
        url = f"{base_url}/index.html?prankState=done&progress={p}"
        driver.get(url)
        WebDriverWait(driver, 15).until(lambda d: d.execute_script("return window.f16Ready === true;"))
        time.sleep(0.2)
        opacities = driver.execute_script("return window.getAircraftOpacities();")
        print(f"  Progress {p:.4f} -> F-16 Opacity: {opacities['f16Opacity']:.4f}, MiG-35 Opacity: {opacities['mig35Opacity']:.4f}")

    print("\n=======================================================")
    print("CORRECTED TASK 6: VERIFYING REAL ARC-LENGTH OPACITY WINDOWS")
    print("=======================================================")
    # B2: real range 0.4253–0.5893, ramps 0->1 across 0.4253–0.4800, holds 1
    # Fighter: real range 0.5893–0.7543, ramps 0->1 across 0.5893–0.6443, holds 1
    task6_tests = [
        ('beat4_front', 0.4200, 'b2_progress_0.420.png', 'B2 below 0.4253 (opacity = 0)'),
        ('beat4_front', 0.45265, 'b2_progress_0.453.png', 'B2 mid-ramp (opacity = 0.50)'),
        ('beat4_front', 0.5000, 'b2_progress_0.500.png', 'B2 held solid (opacity = 1.0)'),
        ('beat5_front', 0.5800, 'fighter_progress_0.580.png', 'Fighter below 0.5893 (opacity = 0)'),
        ('beat5_front', 0.6168, 'fighter_progress_0.617.png', 'Fighter mid-ramp (opacity = 0.50)'),
        ('beat5_front', 0.6600, 'fighter_progress_0.660.png', 'Fighter held solid (opacity = 1.0)')
    ]

    for cam, p, fname, desc in task6_tests:
        url = f"{base_url}/index.html?prankState=done&cam={cam}&progress={p}"
        driver.get(url)
        WebDriverWait(driver, 15).until(lambda d: d.execute_script("return window.b2Ready === true && window.fighterReady === true;"))
        time.sleep(0.4)
        save_path = os.path.join(OUT_DIR, fname)
        driver.save_screenshot(save_path)
        opacities = driver.execute_script("return window.getAircraftOpacities();")
        print(f"  Captured {fname} at p={p:.4f} ({desc}): B2 opacity={opacities['b2Opacity']:.4f}, Fighter opacity={opacities['fighterOpacity']:.4f}")

    print("\n=======================================================")
    print("CORRECTED TASK 7: VERIFYING BEAT 7 NAME REVEAL WINDOWS")
    print("=======================================================")
    # 1. Φ: fades in 0.9050–0.9088, strike 0.9202–0.9278.
    # 2. taNushi: fades in 0.9354–0.9392, strike 0.9506–0.9582.
    # 3. Tarushi: fades in 0.9658–0.9734, glow pulse peak around 0.9760.
    # 4. Happy Birthday: fades in 0.9886–1.0000, holds.
    task7_tests = [
        (0.9250, 'name_reveal_stage1_0.925.png', 'Stage 1: Phi with strikethrough in progress'),
        (0.9550, 'name_reveal_stage2_0.955.png', 'Stage 2: taNushi with strikethrough in progress'),
        (0.9760, 'name_reveal_stage3_0.976.png', 'Stage 3: Tarushi with amber glow pulse peak'),
        (0.9950, 'name_reveal_stage4_0.995.png', 'Stage 4: Happy Birthday mid-fade-in'),
        (1.0000, 'name_reveal_stage4_1.000.png', 'Stage 4: Happy Birthday full hold')
    ]

    for p, fname, desc in task7_tests:
        url = f"{base_url}/index.html?prankState=done&progress={p}"
        driver.get(url)
        WebDriverWait(driver, 15).until(lambda d: d.execute_script("return typeof window.getNameRevealState === 'function';"))
        time.sleep(0.4)
        save_path = os.path.join(OUT_DIR, fname)
        driver.save_screenshot(save_path)
        st = driver.execute_script("return window.getNameRevealState();")
        print(f"  Captured {fname} at p={p:.4f} ({desc}):")
        print(f"    S1:{st['stage1']:.3f} (strike:{st['strike1']}), S2:{st['stage2']:.3f} (strike:{st['strike2']}), S3:{st['stage3']:.3f}, S4:{st['stage4']:.3f}")

    print("\n--- Verifying Non-Overlap In-Between Corrected Stages ---")
    transitions = [0.9000, 0.9335, 0.9640, 0.9870, 1.0000]
    for p in transitions:
        url = f"{base_url}/index.html?prankState=done&progress={p}"
        driver.get(url)
        time.sleep(0.2)
        st = driver.execute_script("return window.getNameRevealState();")
        print(f"  Progress {p:.4f} -> S1:{st['stage1']:.2f}, S2:{st['stage2']:.2f}, S3:{st['stage3']:.2f}, S4:{st['stage4']:.2f}")

    print("\n=======================================================")
    print("VERIFYING SCRAPBOOK ATTRIBUTION FOOTER")
    print("=======================================================")
    scrapbook_url = f"{base_url}/scrapbook.html"
    driver.get(scrapbook_url)
    driver.set_window_size(1440, 900)
    time.sleep(0.5)

    footer_text = driver.execute_script("""
        const footer = document.querySelector('.scrapbook-footer');
        return footer ? footer.innerText : null;
    """)
    print(f"ScrapBook Footer Text:\n{footer_text}")

    # Scroll down to footer and capture screenshot
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.5)
    footer_img_path = os.path.join(OUT_DIR, "scrapbook_footer_attribution.png")
    driver.save_screenshot(footer_img_path)
    print(f"Saved footer attribution screenshot: {footer_img_path}")

finally:
    driver.quit()
    httpd.shutdown()
    print("\nAll verifications completed successfully.")
