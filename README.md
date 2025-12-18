### 🌐 PathFinder: Shortest Path Finder

A high-performance Flask web application designed to calculate and visualize optimal routes between nodes. This project combines efficient graph algorithms (BFS & Dijkstra) with a premium Cyber-Glassmorphism user interface.

### ✨ Features

## Two Core Algorithms:

Dijkstra's Algorithm: Finds the shortest path based on edge weights (ideal for distance/cost).

BFS (Breadth-First Search): Finds the path with the minimum number of hops (ideal for unweighted graphs).

Dynamic Edge Management: Add connections between nodes with custom weights directly from the UI.

Cyber-Glassmorphism UI: A modern, translucent interface with smooth animations and a responsive design.

Data Persistence: Automatic saving and loading of graph data using JSON storage.

Responsive Navigation: Sidebar-based layout for seamless switching between adding edges and finding paths.

### 🛠️ Tech Stack

Backend: Python 3, Flask

Algorithms: Dijkstra, Breadth-First Search (BFS)

Frontend: HTML5, CSS3 (Custom Glassmorphism), JavaScript (ES6)

Data Storage: JSON (Local File System)

### 📁 Project Structure

Python_Project_3rdSem/
│
├── static/                  # Client-side assets
│   ├── css/
│   │   └── style.css        # Premium UI styling
│   └── js/
│       └── script.js        # Animations & UI logic
│
├── templates/               # Server-side HTML
│   └── index.html           # Main application interface
│
├── backend/                 # Python Logic
│   ├── __init__.py          # Package marker
│   ├── main.py              # Flask Server entry point
│   ├── logic.py             # Graph algorithms
│   └── file_handler.py      # JSON database manager
│
├── database/                # Auto-generated
│   └── data.db              # Persistent graph data
│
├── requirements.txt         # Dependency list
└── README.md                # Project documentation


### 🚀 Installation & Setup

Clone the Repository:

git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd Python_Project_3rdSem


Install Dependencies:

pip install -r requirements.txt


Run the Application:

python -m backend.main


Access the UI:
Open your browser and navigate to http://127.0.0.1:5000.

### 📖 Usage

Add Connections: Use the "Add Connection" tab to define nodes (e.g., A to B) and their weights.

Find Path: Switch to the "Find Path" tab, enter your start and end nodes, select an algorithm, and click "Find Route".

View Results: The UI will display the optimal sequence of nodes and the total calculated cost.

Created for 3rd Semester Python Project.
