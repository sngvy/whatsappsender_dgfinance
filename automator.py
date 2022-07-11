from io import BytesIO
import win32clipboard
from PIL import Image
import keyboard
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException, NoAlertPresentException
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from urllib.parse import quote
from sys import platform

options = Options()
if platform == "win32":
	options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"

print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("+++++                                               ++++++")
print("+++++  Программа автоматизации рассылки на WhatsApp  +++++")
print("+++++         Собственность ДиДжи Финанс Рус        ++++++")
print("+++++                github.com/sngvy               ++++++")
print("+++++                                               ++++++")
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

f = open("message.txt", "r", encoding="utf-8")
message = f.read()
f.close()

print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("++++++++++++++++++   Текст сообщения:   ++++++++++++++++++")
print(message)
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
message = quote(message)

numbers = []
f = open("numbers.txt", "r")
for line in f.read().splitlines():
	if line != "":
		numbers.append(line)
f.close()
total_number=len(numbers)
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print(f'Загружено {total_number} номеров')
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print()
delay = 30

driver = webdriver.Chrome(ChromeDriverManager().install())
print('Сейчас откроется страница авторизации WhatsApp Web. Нажмите ENTER после сканирования QR на телефоне, чтобы приступить к рассылке')
driver.get('https://web.whatsapp.com')
input('')
for idx, number in enumerate(numbers):
	number = number.strip()
	if number == "":
		continue
	print('Номер {} из {} - отправка сообщения на номер {}'.format((idx+1), total_number, number))
	try:
		url = 'https://web.whatsapp.com/send?phone=' + number + '&text=' + message
		sent = False
		for i in range(1):
			if not sent:
				driver.get(url)
				try:
					msgbox = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//div[@class="_2lMWa"]//div[@role="textbox"]')))
				except Exception as e:
					print(f'Номер {number} не найден в WhatsApp')
				else:
					sleep(10)
					def send_to_clipboard(clip_type, data):
						win32clipboard.OpenClipboard()
						win32clipboard.EmptyClipboard()
						win32clipboard.SetClipboardData(clip_type, data)
						win32clipboard.CloseClipboard()
					filepath = 'doc.png'
					image = Image.open(filepath)
					output = BytesIO()
					image.convert("RGB").save(output, "BMP")
					data = output.getvalue()[14:]
					output.close()
					send_to_clipboard(win32clipboard.CF_DIB, data)
					msgbox.click()
					msgbox.send_keys(Keys.CONTROL + "v")
					sleep(10)
					msgbox = driver.find_element(By.XPATH, '//div[@class="_13NKt copyable-text selectable-text"]')
					msgbox.click()
					sndbtn = driver.find_element(By.XPATH, '//div[@class="_33pCO"]')
					sndbtn.click()
					sent=True
					print(f'Сообщение на номер {number} отправлено')
					sleep(10)
	except Exception as e:
		print(f'Не удалось отправить сообщение на номер {number}')