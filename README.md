# Mastering Statecharts with Python & Sismic

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Statecharts](https://img.shields.io/badge/architecture-statecharts-green)

This repository contains a progressive, chapter-based tutorial for learning **Harel Statecharts** using the [Sismic](https://sismic.readthedocs.io/) library in Python.

While the goal for me was to learn about statecharts, I will keep the code here if it helps someone else. I was working on implementing the TCP/IP networking stack, and quickly got pulled into having to implement state machines within states of larger state machines. I read [this paper](https://www.sciencedirect.com/science/article/pii/0167642387900359), which carries a quote that aptly summarizes the situation I found myself in.

> However, it is also generally agreed that a complex system cannot be beneficially described in this naive fashion, because of the unmanageable, exponentially growing multitude of states, all of which have to be arranged in a ‘flat’ unstratified fashion, resulting in an unstructured, unrealistic, and chaotic state diagram. To be useful, a state/event approach must be modular, hierarchical and well-structured. It must also solve the exponential blow-up problem by somehow relaxing the requirement that all combinations of states have to be represented explicitly. 

The goal of this tutorial of sorts, is to understand hierarchal, orthogonal, and event-driven statecharts capable of handling complex systems, such as networking protocols and stacks.
This is also to appreciate and gratitude to all the people who have maintained the sismic library for more than a decade, and curating a great selection of features to incorporate in the library (schema, design by contract, bdd).

## The Scenario: "The Smart Vault"

Throughout these chapters, we build and evolve a **Secure Vault System**. 
* We start with a simple lock (Open/Closed).
* We evolve it to handle PIN authentication, biometric timeouts, tamper protection, and battery management.
* We robustify it with Design by Contract (DbC) and automated tests.
* Finally we take a look at the synchronized and asynchronous behaviour of the sismic library and the interpreter object.

## Chapter Roadmap

| Chapter | Title | Concepts Covered |
| :--- | :--- | :--- |
| **01** | **The Linear Workflow** | Basic YAML structure, the Interpreter loop, Event queueing. |
| **02** | **Data & Context** | Passing payloads (`event.pin`), Guards (`event.x == context.y`), Context variables. |
| **03** | **Python Integration** | Binding Python methods to states, executing side-effects (Actions). |
| **04** | **Time & Automation** | Timers (`after(5)`), Internal transitions. |
| **05** | **Complex Architecture** | **Hierarchy** (Nested states) and **Orthogonality** (Parallel regions). |
| **06** | **Robustness** | **Design by Contract**, Invariants, Pre/Post conditions, Exception handling. |
| **07** | **Testing & Visualization** | Generating PlantUML diagrams, and Unit testing. |
| **08** | **Synchronization and Multiple Statecharts** | Property statecharts, connecting and synchronizing multiple statecharts. |
| **09** | **Async, Pause & Resume** | Async Processing, Pausing and Resuming statechart execution. |

## Getting Started

0. You can run the commands present in the chapter in a compute environment of your choice, but I prefer to use a container, and you can use a command such as: `docker run --rm -it --name sismic-dev -w /workspace python:3.6 bash` to start a usable container.
1. **Clone the repository:**
   ```bash
   git clone https://github.com/outcompute/sismic-statecharts-tutorial.git
   cd sismic-statecharts-tutorial
    ````

2.  **Install Sismic:**
    Sismic is the engine we use to execute the YAML statecharts.

    ```bash
    pip install sismic
    ```

3.  **Run a Chapter:**
    Navigate to a chapter directory and run the runner script.

    ```bash
    cd chapter_01
    python run_vault.py
    ```

## Resources & References
If you want to dive deeper into the theory and the tool:

### The Theory (Statecharts)

  * **[Statecharts: A Visual Formalism for Complex Systems (PDF)](https://www.sciencedirect.com/science/article/pii/0167642387900359)**: The original 1987 paper by David Harel. This is the academic foundation of everything used in this repo.
  * **[Statecharts.dev](https://statecharts.dev/)**: An excellent, friendly introduction to why statecharts are better than boolean flags.
  * **[W3C SCXML Specification](https://www.w3.org/TR/scxml/)**: Sismic is largely based on SCXML (State Chart XML), the web standard for state machines.

### The Tool (Sismic)

  * **[Sismic Documentation](https://sismic.readthedocs.io/en/latest/)**: The official guide and API reference.
  * **[Sismic GitHub](https://github.com/AlexandreDecan/sismic)**: Source code and examples.


## Contributing

Feel free to fork this repository and add your own scenarios\! If you find a bug in the examples, please open an issue. If you want to add a chapter to this very repo, raise a PR.
