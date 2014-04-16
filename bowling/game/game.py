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
        if self.current_frame.has_no_rolls_left:
            self.get_next_frame()
        self.current_frame.roll(pins)

    def get_next_frame(self):
        self.completed_frames.append(self.current_frame)
        self.current_frame = self.available_frames.pop(0)

    def score(self):
        points = 0
        for index, frame in enumerate(self.all_frames):
            points += frame.score
            if frame.is_spare:
                points += self.all_frames[index+1].completed_rolls[0].score
            if frame.is_strike:
                try:
                    points += self.all_frames[index+1].completed_rolls[0].score
                    points += self.all_frames[index+1].completed_rolls[1].score
                except IndexError:
                    try:
                        points += self.all_frames[index+2].completed_rolls[0].score
                    except IndexError:
                        pass
        return points

    @property
    def all_frames(self):
        return self.completed_frames + [self.current_frame]


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
    def has_no_rolls_left(self):
        return len(self.available_rolls) == 0

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
