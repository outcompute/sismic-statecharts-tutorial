import os
from sismic.io import import_from_yaml
from sismic.interpreter import Interpreter
from sismic.clock import SimulatedClock

def run_synchronization_demo():
    path = os.path.dirname(__file__)
    vault_sc = import_from_yaml(filepath=os.path.join(path, 'vault_ch8.yaml'))
    charger_sc = import_from_yaml(filepath=os.path.join(path, 'charger_ch8.yaml'))
    monitor_sc = import_from_yaml(filepath=os.path.join(path, 'monitor_ch8.yaml'))

    master_clock = SimulatedClock()

    vault = Interpreter(vault_sc, clock=master_clock)
    charger = Interpreter(charger_sc, clock=master_clock)
    monitor = Interpreter(monitor_sc, clock=master_clock)

    # WIRING
    vault.bind(charger)
    charger.bind(vault)

    # FIX 1: The Bridge now handles 'MetaEvent' objects correctly
    def bridge_to_monitor(meta_event):
        # We look for the specific internal event that signals a state entry
        if meta_event.name == 'state entered':
            # meta_event.state is the string name (e.g., 'Charging')
            monitor.queue(
                'step', 
                entered_states=[meta_event.state], 
                configuration=vault.configuration
            ).execute()

    vault.attach(bridge_to_monitor)

    print("--- SYSTEM STARTUP ---")
    vault.execute()
    charger.execute()
    monitor.execute()

    def propagate_system():
        # Spin the cycle enough times for messages to ping-pong
        # If there are no events, then these calls will have no effect
        for _ in range(3):
            vault.execute()
            charger.execute()

    # ==========================================
    # SCENARIO 1: Successful Auto-Charge
    # ==========================================
    print("\n[Scenario 1] Waiting for battery drain...")
    
    master_clock.time += 2.0
    propagate_system() 
    print_status(vault, charger)

    print("\n[Scenario 1] Waiting for charge cycle (5s)...")
    master_clock.time += 5.0
    propagate_system()
    print_status(vault, charger)


    # ==========================================
    # SCENARIO 2: Triggering the Safety Monitor
    # ==========================================
    print("\n[Scenario 2] Creating a Hazard...")
    
    # 1. Clean up from previous scenario (Ensure we are in 'Full')
    print(">> Aging battery logic to settle state...")
    master_clock.time += 0.1
    propagate_system()

    # 2. FIX 2: Age the battery significantly BEFORE unlocking
    # We want Battery Age = 1.5s, Door Open Age = 0.0s
    print(">> Aging battery by 1.5s (approaching death)...")
    master_clock.time += 1.5
    propagate_system()
    
    # 3. Unlock the door
    print(">> User Unlocks Door")
    vault.queue('PIN_ENTERED', code=1234).execute()
    
    # 4. Push over the edge
    # Advance 0.5s.
    # Battery Age: 0.1 + 1.5 + 0.5 = 2.0s (Triggers Low -> Charging)
    # Door Age: 0.0 + 0.5 = 0.5s (Still Open)
    # Result: Unlocked + Charging = VIOLATION
    print(">> Advancing 0.5s...")
    master_clock.time += 0.5 
    
    propagate_system()

    # HazardDetected is a final state, which means no more pending states
    if len(monitor.configuration) == 0: 
        print("\nMonitor successfully caught the violation and terminated.")
    else:
        print("\nMonitor failed to catch violation.")
        print(f"Monitor State: {monitor.configuration}")

def print_status(vault, charger):
    v_state = [s for s in vault.configuration if s in ['Full', 'Low', 'Charging', 'Locked', 'Unlocked']]
    c_state = [s for s in charger.configuration if s in ['Idle', 'Charging']]
    print(f"STATUS | Vault: {v_state} | Charger: {c_state}")

if __name__ == '__main__':
    run_synchronization_demo()