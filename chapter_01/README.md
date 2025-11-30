# Chapter 1: The Linear Workflow

## Goal

In this chapter, you will learn the fundamental building blocks of Sismic:

1. **The YAML Structure:** How to define a simple, flat list of states.
2. **The Interpreter Loop:** How to load that YAML into Python and make it move.
3. **Event Queueing:** How to send signals to the machine.

## The YAML file

```yaml
statechart:  # MANDATORY: The root key. Sismic looks for this to start parsing.
  name: chapter_01  # Metadata: Name of the chart. Useful for logging and debugging.
  description: A basic linear workflow for a safe.  # Metadata: Optional documentation.

  root state:  # MANDATORY: The top-level container. All states must live inside a root.
    name: Active  # The name of this container state.
    initial: Idle  # CRITICAL: Tells the engine which state to enter immediately upon start.
    
    states:  # A list defining the children of "Active"
      - name: Idle  # DEFINITION: A state named "Idle"
        transitions:  # LOGIC: A list of rules for leaving this state
          - event: BUTTON_PRESSED  # TRIGGER: The specific signal string the engine listens for. These events will be sent by interpreter.queue('BUTTON_PRESSED') from the Python file.
            target: Authenticating  # DESTINATION: The name of the next state to move to.
            action: print(">> System Woke Up")  # SIDE EFFECT: Python code executed *during* the transition.

      - name: Authenticating
        transitions:
          - event: PIN_ACCEPTED
            target: Unlocked
            action: print(">> PIN Verified. Solenoid clicked.")

      - name: Unlocked
        transitions:
          - event: DOOR_PULLED
            target: Open
            action: print(">> Door is now physically open.")

      - name: Open
        # This state has no 'transitions' block.
        # It is a "dead end" (or sink state).
        # The system stays here forever because no events are defined to leave it.
```

## How to Run

1. Ensure you have Sismic installed:

    ```bash
    pip install sismic
    ````

2.  Run the Python script:

    ```bash
    python run_vault.py
    ```

## What to Look For
  * **State Names:** Notice how the output `Current State` changes from `[]` to `['Authenticating']`, and so on.
  * **Actions:** Notice the lines starting with `>>`. These are printed automatically by the Sismic engine because we defined `action: print(...)` in the YAML file.
  * **The Invalid Step:** At the end of the script, we try to press the button while the door is Open. Notice that the state **does not change**. This is the core power of a State Machine: if a transition isn't defined for the current state, the event is safely ignored.

## Playground: Things to Try

Modify `vault.yaml` to learn the mechanics:

1.  **Create a Loop:**

      * Currently, the `Open` state is a dead end.
      * Add a transition to the `Open` state so that the event `DOOR_CLOSED` moves the system back to `Idle`.
      * *Hint:* Add `transitions:` block under `Open`.

2.  **Break the Logic:**

      * Try changing the `target` of `BUTTON_PRESSED` to `Unlocked` directly (bypassing the PIN). Run the script and see how the logic changes.

3.  **Add a Cancel Button:**

      * Add a transition to the `Authenticating` state.
      * If the event `CANCEL` is received, target `Idle`.
      * Update `run_vault.py` to test this path.

## Key Concept: "Queue & Execute"

You will notice this pattern in the Python code:

```python
interpreter.queue('EVENT_NAME')
interpreter.execute()
```

Sismic is **step-based**. `queue` puts the event in a waiting line. Nothing happens until you call `execute`. This allows you to queue multiple events (like a rapid burst of network packets) and process them in order.
