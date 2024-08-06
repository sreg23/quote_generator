import zmq
import time

# Function to request a quote from the microservice
def request_quote():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    socket.setsockopt(zmq.RCVTIMEO, 2000)  # Set a timeout of 2000 ms for receiving

    try:
        socket.send_string("REQUEST_QUOTE")
        quote = socket.recv_string()
        if quote.startswith("An error occurred") or quote == "Unknown request":
            return f"Server error: {quote}"
        return quote
    except zmq.Again:
        return "Request timed out."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Function to display the task list and an inspirational quote
def display_todo_list(todo_list, quote):
    start_time = time.time()
    print("\n--- To-Do List ---")
    for idx, task in enumerate(todo_list, 1):
        print(f"{idx}. {task}")

    elapsed_time = time.time() - start_time
    if elapsed_time > 2:
        print("Warning: The task list took more than 2 seconds to display.")

    print("\n--- Inspirational Quote ---")
    if quote:
        print(f"{quote}\n")
    else:
        print("Could not retrieve a quote at this time.\n")

def main():
    # Simulated To-Do list
    todo_list = [
        "Complete Python project",
        "Read a book",
        "Exercise for 30 minutes",
        "Call a friend",
    ]

    # Track displayed quotes to ensure no repetition until all have been used
    displayed_quotes = set()

    for _ in range(10):  # Simulate multiple requests
        quote = request_quote()
        while quote in displayed_quotes:
            quote = request_quote()

        displayed_quotes.add(quote)
        if len(displayed_quotes) == len(quote):  # Reset after all quotes are used
            displayed_quotes.clear()

        display_todo_list(todo_list, quote)

if __name__ == "__main__":
    print("Starting test script to simulate To-Do list calls...")
    main()

