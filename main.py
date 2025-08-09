from typing import TypedDict, List, Union, Literal
from langgraph.graph import StateGraph
import random

class TutorState(TypedDict):
    student_name: str
    current_level: int
    difficulty: Literal["easy", "medium", "hard"]
    current_problem: dict
    student_answer: Union[float, None]
    hints_remaining: int
    problems_attempted: int
    correct_answers: int
    streak: int
    feedback: str
    conversation_history: List[str]
    is_finished: bool

def generate_word_problem(difficulty: str) -> dict:
    """Generate a word problem based on difficulty"""
    templates = {
        "easy": [
            lambda: {
                "question": f"If you have {random.randint(1, 10)} apples and your friend gives you {random.randint(1, 5)} more, how many apples do you have?",
                "operation": "+",
                "nums": [random.randint(1, 10), random.randint(1, 5)]
            },
            lambda: {
                "question": f"You have {random.randint(5, 15)} cookies and eat {random.randint(1, 5)} of them. How many cookies are left?",
                "operation": "-",
                "nums": [random.randint(5, 15), random.randint(1, 5)]
            }
        ],
        "medium": [
            lambda: {
                "question": f"A restaurant sells {random.randint(20, 50)} pizzas each day. How many pizzas do they sell in {random.randint(3, 7)} days?",
                "operation": "*",
                "nums": [random.randint(20, 50), random.randint(3, 7)]
            },
            lambda: {
                "question": f"If {random.randint(2, 5)} friends share {random.randint(10, 30)} candies equally, how many candies does each friend get?",
                "operation": "/",
                "nums": [random.randint(10, 30), random.randint(2, 5)]
            }
        ],
        "hard": [
            lambda: {
                "nums": [random.randint(10, 30), random.randint(2, 5), random.randint(5, 15)],
                "question": lambda nums: f"You start with {nums[0]} marbles. You lose {nums[1]} marbles, then win {nums[2]} more. How many marbles do you have now?",
                "operation": "complex"
            }
        ]
    }
    
    problem_template = random.choice(templates[difficulty])
    problem = problem_template()
    
    if problem["operation"] == "+":
        answer = sum(problem["nums"])
    elif problem["operation"] == "-":
        answer = problem["nums"][0] - problem["nums"][1]
    elif problem["operation"] == "*":
        answer = problem["nums"][0] * problem["nums"][1]
    elif problem["operation"] == "/":
        answer = problem["nums"][0] / problem["nums"][1]
    elif problem["operation"] == "complex":
        # For complex problems: start - losses + wins
        answer = problem["nums"][0] - problem["nums"][1] + problem["nums"][2]
    
    return {
        "question": problem["question"],
        "correct_answer": answer,
        "difficulty": difficulty,
        "hints": [
            "Try breaking down the problem into smaller parts",
            "Write down the important numbers",
            f"The operation(s) you need: {problem['operation']}"
        ]
    }

def greet_student(state: TutorState) -> TutorState:
    """Initial greeting and setup"""
    message = f"Hello {state['student_name']}! Welcome to the Adaptive Math Tutor! 🎓\n"
    message += "We'll start with easy problems and adjust the difficulty based on your performance.\n"
    message += "You can ask for hints by typing 'hint' instead of an answer (you have 3 hints per session)."
    
    state['conversation_history'] = [message]
    state['current_level'] = 1
    state['difficulty'] = "easy"
    state['problems_attempted'] = 0
    state['correct_answers'] = 0
    state['streak'] = 0
    state['hints_remaining'] = 3
    return state

def present_problem(state: TutorState) -> TutorState:
    """Present a new problem to the student"""
    # Adjust difficulty based on performance
    if state['streak'] >= 3 and state['difficulty'] == "easy":
        state['difficulty'] = "medium"
        state['conversation_history'].append("\n🎉 Level Up! You've advanced to medium difficulty!")
    elif state['streak'] >= 3 and state['difficulty'] == "medium":
        state['difficulty'] = "hard"
        state['conversation_history'].append("\n🌟 Amazing! You've reached hard difficulty!")
    elif state['streak'] <= -2 and state['difficulty'] == "hard":
        state['difficulty'] = "medium"
        state['conversation_history'].append("\nLet's go back to medium difficulty and build up your skills!")
    elif state['streak'] <= -2 and state['difficulty'] == "medium":
        state['difficulty'] = "easy"
        state['conversation_history'].append("\nLet's practice with some easier problems!")

    problem = generate_word_problem(state['difficulty'])
    state['current_problem'] = problem
    
    # Add difficulty indicator emoji
    difficulty_emoji = {"easy": "🟢", "medium": "🟡", "hard": "🔴"}
    
    message = f"\n{difficulty_emoji[state['difficulty']]} Problem #{state['problems_attempted'] + 1}:\n"
    message += problem['question']
    message += "\n(Type 'hint' if you need help)"
    
    state['conversation_history'].append(message)
    return state

