import sys
import io
from helpers.llm import call_llm, get_message_output
from helpers.prompts import loop_prompt

# In a loop, prompt AI with the problem and the actions that were done before.
# AI needs to give the next action(s) to take from these possible actions:
# - Open an application
# - Read the content of X application to get the current state of the system
# - Take a screenshot of X application to observe the current state of the system
# - Perform actions in X application
# - Ask the user for more information

# See this to add images to the prompt: https://huggingface.co/docs/huggingface_hub/package_reference/inference_client#huggingface_hub.InferenceClient.chat_completion.example-6


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

    prompt_string = loop_prompt.format(
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

```python
from dogtail import tree
from dogtail import utils
import pyautogui

# Open Thunderbird Mail
utils.run('thunderbird')
thunderbird = tree.root.application('Thunderbird Mail')

# Get the application tree
tree_dump = get_dump_application_tree_code(thunderbird)

# Return the application tree and name
{
    "tree": tree_dump,
    "application": "Thunderbird Mail"
}
```

2. 

"""

