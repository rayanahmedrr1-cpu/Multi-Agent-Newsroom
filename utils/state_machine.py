class StateMachine:
    def __init__(self):
        self.state = "IDLE"
        self.history = []

    def transition(self, new_state):
        from datetime import datetime

        log = {
            "from": self.state,
            "to": new_state,
            "timestamp": datetime.utcnow().isoformat()
        }

        self.history.append(log)
        self.state = new_state

        return log