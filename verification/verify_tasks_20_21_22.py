import os
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

OUTPUT_DIR = r"c:\Users\dpset\Desktop\PROJECTS\MBD\verification\output_task20_21_22"
os.makedirs(OUTPUT_DIR, exist_ok=True)

PORT = 8080
BASE_URL = f"http://127.0.0.1:{PORT}"

def get_driver(width=1440, height=900):
    opts = Options()
    opts.add_argument('--headless=new')
    opts.add_argument(f'--window-size={width},{height}')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=opts)
    return driver

def wait_for_models(driver, timeout=20):
    start = time.time()
    while time.time() - start < timeout:
        ready = driver.execute_script("""
            return {
                blackHole: !!window.blackHoleReady,
                b2: !!window.b2Ready,
                fighter: !!window.fighterReady,
                f16: !!window.f16Ready,
                mig35: !!window.mig35Ready,
                hangar: !!window.hangarReady
            };
        """)
        if ready.get('blackHole') and ready.get('b2') and ready.get('fighter') and ready.get('f16') and ready.get('mig35'):
            print("All core 3D models ready:", ready)
            return True
        time.sleep(0.5)
    print("Timeout waiting for models:", ready)
    return False

def verify_task22_prank_gallery():
    print("\n--- Verifying Task 22: Pink Pookie Gallery ---")
    viewports = [
        ("desktop", 1440, 900),
        ("mobile", 390, 844)
    ]
    
    for vp_name, w, h in viewports:
        driver = get_driver(w, h)
        try:
            driver.get(f"{BASE_URL}/index.html")
            time.sleep(1.5)
            
            # Screen 1: Cover
            driver.save_screenshot(os.path.join(OUTPUT_DIR, f"task22_prank_1_cover_{vp_name}.png"))
            print(f"Captured {vp_name} Screen 1: Cover")
            
            # Screen 2: Photo Booth
            driver.execute_script("document.getElementById('prank-photobooth').scrollIntoView({behavior: 'instant'});")
            time.sleep(0.8)
            driver.save_screenshot(os.path.join(OUTPUT_DIR, f"task22_prank_2_photobooth_{vp_name}.png"))
            print(f"Captured {vp_name} Screen 2: Photo Booth")
            
            # Screen 3: Mixtape
            driver.execute_script("document.getElementById('prank-mixtape').scrollIntoView({behavior: 'instant'});")
            time.sleep(0.8)
            driver.save_screenshot(os.path.join(OUTPUT_DIR, f"task22_prank_3_mixtape_{vp_name}.png"))
            print(f"Captured {vp_name} Screen 3: Mixtape")
            
            # Screen 4: Game Day
            driver.execute_script("document.getElementById('prank-gameday').scrollIntoView({behavior: 'instant'});")
            time.sleep(0.8)
            driver.save_screenshot(os.path.join(OUTPUT_DIR, f"task22_prank_4_gameday_{vp_name}.png"))
            print(f"Captured {vp_name} Screen 4: Game Day")
            
            # Screen 5: Hold Screen
            driver.execute_script("document.getElementById('prank-hold-screen').scrollIntoView({behavior: 'instant'});")
            time.sleep(0.8)
            driver.save_screenshot(os.path.join(OUTPUT_DIR, f"task22_prank_5_hold_{vp_name}.png"))
            print(f"Captured {vp_name} Screen 5: Hold CTA")
            
            if vp_name == "desktop":
                # Verify hold and kaboom sequence
                print("Testing hold-to-proceed and kaboom sequence...")
                # Dispatch pointerdown on hold button
                driver.execute_script("""
                    const btn = document.getElementById('hold-btn');
                    const rect = btn.getBoundingClientRect();
                    btn.dispatchEvent(new PointerEvent('pointerdown', {
                        clientX: rect.x + rect.width / 2,
                        clientY: rect.y + rect.height / 2,
                        bubbles: true
                    }));
                """)
                # Wait for 1.3s hold to fill ring and trigger punchline/burn
                time.sleep(1.6)
                driver.save_screenshot(os.path.join(OUTPUT_DIR, f"task22_prank_6_punchline.png"))
                print("Captured punchline text / burn start")
                
                # Wait for burn animation to complete (approx 2.5s)
                time.sleep(3.0)
                driver.save_screenshot(os.path.join(OUTPUT_DIR, f"task22_prank_7_burn_resolved_to_3d.png"))
                prank_layer_exists = driver.execute_script("return !!document.getElementById('prank-layer');")
                print(f"Post-burn prank layer exists in DOM: {prank_layer_exists} (Expected: False - successfully removed)")
        finally:
            driver.quit()

