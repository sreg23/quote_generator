# Inspirational quote generator
Generate random inspirational quotes

This microservice provides inspirational quotes. It is designed to be integrated with a To-Do list application to display a quote each time the list is shown.

## Communication Contract

**### 1. How to Programmatically Request Data**

To request a quote from the microservice, use ZeroMQ to send a `REQUEST_QUOTE` message. Here is an example call in Python:

```python
import zmq

def request_quote():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    socket.setsockopt(zmq.RCVTIMEO, 2000)  # Set a timeout of 3000 ms for receiving

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


**### 2. How to Programmatically Receive Data**

The response from the microservice will be a single quote string which is an inspirational quote. 
Each time a quote is requested, the microservice sends back one of these strings as a single quote.

Here is an example of how you can handle the response:

def display_task_list(task_list):
    print("\n--- To-Do List ---")
    for idx, task in enumerate(task_list, 1):
        print(f"{idx}. {task}")

    print("\n--- Inspirational Quote ---")
    quote = request_quote()
    if quote:
        print(f"{quote}\n")
    else:
        print("Could not retrieve a quote at this time.\n")

# Example usage
def main():
    task_list = [
        "Complete project",
        "Walk the dog",
        "Exercise for 30 minutes",
        "Call Mom",
    ]

    display_task_list(task_list)

if __name__ == "__main__":
    main()
