# Chapter 3: Python Integration (Binding)

## Goal

In this chapter, we separate the **Logic** (YAML) from the **Implementation** (Python).

* **Chapter 1 & 2:** We wrote `print()` statements inside the YAML. This is messy and hard to test.
* **Chapter 3:** We create a dedicated Python class (`VaultHardware`) and "inject" it into the Statechart.

## The YAML file
```yaml
statechart:
  name: chapter_03
  description: Controlling external Python objects (Hardware Layer).

  preamble: |
    # We don't need to define logic here anymore!
    # We just define simple constants.
    CORRECT_PIN = 9999
    # We will access 'hw' later which is not present in preamble
    # because we will inject it from Python later.

  root state:
    name: Active
    initial: Locked

    states:
      - name: Locked
        # ON ENTRY: When we enter 'Locked', ensure the hardware is locked.
        on entry: |
          hw.set_led('RED')
          hw.lock_mechanism()

        transitions:
          - event: PIN_ENTERED # If the code is entered ...
            guard: event.code != CORRECT_PIN # ... and it is incorrect ...
            target: Locked  # ... then, self-transition to trigger on_entry routines
            action: |
               hw.beep(times=3) # Beep three times ... 
               hw.flash_led('RED') # ... and flash the LED as feedback

          - event: PIN_ENTERED
            guard: event.code == CORRECT_PIN
            target: Unlocked
            action: hw.beep(times=1) # No flashing LEDs here

      - name: Unlocked
        # ON ENTRY: When we enter 'Unlocked', ensure the hardware is now unlocked.
        on entry: |
          hw.set_led('GREEN') # The LED is GREEN to signify unlocked status ...
          hw.unlock_mechanism() # ... and the door is unlocked

        transitions:
          - event: LOCK_CMD
            target: Locked
```

## How to Run

```bash
python run_binding.py
```

## Key Concepts

### 1. The Context Injection

In `run_binding.py`, this is the magic line:

```python
interpreter = Interpreter(statechart, initial_context={'hw': real_hardware})
```
We tell Sismic: "When you run this chart, create a variable named `hw` and point it to my Python object."

### 2. Calling Methods in YAML

In `vault_binding.yaml`, we can now call any public method of that object:

```yaml
on entry:
  hw.set_led('RED')
  hw.lock_mechanism()
```
### 3. "On Entry" vs "Transitions"

You will notice we used `on entry` for the LED and Lock.

* **Transitions (`action`)**: Happen *while moving* between states. Good for instantaneous feedback (Beeps).
* **State (`on entry`)**: Happens *when arriving* at a state. Good for setting persistent status (LED color, Door Lock status).

This ensures that no matter *how* we got to the `Locked` state (from boot, or from user re-locking), the door is guaranteed to be locked.

## Playground: Things to Try

1.  **Add a new Hardware Feature:**
    * Add a method `send_sms(message)` to the `VaultHardware` class in Python.
    * Update the YAML to call `hw.send_sms("Welcome Home")` when the state becomes `Unlocked`.

2.  **State Inspection:**
    * In the `run_binding.py`, try printing `real_hardware._is_locked` at the end of the script. You will see the Statechart successfully mutated the Python object's state.