def process_answer(state: TutorState) -> TutorState:
    """Process the student's answer or hint request"""
    if isinstance(state['student_answer'], str) and state['student_answer'] == "hint":
        if state['hints_remaining'] > 0:
            hint = state['current_problem']['hints'][3 - state['hints_remaining']]
            state['hints_remaining'] -= 1
            state['conversation_history'].append(f"\n💡 Hint: {hint}")
            state['conversation_history'].append(f"({state['hints_remaining']} hints remaining)")
        else:
            state['conversation_history'].append("\n❌ Sorry, you're out of hints!")
        return state
    elif state['student_answer'] is not None:
        return check_answer(state)
    return state

def check_answer(state: TutorState) -> TutorState:
    """Check the student's answer and provide feedback"""
    correct_answer = state['current_problem']['correct_answer']
    student_answer = state['student_answer']
    
    state['problems_attempted'] += 1
    
    try:
        # Check if answer is within 0.1 for division problems
        is_correct = abs(float(student_answer) - correct_answer) < 0.1
    except (TypeError, ValueError):
        is_correct = False
    
    if is_correct:
        state['correct_answers'] += 1
        state['streak'] += 1
        feedback = random.choice([
            "Excellent work! 🌟",
            "Perfect! Keep it up! ✨",
            "You're doing great! 🎯",
            "Outstanding! 🏆"
        ])
    else:
        state['streak'] = max(-3, state['streak'] - 1)
        feedback = f"Not quite. The correct answer is {correct_answer:.1f}. Keep trying! 💪"
    
    state['conversation_history'].append(f"Your answer: {student_answer}")
    state['conversation_history'].append(feedback)
    
    # Add performance statistics
    accuracy = (state['correct_answers'] / state['problems_attempted']) * 100
    stats = f"\nStats:\n"
    stats += f"✓ Accuracy: {accuracy:.1f}%\n"
    stats += f"🔥 Current streak: {max(0, state['streak'])}\n"
    stats += f"📚 Current level: {state['difficulty'].title()}"
    state['conversation_history'].append(stats)
    
    # Check if we should continue
    state['is_finished'] = state['problems_attempted'] >= 8
    return state

def router(state: TutorState) -> dict:
    """Route to either the next problem or end the session"""
    # The router should return a dict with the next node to execute
    if state['is_finished']:
        return {"next": "end_session"}
    return {"next": "present_problem"}

def end_session(state: TutorState) -> TutorState:
    """End the tutoring session with final feedback"""
    final_accuracy = (state['correct_answers'] / state['problems_attempted']) * 100
    message = "\n🎓 Session Complete! 🎓\n"
    message += f"Final score: {state['correct_answers']}/{state['problems_attempted']} ({final_accuracy:.1f}%)\n"
    message += f"Highest level reached: {state['difficulty'].title()}\n"
    
    # Add personalized feedback
    if final_accuracy >= 90:
        message += "Outstanding performance! You're ready for even bigger challenges! 🏆"
    elif final_accuracy >= 70:
        message += "Great work! Keep practicing to reach the next level! 🌟"
    else:
        message += "Good effort! Remember, every problem you tackle helps you improve! 💪"
    
    state['conversation_history'].append(message)
    return state

# Create the graph
graph = StateGraph(TutorState)

# Add nodes
graph.add_node("greet", greet_student)
graph.add_node("present_problem", present_problem)
graph.add_node("process_answer", process_answer)
graph.add_node("router", lambda state: router(state))
graph.add_node("end_session", end_session)

# Add edges
graph.add_edge("greet", "present_problem")
graph.add_edge("present_problem", "process_answer")
graph.add_edge("process_answer", "router")
# Add conditional edges from router based on the "next" key in the returned dict
graph.add_conditional_edges(
    "router",
    lambda x: x["next"]
)

# Set entry and finish points
graph.set_entry_point("greet")
graph.set_finish_point("end_session")

# Compile the graph
app = graph.compile()

# Interactive usage
if __name__ == "__main__":
    # Get student name
    name = input("Please enter your name: ")
    
    # Initial state
    initial_state = {
        "student_name": name,
        "current_level": 1,
        "difficulty": "easy",
        "current_problem": None,
        "student_answer": None,
        "hints_remaining": 3,
        "problems_attempted": 0,
        "correct_answers": 0,
        "streak": 0,
        "feedback": "",
        "conversation_history": [],
        "is_finished": False
    }
    
    # Start tutoring session
    state = initial_state
    
    # First run through greeting and first problem
    state = app.invoke(state)
    print("\n".join(state["conversation_history"]))
    
    # Interactive session
    while not state["is_finished"]:
        # Get user's answer
        answer = input("\nYour answer (or type 'hint' for help): ").strip().lower()
        
        # Process the answer
        if answer == 'hint':
            state["student_answer"] = "hint"
        else:
            try:
                state["student_answer"] = float(answer)
            except ValueError:
                print("Please enter a valid number or 'hint'")
                continue
        
        # Update state and show results
        state = app.invoke(state)
        print("\n".join(state["conversation_history"][-5:]))  # Show last 5 messages
