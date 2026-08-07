# 🏭 PetroOpt AI

## Intelligent Petrochemical Production Optimization System

PetroOpt AI is an intelligent decision support system for petrochemical production planning.

The system combines **Linear Programming**, **Genetic Algorithm**, and an **AI-based Chat Assistant** to optimize refinery production, schedule maintenance tasks, and analyze optimization results.

---

# Features

## Production Optimization

- Linear Programming optimization using PuLP
- Maximum profit calculation
- Feed constraint handling
- Energy constraint handling
- Production planning

---

## Maintenance Scheduling

- Genetic Algorithm
- Tournament Selection
- Order Crossover (OX)
- Swap Mutation
- Fitness Evaluation
- Maintenance Schedule Generation

---

## AI Chat Assistant

The intelligent chatbot can answer questions about:

- Profit Analysis
- Feed Analysis
- Energy Analysis
- Production Analysis
- Maintenance Analysis
- Optimization Summary
- Optimization Recommendations
- Bottleneck Detection
- Production Unit Explanation
- Production Unit Comparison

The chatbot also supports:

- Intent Detection
- Conversation Memory

---

## Data Visualization

- Production Dashboard
- Production Table
- Production Bar Chart

---

# Project Structure

```
PetroOptAI/

│
├── app.py
│
├── chatbot/
│   ├── assistant.py
│   ├── conversation.py
│   └── memory.py
│
├── ga/
│   ├── chromosome.py
│   ├── crossover.py
│   ├── fitness.py
│   ├── genetic.py
│   ├── mutation.py
│   ├── population.py
│   └── selection.py
│
├── lp/
│   ├── optimizer.py
│   ├── model.py
│   └── constraints.py
│
├── models/
│   ├── refinery.py
│   ├── maintenance.py
│   └── result.py
│
├── utils/
│   ├── validator.py
│   └── charts.py
│
├── requirements.txt
└── README.md
```

---

# Technologies Used

- Python
- Streamlit
- PuLP
- Genetic Algorithm
- Pandas
- Matplotlib

---

# Installation

Install the required packages:

```bash
pip install -r requirements.txt
```

---

# Run the Project

```bash
python -m streamlit run app.py
streamlit run app.py
```

---

# Optimization Algorithms

## Linear Programming

The optimization model uses Linear Programming to maximize refinery profit while satisfying:

- Feed constraints
- Energy constraints
- Production capacity constraints

---

## Genetic Algorithm

The maintenance scheduler is implemented using:

- Chromosome Representation
- Tournament Selection
- Order Crossover (OX)
- Swap Mutation
- Fitness Function

---

## AI Chat Assistant

The chatbot includes:

- Rule-based Intent Detection
- Conversation Memory
- Context-aware Follow-up Responses
- Refinery Data Analysis

---

# Example Questions

The AI assistant can answer questions such as:

- Show profit
- Show production
- Show feed analysis
- Show energy analysis
- Show maintenance schedule
- Show recommendations
- Show summary
- Explain Propylene
- Compare production units
- Show bottleneck

---

# Amirali Shahvaranian

B.Sc. Industrial Engineering Student
Sharif University of Technology, International Campus

PetroOpt AI