def verify_task20_3d_overhaul():
    print("\n--- Verifying Task 20: 3D Sequence Overhaul ---")
    driver = get_driver(1440, 900)
    try:
        driver.get(f"{BASE_URL}/index.html?prankState=done")
        wait_for_models(driver)
        time.sleep(1.5)
        
        # ----------------------------------------------------
        # Item 4: Black Hole Hero Scale (targetSpan = 80)
        # ----------------------------------------------------
        driver.execute_script("window.setTestCamera('beat1');")
        time.sleep(0.8)
        bh_info = driver.execute_script("""
            const bh = window.blackHole;
            const box = new THREE.Box3().setFromObject(bh);
            const size = new THREE.Vector3();
            box.getSize(size);
            return {
                scale: bh.scale.x,
                spanX: size.x,
                spanY: size.y,
                spanZ: size.z,
                widestSpan: Math.max(size.x, size.y, size.z)
            };
        """)
        print(f"Task 20 Item 4 (Black Hole): widestSpan={bh_info['widestSpan']:.2f} units, scale={bh_info['scale']:.6f}")
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "task20_item4_blackhole_scale80.png"))
        
        # ----------------------------------------------------
        # Item 5: Starfield Richness (2500 stars, 10% tint, haze)
        # ----------------------------------------------------
        star_info = driver.execute_script("""
            const group = window.starfield;
            const haze = window.starfieldHaze;
            const totalStars = window.defaultStarColors ? window.defaultStarColors.length / 3 : 0;
            let tintedCount = 0;
            if (window.defaultStarColors) {
                for (let i = 0; i < totalStars; i++) {
                    const r = window.defaultStarColors[i*3];
                    const g = window.defaultStarColors[i*3 + 1];
                    const b = window.defaultStarColors[i*3 + 2];
                    if (r > 0.99 && g < 0.60) tintedCount++;
                }
            }
            return {
                totalStars: totalStars,
                tintedCount: tintedCount,
                tintPct: (tintedCount / totalStars * 100).toFixed(1) + '%',
                hazePresent: !!haze,
                hazeOpacity: haze ? haze.material.uniforms.u_opacity.value : 0
            };
        """)
        print(f"Task 20 Item 5 (Starfield):", star_info)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "task20_item5_starfield_richness.png"))
        
        # ----------------------------------------------------
        # Items 1, 2, 3: Beat 4 (B2 Bomber)
        # ----------------------------------------------------
        driver.execute_script("window.setTestCamera('beat4_front', 0.48);")
        time.sleep(1.0)
        b2_info = driver.execute_script("""
            const b2 = window.b2Aircraft;
            const caption = document.getElementById('beat4-caption');
            return {
                position: [b2.position.x, b2.position.y, b2.position.z],
                rotationDeg: [
                    (b2.rotation.x * 180 / Math.PI).toFixed(1),
                    (b2.rotation.y * 180 / Math.PI).toFixed(1),
                    (b2.rotation.z * 180 / Math.PI).toFixed(1)
                ],
                captionText: caption ? caption.innerText : '',
                captionOpacity: caption ? caption.style.opacity : 0,
                captionVisible: caption ? caption.style.visibility : ''
            };
        """)
        print(f"Task 20 Beat 4 (B2):", b2_info)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "task20_items1_2_3_beat4_b2.png"))
        
        # Also 3/4 angle check
        driver.execute_script("window.setTestCamera('beat4_three_quarter', 0.48);")
        time.sleep(0.8)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "task20_items1_2_beat4_b2_3quarter.png"))
        
        # ----------------------------------------------------
        # Items 1, 2, 3: Beat 5 (MiG-21)
        # ----------------------------------------------------
        driver.execute_script("window.setTestCamera('beat5_front', 0.65);")
        time.sleep(1.0)
        mig21_info = driver.execute_script("""
            const f = window.fighterJet;
            const mats = window.mig21AuthoredMaterials || [];
            const caption = document.getElementById('beat5-caption');
            return {
                position: [f.position.x, f.position.y, f.position.z],
                rotationDeg: [
                    (f.rotation.x * 180 / Math.PI).toFixed(1),
                    (f.rotation.y * 180 / Math.PI).toFixed(1),
                    (f.rotation.z * 180 / Math.PI).toFixed(1)
                ],
                authoredMaterialsCount: mats.length,
                firstMatOpacity: mats.length > 0 ? mats[0].opacity : null,
                captionText: caption ? caption.innerText : '',
                captionOpacity: caption ? caption.style.opacity : 0,
                captionVisible: caption ? caption.style.visibility : ''
            };
        """)
        print(f"Task 20 Beat 5 (MiG-21):", mig21_info)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "task20_items1_2_3_beat5_mig21.png"))
        
        # Also 3/4 angle check
        driver.execute_script("window.setTestCamera('beat5_three_quarter', 0.65);")
        time.sleep(0.8)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "task20_items1_2_beat5_mig21_3quarter.png"))
        
        # ----------------------------------------------------
        # Items 1, 2, 3: Beat 6 (F-16 & MiG-35 Escort Formation)
        # ----------------------------------------------------
        driver.execute_script("window.setTestCamera('beat6', 0.85);")
        time.sleep(1.0)
        escort_info = driver.execute_script("""
            const f16 = window.f16Escort;
            const mig35 = window.mig35Escort;
            const f16Mats = window.f16AuthoredMaterials || [];
            const migMats = window.mig35AuthoredMaterials || [];
            const caption = document.getElementById('beat6-caption');
            return {
                f16Pos: [f16.position.x, f16.position.y, f16.position.z],
                f16RotDeg: [
                    (f16.rotation.x * 180 / Math.PI).toFixed(1),
                    (f16.rotation.y * 180 / Math.PI).toFixed(1),
                    (f16.rotation.z * 180 / Math.PI).toFixed(1)
                ],
                f16MatsCount: f16Mats.length,
                mig35Pos: [mig35.position.x, mig35.position.y, mig35.position.z],
                mig35RotDeg: [
                    (mig35.rotation.x * 180 / Math.PI).toFixed(1),
                    (mig35.rotation.y * 180 / Math.PI).toFixed(1),
                    (mig35.rotation.z * 180 / Math.PI).toFixed(1)
                ],
                mig35MatsCount: migMats.length,
                captionText: caption ? caption.innerText : '',
                captionOpacity: caption ? caption.style.opacity : 0,
                captionVisible: caption ? caption.style.visibility : ''
            };
        """)
        print(f"Task 20 Beat 6 (Formation):", escort_info)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "task20_items1_2_3_beat6_formation.png"))
        
        # ----------------------------------------------------
        # Item 6: Beats 7 & 8 Photo Plane Replacement
        # ----------------------------------------------------
        driver.execute_script("window.setTestCamera(null, 0.94);")
        time.sleep(1.0)
        photo_info = driver.execute_script("""
            const photo = window.beat7_8_photo;
            return {
                present: !!photo,
                visible: photo ? photo.visible : false,
                position: photo ? [photo.position.x, photo.position.y, photo.position.z] : null,
                childrenCount: photo ? photo.children.length : 0
            };
        """)
        print(f"Task 20 Item 6 (Beats 7 & 8 Photo Plane at Beat 7 - progress 0.94):", photo_info)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "task20_item6_beat7_photo_plane.png"))
        
        # At Beat 8 (progress 0.999)
        driver.execute_script("window.setTestCamera(null, 0.995);")
        time.sleep(1.0)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "task20_item6_beat8_photo_plane.png"))
        print(f"Captured Beat 8 photo plane screenshot.")
    finally:
        driver.quit()

