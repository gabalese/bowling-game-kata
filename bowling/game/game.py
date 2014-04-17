class Game(object):
    def __init__(self, number_of_frames):
        self.available_frames = self.create_frames(number_of_frames)
        self.completed_frames = []
        self.current_frame = self.available_frames.pop(0)

    @staticmethod
    def create_frames(how_many):
        frames = []
        for n in range(how_many-1):
            frames.append(Frame())
        frames.append(LastFrame())
        return frames

    def roll(self, pins):
        if not self.current_frame.has_rolls_left:
            self.get_next_frame()
        self.current_frame.roll(pins)

    def get_next_frame(self):
        self.completed_frames.append(self.current_frame)
        self.current_frame = self.available_frames.pop(0)

    def score(self):
        return self.get_score(self.completed_frames + [self.current_frame], 0)

    def get_score(self, remaining_frames, points_accumulator):
        head, tail = remaining_frames[0], remaining_frames[1:]
        points_accumulator += head.score
        roll_scores = self.get_roll_scores(tail[0:2])
        if len(tail) == 0:
            return points_accumulator
        if head.is_spare:
            points_accumulator += roll_scores.next()
        if head.is_strike:
            points_accumulator += roll_scores.next() + roll_scores.next()
        return self.get_score(tail, points_accumulator)

    @staticmethod
    def get_roll_scores(frames):
        for frame in frames:
            for roll in frame.completed_rolls:
                yield roll.score


class Frame(object):
    def __init__(self):
        self.available_rolls = [Roll(), Roll()]
        self.completed_rolls = []
        self.score = 0

    def roll(self, pins):
        current_roll = self.get_next_roll()
        current_roll.score = pins
        self.score += current_roll.score
        self.completed_rolls.append(current_roll)
        if current_roll.is_strike:
            self.available_rolls.pop(0)

    def get_next_roll(self):
        return self.available_rolls.pop(0)

    @property
    def has_rolls_left(self):
        return len(self.available_rolls) > 0

    @property
    def is_spare(self):
        return self.score == 10 and self.completed_rolls[0].score != 10

    @property
    def is_strike(self):
        return self.score == 10 and self.completed_rolls[0].score == 10


class LastFrame(Frame):
    def __init__(self):
        super(LastFrame, self).__init__()

    def roll(self, pins):
        current_roll = self.get_next_roll()
        current_roll.score = pins
        self.score += current_roll.score
        self.completed_rolls.append(current_roll)
        if self.is_spare or self.is_strike:
            self.available_rolls.append(Roll())


class Roll(object):
    def __init__(self):
        self.score = 0

    @property
    def is_strike(self):
        return self.score == 10
