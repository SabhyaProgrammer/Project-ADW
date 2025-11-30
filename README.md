# 🌿 Herb Inventory System

A professional, lightweight, and efficient command-line interface (CLI) application designed for managing a detailed inventory of herbs. This system allows users to track herb names, prices, and locations with ease, persisting data securely in a JSON format.

## 📋 Table of Contents
- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Data Storage](#-data-storage)
- [Contributing](#-contributing)

## ✨ Features

The Herb Inventory System offers a robust set of tools for inventory management:

*   **➕ Add New Herbs**: Input detailed information including Name, Price, and Location (City/Region).
*   **👀 View Inventory**: Display a formatted table of all herbs currently in the system with IDs for easy reference.
*   **✏️ Edit Existing Entries**: Modify specific details (Name, Price, or Location) of any herb in the inventory.
*   **🗑️ Delete Entries**: Remove outdated or incorrect entries from the database securely.
*   **💾 Persistent Storage**: Automatically saves all data to a local `herbs_data.json` file, ensuring no data is lost between sessions.
*   **🛡️ Input Validation**: Robust error handling for invalid prices or menu selections.

## 🛠 Prerequisites

Before running this project, ensure you have the following installed:

*   **Python 3.6+**: This project is built using standard Python libraries. You can download it from [python.org](https://www.python.org/downloads/).

## 🚀 Installation

1.  **Clone the Repository** (or download the source code):
    ```bash
    git clone <repository-url>
    cd S2
    ```

2.  **Verify Files**:
    Ensure `mini-project_s2.py` is present in the directory.

## 📖 Usage

To start the application, run the main Python script from your terminal:

```bash
python mini-project_s2.py
```

### Main Menu Navigation

Once the application starts, you will be presented with the following options:

1.  **Add Herb**: Follow the prompts to enter the herb's name, price, and location. Type `back` at any prompt to return to the previous step.
2.  **View Inventory**: Lists all herbs with their unique ID, Name, Price, and Location.
3.  **Edit Herb**: Enter the ID of the herb you wish to modify, then select the specific field to update.
4.  **Delete Herb**: Enter the ID of the herb to remove it permanently.
5.  **Save and Quit**: Saves your current session's changes to `herbs_data.json` and exits the program.

> **Note**: Always choose "Save and Quit" to ensure your latest changes are written to the disk.

## 📂 Project Structure

```text
S2/
├── mini-project_s2.py    # Main application entry point and logic
├── herbs_data.json       # JSON database storing inventory records (auto-generated)
├── Untitled-2.py         # Utility script for generating sample data (Optional)
└── README.md             # Project documentation
```

## 🧪 Developer Tools

### Sample Data Generator
The project includes a utility script `Untitled-2.py` that can generate random "Isekai-style" herb data for testing purposes.

**Usage:**
```bash
python Untitled-2.py --generate-sample [count] [seed]
```
*   `count`: Number of herbs to generate (default: 100)
*   `seed`: Random seed for reproducibility (default: 42)

*Note: This will replace your current in-memory list and save it to `herbs_data.json`.*

## 💾 Data Storage

Data is stored in `herbs_data.json` in a human-readable JSON format. 

**Example Data Structure:**
```json
[
    {
        "name": "Lavender",
        "price": 12.50,
        "location": "Provence"
    },
    {
        "name": "Basil",
        "price": 5.00,
        "location": "Rome"
    }
]
```

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements or new features (like search functionality or export to CSV), feel free to fork the repository and submit a pull request.

---
*Generated for the Herb Inventory System Project.*
