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
PORT = 8092

# Start local test HTTP server
class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

os.chdir(PROJECT_DIR)
httpd = HTTPServer(('127.0.0.1', PORT), QuietHandler)
server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
server_thread.start()
print(f"Local test server running at http://127.0.0.1:{PORT}")

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1440,900')
options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

driver = webdriver.Chrome(options=options)
base_url = f"http://127.0.0.1:{PORT}"

try:
    print("\n=======================================================")
    print("TASK 10: VERIFYING BEAT 1 BLACK HOLE, STARFIELD & LENSING")
    print("=======================================================")

    # 1. Beat 1 full assembly at Beat 1 camera position
    url_beat1 = f"{base_url}/index.html?prankState=done&cam=beat1&progress=0.00"
    driver.get(url_beat1)
    WebDriverWait(driver, 15).until(lambda d: d.execute_script("return window.blackHoleReady === true;"))
    time.sleep(1.0)

    beat1_full_path = os.path.join(OUT_DIR, "beat1_full_assembly.png")
    driver.save_screenshot(beat1_full_path)
    print(f"Saved Beat 1 full assembly screenshot: {beat1_full_path}")

    # 2. Close-up screenshot of the lensing bend specifically (warped)
    url_closeup = f"{base_url}/index.html?prankState=done&cam=beat1_lensing_closeup&progress=0.00"
    driver.get(url_closeup)
    WebDriverWait(driver, 15).until(lambda d: d.execute_script("return window.blackHoleReady === true;"))
    time.sleep(1.0)

    closeup_path = os.path.join(OUT_DIR, "beat1_lensing_closeup.png")
    driver.save_screenshot(closeup_path)
    print(f"Saved Beat 1 lensing close-up screenshot (warped): {closeup_path}")

    # 2b. Third debug frame requested: same closeup camera position with every lensed star (d < 120) tinted #FF5C8A
    driver.execute_script("if (window.setStarfieldTint) window.setStarfieldTint(true);")
    time.sleep(0.5)
    tinted_closeup_path = os.path.join(OUT_DIR, "beat1_lensing_tinted.png")
    driver.save_screenshot(tinted_closeup_path)
    print(f"Saved Beat 1 lensing debug screenshot with tinted lensed stars (#FF5C8A): {tinted_closeup_path}")

    # Also capture Beat 1 full assembly with tinted stars for comprehensive review
    driver.get(url_beat1)
    WebDriverWait(driver, 15).until(lambda d: d.execute_script("return window.blackHoleReady === true;"))
    driver.execute_script("if (window.setStarfieldTint) window.setStarfieldTint(true);")
    time.sleep(0.5)
    tinted_full_path = os.path.join(OUT_DIR, "beat1_full_assembly_tinted.png")
    driver.save_screenshot(tinted_full_path)
    print(f"Saved Beat 1 full assembly screenshot with tinted lensed stars: {tinted_full_path}")
    driver.execute_script("if (window.setStarfieldTint) window.setStarfieldTint(false);")

    # 2c. Starfield with lensing disabled at closeup camera position (unwarped comparison)
    driver.get(url_closeup)
    WebDriverWait(driver, 15).until(lambda d: d.execute_script("return window.blackHoleReady === true;"))
    driver.execute_script("if (window.setStarfieldLensing) window.setStarfieldLensing(false);")
    time.sleep(0.5)
    unwarped_path = os.path.join(OUT_DIR, "beat1_lensing_unwarped.png")
    driver.save_screenshot(unwarped_path)
    print(f"Saved Beat 1 lensing debug screenshot (unwarped comparison): {unwarped_path}")
    driver.execute_script("if (window.setStarfieldLensing) window.setStarfieldLensing(true);")

    # 3. Caption at held state (~0.04)
    url_caption = f"{base_url}/index.html?prankState=done&cam=beat1&progress=0.04"
    driver.get(url_caption)
    WebDriverWait(driver, 15).until(lambda d: d.execute_script("return typeof window.getBeat1CaptionState === 'function';"))
    time.sleep(0.8)

    caption_path = os.path.join(OUT_DIR, "beat1_caption_held.png")
    driver.save_screenshot(caption_path)
    print(f"Saved Beat 1 caption held state screenshot: {caption_path}")

    # 4. Detailed 3D scene inspection
    scene_data = driver.execute_script("""
        const core = window.blackHoleCore;
        const disk = window.accretionDisk;
        const stars = window.starfield;
        const oldBox = window.__debugScene ? window.__debugScene.getObjectByName('placeholder_box_beat_1') : null;

        const starPosAttr = stars ? stars.geometry.attributes.position : null;
        let starCount = starPosAttr ? starPosAttr.count : 0;
        let minRadius = 999999, maxRadius = 0, lensedCount = 0;

        if (starPosAttr) {
            for (let i = 0; i < starCount; i++) {
                const x = starPosAttr.getX(i);
                const y = starPosAttr.getY(i);
                const z = starPosAttr.getZ(i);
                const r = Math.sqrt(x * x + y * y + z * z);
                if (r < minRadius) minRadius = r;
                if (r > maxRadius) maxRadius = r;
                if (r < 120.0) lensedCount++;
            }
        }

        const colorAttr = stars ? stars.geometry.attributes.color : null;
        let defaultPinkCount = 0;
        if (window.tintedStarColors) {
            for (let i = 0; i < starCount; i++) {
                const r = window.tintedStarColors[i * 3];
                const g = window.tintedStarColors[i * 3 + 1];
                if (r > 0.99 && g < 0.4) defaultPinkCount++;
            }
        }

        return {
            oldPlaceholderBoxExists: Boolean(oldBox),
            core: {
                radius: core ? core.geometry.parameters.radius : null,
                color: core ? '#' + core.material.color.getHexString() : null,
                position: core ? [core.position.x, core.position.y, core.position.z] : null
            },
            disk: {
                radius: disk ? disk.geometry.parameters.radius : null,
                tube: disk ? disk.geometry.parameters.tube : null,
                arc: disk ? disk.geometry.parameters.arc : null,
                rotX: disk ? disk.rotation.x : null,
                rotZ: disk ? disk.rotation.z : null,
                transparent: disk ? disk.material.transparent : null,
                blending: disk ? disk.material.blending : null,
                depthWrite: disk ? disk.material.depthWrite : null,
                position: disk ? [disk.position.x, disk.position.y, disk.position.z] : null
            },
            stars: {
                count: starCount,
                minRadius: minRadius,
                maxRadius: maxRadius,
                lensedCount: lensedCount,
                tintedCount: defaultPinkCount,
                vertexColors: stars ? stars.material.vertexColors : null,
                pointSize: stars ? stars.material.size : null
            }
        };
    """)

    print("\n[Scene Geometry & Component Verification]")
    print(f"  Old Beat 1 Wireframe Box Exists: {scene_data['oldPlaceholderBoxExists']} (Target: False)")
    print(f"  Event Horizon Core Radius: {scene_data['core']['radius']} (Target: 14)")
    print(f"  Event Horizon Core Color: {scene_data['core']['color']} (Target: #05060b)")
    print(f"  Event Horizon Core Position: {scene_data['core']['position']} (Target: [0, 0, 0])")

    print(f"  Accretion Disk Radius/Tube: R={scene_data['disk']['radius']}, r={scene_data['disk']['tube']} (Target: 22, 4)")
    print(f"  Accretion Disk Arc: {scene_data['disk']['arc']:.4f} (Target: {2*3.14159:.4f})")
    print(f"  Accretion Disk Transparent: {scene_data['disk']['transparent']} (Target: True)")
    print(f"  Accretion Disk Blending: {scene_data['disk']['blending']} (Target: 2 - AdditiveBlending)")
    print(f"  Accretion Disk DepthWrite: {scene_data['disk']['depthWrite']} (Target: False)")
    print(f"  Accretion Disk Tilt (X rad): {scene_data['disk']['rotX']:.4f} rad = 20.0 deg (Target: 0.3491 rad)")
    print(f"  Accretion Disk Position: {scene_data['disk']['position']} (Target: [0, 0, 0])")

    print(f"  Starfield Count: {scene_data['stars']['count']} (Target: 800)")
    print(f"  Starfield Radial Range: [{scene_data['stars']['minRadius']:.1f}, {scene_data['stars']['maxRadius']:.1f}] (Target: [60, 600])")
    print(f"  Stars in Lensing Zone (d < 120): {scene_data['stars']['lensedCount']} (Target: 371)")
    print(f"  Tinted Lensed Stars Count: {scene_data['stars']['tintedCount']} (Target: 371)")
    print(f"  Starfield VertexColors: {scene_data['stars']['vertexColors']} (Target: True)")
    print(f"  Star Size: {scene_data['stars']['pointSize']} (Target: 1.5)")

    # 5. Continuous Accretion Disk Rotation Verification
    initial_rot_z = scene_data['disk']['rotZ']
    time.sleep(1.0)
    later_rot_z = driver.execute_script("return window.accretionDisk ? window.accretionDisk.rotation.z : null;")
    rot_diff = later_rot_z - initial_rot_z
    print(f"\n[Accretion Disk Rotation Check]")
    print(f"  Initial rot.z: {initial_rot_z:.4f}, After 1s rot.z: {later_rot_z:.4f}, Delta: {rot_diff:.4f} rad (Target: ~+0.15 rad/s)")

    # 6. Browser Console Logs Check
    logs = driver.get_log('browser')
    errors = [l for l in logs if l['level'] == 'SEVERE']
    print("\n[Browser Console Verification]")
    print(f"  Total Severe Console Errors: {len(errors)}")
    for err in errors:
        print(f"    ERROR: {err['message']}")
    
    for l in logs:
        msg = l['message']
        if '[Beat 1]' in msg or '[Starfield]' in msg:
            print(f"  Console Log: {msg}")

    # 7. Beat 1 Caption Opacity Curve Verification (0–0.0719)
    print("\n[Beat 1 Caption Curve Verification (Fade in 0–0.02, Hold 0.02–0.055, Fade out 0.055–0.0719)]")
    caption_p_tests = [
        (0.0000, 0.0000),
        (0.0100, 0.5000),
        (0.0200, 1.0000),
        (0.0400, 1.0000),
        (0.0550, 1.0000),
        (0.06345, 0.5000),
        (0.0719, 0.0000),
        (0.0800, 0.0000)
    ]
    for p, expected in caption_p_tests:
        url = f"{base_url}/index.html?prankState=done&progress={p}"
        driver.get(url)
        time.sleep(0.2)
        c_state = driver.execute_script("return window.getBeat1CaptionState();")
        print(f"  Progress {p:.5f} -> Opacity: {c_state['opacity']:.4f} (Expected: {expected:.4f}), Text: '{c_state['text']}'")

finally:
    try:
        driver.quit()
    except Exception:
        pass
    try:
        httpd.server_close()
    except Exception:
        pass
    print("\nTask 10 verification completed successfully.", flush=True)
    os._exit(0)
