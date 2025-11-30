import os
from sismic.io import import_from_yaml
from sismic.interpreter import Interpreter
from sismic.clock import SimulatedClock

def run_complex_demo():
    filepath = os.path.join(os.path.dirname(__file__), 'vault_complex.yaml')
    statechart = import_from_yaml(filepath=filepath)

    sim_clock = SimulatedClock()
    interpreter = Interpreter(statechart, clock=sim_clock)

    # Boot
    interpreter.execute()
    print("--- System Active (Parallel Regions Started) ---")
    print_state(interpreter)

    # 1. Interact with Security (Time 0.0s)
    print("\n[User] Unlocking...")
    interpreter.queue('PIN_ENTERED', code=1234).execute()
    print_state(interpreter)

    # 2. Advance Time (2.0s)
    # Effect: Security should Auto-Lock (after 2s)
    # Effect: Power should still be Full (requires 4s)
    print(f"\n[Time] Advancing 2.0s...")
    sim_clock.time += 2.0
    interpreter.execute()
    print_state(interpreter)

    # 3. Advance Time (2.5s more -> Total 4.5s)
    # Effect: Security is still Locked.
    # Effect: Power should transition Full -> Low (happens at 4s)
    print(f"\n[Time] Advancing 2.5s (Total 4.5s)...")
    sim_clock.time += 2.5
    interpreter.execute()
    print_state(interpreter)

    # 4. Global Interrupt
    # We are in 'Locked' and 'LowBattery'.
    # Triggering MASTER_RESET should kill BOTH regions.
    print("\n[User] Hitting Master Reset Button...")
    interpreter.queue('MASTER_RESET').execute()
    print_state(interpreter)

    # 5. Reboot
    print("\n[User] Rebooting...")
    interpreter.queue('REBOOT').execute()
    print_state(interpreter)

def print_state(interpreter):
    # This will now show MULTIPLE states (e.g., ['Locked', 'FullBattery'])
    # We filter out the container names ('Active', 'SecurityRegion', 'PowerRegion') 
    # to keep the output clean, usually standard practice in logging.
    all_states = sorted(interpreter.configuration)
    leaf_states = [s for s in all_states if s in ['Locked', 'Unlocked', 'FullBattery', 'LowBattery', 'DeadBattery', 'Maintenance']]
    print(f"Current Status: {leaf_states}")

if __name__ == '__main__':
    run_complex_demo()