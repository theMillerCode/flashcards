import random

# Function to create a random math problem
def generate_problem():
    num1 = random.randint(0, 12)
    num2 = random.randint(1, 12)  # Avoid zero for division
    operation = random.choice(['+', '-', '*', '/'])
    if operation == '+':
        problem = f"{num1} + {num2}"
        answer = str(num1 + num2)
    elif operation == '-':
        num1, num2 = max(num1, num2), min(num1, num2)  # Ensure num1 >= num2
        problem = f"{num1} - {num2}"
        answer = str(num1 - num2)
    elif operation == '*':
        problem = f"{num1} * {num2}"
        answer = str(num1 * num2)
    else:  # Division
        num2 = random.randint(1, 12)  # Ensure divisor is not zero
        num1 = num2 * random.randint(1, 12)  # Make num1 a multiple of num2
        problem = f"{num1} / {num2}"
        answer = str(num1 // num2)  # Integer division
    return problem, answer

