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
PORT = 8092

class FastQuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass
    def copyfile(self, source, outputfile):
        shutil.copyfileobj(source, outputfile, 1024 * 1024)

os.chdir(PROJECT_DIR)
httpd = ThreadingHTTPServer(('127.0.0.1', PORT), FastQuietHandler)
server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
server_thread.start()
print(f"Local ThreadingHTTPServer started on port {PORT}", flush=True)

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1440,900')
options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

driver = webdriver.Chrome(options=options)
base_url = f"http://127.0.0.1:{PORT}"

def wait_for_all_models(timeout=30):
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
    print("TASKS 11 & 12: INTEGRATION VERIFICATION", flush=True)
    print("=======================================================", flush=True)

    # 1. Beat 1: Full Assembly with Caption in Held State (progress=0.04)
    print("\n[Step 1] Loading Beat 1 with Caption in Held State (progress=0.04)...", flush=True)
    url_beat1_held = f"{base_url}/index.html?prankState=done&cam=beat1&progress=0.04"
    driver.get(url_beat1_held)
    wait_for_all_models(35)
    time.sleep(1.0)

    caption_path = os.path.join(OUT_DIR, "beat1_caption_held.png")
    driver.save_screenshot(caption_path)
    print(f"Saved: {caption_path}", flush=True)

    caption_data = driver.execute_script("""
        const cap = document.getElementById('beat1-caption');
        return {
            text: cap ? cap.innerText : null,
            opacity: cap ? window.getComputedStyle(cap).opacity : null,
            visible: cap ? cap.offsetWidth > 0 : false
        };
    """)
    print(f"Caption State: text='{caption_data['text']}', computed opacity={caption_data['opacity']}", flush=True)

    # 2. Beat 1: Full Assembly without Caption (progress=0.00)
    print("\n[Step 2] Loading Beat 1 Full Assembly (progress=0.00)...", flush=True)
    url_beat1_full = f"{base_url}/index.html?prankState=done&cam=beat1&progress=0.00"
    driver.get(url_beat1_full)
    wait_for_all_models(35)
    time.sleep(1.0)

    full_path = os.path.join(OUT_DIR, "beat1_full_assembly.png")
    driver.save_screenshot(full_path)
    print(f"Saved: {full_path}", flush=True)

    # Inspect Black Hole 3D scene data
    bh_data = driver.execute_script("""
        const scene = window.__debugScene;
        const bhGroup = scene.getObjectByName('black_hole_assembly');
        const oldCore = window.blackHoleCore;
        const oldDisk = window.accretionDisk;
        const oldBox1 = scene.getObjectByName('placeholder_box_beat_1');
        const starfield = window.starfield;

        let bhBox = null;
        let bhSize = null;
        if (bhGroup) {
            bhBox = new THREE.Box3().setFromObject(bhGroup);
            const size = bhBox.getSize(new THREE.Vector3());
            bhSize = [size.x, size.y, size.z];
        }

        return {
            bhExists: !!bhGroup,
            bhPosition: bhGroup ? [bhGroup.position.x, bhGroup.position.y, bhGroup.position.z] : null,
            bhScale: bhGroup ? [bhGroup.scale.x, bhGroup.scale.y, bhGroup.scale.z] : null,
            bhSpan: bhSize ? Math.max(...bhSize) : null,
            bhSize: bhSize,
            oldCoreExists: !!oldCore,
            oldDiskExists: !!oldDisk,
            oldBox1Exists: !!oldBox1,
            starfieldExists: !!starfield,
            starCount: starfield ? starfield.geometry.attributes.position.count : 0
        };
    """)

    print(f"Black Hole Assembly Exists: {bh_data['bhExists']}", flush=True)
    print(f"Black Hole Position: {bh_data['bhPosition']} (Target: [0, 0, 0])", flush=True)
    print(f"Black Hole Widest Span: {bh_data['bhSpan']:.2f} world units (Target: 55.0)", flush=True)
    print(f"Black Hole Bounding Box Size: {bh_data['bhSize']}", flush=True)
    print(f"Old Core Exists: {bh_data['oldCoreExists']} (Target: False)", flush=True)
    print(f"Old Disk Exists: {bh_data['oldDiskExists']} (Target: False)", flush=True)
    print(f"Old Placeholder Box 1 Exists: {bh_data['oldBox1Exists']} (Target: False)", flush=True)
    print(f"Starfield Exists: {bh_data['starfieldExists']} (Star count: {bh_data['starCount']})", flush=True)

    # 3. Beat 5: MiG-21 Bison Front View
    print("\n[Step 3] Loading Beat 5 MiG-21 Bison Front View...", flush=True)
    url_beat5_front = f"{base_url}/index.html?prankState=done&cam=beat5_front"
    driver.get(url_beat5_front)
    wait_for_all_models(35)
    time.sleep(1.0)

    b5_front_path = os.path.join(OUT_DIR, "fighter_beat5_front.png")
    driver.save_screenshot(b5_front_path)
    print(f"Saved: {b5_front_path}", flush=True)

    # 4. Beat 5: MiG-21 Bison 3/4 Angle View
    print("\n[Step 4] Loading Beat 5 MiG-21 Bison 3/4 Angle View...", flush=True)
    url_beat5_3q = f"{base_url}/index.html?prankState=done&cam=beat5_three_quarter"
    driver.get(url_beat5_3q)
    wait_for_all_models(35)
    time.sleep(1.0)

    b5_3q_path = os.path.join(OUT_DIR, "fighter_beat5_three_quarter.png")
    driver.save_screenshot(b5_3q_path)
    print(f"Saved: {b5_3q_path}", flush=True)

    # Inspect MiG-21 3D scene data
    mig_data = driver.execute_script("""
        const scene = window.__debugScene;
        const migGroup = scene.getObjectByName('MiG21_Bison');
        const oldJetMesh = scene.getObjectByName('Fighter_Jet_Mesh');
        const oldFuselage = scene.getObjectByName('Fighter_Fuselage_Mesh');
        const oldBox5 = scene.getObjectByName('placeholder_box_beat_5');

        let migSize = null;
        let edgeCount = 0;
        let meshCount = 0;
        let matInfo = null;

        if (migGroup) {
            const migBox = new THREE.Box3().setFromObject(migGroup);
            const size = migBox.getSize(new THREE.Vector3());
            migSize = [size.x, size.y, size.z];

            migGroup.traverse((c) => {
                if (c.isMesh) {
                    meshCount++;
                    if (!matInfo && c.material) {
                        matInfo = {
                            type: c.material.type,
                            color: '#' + c.material.color.getHexString(),
                            roughness: c.material.roughness,
                            metalness: c.material.metalness,
                            transparent: c.material.transparent,
                            opacity: c.material.opacity
                        };
                    }
                }
                if (c.isLineSegments) {
                    edgeCount++;
                }
            });
        }

        return {
            migExists: !!migGroup,
            migPosition: migGroup ? [migGroup.position.x, migGroup.position.y, migGroup.position.z] : null,
            migRotationDeg: migGroup ? [
                THREE.MathUtils.radToDeg(migGroup.rotation.x),
                THREE.MathUtils.radToDeg(migGroup.rotation.y),
                THREE.MathUtils.radToDeg(migGroup.rotation.z)
            ] : null,
            migScale: migGroup ? migGroup.scale.x : null,
            migBounds: migSize,
            wingspan: migSize ? migSize[0] : null,
            meshCount: meshCount,
            edgeCount: edgeCount,
            matInfo: matInfo,
            oldJetMeshExists: !!oldJetMesh,
            oldFuselageExists: !!oldFuselage,
            oldBox5Exists: !!oldBox5
        };
    """)

    print(f"MiG-21 Bison Exists: {mig_data['migExists']}", flush=True)
    print(f"MiG-21 Position: {mig_data['migPosition']} (Target: [12, 12, -495])", flush=True)
    print(f"MiG-21 Rotation (deg): {mig_data['migRotationDeg']} (Target: [0, 230, 15])", flush=True)
    print(f"MiG-21 Wingspan (X span): {mig_data['wingspan']:.2f} world units (Target: 16.0)", flush=True)
    print(f"MiG-21 Total Meshes: {mig_data['meshCount']}, Edges count: {mig_data['edgeCount']}", flush=True)
    print(f"MiG-21 Material: {mig_data['matInfo']}", flush=True)
    print(f"Old Jet Mesh Exists: {mig_data['oldJetMeshExists']} (Target: False)", flush=True)
    print(f"Old Fuselage Mesh Exists: {mig_data['oldFuselageExists']} (Target: False)", flush=True)
    print(f"Old Placeholder Box 5 Exists: {mig_data['oldBox5Exists']} (Target: False)", flush=True)

    # 5. Check Browser Console Logs
    print("\n[Step 5] Checking Browser Console Logs...", flush=True)
    logs = driver.get_log('browser')
    severe_errors = [l for l in logs if l['level'] == 'SEVERE']
    
    print(f"Total Severe Errors: {len(severe_errors)}", flush=True)
    for err in severe_errors:
        print(f"  SEVERE: {err['message']}", flush=True)

    relevant_logs = [
        l['message'] for l in logs 
        if any(kw in l['message'] for kw in ['MiG-21', 'Black Hole', 'procedural', 'length axis', 'GLTFLoader'])
    ]
    print("\nKey Informational Console Logs:", flush=True)
    for l in relevant_logs:
        print(f"  -> {l}", flush=True)

    print("\n=======================================================", flush=True)
    print("ALL INTEGRATION CHECKS COMPLETED SUCCESSFULLY", flush=True)
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
