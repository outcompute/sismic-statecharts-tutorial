import os
from sismic.io import import_from_yaml
from sismic.interpreter import Interpreter

def run_vault():
    # 1. Load the YAML file
    # Ensure the path matches where you saved the file
    filepath = os.path.join(os.path.dirname(__file__), 'vault.yaml')
    statechart = import_from_yaml(filepath=filepath)

    # 2. Create the Interpreter
    # This is the "Engine" that will run your logic
    interpreter = Interpreter(statechart)

    # Boot up the machine to enter the initial state
    interpreter.execute() 

    print("--- Simulation Started ---")
    print_current_state(interpreter)  # Now this will show ['Active', 'Idle']

    # 3. Step 1: Wake up the system
    print("\n[Action] User presses button...")
    interpreter.queue('BUTTON_PRESSED')
    interpreter.execute()
    print_current_state(interpreter)

    # 4. Step 2: Enter correct PIN
    print("\n[Action] User enters correct PIN...")
    interpreter.queue('PIN_ACCEPTED')
    interpreter.execute()
    print_current_state(interpreter)

    # 5. Step 3: Open the door
    print("\n[Action] User pulls the door open...")
    interpreter.queue('DOOR_PULLED')
    interpreter.execute()
    print_current_state(interpreter)

    # 6. Step 4: Invalid action
    print("\n[Action] User presses button while door is open (Invalid)...")
    interpreter.queue('BUTTON_PRESSED')
    interpreter.execute()
    print_current_state(interpreter)

def print_current_state(interpreter):
    # interpreter.configuration returns a list of active states.
    # We create a clean string for display.
    active_states = [s for s in interpreter.configuration]
    print(f"Current State: {active_states}")

if __name__ == '__main__':
    run_vault()