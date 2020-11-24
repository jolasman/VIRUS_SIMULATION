
import uuid
import random

class Agent:
    def __init__(self, pos_X, pos_Y, name="anonymous", age=None, health_status=0, immune_system_response=0):
        if age is None:
            age = random.randint(0, 100)

        if name is None:
            name = "anonymous"

        if health_status is None:
            health_status = 0

        if immune_system_response is None:
            immune_system_response = 0

        self.id = uuid.uuid1()
        self.name = name
        self.age = age
        self.health_status = health_status
        self.previous_health_status = None
        self.immune_system_response = immune_system_response
        self.pos_X = pos_X
        self.pos_Y = pos_Y
        self.pos_tuple = (self.pos_X, self.pos_Y)
        self.infected_days = None
        self.recovered = False

    def step(self, new_posX, new_posY):
        """
        Simulating the environment step
        """
        self.pos_X = new_posX
        self.pos_Y = new_posY

    def set_position(self, pos_X, pos_Y):
        """
        """
        self.pos_X = pos_X
        self.pos_Y = pos_Y
        self.pos_tuple = (self.pos_X, self.pos_Y)

    def __str__(self):
        return f"\n\nAgent {self.id}\nName: {self.name}\nAge: {self.age}\nHealth Status: {self.health_status}\nImmune System Response: {self.immune_system_response}\nPosition: ({self.pos_X}, {self.pos_Y}) "
