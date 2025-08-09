# Adaptive Math Tutor using LangGraph

An interactive command-line math tutoring system built with LangGraph that adapts to student performance.

## Features

- 🎯 Adaptive difficulty levels (Easy, Medium, Hard)
- 💡 Hint system with 3 hints per session
- 📊 Real-time performance tracking
- 🔄 Dynamic problem generation
- 📈 Progress tracking with streaks
- 🎓 Personalized feedback

## Project Structure

```
langgraph/
├── agents/              # Basic agent examples
│   ├── 01.py           # Simple compliment agent
│   ├── 02.py           # Calculator agent
│   ├── 03.py           # Multi-node agent
│   └── 04.py           # Conditional edges agent
├── main.py             # Advanced adaptive math tutor
└── README.md           # Project documentation
```

## Requirements

- Python 3.8+
- langgraph

## Installation

1. Create a virtual environment:
```bash
python -m venv .venv
```

2. Activate the virtual environment:
```bash
# On Windows
.venv\Scripts\activate

# On Unix or MacOS
source .venv/bin/activate
```

3. Install dependencies using uv (recommended):
```bash
uv pip install -r requirements.txt
# OR use the locked dependencies for exact versions
uv pip install --requirements uv.lock
```

Alternatively, using pip:
```bash
pip install langgraph
```

## Usage

Run the advanced math tutor:
```bash
python main.py
```

Or try the basic examples in the agents folder:
```bash
python agents/01.py  # Try the simple compliment agent
python agents/02.py  # Try the calculator agent
python agents/03.py  # Try the multi-node agent
python agents/04.py  # Try the conditional edges agent
```

## Features in Detail

### Adaptive Difficulty
- Easy: Simple addition and subtraction with small numbers
- Medium: Multiplication and division
- Hard: Multi-step word problems

### Performance Tracking
- Tracks accuracy percentage
- Maintains winning streaks
- Adjusts difficulty based on performance

### Hint System
- 3 hints available per session
- Progressive hints from general to specific
- Helps students learn problem-solving strategies


