# Chapter 9: Async, Pause & Resume (Persistence)

## Goal

Software crashes. Servers restart. Users close browser tabs.
A robust system must handle interruption.

This chapter is an attempt to learn how to **Serialize** (Freeze) a running Statechart into a file and **Deserialize** (Thaw) it later. This allows long-running workflows (like a 3-day approval process or a large firmware update) to survive system restarts.

## How to Run

```bash
python run_persistence.py
```
## Key Concepts

### 1. Serialization (`pickle`)

Sismic interpreters are standard Python objects. We can use Python's built-in `pickle` module to turn the entire memory structure (Current State, Context Variables, History) into a byte stream.

```python
# Save to disk
with open('snapshot.pkl', 'wb') as f:
    pickle.dump(interpreter, f)
```
### 2. Deserialization

When we load it back:

```python
# Load from disk
with open('snapshot.pkl', 'rb') as f:
    interpreter = pickle.load(f)
```
The interpreter wakes up **exactly** as it was.
* If it was in the `Downloading` state, it is still there.
* If the variable `progress` was `30`, it is still `30`.

### Use Cases
1.  **Web Servers:** A user does Step 1 of a wizard. You save the state to a database. They come back next week for Step 2. You load the state and resume and check if anything has changed.
2.  **Game Saves:** Saving the exact state of AI characters or quest progress.
3.  **Fault Tolerance:** Periodically saving state so that if the power goes out, the machine recovers automatically on reboot.

## Playground: Things to Try

1.  **The "Live" Edit:**
    * In `run_persistence.py`, after loading the interpreter but *before* resuming, try hacking the memory:
    * `resurrected_interpreter.context['progress'] = 90`
    * Run it. You will see it jump instantly to 90% and finish faster. This demonstrates how you can inspect and patch "frozen" systems.