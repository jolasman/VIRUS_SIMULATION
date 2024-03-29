import json
import yaml
import sys
import math

with open('../config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

simulation = config['SIMULATION']['PARAMS']
static = config['SIMULATION']['STATIC']['PARAMS']
agent = config['SIMULATION']['AGENT']['PARAMS']
colors = config['SIMULATION']['VISUALIZATION']['PARAMS']['COLORS_DICT']
graphic_sizes = config['SIMULATION']['VISUALIZATION']['PARAMS']['SIZES']

LOG_LEVEL = config['LOG_LEVEL']
APP_NAME = config['APP_NAME']
EPISODES = simulation['EPISODES']
TOTAL_NUMBER_OF_AGENTS = simulation['TOTAL_NUMBER_OF_AGENTS']
TRAVELLING_NUMBER_OF_AGENTS = simulation['TRAVELLING_NUMBER_OF_AGENTS']

# vaccine
vaccinated_prcnt_of_agents = simulation['VACCINATED_PRCNT_OF_AGENTS']
if vaccinated_prcnt_of_agents > 1 or vaccinated_prcnt_of_agents < 0:  # default value
    VACCINATED_PRCNT_OF_AGENTS = 0.1
else:
    VACCINATED_PRCNT_OF_AGENTS = vaccinated_prcnt_of_agents
    
# https://www.npr.org/sections/health-shots/2021/01/12/956051995/why-you-should-still-wear-a-mask-and-avoid-crowds-after-getting-the-covid-19-vac?t=1610797724544
FIRST_DOSE_IMMUNE_TIME = simulation['FIRST_DOSE_IMMUNE_TIME']  # days
FIRST_DOSE_IMMUNE_PRCNT = simulation['FIRST_DOSE_IMMUNE_PRCNT']  # percentage
SECOND_DOSE_IMMUNE_TIME = simulation['SECOND_DOSE_IMMUNE_TIME']  # days, a week after the second dose
SECOND_DOSE_IMMUNE_PRCNT = simulation['SECOND_DOSE_IMMUNE_PRCNT'] # percentage

NO_MORE_SICK_AGENTS_TRAVELLING_STEP = simulation['NO_MORE_SICK_AGENTS_TRAVELLING_STEP']

SIZE = simulation['SIZE']
PIXELS = simulation['PIXELS']
RANDOM_LIMIT = simulation['RANDOM_LIMIT']

# percentage of the agents that moves in the step
AGENTS_MOVEMENT_PERCENTAGE = simulation['AGENTS_MOVEMENT_PERCENTAGE']
quarantine_x = simulation['QUARANTINE_X']
quarantine_y = simulation['QUARANTINE_Y']
dead_x = simulation['DEAD_X']
dead_y = simulation['DEAD_Y']
if (dead_x > 0 or dead_x < SIZE) or (dead_y > 0 or dead_y < SIZE):
    DEAD_X = -1
    DEAD_Y = -1
else:
    DEAD_X = dead_x
    DEAD_Y = dead_y

if (quarantine_x > 0 or quarantine_x < SIZE) or (quarantine_y > 0 or quarantine_y < SIZE):
    QUARANTINE_X = -10
    QUARANTINE_Y = -10
else:
    QUARANTINE_X = quarantine_x
    QUARANTINE_Y = quarantine_y


# number of people detected and starting quarantine
QUARANTINE_PERCENTAGE = simulation['QUARANTINE_PERCENTAGE']
# number of days until peoople goo to quarantine
QUARANTINE_DAYS = simulation['QUARANTINE_DAYS']


# probabilities of being of one type in random simulation with no static values
HEALTH_ARRAY_P = [agent['HEALTH_ARRAY_SICK_P'],
                  agent['HEALTH_ARRAY_ASYMP_P'], agent['HEALTH_ARRAY_HEALTHY_P']]

# Probability of recovering but with sequels
RECOVERY_SEQUELS_P = agent['RECOVERY_SEQUELS_P']

# Probability of being infected when in contact with an infected agent
SICK_P = agent['SICK_P']
ASYMPTOMATIC_P = agent['ASYMPTOMATIC_P']
HEALTHY_P = agent['HEALTHY_P']

# initial minimal distance between agents
SOCIAL_DISTANCE = agent['SOCIAL_DISTANCE']
# can move to a position x y +SOCIAL_DISTANCE_STEP and -SOCIAL_DISTANCE_STEP
SOCIAL_DISTANCE_STEP = agent['SOCIAL_DISTANCE_STEP']
# distance that triggers a possible contagious if one of the agents is infected
CONTAGIOUS_DISTANCE = agent['CONTAGIOUS_DISTANCE']
# number of times the agent tries to keep the social distance until quit
SOCIAL_DISTANCE_TRIES = agent['SOCIAL_DISTANCE_TRIES']

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
SICK_PRCNTG = static['SICK_PRCNTG']
ASYMP_PRCNTG = static['ASYMP_PRCNTG']
if sum([SICK_PRCNTG + ASYMP_PRCNTG]) > 1:
    sys.exit(f"SICK_PRCNTG + ASYMP_PRCNTG must sum to 1")

IMMMUNE_IMR_PRCNTG = static['IMMMUNE_IMR_PRCNTG']
ASYMP_IMR_PRCNTG = static['ASYMP_IMR_PRCNTG']
MOD_IMR_PRCNTG = static['MOD_IMR_PRCNTG']
SEVERE_IMR_PRCNTG = static['SEVERE_IMR_PRCNTG']
DEAD_IMR_PRCNTG = static['DEAD_IMR_PRCNTG']
if math.ceil(sum([IMMMUNE_IMR_PRCNTG + ASYMP_IMR_PRCNTG + MOD_IMR_PRCNTG + SEVERE_IMR_PRCNTG + DEAD_IMR_PRCNTG])) != 1:
    sys.exit(f"IMMMUNE_IMR_PRCNTG + ASYMP_IMR_PRCNTG + MOD_IMR_PRCNTG + SEVERE_IMR_PRCNTG + DEAD_IMR_PRCNTG must sum to 1")

AGENTS_WEARING_MASK_PRCNTG = static['AGENTS_WEARING_MASK_PRCNTG']
if AGENTS_WEARING_MASK_PRCNTG > 1:
    sys.exit(f"AGENTS_WEARING_MASK_PRCNTG must be less or equal to 1")

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
IMR_SEVERE_INFECTED = 3
IMR_DEADLY_INFECTED = 4


IMR_DICT = {
    0: "IMR_IMMUNE",
    1: "IMR_ASYMPTOMATIC",
    2: "IMR_MODERATELY_INFECTED",
    3: "IMR_SEVERE_INFECTED",
    4: "IMR_DEADLY_INFECTED"
}

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
                                      INFECTED_DAYS_THRESHOLD_FOR_DEAD))  # severe symptoms

ADM_HOSP_P = TOTAL_ADMITTED_TO_HOSPITAL / TOTAL_CONF_PEOP_PORTUGAL
ADM_HOSP_ICU_P = TOTAL_ADMITTED_TO_HOSPITAL_ICU / TOTAL_CONF_PEOP_PORTUGAL
HOME_RECOVERY_P = 1 - (ADM_HOSP_ICU_P + ADM_HOSP_P)

# print(ADM_HOSP_P) 0.04421341729553618
# print(ADM_HOSP_ICU_P) 0.009040654594049688
# print(HOME_RECOVERY_P) 0.9467459281104141
# print(TOTAL_DEATH / TOTAL_CONF_PEOP_PORTUGAL) 0.015061439139304626


CHART_DATA = "../data/chart_data.txt"

PICKLE_DATA = "../data/pickle/"
