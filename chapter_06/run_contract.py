import os
from sismic.io import import_from_yaml
from sismic.interpreter import Interpreter
from sismic.exceptions import ContractError

def run_contract_demo():
    filepath = os.path.join(os.path.dirname(__file__), 'vault_contract.yaml')
    statechart = import_from_yaml(filepath=filepath)
    interpreter = Interpreter(statechart)

    interpreter.execute()
    print("--- System Active ---")
    print(f"Invariant: attempts < {interpreter.context['MAX_ATTEMPTS']}")

    # 1. Normal Operation
    print("\n[Test] Normal failures (Safe)...")
    interpreter.queue('PIN_ENTERED', code=0000).execute() # attempts=1
    print(f"Attempts: {interpreter.context['attempts']}")

    interpreter.queue('PIN_ENTERED', code=0000).execute() # attempts=2
    print(f"Attempts: {interpreter.context['attempts']}")

    # Reset for the crash test
    interpreter.context['attempts'] = 0
    print(">> Counter reset.")
    # Wait, did the code just set a context/preamble variable to an arbitrary value? Yes

    # 2. The Crash Test
    print("\n[Test] Triggering the BUG...")
    try:
        # Step 1: attempts -> 1 (Safe)
        interpreter.queue('DEV_TEST_FAIL').execute()
        print(f"Attempts: {interpreter.context['attempts']}")

        # Step 2: attempts -> 2 (Safe)
        interpreter.queue('DEV_TEST_FAIL').execute()
        print(f"Attempts: {interpreter.context['attempts']}")

        # Step 3: attempts -> 3 (UNSAFE!)
        # The 'Locked' state requires attempts < 3.
        # This step will execute the action, update the context, 
        # THEN check the invariant. It will fail.
        print(">> Triggering violation...")
        interpreter.queue('DEV_TEST_FAIL').execute()

    except ContractError as e:
        header_sep = "="*24
        print("\n")
        print(header_sep)
        print("SAFETY SYSTEM TRIGGERED!")
        print(header_sep)
        print(f"Error: {e}")
        print("The system prevented an invalid state.")

if __name__ == '__main__':
    run_contract_demo()