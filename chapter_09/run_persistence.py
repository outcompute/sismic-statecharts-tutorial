import os
import pickle
from sismic.io import import_from_yaml
from sismic.interpreter import Interpreter
from sismic.clock import SimulatedClock

FILENAME = 'vault_snapshot.pkl'

def run_persistence_demo():
    path = os.path.dirname(__file__)
    yaml_path = os.path.join(path, 'firmware.yaml')
    pickle_path = os.path.join(path, FILENAME)

    # ==========================================
    # SESSION 1: The Crash
    # ==========================================
    print("--- SESSION 1: STARTING UPDATE ---")

    # 1. Start fresh
    statechart = import_from_yaml(filepath=yaml_path)
    # Note: We don't use SimulatedClock here to simplify pickling 
    # (SimulatedClock is pickleable, but standard clock is easier for simple demos)
    interpreter = Interpreter(statechart) 
    interpreter.execute()

    # 2. Start the process
    interpreter.queue('START_UPDATE').execute()

    # 3. Simulate some progress
    interpreter.queue('CHUNK_RECEIVED').execute() # 10%
    interpreter.queue('CHUNK_RECEIVED').execute() # 20%
    interpreter.queue('CHUNK_RECEIVED').execute() # 30%

    print(f"\n[Status] Current State: {interpreter.configuration}")
    print(f"[Status] Progress Variable: {interpreter.context['progress']}%")

    # 4. SIMULATE POWER FAILURE (Save & Kill)
    print("\n⚡ POWER FAILURE! SAVING STATE TO DISK... ⚡")

    with open(pickle_path, 'wb') as f:
        pickle.dump(interpreter, f)

    del interpreter
    print(">> System Shutdown. Interpreter object deleted.")
    print(">> (In a real scenario, the script would end here.)")

    # ==========================================
    # SESSION 2: The Resume
    # ==========================================
    print("\n\n--- SESSION 2: REBOOT & RESUME ---")

    # 1. Load from Disk
    if os.path.exists(pickle_path):
        print(f">> Found snapshot: {FILENAME}")
        with open(pickle_path, 'rb') as f:
            resurrected_interpreter = pickle.load(f)
        print(">> State loaded successfully.")
    else:
        print("Error: Snapshot not found!")
        return

    # 2. Verify Memory
    # Did it remember we were at 30%?
    current_progress = resurrected_interpreter.context['progress']
    print(f"[Status] Resumed State: {resurrected_interpreter.configuration}")
    print(f"[Status] Resumed Progress: {current_progress}%")

    if current_progress == 30:
        print("SUCCESS: Memory preserved.")
    else:
        print("FAILURE: Memory lost.")

    # 3. Finish the Job
    print("\n>> Resuming Download...")
    # Loop until 100%
    while resurrected_interpreter.context['progress'] < 100:
        resurrected_interpreter.queue('CHUNK_RECEIVED').execute()

    print("\n>> Process Finished.")
    print(f"[Status] Final State: {resurrected_interpreter.configuration}")

    # Cleanup
    if os.path.exists(pickle_path):
        os.remove(pickle_path)
        print("\n(Snapshot file cleaned up)")

if __name__ == '__main__':
    run_persistence_demo()