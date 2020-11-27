import json
EPISODES = 500
TOTAL_NUMBER_OF_AGENTS = 1_000
SIZE = 200
RANDOM_LIMIT = 20
AGENTS_MOVEMENT_PERCENTAGE = 1  # percentage of the agents that moves in the step
QUARENTINE_X = -10
QUARENTINE_Y = -10
DEAD_X = -1
DEAD_Y = -1
QUARENTINE_PERCENTAGE = 0.5 # number of people detected and starting quarentine
QUARENTINE_DAYS = 5 # number of days until peoople goo to quarentine

# Statit simulation values
SICK_NBR = 200
HEALTHY_NBR = 800
IMMMUNE_IMR_NBR = 10
ASYMP_IMR_NBR = 50
MOD_IMR_NBR = 190
HIGH_IMR_NBR = 650
DEAD_IMR_NBR = 100
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
HEALTH_ARRAY_P = [0.02, 0.001, 0.979]  # probabilities of being of one type


# immune_system_response probability, how will be its symptoms
IMMUNE_P = 0.005  # Immune
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

SOCIAL_DISTANCE = 0  # initial minimal distance between agents
# can move to a position x y +SOCIAL_DISTANCE_STEP and -SOCIAL_DISTANCE_STEP
SOCIAL_DISTANCE_STEP = 0
# distance that triggers a possible contagious if one of the agents is infected
CONTAGIOUS_DISTANCE = 2


INFECTED_DAYS_THRESHOLD_FOR_INFECTED = 15  # after X days agents recover
# people die after X days if immune system type IMR_DEADLY_INFECTED
INFECTED_DAYS_THRESHOLD_FOR_DEAD = 5
INFECTED_DAYS_THRESHOLD_FOR_NOT_CONTAGIOUS = 10  # stop the virus propagation


# Check this site to see the base for the propability of being deadly infected for age. Updated date : 11/25/2020 12:00 p.m.
# https://covid19.min-saude.pt/ponto-de-situacao-atual-em-portugal/
# using service response saved on file
with open('data.jsonc') as f:
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




# graphics sizes
FOUR_PLOTS_FIG_SIZE_X = 8
FOUR_PLOTS_FIG_SIZE_Y = 8

ALL_DATA_PLOT_FIG_SIZE_X = 12
ALL_DATA_PLOT_FIG_SIZE_Y = 10

SIMULATION_GRAPHICS_SIZE_X = 900
SIMULATION_GRAPHICS_SIZE_Y = 900
