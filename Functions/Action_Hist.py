# Simple in-memory log for this session. It resets when the program closes.
history=[]
history = []

def pull_hist():
    # Print every message we've stored, in the order they happened.
    for i in history:
        print(i)

def push_hist(message):
    # Add one new line to the log.
    history.append(message)

