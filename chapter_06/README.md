# Chapter 6: Robustness (Design by Contract)

## Goal

In complex systems (like medical devices or banking protocols), bugs can be dangerous. We don't want to just "hope" our logic is correct. We want to **enforce** it.

In this chapter, you will learn to use **Contracts**:
1.  **Invariants (`always`):** Rules that must be true *all the time* while in a specific state.
2.  **Preconditions (`before`):** Rules that must be true *before* a transition is allowed.
3.  **Postconditions (`after`):** Rules that must be true *after* a transition finishes.

Do check out this [page in the documentation](https://sismic.readthedocs.io/en/latest/contract.html). Note the usage of the `__old__` keyword in the documentation, along with examples of kind of checks implemented with `before` and `after`.

## How to Run

```bash
python run_contract.py
```
## Key Concepts

### The Invariant

In `vault_contract.yaml`, we added this to the `Locked` state:

```yaml
- name: Locked
  contract:
    - always: attempts < MAX_ATTEMPTS
```
This tells Sismic: *"While I am in the 'Locked' state (or in any child state of it), `attempts` should **always** be less than 3. If not, STOP EVERYTHING."*

### The Bug

We created a transition `DEV_TEST_FAIL` that increments the counter but **does not leave** the `Locked` state.

1.  `attempts` becomes 3.
2.  The state is still `Locked`.
3.  Sismic checks the invariant: `3 < 3` is `False`.
4.  Sismic raises `ContractError`.

### Why is this useful?

Without contracts, the system would silently continue with `attempts = 4, 5, 6...` and the user would never get locked out. The "Lockdown" feature would be broken, but nobody would know until a hacker brute-forced the safe.

With contracts, the system crashes safely during development/testing, alerting you exactly where the logic flaw is.

Note that contracts can be applied to states and transitions. The following extract from the documentation should be helpful to understand how they are used.
> For states:
> - state preconditions are checked before the state is entered (i.e., before executing on entry), in the order of occurrence of the preconditions.
> - state postconditions are checked after the state is exited (i.e., after executing on exit), in the order of occurrence of the postconditions.
> - state invariants are checked at the end of each macro step, in the order of occurrence of the invariants. The state must be in the active configuration.
> 
> For transitions:
> - the preconditions are checked before starting the process of the transition (and before executing the optional transition action).
> - the postconditions are checked after finishing the process of the transition (and after executing the optional transition action).
> - the invariants are checked twice: one before starting and a second time after finishing the process of the transition. 

Note that contracts are different from `on entry` and `on exit` and are used to establish adherence to prescribed performance envelopes.

## Playground: Things to Try

1.  **Fix the Bug:**
    * Modify the `DEV_TEST_FAIL` transition in the YAML.
    * Add a guard: `guard: attempts + 1 < MAX_ATTEMPTS`.
    * Run the script again. It should no longer crash (it will just ignore the 3rd click).

2.  **Add a Precondition:**
    * Add a contract to the `Unlocked` state.
    * `before: attempts == 0`.
    * This ensures we never accidentally unlock the door while carrying over "failed attempts" data from a previous session.