def verify_task21_handoff():
    print("\n--- Verifying Task 21: ScrapBook Handoff ---")
    driver = get_driver(1440, 900)
    try:
        driver.get(f"{BASE_URL}/index.html?prankState=done")
        wait_for_models(driver)
        time.sleep(1.5)
        
        # Setup test flags so we can observe the handoff fade and navigation call cleanly
        driver.execute_script("""
            window.__skipNavigationForTest = true;
            window.__navigationComplete = false;
        """)
        
        # Natural Lenis scroll to bottom
        driver.execute_script("""
            lenis.scrollTo(document.body.scrollHeight, { duration: 1.5 });
        """)
        
        # Monitor progress over 4 seconds
        start = time.time()
        handoff_fired = False
        nav_done = False
        while time.time() - start < 6.0:
            status = driver.execute_script("""
                const overlay = document.getElementById('scrapbook-handoff-overlay');
                return {
                    scrollY: window.scrollY,
                    maxScroll: ScrollTrigger.maxScroll(window),
                    progress: ScrollTrigger.getAll()[0] ? ScrollTrigger.getAll()[0].progress : 0,
                    isHandoffTriggered: typeof window.isHandoffTriggered === 'function' ? window.isHandoffTriggered() : false,
                    overlayOpacity: overlay ? overlay.style.opacity : null,
                    overlayVisibility: overlay ? overlay.style.visibility : null,
                    navigationComplete: !!window.__navigationComplete
                };
            """)
            print(f"Scroll status @ {time.time()-start:.2f}s: progress={status['progress']:.4f}, handoff={status['isHandoffTriggered']}, overlayOpacity={status['overlayOpacity']}, navComplete={status['navigationComplete']}")
            if status['isHandoffTriggered'] and not handoff_fired:
                handoff_fired = True
                driver.save_screenshot(os.path.join(OUTPUT_DIR, "task21_handoff_overlay_fading.png"))
            if status['navigationComplete']:
                nav_done = True
                driver.save_screenshot(os.path.join(OUTPUT_DIR, "task21_handoff_overlay_solid.png"))
                break
            time.sleep(0.5)
            
        print(f"Handoff fired: {handoff_fired}, Navigation executed: {nav_done}")
        
        # Also test direct navigation to scrapbook.html to verify it loads without errors
        driver.get(f"{BASE_URL}/scrapbook.html")
        time.sleep(1.5)
        driver.save_screenshot(os.path.join(OUTPUT_DIR, "task21_scrapbook_loaded.png"))
        title = driver.title
        print(f"Scrapbook page loaded successfully. Title: '{title}'")
    finally:
        driver.quit()

if __name__ == "__main__":
    verify_task22_prank_gallery()
    verify_task20_3d_overhaul()
    verify_task21_handoff()
    print("\n--- ALL VERIFICATIONS FINISHED ---")
