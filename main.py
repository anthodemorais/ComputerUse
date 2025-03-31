import pywinauto
import time
import pywinauto.keyboard
from helpers.llm import call_llm, get_message_output
from helpers.prompts import computer_use_system_prompt_plan, computer_use_system_prompt_code


def read_screen_content():
    app = pywinauto.Application(backend="uia").start('notepad.exe')

    time.sleep(2)

    app.connect(title_re=".* Bloc-notes")

    app.top_window().child_window(title="Ajouter un nouvel onglet").click_input()

    pywinauto.keyboard.send_keys("Hello World! The program is working fine.", with_spaces=True)

    app.top_window().child_window(title="Fichier").click_input()

    time.sleep(2)

    app.top_window().child_window(title="Enregistrer", found_index=0, control_type="MenuItem").select()


# messages = [
#     {
#         "role": "system",
#         "content": computer_use_system_prompt_plan
#     },
#     {
#         "role": "user",
#         "content": "Send an email to anthonyd-m@live.com saying 'Hello World!'"
#     },
# ]
# llm_plan = call_llm(messages)

# print(get_message_output(llm_plan))

llm_plan = """
**Step-by-Step Plan to Send the Email:**

1. **Open Microsoft Outlook:**
   - **Action:** Launch Outlook via the Start Menu or taskbar shortcut. If already running, bring it to the foreground.
   - **Tool:** `pywinauto` to execute `Start > Outlook` or activate the existing window.

2. **Create a New Email:**
   - **Action:** Use the keyboard shortcut `Ctrl + N` to open a new email window.
   - **Tool:** `pywinauto` to send the keystrokes to the Outlook window.

3. **Enter Recipient Email Address:**
   - **Action:** Type `anthonyd-m@live.com` into the "To" field.
   - **Tool:** `pywinauto` to set text in the "To" input field. If focus isn’t already there, use `Tab` to navigate.

4. **Skip Subject (Optional):**
   - **Action:** Press `Tab` to move from the "To" field to the email body. The subject line will be left empty unless required.
   - **Tool:** `pywinauto` to send `{TAB}` keystrokes.

5. **Compose the Email Body:**
   - **Action:** Type `Hello World!` into the body of the email.
   - **Tool:** `pywinauto` to send the text directly to the body field or simulate typing.

6. **Send the Email:**
   - **Action:** Press `Ctrl + Enter` to send the email immediately.
   - **Tool:** `pywinauto` to send the keystrokes to the email window.

7. **Verify Sent Confirmation (Optional):**
   - **Action:** Check Outlook’s "Sent Items" folder to confirm delivery (if robustness is critical).
   - **Tool:** `pywinauto` to navigate to the "Sent Items" folder and verify the latest entry.

**Programs Used:**  
- **Microsoft Outlook** for composing and sending the email.  
- **pywinauto** for automating window interactions and keystrokes.  

**Notes:**  
- If Outlook prompts for login or security permissions (e.g., "Allow this app to send emails?"), manual intervention may be required.  
- The subject line is omitted unless specified; adjust if the user prefers a custom subject.
"""

messages = [
    {
        "role": "user",
        "content": "Write a Python script that I can run to open the ThunderbirdMail app and send an email to anthonyd-m@live.com saying 'Hello World!'. Use the Dogtail library."
    },
   #  {
   #      "role": "system",
   #      "content": computer_use_system_prompt_code.format(llm_plan)
   #  },
]

print(messages)

llm_code = call_llm(messages)
print(get_message_output(llm_code))



"""
Here's a Python script using Dogtail to automate sending an email through Thunderbird. Note that this requires proper accessibility setup in Thunderbird and Linux.

```python
#!/usr/bin/env python3
import subprocess
import time
from dogtail.tree import root
from dogtail.utils import run

# Launch Thunderbird if not running
try:
    app = root.application('Thunderbird')
except Exception:
    subprocess.Popen(['thunderbird'])
    time.sleep(10)  # Wait for Thunderbird to launch
    app = root.application('Thunderbird')

# Create new message using keyboard shortcut
app.typeText('<Ctrl>N')
time.sleep(3)  # Wait for compose window

# Get compose window
compose_win = app.window('Write:')

# Fill recipient
to_field = compose_win.findChild(
    lambda x: x.roleName == 'text' and x.name == 'To'
)
to_field.textEntry = 'anthonyd-m@live.com'

# Fill subject
subject_field = compose_win.findChild(
    lambda x: x.roleName == 'text' and x.name == 'Subject'
)
subject_field.textEntry = 'Hello from Dogtail'

# Fill body (might need to click first depending on Thunderbird version)
body_field = compose_win.findChild(
    lambda x: x.roleName == 'document text' or x.roleName == 'text'
)
body_field.click()
body_field.textEntry = 'Hello World!'

# Send using keyboard shortcut (Ctrl+Enter)
app.typeText('<Ctrl><Enter>')
```

Before running this script:

1. Install dependencies:
```bash
sudo apt install python3-dogtail at-spi2-core
pip3 install dogtail
```

2. Enable accessibility in Thunderbird:
- Go to Preferences > Advanced > General
- Click Config Editor
- Search for `accessibility.force_disabled`
- Set value to `0` and restart Thunderbird

3. Make sure Thunderbird is configured with an email account

The script will:
1. Launch Thunderbird if not running
2. Open a new message window
3. Fill in recipient, subject, and body
4. Send the email using keyboard shortcuts

Note: UI element names may vary slightly between Thunderbird versions. You may need to adjust the element identifiers using `accerciser` (GUI inspector tool) for your specific setup.
"""

