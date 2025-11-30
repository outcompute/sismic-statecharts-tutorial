# Chapter 2: Data & Context

## Goal

In this chapter, we stop treating events as simple "signals" and start treating them as "data carriers". You will learn:

1. **Preamble:** How to initialize global variables (context) for your machine.
2. **Event Payloads:** How to send data (like `code=1234`) from Python to the Statechart.
3. **Guards:** How to use boolean logic to decide which path to take.

## The YAML file
```yaml
statechart:
  name: chapter_02
  description: A vault that checks a PIN code using Deterministic Guards.

  # PREAMBLE: This Python code block runs ONCE when the interpreter is initialized.
  # Variables defined here become the "Global Memory" (Context) of the machine.
  preamble: |
    # This is Python code below
    correct_pin = 1234
    
    # You can define helper functions here to keep your YAML logic clean.
    # is_admin() is used in `guard` within `transitions`
    def is_admin(code):
        return code == 9999

  root state:
    name: Active
    initial: Locked

    states:
      - name: Locked
        transitions:
          # 1. Admin Check
          - event: PIN_ENTERED
            # GUARD: A Python boolean expression.
            # 'event.code' comes from interpreter.queue('PIN_ENTERED', code=9999).
            # If this evaluates to True, the transition is taken.
            guard: is_admin(event.code)
            target: Unlocked
            # ACTION: Python code executed during the transition.
            # The pipe '|' (Block Scalar) allows using colons/quotes safely in YAML.
            action: |
              print(">> ADMIN OVERRIDE. Unlocking...")

          # 2. User Success Check
          - event: PIN_ENTERED
            guard: event.code == correct_pin
            target: Unlocked
            action: |
              print(f">> Success! PIN {event.code} accepted.")

          # 3. Failure Check
          # DETERMINISM: Sismic requires that exactly ONE path be valid.
          # We must explicitly exclude Admin and Success cases here using 'and not'.
          # If we just used 'guard: True' (or no guard), this would crash when
          # 'correct_pin' is entered because two paths would be valid simultaneously.
          - event: PIN_ENTERED
            guard: event.code != correct_pin and not is_admin(event.code)
            target: ErrorState
            action: |
              print(f">> FAILURE: PIN {event.code} is incorrect.")

      - name: Unlocked
        transitions:
          - event: LOCK
            target: Locked
            action: print(">> System re-armed.")

      - name: ErrorState
        transitions:
          - event: RESET
            target: Locked
            action: print(">> Error cleared.")
```

## How to Run

```bash
python run_passcode.py
```

## Key Concepts

### 1. The Preamble

In `vault_passcode.yaml`, look at the top:

```yaml
preamble: |
  correct_pin = 1234
```
This is standard Python code. Any variable defined here is accessible anywhere in your YAML using its name. It effectively acts as the "Memory" of your state machine. We are also defining a Python function in there to be used in transitions.

### 2. Passing Data

In `run_passcode.py`:

```python
interpreter.queue('PIN_ENTERED', code=0000)
```

Any keyword argument you add to `.queue()` becomes a property of the `event` object in the YAML.

* Python: `code=0000`
* YAML: `event.code`
### 3. Guards (The Branching Logic)

In `vault_passcode.yaml`, we see one state (`Locked`) with multiple transitions for the *same* event?

```yaml
transitions:
  - guard: is_admin(event.code)
    target: Unlocked
  - guard: event.code == correct_pin
    target: Unlocked
  - guard: event.code != correct_pin
    target: ErrorState
```
Sismic checks these **in order**.

1. Is the code for an admin? If yes -> Go to Unlocked. Stop checking.
2. Is the code correct? If yes -> Go to Unlocked. Stop checking.
2. Is the code correct? If no -> Go to ErrorState.

## Playground: Things to Try

1. **Change the Password:**
   * Open the YAML and change `correct_pin` in the preamble.
   * Rerun the script to see the old code fail.

2. **Add a "Duress" Code:**
   * Add a new variable in preamble: `duress_pin = 6666`.
   * Add a new transition in `Validating`.
   * Guard: `event.code == duress_pin`.
   * Target: `Unlocked` (It should still open!).
   * Action: `print(">> SILENT ALARM TRIGGERED! POLICE DISPATCHED.")`
   * *Important:* Place this transition *before* the success check to ensure it catches it.

3. **Inspect the Context:**
   * In the Python script, try printing the internal memory of the machine:
     ```python
     print(interpreter.context['correct_pin'])
     ```