import UI

history = []

def pull_hist():
    UI.header("Session Action History", "Chronological audit log of operations")
    UI.history_table(history)

def push_hist(message):
    history.append(str(message))
