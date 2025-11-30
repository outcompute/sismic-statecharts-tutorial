# Chapter 7: Testing & Visualization

## Goal

This chapter moves from "playing" with statecharts to "engineering" them.
1. **Visualization:** We will generate a visual diagram of our logic with a script. This helps to get a visual representation of what the states and their transitions look like.
2. **Automated Testing:** We will write a test suite using Python's `unittest` framework to prove our logic works.

## How to Run

### 1. Generate Diagram
```bash
python visualize.py
````

This generates a UML output and prints it on the screen. Copy the text, and paste it into [PlantText](https://www.planttext.com/) or the [PlantUML Server](http://www.plantuml.com/plantuml/) to see your chart.

### 2\. Run Tests

```bash
python test_vault.py
```

You should see `OK` indicating all 5 tests passed.

## Key Concepts

### Visualization (`export_to_plantuml`)

Sismic can read your YAML and output standard PlantUML code.

  * **Benefit:** You edit the YAML to change behavior, run the script, and your design documents are instantly updated. No more manually drawing boxes in Visio/Lucidchart\!

### Unit Testing (`SimulatedClock`)

Testing time-based logic is usually hard. With Sismic:

1.  We use `SimulatedClock`.
2.  We perform an action.
3.  We fast-forward time instantly (`clock.time += 4`).
4.  We assert the new state (`assertInState('LowBattery')`).

This allows us to test "4 hours of battery drain" in 0.001 seconds.

We verify that even in a test environment, we queue a dummy event after moving the clock to ensure the interpreter performs a cycle to check the timers.

## Debugging & Inspection

When writing tests, it is helpful to inspect the internal state of the machine. You can print these properties inside your Python scripts or tests:

### 1\. Active States (`configuration`)

Returns a list of all states the machine is currently in.

```python
print(interpreter.configuration)
# Output: ['Active', 'SecurityRegion', 'Locked']
```

### 2\. Internal Memory (`context`)

Returns the dictionary of variables defined in the preamble or modified by actions.

```python
print(interpreter.context)
# Output: {'CORRECT_PIN': 1234, 'attempts': 2}
```

### 3\. Execution Trace (`execute()`)

The `execute()` method returns a list of "Steps" taken during that cycle. If the list is empty, nothing happened.

```python
steps = interpreter.execute()
for step in steps:
    print(f"Left: {step.exited_states} -> Entered: {step.entered_states}")
```

### 4\. Current Time (`clock.time`)

Useful for verifying your `SimulatedClock` logic.

```python
print(f"Virtual Time: {interpreter.clock.time}s")
```