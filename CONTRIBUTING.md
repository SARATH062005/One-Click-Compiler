# Contributing to One-Click-Compiler

Thank you for your interest in improving One-Click-Compiler.  
We welcome bug reports, feature suggestions, and code contributions that make the tool more reliable, user-friendly, and maintainable.

---

## How to contribute

You can contribute by:
- Reporting bugs or requesting new features.
- Submitting fixes, improvements, or new functionality via pull requests.
- Enhancing documentation, examples, or project structure.

---

## Reporting bugs or requesting features

Before creating a new issue, please:
- Check the [issue tracker](link-to-your-repo/issues) to see if it already exists.
- Open a new issue if it’s not yet reported.

When reporting a bug, include:
- A clear description of the problem.
- Steps to reproduce the issue.
- Any relevant terminal output or error messages.
- Your environment details (Windows version, Python version, Visual Studio version, OpenCV version).

---

## Submitting code changes

1. **Create a new branch** from `main`:
   ```bash
   git checkout -b feat/short-description
   ```
    or
    ```bash
    git checkout -b fix/short-description
    ```

2. **Implement your changes**

   * Keep the separation between the UI (`main.py`) and backend logic (`backend_operations.py`).
   * Test thoroughly before submitting.

3. **Commit your changes** with a clear, concise message:

   ```bash
   git commit -m "feat: add confirmation dialog before running"
   ```

4. **Push your branch** and open a Pull Request against `main`:

   ```bash
   git push origin feat/short-description
   ```

   * In the PR description, explain **what** you changed and **why**.

---

## Style guidelines

* Maintain logical separation between UI and backend code.
* Use descriptive variable names and clear, readable code.
* Add comments for complex logic.
* Prefer simplicity over unnecessary complexity.

---

## Review process

All contributions will be reviewed for:

* Correctness and safety of changes.
* Readability and maintainability.
* Consistency with project goals and structure.
* Documentation updates if applicable.

We appreciate your contributions and your effort in keeping One-Click-Compiler efficient and easy to use.✨

