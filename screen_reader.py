import pytesseract
import pyautogui



screenshot = pyautogui.screenshot()
text = pytesseract.image_to_string(screenshot)
data = pytesseract.image_to_data(screenshot)

print(text)
print(data)
print(screenshot)