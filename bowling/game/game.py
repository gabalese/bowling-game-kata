class Game(object):
    def __init__(self):
        self.available_frames = [Frame(), Frame(), Frame(), Frame(), Frame(),
                                 Frame(), Frame(), Frame(), Frame(), TenthFrame()]
        self.completed_frames = []
        self.current_frame = self.available_frames.pop(0)

    def roll(self, pins):
        if self.current_frame.has_no_rolls_left:
            self.get_next_frame()
        self.current_frame.roll(pins)

    def get_next_frame(self):
        self.completed_frames.append(self.current_frame)
        self.current_frame = self.available_frames.pop(0)

    def score(self):
        self.completed_frames.append(self.current_frame)
        points = 0
        for index, frame in enumerate(self.completed_frames):
            points += frame.score
            if frame.score == 10:
                try:
                    points += self.completed_frames[index+1].completed_rolls[0].score
                except IndexError:
                    pass
            if frame.is_strike:
                try:
                    points += self.completed_frames[index+1].completed_rolls[1].score
                except IndexError:
                    try:
                        points += self.completed_frames[index+2].completed_rolls[0].score
                    except IndexError:
                        pass
        return points


class Frame(object):
    def __init__(self):
        self.available_rolls = [Roll(), Roll()]
        self.completed_rolls = []
        self.score = 0
        self.is_spare = False
        self.is_strike = False

    def roll(self, pins):
        current_roll = self.available_rolls.pop(0)
        current_roll.score = pins
        self.score += current_roll.score
        if self.score == 10:
            if self.has_rolls_left:
                self.is_strike = True
                self.available_rolls.pop(0)
            else:
                self.is_spare = True
        self.completed_rolls.append(current_roll)

    @property
    def has_no_rolls_left(self):
        return len(self.available_rolls) == 0

    @property
    def has_rolls_left(self):
        return len(self.available_rolls) > 0


class TenthFrame(Frame):
    def __init__(self):
        super(TenthFrame, self).__init__()
        self.available_rolls = [Roll(), Roll(), Roll()]

    def roll(self, pins):
        current_roll = self.available_rolls.pop(0)
        current_roll.score = pins
        self.score += current_roll.score
        if self.score == 10:
            if self.has_rolls_left:
                self.is_strike = True
            else:
                self.is_spare = True
        self.completed_rolls.append(current_roll)


class Roll(object):
    def __init__(self):
        self.score = 0
