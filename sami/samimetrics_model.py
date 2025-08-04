from .sami_model import Sami


class SamiMetrics:
    def __init__(self, sami: Sami):
        self.sami = sami

    @property
    def total_sleep(self):
        return (
            self.sami.bedtime
            + self.sami.wakeup
            + self.sami.nonstop
            + self.sami.energy
            + self.sami.naptime
            + self.sami.phone
            + self.sami.reading
        )

    @property
    def total_food(self):
        return (
            self.sami.fruits
            + self.sami.vegetables
            + self.sami.meals
            + self.sami.desserts
            + self.sami.sugardrinks
            + self.sami.nosugardrinks
        )

    @property
    def total_move(self):
        return (
            self.sami.homework
            + self.sami.garden
            + self.sami.outsidetime
            + self.sami.endurancesport
            + self.sami.yogasport
        )

    @property
    def total_idea(self):
        return (
            self.sami.computer
            + self.sami.youtube
            + self.sami.administrative
            + self.sami.papergames
            + self.sami.videogames
        )

    @property
    def total_sami(self):
        return (
            self.total_sleep
            +self.total_food
            +self.total_move
            +self.total_idea
        )
