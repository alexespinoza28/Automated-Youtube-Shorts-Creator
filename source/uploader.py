from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By


login_info = []
with open(r"C:\Users\max59\Downloads\emailandlogin.txt", "r") as file:
    login_info.append(file.readline().strip()) 
    login_info.append(file.readline().strip())

# Set up the WebDriver (using Chrome in this example)
service = Service(executable_path=r"C:\Users\max59\Desktop\Projects\reddit-bot\source\chromedriver.exe")
driver = webdriver.Chrome(service=service)


# Open a webpage
driver.get("https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Den%26next%3Dhttps%253A%252F%252Fwww.youtube.com%252F&ec=65620&hl=en&ifkv=Ab5oB3pIGAAnsNDb-Emftx_tNvvpG7h0J_uuoTYgcsUAgL8yfcKYWwMWsVTSRmOjNtTlfI_bdUt_&passive=true&service=youtube&uilel=3&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S2099760470%3A1724372931158466&ddm=0")

signin = driver.find_element(By.CLASS_NAME,"yt-spec-touch-feedback-shape__fill")
signin.click()
enter_email = driver.find_element(By.CLASS_NAME, "whsOnd zHQkBf")
enter_email.send_keys(login_info[0] + Keys.ENTER)


time.sleep(5)

# Close the browser
driver.quit()
