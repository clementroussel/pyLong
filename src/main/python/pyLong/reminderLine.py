class ReminderLine:

    def __init__(self):
        self.active = True
        
        self.title = ""

        self.x = 0.

        self.subplots = []

    def __eq__(self, other):
        return self.x == other.x

    def __ne__(self, other):
        return self.x != other.x

    def __gt__(self, other):
        return self.x > other.x

    def __ge__(self, other):
        return self.x >= other.x

    def __lt__(self, other):
        return self.x < other.x

    def __le__(self, other):
        return self.x >= other.x
