# Chapter 8: Synchronization & Property Statecharts

## Goal

Complex systems are rarely a single monolithic brain. They are often composed of multiple independent agents working together (Distributed Systems).

In this chapter, we explore how Statecharts communicate with the outside world and each other. We will cover:
1.  **Plumbing:** The difference between `send()`, `bind()`, and `attach()`.
2.  **Architecture:** Building a "System of Systems" with three independent statecharts.

---

##  PART 1: The Plumbing (`bind` vs `attach`)

Before connecting complex machines, we must understand the two ways data flows out of a Statechart. Run the basic demo to see this in action:

```bash
python run_basic_comms.py
````

### 1\. The Public Channel (`bind`)

  * **Trigger:** Explicitly triggered by `send('EVENT_NAME')` in your YAML action.
  * **Analogy:** A **Walkie-Talkie**. You press a button and shout a specific message. Only people tuned to your channel hear it.
  * **Use Case:** Business Logic. (e.g., "Tell the charger to start", "Tell the UI to close").
  * **Code:**
    ```python
    interpreter.bind(other_interpreter)
    # OR
    interpreter.bind(my_python_callback)
    ```

### 2\. The Internal Bus (`attach`)

  * **Trigger:** Automatically triggered by **ANY** activity (Entering a state, starting a step, processing a transition).
  * **Analogy:** A **Stethoscope**. The machine doesn't know you are listening. You hear everything: heartbeats, breathing, digestion.
  * **Use Case:** Observability, Logging, Debugging, and Runtime Verification.
  * **Code:**
    ```python
    interpreter.attach(my_logging_function)
    ```

-----

## PART 2: The Triad System

Now we apply these concepts to build a system of three interacting machines.

```bash
python run_sync.py
```

### The Actors

1.  **The Vault (The Master):** Controls the door and battery. It uses `bind` to talk to the Charger.
2.  **The Charger (The Worker):** An external robot. It waits for `BATTERY_LOW`, works for 5 seconds, and replies `CHARGE_COMPLETE`.
3.  **The Monitor (The Policeman):** A **Property Statechart**. It uses `attach` to silently watch the Vault. If the Vault ever enters the `Charging` state while `Unlocked`, the Monitor triggers an alarm.

### Key Concept 1: The Propagation Cycle

In a distributed system, messages take time to travel.

1.  Vault sends `BATTERY_LOW`. (It sits in Charger's mailbox).
2.  Charger wakes up, reads mail, sends `CHARGE_STARTED`. (It sits in Vault's mailbox).
3.  Vault wakes up, reads mail, enters `Charging`.

In our Python script, we simulate this using a helper function `propagate_system()`, which forces all interpreters to cycle multiple times to ensure all pending messages are processed.

### Key Concept 2: The Bridge (Meta-Events to Strings)

The Monitor needs to know what state the Vault is in. We use `attach()` to bridge the gap.

  * **Sismic Output:** `attach` provides `MetaEvent` objects containing raw State Objects.
  * **Monitor Input:** The Monitor YAML expects simple Strings (e.g., `'Charging'`).

We write a bridge function to convert them:

```python
def bridge(meta_event):
    if meta_event.name == 'state entered':
        # Convert Object -> String -> Send to Monitor
        monitor.queue('step', entered_states=[meta_event.state])
```

## Playground: Things to Try

1.  **The Disconnect:**

      * Comment out `vault.bind(charger)` in `run_sync.py`.
      * Run it. The Vault will cry for help (`BATTERY_LOW`), but the Charger will never wake up.

2.  **The Strict Monitor:**

      * Modify `monitor_ch8.yaml`.
      * Add a timer to fail if the battery stays `Low` for more than 10 seconds (implying the charger is broken or disconnected).
