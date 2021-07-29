class FlagState:
    def __init__(self):
        self.reason = "Not supplied"
        self.flagged = False

    def update_state(self, flagged=False, reason="Not supplied"):
        if reason:
            self.reason = reason
        else:
            self.reason = "Not supplied"
        self.flagged = flagged

