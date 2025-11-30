# Chapter 5: Complex Architecture (Hierarchy & Orthogonality)

## Goal

This chapter introduces the two most powerful features of Harel Statecharts.

1.  **Hierarchy (Nested States):**
    * **Problem:** If I have 50 states, and I want a "Stop" button to work in all of them, I don't want to draw 50 lines to the "Stopped" state.
    * **Solution:** Put the 50 states inside a parent `Active` state. Draw 1 line from `Active` to `Stopped`.

2.  **Orthogonality (Parallel Regions):**
    * **Problem:** Real systems do multiple things at once (e.g., Monitoring Battery + Listening for Input).
    * **Solution:** `parallel states`. The system is in *multiple* states simultaneously.

## The YAML file
There are three kinds of states demonstrated in the YAML, and they look something like this, with a description of these right after the YAML block below.

```yaml
states:
  # TYPE 1: COMPOSITE
  - name: CompositeParent
    initial: ChildA          # <--- REQUIRED
    states:
      - name: ChildA
      - name: ChildB

  # TYPE 2: PARALLEL
  - name: ParallelParent
    # No 'initial' here! It goes to Region1 AND Region2
    parallel states:         # <--- KEYWORD CHANGE
      - name: Region1
      - name: Region2

  # TYPE 3: SIMPLE
  - name: SimpleState
    transitions:             # <--- Logic to leave
      - event: GO
        target: CompositeParent
```

### 1\. The Composite State

  * **Official Term:** **Composite State** (or Compound State).
  * **Behavior:** This state is a "Container." Being inside this state means you **must** be inside exactly *one* of its children.
  * **Requirement:** Because you must be in a child state, you must specify which one to start in using the `initial:` field.
  * **Relevant Documentation:** [Composite States](https://sismic.readthedocs.io/en/latest/format.html#composite-states)

### 2\. The Parallel State

  * **Official Term:** **Parallel State** (or Orthogonal State).
  * **Behavior:** This state is a "Fork." Being inside this state means you are inside **all** of its children (Regions) simultaneously.
  * **Requirement:** You do not define a single `initial` for the parent, because it doesn't pick *one*. Instead, it enters every child region, and each region must handle its own initialization. This is useful to represent multiple state machines within a single system.
  * **Relevant Documentation:** [Orthogonal States](https://sismic.readthedocs.io/en/latest/format.html#orthogonal-states)
)

### 3\. The Simple State

  * **Official Term:** **Simple State** (or Leaf State / Atomic State).
  * **Behavior:** This is the bottom of the hierarchy. It performs actions (`on entry`, `on exit`) and waits for events to trigger transitions.
  * **Requirement:** It has no `states` or `parallel states` list.
  * **Relevant Documentation:** [Transitions](https://sismic.readthedocs.io/en/latest/format.html#transitions)

Check the full YAML file for the remaining details.

## How to Run

```bash
python run_complex.py
```
## Key Concepts

### 1. Global Interrupt (Hierarchy)

We defined a transition on the root `Active` container:

```yaml
- event: MASTER_RESET
  target: Maintenance
```
This acts as a "Super-Transition". It doesn't matter if we are in `Locked` or `Unlocked`, or if the battery is `Low` or `Full`. Because those states are *inside* `Active`, this transition rips us out of all of them and sends us to `Maintenance`.

### 2. Parallel Execution
In `vault_complex.yaml`, we define:

```yaml
- name: Active
  parallel states:
    - name: SecurityRegion
    - name: PowerRegion
```
When the system enters `Active`, it effectively forks. It enters the `initial` state of **every** child region.
* It enters `Locked` (Region 1)
* It enters `FullBattery` (Region 2)

**Important:** An event is sent to *all* regions.
* If we send `PIN_ENTERED`, Region 1 acts on it. Region 2 ignores it.
* If we send `after(4)`, Region 2 acts on it. Region 1 ignores it.

## Playground: Things to Try

1.  **Kill it with Dead Battery:**
    * Add a transition to `DeadBattery` in the YAML, to go to Maintenance state after one second.
    * Run the simulation longer. Watch the battery die, and see if it forces the whole system into Maintenance mode automatically.
    * Edit the `print_state()` method and print `all_states` within it to understand all the states the system represented within the statechart is in.

2.  **Add a Third Region:**
    * Add a `NetworkRegion` parallel to Security and Power.
    * States: `Connected`, `Disconnected`.
    * Make `MASTER_RESET` only work if `NetworkRegion` is `Connected` (using a guard).
