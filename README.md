# Adaptive Urban Ecosystem - ML Enhanced 🏙️🧠

A sophisticated agent-based simulation exploring the dynamics of an adaptive urban environment. This project models the complex interactions between intelligent agents, resource consumption, traffic congestion, and environmental impact, visualized through a real-time, multi-panel dashboard.

![Status](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## 🌟 Key Features

### 🧠 Intelligent Agents (`src/agents.py`)
- **Cognitive Architecture**: Agents possess memory, learning capabilities, and distinct personalities (Risk Tolerance, Exploration, Social, Efficiency).
- **Adaptive Decision Making**: Agents evaluate moves based on a weighted scoring system considering resources, traffic, pollution, and personal traits.
- **Learning**: Agents adapt their preferences over time based on successful or failed outcomes.
- **Internal State**: Simulation of Energy, Stress, and Satisfaction levels.

### 🌍 Dynamic Environment (`src/world.py`, `src/simulation.py`)
- **Multi-Layered Grid**:
  - **🌱 Resources**: Regenerating resource patches.
  - **🚗 Traffic**: Dynamic congestion based on agent density and movement.
  - **☁️ Pollution**: Environmental impact accumulation and diffusion.
- **Sector Analysis**: The world is divided into sectors to analyze regional health and efficiency.

### 📊 Real-Time Visualization (`src/main.py`)
A comprehensive **Matplotlib Dashboard** displaying 8 real-time metrics:
1.  **Resource Map**: Heatmap of available resources.
2.  **Traffic Grid**: Visualization of congestion hotspots.
3.  **Pollution Map**: Environmental impact tracking.
4.  **Population Density**: Agent distribution heatmap.
5.  **Zone Efficiency**: Ratio of resources to traffic.
6.  **Sector Health**: Bar charts showing regional performance.
7.  **Live Metrics**: Time-series graphs for Resources, Traffic, Pollution, Health, and Satisfaction.
8.  **System Stats**: Real-time numerical summary and overall system status (Good/Fair/Critical).

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- `pip` (Python package installer)

### Installation

1.  **Clone the Repository**
    ```bash
    git clone <repository-url>
    cd adaptive-urban-ecosystem
    ```

2.  **Create a Virtual Environment (Recommended)**
    ```bash
    # Windows
    python -m venv .venv
    .venv\Scripts\activate

    # macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    *If `requirements.txt` is missing, install manually:*
    ```bash
    pip install numpy matplotlib
    ```

---

## 🎮 Usage

Run the main simulation script from the project root:

```bash
python src/main.py
```

### Controls & Configuration
The simulation runs automatically. You can modify parameters in `src/main.py` to customize the experience:

- **Grid Size**: Change `width=40, height=40` in `Simulation()` initialization.
- **Population**: Adjust `n=60` in `sim.populate_random_people()`.
- **Simulation Speed**: Modify `interval=50` in `FuncAnimation`.

---

## 📂 Project Structure

```plaintext
adaptive-urban-ecosystem/
├── src/
│   ├── agents.py       # Agent logic (Person, AdvancedAgent)
│   ├── main.py         # Entry point & Visualization setup
│   ├── simulation.py   # Core simulation loop & state management
│   ├── world.py        # Grid & Environment definitions
│   └── utils.py        # Helper functions
├── notebooks/          # Jupyter notebooks for analysis
├── tests/              # Unit tests
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

---

## 🧠 How It Works

1.  **Initialization**: The world is generated with random resource clusters. Agents are spawned with randomized personalities.
2.  **Step Loop**:
    - **Perception**: Agents scan their local environment (vision range).
    - **Decision**: Agents score potential moves based on their internal weights and personality.
    - **Action**: Agents move, consume resources, and generate traffic/pollution.
    - **Update**: The environment updates (resource regrowth, pollution diffusion).
    - **Learning**: Agents update their memories and weights based on the outcome.
3.  **Visualization**: The dashboard updates every frame to reflect the new state.

---

## 🛠️ Customization

### Modifying Agent Behavior
Edit `src/agents.py` to tweak:
- `preference_weights`: How much agents care about different factors.
- `personality`: Ranges for random personality traits.
- `_calculate_move_score`: The logic for choosing where to move.

### Adjusting Environment Rules
Edit `src/simulation.py` (or `world.py`) to change:
- Resource regeneration rates.
- Pollution decay and spread.
- Traffic decay rates.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1.  Fork the project
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
