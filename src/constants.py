import json
import yaml

with open('../config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

simulation = config['SIMULATION']['PARAMS']
static = config['SIMULATION']['STATIC']['PARAMS']
agent = config['SIMULATION']['AGENT']['PARAMS']
colors = config['SIMULATION']['VISUALIZATION']['PARAMS']['COLORS_DICT']
graphic_sizes = config['SIMULATION']['VISUALIZATION']['PARAMS']['SIZES']

LOG_LEVEL = config['LOG_LEVEL']
EPISODES = simulation['EPISODES']
TOTAL_NUMBER_OF_AGENTS = simulation['TOTAL_NUMBER_OF_AGENTS']
SIZE = simulation['SIZE']
RANDOM_LIMIT = simulation['RANDOM_LIMIT']
# percentage of the agents that moves in the step
AGENTS_MOVEMENT_PERCENTAGE = simulation['AGENTS_MOVEMENT_PERCENTAGE']
QUARENTINE_X = simulation['QUARENTINE_X']
QUARENTINE_Y = simulation['QUARENTINE_Y']
DEAD_X = simulation['DEAD_X']
DEAD_Y = simulation['DEAD_Y']
# number of people detected and starting quarentine
QUARENTINE_PERCENTAGE = simulation['QUARENTINE_PERCENTAGE']
# number of days until peoople goo to quarentine
QUARENTINE_DAYS = simulation['QUARENTINE_DAYS']


# probabilities of being of one type in random simulation with no static values
HEALTH_ARRAY_P = [agent['HEALTH_ARRAY_SICK_P'],
                  agent['HEALTH_ARRAY_ASYMP_P'], agent['HEALTH_ARRAY_HEALTHY_P']]

# Probability of recovering but with sequels
RECOVERY_SEQUELS_P = agent['RECOVERY_SEQUELS_P']

# probability of of being infected when being in contact with a type of agent
SICK_P = agent['SICK_P']
ASYMPTOMATIC_P = agent['ASYMPTOMATIC_P']
HEALTHY_P = agent['HEALTHY_P']

# initial minimal distance between agents
SOCIAL_DISTANCE = agent['SOCIAL_DISTANCE']
# can move to a position x y +SOCIAL_DISTANCE_STEP and -SOCIAL_DISTANCE_STEP
SOCIAL_DISTANCE_STEP = agent['SOCIAL_DISTANCE_STEP']
# distance that triggers a possible contagious if one of the agents is infected
CONTAGIOUS_DISTANCE = agent['CONTAGIOUS_DISTANCE']


# after X days agents recover
INFECTED_DAYS_THRESHOLD_FOR_INFECTED = agent['INFECTED_DAYS_THRESHOLD_FOR_INFECTED']
# people die after X days if immune system type IMR_DEADLY_INFECTED
INFECTED_DAYS_THRESHOLD_FOR_DEAD = agent['INFECTED_DAYS_THRESHOLD_FOR_DEAD']
# stop the virus propagation
INFECTED_DAYS_THRESHOLD_FOR_NOT_CONTAGIOUS = agent['INFECTED_DAYS_THRESHOLD_FOR_NOT_CONTAGIOUS']

# wear a mask cases
CONTAGIOUS_AGENT_MASK = agent['CONTAGIOUS_AGENT_MASK']
HEALTHY_AGENT_MASK = agent['HEALTHY_AGENT_MASK']
CONTAGIOUS_AGENT_MASK_HEALTHY_MASK = agent['CONTAGIOUS_AGENT_MASK_HEALTHY_MASK']
CONTAGIOUS_AGENT_NO_MASK_HEALTHY_NO_MASK = agent['CONTAGIOUS_AGENT_NO_MASK_HEALTHY_NO_MASK']

# Static simulation values
SICK_NBR = static['SICK_NBR']
IMMMUNE_IMR_NBR = static['IMMMUNE_IMR_NBR']
ASYMP_IMR_NBR = static['ASYMP_IMR_NBR']
MOD_IMR_NBR = static['MOD_IMR_NBR']
HIGH_IMR_NBR = static['HIGH_IMR_NBR']
DEAD_IMR_NBR = static['DEAD_IMR_NBR']
PEOPLE_WEARING_MASK = static['PEOPLE_WEARING_MASK']

# BGR
COLORS_DICT = {0: (colors['SICK_COLOR'][0], colors['SICK_COLOR'][1], colors['SICK_COLOR'][2]),
               1: (colors['ASYMPTOMATIC_COLOR'][0], colors['ASYMPTOMATIC_COLOR'][1], colors['ASYMPTOMATIC_COLOR'][2]),
               2: (colors['WITH_DISEASES_SEQUELAES_COLOR'][0], colors['WITH_DISEASES_SEQUELAES_COLOR'][1], colors['WITH_DISEASES_SEQUELAES_COLOR'][2]),
               3: (colors['TOTAL_RECOVERY_COLOR'][0], colors['TOTAL_RECOVERY_COLOR'][1], colors['TOTAL_RECOVERY_COLOR'][2]),
               4: (colors['DEAD_COLOR'][0], colors['DEAD_COLOR'][1], colors['DEAD_COLOR'][2]),
               5: (colors['HEALTHY_COLOR'][0], colors['HEALTHY_COLOR'][1], colors['HEALTHY_COLOR'][2])
               }

# graphics sizes
FOUR_PLOTS_FIG_SIZE_X = graphic_sizes['FOUR_PLOTS_FIG_SIZE_X']
FOUR_PLOTS_FIG_SIZE_Y = graphic_sizes['FOUR_PLOTS_FIG_SIZE_Y']

ALL_DATA_PLOT_FIG_SIZE_X = graphic_sizes['ALL_DATA_PLOT_FIG_SIZE_X']
ALL_DATA_PLOT_FIG_SIZE_Y = graphic_sizes['ALL_DATA_PLOT_FIG_SIZE_Y']

SIMULATION_GRAPHICS_SIZE_X = graphic_sizes['SIMULATION_GRAPHICS_SIZE_X']
SIMULATION_GRAPHICS_SIZE_Y = graphic_sizes['SIMULATION_GRAPHICS_SIZE_Y']

######################################################################################

# health_status
SICK = 0
ASYMPTOMATIC = 1
WITH_DISEASES_SEQUELAES = 2  # With disease's sequelaes
TOTAL_RECOVERY = 3  # Total recovery, no symptoms while infected
DEAD = 4
HEALTHY = 5


HEALTH_STATUS_DICT = {
    0: "SICK",
    1: "ASYMPTOMATIC",
    2: "WITH_DISEASES_SEQUELAES",
    3: "TOTAL_RECOVERY",
    4: "DEAD",
    5: "HEALTHY"
}

# when generating the agents, first iterations values
HEALTH_ARRAY = [SICK, ASYMPTOMATIC, HEALTHY]

# Immune response value
IMR_IMMUNE = 0
IMR_ASYMPTOMATIC = 1
IMR_MODERATELY_INFECTED = 2
IMR_HIGHLY_INFECTED = 3
IMR_DEADLY_INFECTED = 4


# Check this site to see the base for the propability of being deadly infected for age. Updated date : 11/25/2020 12:00 p.m.
# https://covid19.min-saude.pt/ponto-de-situacao-atual-em-portugal/
# using service response saved on file
with open('../data/data.jsonc') as f:
    data = json.load(f)

LAST_DATA_POSITION = data["features"][-1]["attributes"]

TOTAL_CONF_PEOP_PORTUGAL = int(LAST_DATA_POSITION["ConfirmadosAcumulado"])
TOTAL_DEATH = int(LAST_DATA_POSITION["Obitos"])  # total number of people dead

# probability of deadly immune response
AGE_0_09_P_DIR = (int(LAST_DATA_POSITION["obitos0009m"]) + int(
    LAST_DATA_POSITION["obitos0009f"])) / TOTAL_CONF_PEOP_PORTUGAL

AGE_10_19_P_DIR = (int(LAST_DATA_POSITION["obitos1019m"]) + int(
    LAST_DATA_POSITION["obitos1019f"])) / TOTAL_CONF_PEOP_PORTUGAL

AGE_20_29_P_DIR = (int(LAST_DATA_POSITION["obitos2029m"]) + int(
    LAST_DATA_POSITION["obitos2029f"])) / TOTAL_CONF_PEOP_PORTUGAL

AGE_30_39_P_DIR = (int(LAST_DATA_POSITION["obitos3039m"]) + int(
    LAST_DATA_POSITION["obitos3039f"])) / TOTAL_CONF_PEOP_PORTUGAL

AGE_40_49_P_DIR = (int(LAST_DATA_POSITION["obitos4049m"]) + int(
    LAST_DATA_POSITION["obitos4049f"])) / TOTAL_CONF_PEOP_PORTUGAL

AGE_50_59_P_DIR = (int(LAST_DATA_POSITION["obitos5059m"]) + int(
    LAST_DATA_POSITION["obitos5059f"])) / TOTAL_CONF_PEOP_PORTUGAL

AGE_60_69_P_DIR = (int(LAST_DATA_POSITION["obitos6069m"]) + int(
    LAST_DATA_POSITION["obitos6069f"])) / TOTAL_CONF_PEOP_PORTUGAL

AGE_70_79_P_DIR = (int(LAST_DATA_POSITION["obitos7079m"]) + int(
    LAST_DATA_POSITION["obitos7079f"])) / TOTAL_CONF_PEOP_PORTUGAL

AGE_80_N_P_DIR = (int(LAST_DATA_POSITION["obitos80m"]) + int(
    LAST_DATA_POSITION["obitos80f"])) / TOTAL_CONF_PEOP_PORTUGAL

AGE_P_DIR_ARRAY = [AGE_0_09_P_DIR, AGE_10_19_P_DIR, AGE_20_29_P_DIR, AGE_30_39_P_DIR,
                   AGE_40_49_P_DIR, AGE_50_59_P_DIR, AGE_60_69_P_DIR, AGE_70_79_P_DIR, AGE_80_N_P_DIR]

# getting comulative values
ADMITTED_TO_HOSPITAL = []
ADMITTED_TO_HOSPITAL_ICU = []
for k in data["features"]:
    ADMITTED_TO_HOSPITAL.append(int(k["attributes"]["Internados"]))
    ADMITTED_TO_HOSPITAL_ICU.append(int(k["attributes"]["InternadosUCI"]))

# using a cheating mean as people can be in hospital several weeks. using infected and dead threshoulds to "increase" the mean value
TOTAL_ADMITTED_TO_HOSPITAL = sum(
    ADMITTED_TO_HOSPITAL) / (len(ADMITTED_TO_HOSPITAL) / INFECTED_DAYS_THRESHOLD_FOR_INFECTED)  # moderated symptoms
TOTAL_ADMITTED_TO_HOSPITAL_ICU = sum(ADMITTED_TO_HOSPITAL_ICU) / \
    (len(ADMITTED_TO_HOSPITAL_ICU) / (INFECTED_DAYS_THRESHOLD_FOR_INFECTED +
                                      INFECTED_DAYS_THRESHOLD_FOR_DEAD))  # high symptoms

ADM_HOSP_P = TOTAL_ADMITTED_TO_HOSPITAL / TOTAL_CONF_PEOP_PORTUGAL
ADM_HOSP_ICU_P = TOTAL_ADMITTED_TO_HOSPITAL_ICU / TOTAL_CONF_PEOP_PORTUGAL
HOME_RECOVERY_P = 1 - (ADM_HOSP_ICU_P + ADM_HOSP_P)

# print(ADM_HOSP_P) 0.04421341729553618
# print(ADM_HOSP_ICU_P) 0.009040654594049688
# print(HOME_RECOVERY_P) 0.9467459281104141
# print(TOTAL_DEATH / TOTAL_CONF_PEOP_PORTUGAL) 0.015061439139304626


CHART_DATA = '../data/chart_data.txt'