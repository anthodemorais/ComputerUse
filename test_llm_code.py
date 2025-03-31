from pywinauto import Application
from pywinauto.keyboard import SendKeys
import time
from pywinauto.keyboard import send_keys


# Open the Start menu by sending the Windows key
send_keys("{VK_LWIN down}{VK_LWIN up}")
time.sleep(1)  # Give it a moment to open

# Type the application name (e.g., "Outlook")
send_keys("Outlook")
time.sleep(1)  # Wait for search results to populate

# Press Enter to launch the app
send_keys("{ENTER}")

time.sleep(3)  # Wait for the application to open

app = Application(backend="uia").connect(title_re=".*Outlook.*", found_index=0)

outlook_window = app.top_window()

outlook_window.type_keys('^n')  # Ctrl+N for new email
time.sleep(2)

send_keys("anthonyd-m@live.com")

outlook_window.type_keys('{TAB}')  # Move from To field to Subject line
time.sleep(1)
send_keys('This is a test subject', with_spaces=True)  # Type subject
time.sleep(1)
outlook_window.type_keys('{TAB}')  # Move from Subject line to Body
time.sleep(1)
send_keys("Hello World!", with_spaces=True)  # Type directly into body
time.sleep(1)

outlook_window.type_keys('^{ENTER}')  # Ctrl+Enter to send
time.sleep(5)

# Optional verification (may need adjustment)
sent_items = app.window(title_re=".*Sent Items.*")
if sent_items.exists():
    sent_items.click()
    time.sleep(2)