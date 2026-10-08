import os, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

OUTPUT_DIR = "verification/output_updates"
os.makedirs(OUTPUT_DIR, exist_ok=True)

options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1280,720')
options.add_argument('--mute-audio')
driver = webdriver.Chrome(options=options)

try:
    # 1. Prank Cover (Verify no body scrollbar, guestbook button)
    driver.get("http://localhost:8080/index.html")
    time.sleep(1.5)
    driver.save_screenshot(os.path.join(OUTPUT_DIR, "1_prank_cover.png"))
    print("Captured 1_prank_cover.png")

    # 2. Test Guestbook Modal
    driver.execute_script("document.getElementById('guestbook-btn').click();")
    time.sleep(0.5)
    driver.save_screenshot(os.path.join(OUTPUT_DIR, "2_guestbook_modal.png"))
    print("Captured 2_guestbook_modal.png")
    driver.execute_script("document.getElementById('guestbook-close').click();")
    time.sleep(0.3)

    # 3. Prank Mixtape Screen (Retro Pink Turntable Record Player)
    driver.execute_script("document.getElementById('prank-mixtape').scrollIntoView();")
    time.sleep(0.5)
    driver.save_screenshot(os.path.join(OUTPUT_DIR, "3_prank_mixtape_turntable.png"))
    print("Captured 3_prank_mixtape_turntable.png")

    # Test turntable play toggle
    driver.execute_script("document.getElementById('turntable-play-btn').click();")
    time.sleep(0.5)
    driver.save_screenshot(os.path.join(OUTPUT_DIR, "3b_turntable_playing.png"))
    print("Captured 3b_turntable_playing.png")

    # 4. Prank Hold Screen ("Did you really think my design skill is this bad?")
    driver.execute_script("document.getElementById('prank-hold-screen').scrollIntoView();")
    time.sleep(0.5)
    driver.save_screenshot(os.path.join(OUTPUT_DIR, "4_prank_hold_prompt.png"))
    print("Captured 4_prank_hold_prompt.png")

    # 5. 3D Beat 1: Black Hole & Star Matrix
    driver.get("http://localhost:8080/index.html?prankState=done")
    time.sleep(2)
    # Wait for models to load
    for _ in range(25):
        ready = driver.execute_script("return window.blackHoleReady && window.b2Ready && window.fighterReady;")
        if ready:
            break
        time.sleep(0.5)

    driver.execute_script("if (window.setTestCamera) window.setTestCamera('beat1');")
    time.sleep(0.8)
    driver.save_screenshot(os.path.join(OUTPUT_DIR, "5_beat1_blackhole_matrix.png"))
    print("Captured 5_beat1_blackhole_matrix.png")

    # 6. 3D Beat 4: B-2 Stealth Bomber (No wireframes, new caption)
    driver.execute_script("if (window.setTestCamera) window.setTestCamera('beat4_front');")
    time.sleep(0.8)
    driver.save_screenshot(os.path.join(OUTPUT_DIR, "6_beat4_b2_stealth.png"))
    print("Captured 6_beat4_b2_stealth.png")

    # 7. 3D Beat 5: MiG-21 Bison (No wireframes, new compliment)
    driver.execute_script("if (window.setTestCamera) window.setTestCamera('beat5_front');")
    time.sleep(0.8)
    driver.save_screenshot(os.path.join(OUTPUT_DIR, "7_beat5_mig21.png"))
    print("Captured 7_beat5_mig21.png")

    # 8. 3D Beat 6: Formation (F-16 & MiG-35, no wireframes, Space Week / AEROSS badge)
    driver.execute_script("if (window.setTestCamera) window.setTestCamera('beat6');")
    time.sleep(0.8)
    driver.save_screenshot(os.path.join(OUTPUT_DIR, "8_beat6_formation_aeross.png"))
    print("Captured 8_beat6_formation_aeross.png")

    # 9. 3D Beat 8: End Photo (tarushi-space-end.jpg)
    driver.execute_script("if (window.setTestCamera) window.setTestCamera('beat8');")
    time.sleep(1.0)
    driver.save_screenshot(os.path.join(OUTPUT_DIR, "9_beat8_end_photo.png"))
    print("Captured 9_beat8_end_photo.png")

finally:
    driver.quit()
    print("Test run completed successfully!")
