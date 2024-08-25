from playwright.sync_api import sync_playwright
import time


def screenshot_page(page, folder: str = "./images", prefix: str = "screenshot"):
    timestamp = int(time.time())
    page.screenshot(path=f'{folder}/{prefix}_{timestamp}.png', full_page=True)



def check_bookings_for_passport(take_screenshots: bool = True, screenshot_folder: str = "./images", headless: bool = True):

    url = "https://www.exteriores.gob.es/Consulados/guayaquil/es/ServiciosConsulares/Paginas/index.aspx?scco=Ecuador&scd=149&scca=Pasaportes+y+otros+documentos&scs=Pasaportes+-+Requisitos+y+procedimiento+para+obtenerlo"
    there_are_bookings = False

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        browser_context = browser.new_context()
        page = browser_context.new_page()

        # enter to main site
        page.goto(url)
        link = page.query_selector('a[href*="https://bit.ly/3KWUtqC"]')
        page.evaluate("(link) => link.removeAttribute('target')", link)
        link.click()
        time.sleep(5)

        # click on captch button
        print(page.title())
        button = page.query_selector('#idCaptchaButton')
    
        if button is None:
            return there_are_bookings
    
        button.click()
        time.sleep(20)

        # click on accept terms and conditions
        button = page.query_selector('#bktContinue')
        if button is None:
            return there_are_bookings
        
        button.click()
        time.sleep(5)

        # select type of service 
        # button = page.query_selector('a[href*="#selectservice/bkt1003838"]') # entrega de pasaporte
        button = page.query_selector('a[href*="#selectservice/bkt992332"]') # solicitud renovar pasaporte

        if button is None:
            return there_are_bookings
    
        button.click()
        time.sleep(20)

        not_available_text = page.query_selector("#idDivNotAvailableSlotsTextTop")
        date_picker = page.query_selector("#idDivBktDatetimeDatePickerContent")

        if not_available_text is not None:
            if not not_available_text.is_visible():
                if take_screenshots:
                    screenshot_page(page, screenshot_folder)
                there_are_bookings = True
        else:
            if date_picker is not None:
                if date_picker.is_visible():
                   if take_screenshots:
                    screenshot_page(page, screenshot_folder)
                   there_are_bookings = True

        browser_context.close()
        browser.close()

    return there_are_bookings