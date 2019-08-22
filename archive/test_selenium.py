from selenium import webdriver

driver = webdriver.Chrome('C:\\Users\\Neophile\\Desktop\\sandboxes\\python\\movie-file-fixer\\drivers\\chromedriver.exe')

driver.set_page_load_timeout(30)

driver.get('https://rarbg.to/threat_defence.php?defence=1')
# driver.get('https://rarbg.to/torrents.php')

driver.maximize_window()

driver.implicitly_wait(1)

# driver.get_screenshot_as_file('screenshot.png')

# driver.find_elements_by_tag_name('a').click()
# driver.quit()

