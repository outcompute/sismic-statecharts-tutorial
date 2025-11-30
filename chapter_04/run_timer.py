import os
from sismic.io import import_from_yaml
from sismic.interpreter import Interpreter
# 1. Import the simulated clock explicitly
from sismic.clock import SimulatedClock

def run_timer_demo():
    filepath = os.path.join(os.path.dirname(__file__), 'vault_timer.yaml')
    statechart = import_from_yaml(filepath=filepath)

    # 2. Create a clock we control
    sim_clock = SimulatedClock()
    interpreter = Interpreter(statechart, clock=sim_clock)

    # Boot the machine
    steps = interpreter.execute()
    print(f"--- Vault Active (Boot steps: {len(steps)}) ---")

    # SCENARIO 1: Auto-Lock Feature
    print("\n[Test] Unlocking successfully...")
    interpreter.queue('PIN_ENTERED', code=1234).execute()

    print(f"\n[Time] Clock before incrementing: {sim_clock.time}s. Advancing by 1.0s...")
    # 3. Advance time manually
    sim_clock.time += 1.0
    # calling execute() is sufficient to check timers
    steps = interpreter.execute() 
    print(f"Steps taken: {len(steps)}") # Should be 0 (Timer hasn't fired yet)
    print_state(interpreter) 

    print(f"\n[Time] Clock before incrementing: {sim_clock.time}s. Advancing by 1.5s...")
    sim_clock.time += 1.5 # Total time = 2.5s. This is > 2.0s, so 'after(2)' should fire.

    steps = interpreter.execute()
    print(f"Steps taken: {len(steps)}") # Should be > 0 (Auto-lock triggered)
    print_state(interpreter)

    # SCENARIO 2: Tamper Protection
    # This only works if we are back in 'Locked' state!
    print("\n[Test] Entering wrong PINs...")

    # Attempt 1
    interpreter.queue('PIN_ENTERED', code=0000).execute()
    # Attempt 2
    interpreter.queue('PIN_ENTERED', code=0000).execute()
    # Attempt 3 (Should Trigger Lockdown)
    interpreter.queue('PIN_ENTERED', code=0000).execute()
    print_state(interpreter)

    # Try to unlock during lockdown (Should fail)
    print("\n[User] Trying correct PIN during lockdown...")
    interpreter.queue('PIN_ENTERED', code=1234).execute()

    print(f"\n[Time] Clock before incrementing: {sim_clock.time}s. Advancing by 4.0s (Lockdown expiry)...")
    sim_clock.time += 4.0
    steps = interpreter.execute() # Trigger the 'after(3)' event
    print(f"Steps taken: {len(steps)}")
    print_state(interpreter)

def print_state(interpreter):
    print(f"Current State: {sorted(interpreter.configuration)}")

if __name__ == '__main__':
    run_timer_demo()