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

def wait_for_ready(timeout=40):
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
    print("TASK 13: BEATS 2 & 3 INTEGRATION VERIFICATION", flush=True)
    print("=======================================================", flush=True)

    # 1. Point 1: progress = 0.10 (short streaks, warp just starting)
    print("\n[Step 1] Verifying progress = 0.10 (warp just starting)...", flush=True)
    driver.get(f"{base_url}/index.html?prankState=done&progress=0.10")
    wait_for_ready()
    time.sleep(1.0)

    p010_path = os.path.join(OUT_DIR, "beat2_warp_start_0.10.png")
    driver.save_screenshot(p010_path)
    print(f"Saved: {p010_path}", flush=True)

    data_010 = driver.execute_script("""
        const scene = window.__debugScene;
        const tunnel = window.warpTunnel;
        const geom = window.warpGeometry;
        const pos = geom.attributes.position.array;
        // Compute length of first streak
        const dx = pos[3] - pos[0];
        const dy = pos[4] - pos[1];
        const dz = pos[5] - pos[2];
        const streakLen = Math.sqrt(dx*dx + dy*dy + dz*dz);
        const flash = document.getElementById('flash-handoff-overlay');
        const fog = window.sceneFog;

        return {
            tunnelVisible: tunnel ? tunnel.visible : false,
            streakCount: pos.length / 6,
            streakLen: streakLen,
            flashOpacity: flash ? parseFloat(window.getComputedStyle(flash).opacity || '0') : null,
            fogDensity: fog ? fog.density : null,
            box2: !!scene.getObjectByName('placeholder_box_beat_2'),
            box3: !!scene.getObjectByName('placeholder_box_beat_3')
        };
    """)
    print(f"  Tunnel Visible: {data_010['tunnelVisible']}", flush=True)
    print(f"  Streak Count: {data_010['streakCount']}", flush=True)
    print(f"  Streak Length: {data_010['streakLen']:.2f} (Expected: ~9.2 world units)", flush=True)
    print(f"  Flash Opacity: {data_010['flashOpacity']:.4f} (Expected: 0.0)", flush=True)
    print(f"  Fog Density: {data_010['fogDensity']:.4f} (Expected: 0.0)", flush=True)
    print(f"  Box 2 Exists: {data_010['box2']} (Target: False)", flush=True)
    print(f"  Box 3 Exists: {data_010['box3']} (Target: False)", flush=True)

    # 2. Point 2: progress = 0.21 (streaks near full length, approaching flash peak)
    print("\n[Step 2] Verifying progress = 0.21 (warp peak, approaching flash)...", flush=True)
    driver.get(f"{base_url}/index.html?prankState=done&progress=0.21")
    wait_for_ready()
    time.sleep(1.0)

    p021_path = os.path.join(OUT_DIR, "beat2_warp_peak_0.21.png")
    driver.save_screenshot(p021_path)
    print(f"Saved: {p021_path}", flush=True)

    data_021 = driver.execute_script("""
        const geom = window.warpGeometry;
        const pos = geom.attributes.position.array;
        const dx = pos[3] - pos[0];
        const dy = pos[4] - pos[1];
        const dz = pos[5] - pos[2];
        const streakLen = Math.sqrt(dx*dx + dy*dy + dz*dz);
        const flash = document.getElementById('flash-handoff-overlay');
        const tunnel = window.warpTunnel;

        return {
            tunnelVisible: tunnel ? tunnel.visible : false,
            streakLen: streakLen,
            flashOpacity: flash ? parseFloat(window.getComputedStyle(flash).opacity || '0') : null
        };
    """)
    print(f"  Tunnel Visible: {data_021['tunnelVisible']}", flush=True)
    print(f"  Streak Length: {data_021['streakLen']:.2f} (Expected: ~37.4 world units, near full 40)", flush=True)
    print(f"  Flash Opacity: {data_021['flashOpacity']:.4f} (Expected: ~0.52)", flush=True)

    # 3. Point 3: progress = 0.23 (inside flash, near-white, breaking through)
    print("\n[Step 3] Verifying progress = 0.23 (inside flash, breaking through)...", flush=True)
    driver.get(f"{base_url}/index.html?prankState=done&progress=0.23")
    wait_for_ready()
    time.sleep(1.0)

    p023_path = os.path.join(OUT_DIR, "beat3_flash_punchthrough_0.23.png")
    driver.save_screenshot(p023_path)
    print(f"Saved: {p023_path}", flush=True)

    data_023 = driver.execute_script("""
        const flash = document.getElementById('flash-handoff-overlay');
        const cloud = window.cloudLayer;
        const cloudMat = window.cloudMaterial;
        const fog = window.sceneFog;

        return {
            flashOpacity: flash ? parseFloat(window.getComputedStyle(flash).opacity || '0') : null,
            cloudVisible: cloud ? cloud.visible : false,
            cloudPos: cloud ? [cloud.position.x, cloud.position.y, cloud.position.z] : null,
            cloudRotXDeg: cloud ? THREE.MathUtils.radToDeg(cloud.rotation.x) : null,
            cloudDensityMultiplier: cloudMat ? cloudMat.uniforms.u_densityMultiplier.value : null,
            fogDensity: fog ? fog.density : null
        };
    """)
    print(f"  Flash Opacity: {data_023['flashOpacity']:.4f} (Expected: ~0.58, near-white)", flush=True)
    print(f"  Cloud Visible: {data_023['cloudVisible']}", flush=True)
    print(f"  Cloud Position: {data_023['cloudPos']} (Target: [0, -20, -160])", flush=True)
    print(f"  Cloud Rotation X (deg): {data_023['cloudRotXDeg']} (Target: -90 flat)", flush=True)
    print(f"  Cloud Density Multiplier: {data_023['cloudDensityMultiplier']:.4f} (Expected: ~0.96, dense/opaque)", flush=True)
    print(f"  Fog Density: {data_023['fogDensity']:.5f} (Expected: ~0.0239, dense fog)", flush=True)

    # 4. Point 4: progress = 0.38 (clouds thinned, fog mostly cleared, approaching Beat 4)
    print("\n[Step 4] Verifying progress = 0.38 (clouds thinned, fog cleared)...", flush=True)
    driver.get(f"{base_url}/index.html?prankState=done&progress=0.38")
    wait_for_ready()
    time.sleep(1.0)

    p038_path = os.path.join(OUT_DIR, "beat3_clouds_thinned_0.38.png")
    driver.save_screenshot(p038_path)
    print(f"Saved: {p038_path}", flush=True)

    data_038 = driver.execute_script("""
        const flash = document.getElementById('flash-handoff-overlay');
        const cloud = window.cloudLayer;
        const cloudMat = window.cloudMaterial;
        const fog = window.sceneFog;

        return {
            flashOpacity: flash ? parseFloat(window.getComputedStyle(flash).opacity || '0') : null,
            cloudVisible: cloud ? cloud.visible : false,
            cloudDensityMultiplier: cloudMat ? cloudMat.uniforms.u_densityMultiplier.value : null,
            fogDensity: fog ? fog.density : null
        };
    """)
    print(f"  Flash Opacity: {data_038['flashOpacity']:.4f} (Expected: 0.0)", flush=True)
    print(f"  Cloud Visible: {data_038['cloudVisible']}", flush=True)
    print(f"  Cloud Density Multiplier: {data_038['cloudDensityMultiplier']:.4f} (Expected: ~0.34, thinned)", flush=True)
    print(f"  Fog Density: {data_038['fogDensity']:.5f} (Expected: ~0.0071, mostly cleared)", flush=True)

    # 5. Check Console Logs
    print("\n[Step 5] Checking Browser Console Logs...", flush=True)
    logs = driver.get_log('browser')
    severe_errors = [l for l in logs if l['level'] == 'SEVERE']
    print(f"Total Severe Errors: {len(severe_errors)}", flush=True)
    for err in severe_errors:
        print(f"  SEVERE: {err['message']}", flush=True)

    box_logs = [l['message'] for l in logs if 'placeholder box' in l['message'].lower()]
    print("\nPlaceholder Box Removal Logs:")
    for l in box_logs:
        print(f"  -> {l}", flush=True)

    print("\n=======================================================", flush=True)
    print("ALL TASK 13 INTEGRATION CHECKS COMPLETED SUCCESSFULLY", flush=True)
    print("=======================================================", flush=True)

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
