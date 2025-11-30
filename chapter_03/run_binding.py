import os
import time
from sismic.io import import_from_yaml
from sismic.interpreter import Interpreter

# ---------------------------------------------------------
# 1. The "Real" Hardware Layer
# This class knows HOW to do things, but not WHEN.
# ---------------------------------------------------------
class VaultHardware:
    def __init__(self):
        self._is_locked = True

    def set_led(self, color):
        print(f"[HW] LED turned to {color}")

    def lock_mechanism(self):
        print("[HW] Solenoid ENGAGED (Door is now Locked)")
        self._is_locked = True

    def unlock_mechanism(self):
        print("[HW] Solenoid DISENGAGED (Door is now Open)")
        self._is_locked = False

    def beep(self, times):
        sound = "BEEP " * times
        print(f"[HW] Speaker: {sound.strip()}")

    def flash_led(self, color):
        print(f"[HW] LED flashing {color}...")

# ---------------------------------------------------------
# 2. The Runner
# ---------------------------------------------------------
def run_hardware_demo():
    # A. Instantiate our hardware controller
    real_hardware = VaultHardware()

    # B. Load the Statechart
    filepath = os.path.join(os.path.dirname(__file__), 'vault_binding.yaml')
    statechart = import_from_yaml(filepath=filepath)

    # C. INJECTION: Pass the object into the 'initial_context'
    # This makes the variable 'hw' available inside the YAML.
    interpreter = Interpreter(statechart, initial_context={'hw': real_hardware})

    # Boot up
    print("--- System Booting ---")
    interpreter.execute()

    # Test Interaction
    print("\n[User] Entering Wrong PIN...")
    interpreter.queue('PIN_ENTERED', code=1234).execute()

    print("\n[User] Entering Correct PIN...")
    interpreter.queue('PIN_ENTERED', code=9999).execute()

    print("\n[User] Locking door...")
    interpreter.queue('LOCK_CMD').execute()

if __name__ == '__main__':
    run_hardware_demo()
