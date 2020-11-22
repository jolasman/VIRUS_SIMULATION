EPISODES = 100
TOTAL_NUMBER_OF_AGENTS = 1000
SIZE = 200
RANDOM_LIMIT = 50
AGENTS_MOVEMENT_PERCENTAGE = 1  # percentage of the agents that moves in the step

# health_status
SICK = 0
ASYMPTOMATIC = 1
WITH_DISEASES_SEQUELAES = 2  # With disease's sequelaes
TOTAL_RECOVERY = 3  # Total recovery, no symptoms while infected
DEAD = 4
HEALTHY = 5

RECOVERY_SEQUELS_P = 0.4

HEALTH_STATUS_DICT = {
    0: "SICK",
    1: "ASYMPTOMATIC",
    2: "WITH_DISEASES_SEQUELAES",
    3: "TOTAL_RECOVERY",
    4: "DEAD",
    5: "HEALTHY"
}

# BGR
COLORS_DICT = {0: (0, 0, 255),  # red
               1: (0, 115, 255),  # orange
               2: (255, 0, 196),  # purple
               3: (0, 255, 255),  # yellow
               4: (0, 0, 0),  # dead is black
               5: (0, 255, 0)}  # green


# when generating the agents, first iterations values
HEALTH_ARRAY = [SICK, ASYMPTOMATIC, HEALTHY]
HEALTH_ARRAY_P = [0.01, 0.001, 0.989]  # probabilities of being of one type


# immune_system_response probability, how will be its symptoms
IMMUNE_P = 0.005 # Immune
ASYMPTOMATIC_P = 0.2  # Little symptoms and spread
MODERATELY_INFECTED_P = 0.2  # Moderately symptoms and spread
HIGHLY_INFECTED_P = 0.5  # Lots of symptoms and virus spread
DEADLY_INFECTED_P = 0.095  # Cannot handle the virus

# Immune response value
IMR_IMMUNE = 0
IMR_ASYMPTOMATIC = 1
IMR_MODERATELY_INFECTED = 2
IMR_HIGHLY_INFECTED = 3
IMR_DEADLY_INFECTED = 4

IMR_ARRAY = [IMR_IMMUNE,
             IMR_ASYMPTOMATIC,
             IMR_MODERATELY_INFECTED,
             IMR_HIGHLY_INFECTED,
             IMR_DEADLY_INFECTED]

IMR_ARRAY_P = [IMMUNE_P,
               ASYMPTOMATIC_P,
               MODERATELY_INFECTED_P,
               HIGHLY_INFECTED_P,
               DEADLY_INFECTED_P]


# probability of of being infected when being in contact with a type of agent
SICK_P = 0.8
ASYMPTOMATIC_P = 0.1
HEALTHY_P = 0.1

# graphics sizes
FOUR_PLOTS_FIG_SIZE_X = 12
FOUR_PLOTS_FIG_SIZE_Y = 10

ALL_DATA_PLOT_FIG_SIZE_X = 12
ALL_DATA_PLOT_FIG_SIZE_Y = 10

SIMULATION_GRAPHICS_SIZE_X = 900
SIMULATION_GRAPHICS_SIZE_Y = 900


SOCIAL_DISTANCE = 0 # initial minimal distance between agents
SOCIAL_DISTANCE_STEP = 0 # can move to a position x y +SOCIAL_DISTANCE_STEP and -SOCIAL_DISTANCE_STEP
CONTAGIOUS_DISTANCE = 2 # distance that triggers a possible contagious if one of the agents is infected


INFECTED_DAYS_THRESHOLD_FOR_INFECTED = 15 # after X days agents recover
INFECTED_DAYS_THRESHOLD_FOR_DEAD = 5 # people die after X days if immune system type IMR_DEADLY_INFECTED
INFECTED_DAYS_THRESHOLD_FOR_NOT_CONTAGIOUS = 10 # stop the virus propagation