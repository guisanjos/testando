from selenium import webdriver

driver_path = 'C:\Treinamento\chromedriver-win64\chromedriver-win64\chromedriver.exe'

driver = webdriver.Chrome(driver_path)

driver.get('https://www.jw.org')
driver.maximize_window()