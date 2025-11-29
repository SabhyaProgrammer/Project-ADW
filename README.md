# The Oracle: Cognitive Decision Engine

> "It doesn't just guess. It *thinks*."

**The Oracle** is a next-gen reasoning engine that evaluates choices using a multi-dimensional cognitive framework. Unlike basic decision trees, The Oracle simulates a 5-stage reasoning pipeline to deliver decisions that are logically coherent, adaptive, and ethically aware.

## 🧠 The 5 Dimensions of Cognition

Every decision is analyzed through five distinct lenses:

1.  **Logical Coherence (25%)**: Is the decision rational and consistent with your goals?
2.  **Adaptivity (20%)**: Is the choice flexible enough to handle changing conditions?
3.  **Transparency (20%)**: Is the reasoning clear and easy to explain?
4.  **Innovation (20%)**: Does the option offer a novel or creative approach?
5.  **Ethical Awareness (15%)**: Does the decision respect boundaries and long-term sustainability?

## 🚀 Features

*   **Contextual Awareness**: Adapts to pressure, fatigue, and specific constraints.
*   **Self-Reflective Feedback Loop**: The Oracle learns from your feedback. If you disagree with a choice, it adjusts its internal weights for next time.
*   **Human-Readable Justification**: Get a breakdown of *why* a decision was made, not just a black-box result.
*   **Interactive CLI**: A slick command-line interface to test scenarios or build your own.

## 🛠️ Getting Started

### Prerequisites

*   Python 3.8+

### Installation

Clone the repo and you're good to go. No heavy dependencies.

```bash
git clone https://github.com/yourusername/the-oracle.git
cd the-oracle
```

### Running the Demo

Fire up the engine:

```bash
python demo.py
```

Follow the prompts to choose a scenario (Work, Travel) or create a **Custom Scenario** to test the engine against your own life choices.

## 📂 Project Structure

*   `sage.py`: The brain. Contains the main `Sage` class and the reasoning pipeline.
*   `layers.py`: The neural pathways. Implements Perception, Conditional Logic (Dimensions), Evaluation, and Justification.
*   `models.py`: Data structures for Scenarios, Options, and Decisions.
*   `demo.py`: The interface.
*   `data/`: Where the Oracle stores its memories (learned weights and decision history).

## 🧪 Testing

Want to verify the core logic? Run the test script:

```bash
python verify_sage.py
```

---
*Built with 💻 and ☕ by a 16yo dev.*
