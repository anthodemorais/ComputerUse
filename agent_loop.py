import sys
import io
from helpers.llm import call_llm, get_message_output

# In a loop, prompt AI with the problem and the actions that were done before.
# AI needs to give the next action(s) to take from these possible actions:
# - Open an application
# - Read the content of X application to get the current state of the system
# - Take a screenshot of X application to observe the current state of the system
# - Perform actions in X application
# - Ask the user for more information

# See this to add images to the prompt: https://huggingface.co/docs/huggingface_hub/package_reference/inference_client#huggingface_hub.InferenceClient.chat_completion.example-6

prompt = """
You are an AI agent that has access to a computer system to solve the user's problem.

To make sure to solve the problem correctly, we proceed carefully step by step.

These are the actions that where done before:
- {actions_done}

The result of the last action is: {last_action_result}

After the last action, the content of the application {app_name} is:
- {state}

A screenshot will be attached to this prompt if the last action was to take a screenshot.

Now you need to decide what to do next from these possible actions:
- Open an application
- Read the content of one of the open application to get the current state of the system
- Take a screenshot of one of the open application to observe the current state of the system
- Perform actions in one of the open application
- Ask the user for more information

Please give me the next action to take from these possible actions.
Proceed carefully, think about it and don't output too many actions at once. Only base your actions on the application trees dumped by previous steps.

Your output should only be a single small sentence explaining what to do and then a Python code snippet that does the action and returns the result of the action.
The computer you have is using Ubuntu so to perform actions on the computer, dump the application trees or take screenshots, use the Dogtail library and pyautogui library.

After opening an application or a window within that application, always dump the application tree and return it. Same after performing a few actions in an application.

To dump the content of a window, don't use the dump method of Dogtail. Instead, use a function that will be provided to your program called get_dump_application_tree_code that takes in parameter the node you want to dump.

To return the content of the application, return a formatted dictionary with 2 keys and values:
- "tree": the application tree dumped with get_dump_application_tree_code
- "application": the name of the application
- "screenshots": if you take screenshots, return the images as a list here

If you need to ask clarification to the user, output a sentence starting with "--- Ask the user: " and then the question.

If you think the job is done, output a sentence starting with "--- Done: " and then the message to the user.

These are the applications that you have access to:
- Thunderbird Mail
- LibreOffice Writer
- LibreOffice Calc
- LibreOffice Impress
- Terminal
- Firefox
- File Manager
"""

def get_dump_application_tree_code(application):
    # Backup the original stdout
    original_stdout = sys.stdout
    # Redirect stdout to a StringIO buffer
    sys.stdout = buffer = io.StringIO()
    # Dump the node's structure into the buffer
    application.dump()
    # Restore the original stdout
    sys.stdout = original_stdout
    # Return the captured string
    return buffer.getvalue()


is_done = False
actions_done = []
app_name = None
state = None
screenshots = []
last_action_result = None

while not is_done:
    # Call the LLM with the prompt
    # Analyze the output and take the action
    # Update the state variables
    # If there was an error, feed that back in the prompt

    actions_done_string = "\n-----\n".join(actions_done)
    last_action_result_string = last_action_result if last_action_result else "successful"
    state_string = state if state else "unknown"

    prompt_string = prompt.format(
        actions_done=actions_done_string,
        last_action_result=last_action_result_string,
        app_name=app_name,
        state=state_string
    )

    messages = [
        {"role": "system", "content": prompt_string},
        {"role": "user", "content": "Send an email saying Hello World to anthonyd-m@live.com"}
    ]

    output = get_message_output(call_llm(messages))
    print("AI output:", output)

    is_done = True
    break

    if "--- Done:" in output:
        is_done = True
        print("AI says done")
    
    if "--- Ask the user:" in output:
        question = output.split("--- Ask the user: ")[1].strip()
        print("AI asks:", question)
    
    actions = output.split("```python")[1].strip()
    if actions:
        action_code = actions.split("```")[0].strip()
        print("AI action code:", action_code)
        try:
            state_dict = exec(action_code)  # Execute the action code
            state = state_dict.get("tree", None)
            app_name = state_dict.get("application", None)
            actions_done.append(action_code)
        except Exception as e:
            print("Error executing action code:", e)
            last_action_result = 'Error: {error}'.format(str(e))





"""
1.

AI output: To send the email, I'll open Thunderbird Mail first.

```python
from dogtail.config import config
config.logDebugToStdOut = True
config.logDebugToFile = False

# Launch Thunderbird Mail
from dogtail.procedural import start_app
start_app('thunderbird')

# Get application tree
thunderbird_app = Application('thunderbird')
tree = get_dump_application_tree_code(thunderbird_app)

# Return application state
{"tree": tree, "application": "Thunderbird Mail"}
```

2. 

"""

