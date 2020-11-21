# health_status
# 0 -> Sick
# 1 -> asymptomatic
# 2 -> With disease's sequelaes
# 3 -> Total recovery, no symptoms while infected
# 4 -> Dead
# 5 -> Healthy
SICK = 0
ASYMPTOMATIC = 1
WITH_DISEASES_SEQUELAES = 2
TOTAL_RECOVERY = 3
DEAD = 4
HEALTHY = 5

# immune_system_response, how will be its symptoms
# 0 -> Immune
# 0.1 -> Little symptoms and spread
# 0.5 -> Moderately symptoms and spread
# 0.9 -> Many symptoms and virus spread
IMMUNE_P = 0.05
LITTELE_INFECTED = 0.2
MODERATELY_INFECTED = 0.2
HIGHLY_INFECTED = 0.5
DEADLY_INFECTED = 0.05

# probability of of being infected when being in contact with a type of agent
SICK_P = 0.4
ASYMPTOMATIC_P = 0.1
HEALTHY_P = 0.5


FOUR_PLOTS_FIG_SIZE_X = 12
FOUR_PLOTS_FIG_SIZE_Y = 10

ALL_DATA_PLOT_FIG_SIZE_X = 12
ALL_DATA_PLOT_FIG_SIZE_Y = 10

SIMULATION_GRAPHICS_SIZE_X = 600
SIMULATION_GRAPHICS_SIZE_Y = 600