import os
from collections import defaultdict
from playwright.async_api import async_playwright
from dotenv import load_dotenv

load_dotenv()

LOGIN_URL = "https://vclass.unila.ac.id/login/index.php"
DASHBOARD_URL = "https://vclass.unila.ac.id/my/"

USERNAME = os.getenv("VCLASS_USERNAME")
PASSWORD = os.getenv("VCLASS_PASSWORD")


async def _login_only():
    print("🔐 [VALIDASI] Mulai login")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(LOGIN_URL)
        await page.fill('input[name="username"]', USERNAME)
        await page.fill('input[name="password"]', PASSWORD)
        await page.click('#loginbtn')
        await page.wait_for_timeout(3000)

        if "login" in page.url:
            print("❌ [VALIDASI] Login gagal")
            await browser.close()
            return None

        print("✅ [VALIDASI] Login berhasil")
        await browser.close()
        return USERNAME


async def cek_tugas_belum_dikumpulkan(progress_cb=None):
    hasil = defaultdict(list)
    print("🚀 [CEK] Mulai cek tugas")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        # ===== LOGIN =====
        if progress_cb:
            await progress_cb("🔐 Login ke VClass...")
        await page.goto(LOGIN_URL)
        await page.fill('input[name="username"]', USERNAME)
        await page.fill('input[name="password"]', PASSWORD)
        await page.click('#loginbtn')
        await page.wait_for_timeout(3000)

        if "login" in page.url:
            await browser.close()
            raise Exception("LOGIN GAGAL")

        print("✅ [CEK] Login sukses")

        # ===== DASHBOARD =====
        if progress_cb:
            await progress_cb("📚 Mengambil daftar course...")
        await page.goto(DASHBOARD_URL)

        course_links = await page.locator(
            'a[href*="/course/view.php?id="]'
        ).all()

        enrolled_courses = {}
        for a in course_links:
            url = await a.get_attribute("href")
            name = (await a.inner_text()).strip()
            if url and "id=" in url:
                cid = url.split("id=")[-1]
                enrolled_courses[cid] = name

        total_course = len(enrolled_courses)
        print(f"📘 [CEK] Total course: {total_course}")

        # ===== COURSE LOOP =====
        for idx, (cid, cname) in enumerate(enrolled_courses.items(), start=1):
            print(f"➡️ [CEK] Course {idx}/{total_course}: {cname}")

            if progress_cb:
                await progress_cb(
                    f"➡️ Scan course {idx}/{total_course}\n📘 {cname}"
                )

            course_url = f"https://vclass.unila.ac.id/course/view.php?id={cid}"
            await page.goto(course_url)

            if "/enrol/" in page.url or "/course/view.php" not in page.url:
                print("⛔ [CEK] Skip course tidak valid")
                continue

            assign_links = await page.locator(
                'a[href*="/mod/assign/view.php?id="]'
            ).all()

            assign_urls = list(set([
                await a.get_attribute("href") for a in assign_links if a
            ]))

            for assign_url in assign_urls:
                await page.goto(assign_url)

                try:
                    status_locator = page.locator(
                        "tr:has(th:text('Submission status')) td"
                    )
                    if await status_locator.count() == 0:
                        continue

                    status = await status_locator.inner_text()
                    if "No attempt" not in status and "Belum" not in status:
                        continue

                    judul = await page.locator("h2").inner_text()

                    hasil[cname].append({
                        "judul": judul.strip(),
                        "url": assign_url
                    })

                    print(f"❌ [CEK] {cname} | {judul}")

                except Exception as e:
                    print("⚠️ [CEK] Skip tugas:", e)

        await browser.close()
        print("🛑 [CEK] Selesai")

    return hasil
