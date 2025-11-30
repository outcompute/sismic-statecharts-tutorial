import os
from sismic.io import import_from_yaml
from sismic.interpreter import Interpreter

# ==========================================
# 1. THE "BIND" LISTENER (The Radio)
# ==========================================
# This class mimics an Interpreter or External System.
# It only receives high-level events sent via send().
class MockRadio:
    def __call__(self, event):
        self.queue(event)

    def queue(self, event):
        # Sismic calls this method when the Statechart executes send()
        print(f"\nRADIO (Bound) RECEIVED: '{event.name}'")
        if getattr(event, 'data', None):
            print(f"   Payload: {event.data}")

# ==========================================
# 2. THE "ATTACH" LISTENER (The Technician)
# ==========================================
# This function receives low-level execution details (MetaEvents).
def technician_log(meta_event):
    # We filter slightly to keep the output readable, 
    # but notice how much MORE info this gets.
    name = meta_event.name
    
    if name == 'step started':
        print("TECH  (Attached): [Step Started]")
    elif name == 'state entered':
        print(f"TECH  (Attached): Entered '{meta_event.state}'")
    elif name == 'event sent':
        # The technician even sees that an event was sent out!
        print(f"TECH  (Attached): Outgoing Event -> {meta_event.event.name}")

# ==========================================
# 3. THE RUNNER
# ==========================================
def run_demo():
    path = os.path.dirname(__file__)
    statechart = import_from_yaml(filepath=os.path.join(path, 'basic_comms.yaml'))
    interpreter = Interpreter(statechart)

    # A. BINDING (The Public Channel)
    radio = MockRadio()
    interpreter.bind(radio)
    print(">> Radio bound to Public Channel.")

    # B. ATTACHING (The Internal Debugger)
    interpreter.attach(technician_log)
    print(">> Technician attached to Internal Bus.")

    # Start
    print("\n--- 1. BOOTING SYSTEM ---")
    interpreter.execute()

    print("\n--- 2. GOING LIVE ---")
    # This will trigger entry to 'OnAir', which calls send('HELLO_WORLD')
    interpreter.queue('GO_LIVE').execute()

    print("\n--- 3. STOPPING ---")
    # This will trigger transition to 'Idle', which calls send('GOODBYE')
    interpreter.queue('STOP').execute()

if __name__ == '__main__':
    run_demo()