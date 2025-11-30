import os
from sismic.io import import_from_yaml
from sismic.interpreter import Interpreter

def run_passcode_demo():
    filepath = os.path.join(os.path.dirname(__file__), 'vault_passcode.yaml')
    statechart = import_from_yaml(filepath=filepath)
    interpreter = Interpreter(statechart)
    
    # Boot the machine
    interpreter.execute()
    print("--- Vault Active (Correct PIN is 1234) ---")
    print_state(interpreter)

    # TEST 1: Wrong PIN
    print("\n[User] Entering 0000...")
    # NOTICE: We pass 'code=0000' as a keyword argument.
    # This becomes 'event.code' inside the YAML.
    interpreter.queue('PIN_ENTERED', code=0000)
    interpreter.execute()
    print_state(interpreter)

    # Reset
    print("\n[User] Resetting system...")
    interpreter.queue('RESET')
    interpreter.execute()
    print_state(interpreter)

    # TEST 2: Correct PIN
    print("\n[User] Entering 1234...")
    interpreter.queue('PIN_ENTERED', code=1234)
    interpreter.execute()
    print_state(interpreter)

    # Relock
    print("\n[User] Locking...")
    interpreter.queue('LOCK')
    interpreter.execute()
    print_state(interpreter)

    # TEST 3: Admin PIN (The Helper Function)
    print("\n[User] Entering Admin Code 9999...")
    interpreter.queue('PIN_ENTERED', code=9999)
    interpreter.execute()
    print_state(interpreter)

    # Relock
    print("\n[User] Locking...")
    interpreter.queue('LOCK')
    interpreter.execute()
    print_state(interpreter)

def print_state(interpreter):
    print(f"Current State: {sorted(interpreter.configuration)}")

if __name__ == '__main__':
    run_passcode_demo()