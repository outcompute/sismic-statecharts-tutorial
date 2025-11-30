# Chapter 4: Time & Automation

## Goal

In this chapter, we make the system **autonomous**. It will react to the passage of time without user intervention. You will learn:

1.  **Timed Transitions:** `event: after(seconds)`.
2.  **Internal Transitions:** `internal: true` (Updating memory without exiting the state).
3.  **Counters:** Using Context to track attempts.

Do check this [page in the documentation on this topic](https://sismic.readthedocs.io/en/latest/time.html).

## The YAML file
```yaml
statechart:
  name: chapter_04
  description: Auto-locking and Tamper protection.

  preamble: |
    CORRECT_PIN = 1234
    MAX_ATTEMPTS = 3
    # We define a counter variable in the context
    attempts = 0

  root state:
    name: Active
    initial: Locked
    
    states:
      - name: Locked
        transitions:
          # 1. SUCCESS case
          - event: PIN_ENTERED
            guard: event.code == CORRECT_PIN
            target: Unlocked
            action: |
              attempts = 0 # Reset counter on success
              print(">> PIN Correct.")

          # 2. FAILURE case (Reached MAX_ATTEMPTS incorrect tries)
          # If we hit the limit, go to Lockdown immediately.
          - event: PIN_ENTERED
            guard: event.code != CORRECT_PIN and attempts + 1 >= MAX_ATTEMPTS
            target: Lockdown
            action: |
              attempts = 0
              print(">> MAX ATTEMPTS REACHED! LOCKING DOWN.")

          # 3. FAILURE (Counting)
          # INTERNAL TRANSITION: We do NOT leave the 'Locked' state and just count.
          # Notice there's no target from here.
          - event: PIN_ENTERED
            guard: event.code != CORRECT_PIN and attempts + 1 < MAX_ATTEMPTS
            action: |
              attempts += 1
              print(f">> Wrong PIN. Attempts: {attempts} out of {MAX_ATTEMPTS}")

      - name: Lockdown
        on entry: print(">> SYSTEM FROZEN (Wait 3 seconds...)")
        transitions:
          # TIMED TRANSITION
          # Sismic automatically calculates time elapsed since entering the state.
          # This state has only one transition, which is triggered on expiry of a certain period (3 seconds)
          # So this state will not accept any user input.
          - target: Locked
            guard: after(3)
            action: print(">> Lockdown expired. Ready.")

      - name: Unlocked
        on entry: print(">> Solenoid Retracted (Auto-lock in 2s)")
        transitions:
          # AUTO-LOCK in 2 seconds
          - target: Locked
            guard: after(2)
            action: print(">> AUTO-LOCK TRIGGERED.")

          # Or lock if explicitly requested to be locked
          - event: LOCK_CMD
            target: Locked
```

## How to Run

```bash
python run_timer.py
```
## Key Concepts

### 1. The `after(t)` Event

Sismic has a built-in clock. When you define `after(2)`, Sismic records the timestamp when the state was entered.

Every time you call `interpreter.execute()`, Sismic checks: `CurrentTime - EntryTime >= 2?`. If yes, it fires the transition.

*Note:* In Python, we simulate this by `time.sleep()`, then calling `execute()` to update the machine.

### 2. Internal vs. External Transitions

In the `Locked` state, we count failed attempts:

```yaml
- event: PIN_ENTERED
  internal: true
  action: attempts += 1
```
* **If `internal: false` (Default):** The machine would Exit `Locked` (firing `on exit`), and Re-Enter `Locked` (firing `on entry`). This resets the state timer and re-runs initialization logic.
* **If `internal: true`:** The machine stays *inside* `Locked`. It just runs the action. `on entry` is **not** called again. This is crucial for counting things without resetting the state.

## Playground: Things to Try

1.  **Change the Timeout:**
    * Change `after(2)` in `vault_timer.yaml` to `after(0.1)`.
    * Run the script. You will see it locks almost instantly.

2.  **Add a Warning:**
    * Add a new state `Warning` inside `Unlocked`.
    * Logic: `Unlocked` -> `after(5)` -> `Warning`.
    * Logic: `Warning` -> `after(2)` -> `Locked`.
    * Action on `Warning`: Beep loudly.
