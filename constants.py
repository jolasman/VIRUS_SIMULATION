EPISODES = 100
TOTAL_NUMBER_OF_AGENTS = 1_000
SIZE = 250
RANDOM_LIMIT = 20
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
HEALTH_ARRAY_P = [0.02, 0.001, 0.979]  # probabilities of being of one type


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
FOUR_PLOTS_FIG_SIZE_X = 6
FOUR_PLOTS_FIG_SIZE_Y = 5

ALL_DATA_PLOT_FIG_SIZE_X = 12
ALL_DATA_PLOT_FIG_SIZE_Y = 10

SIMULATION_GRAPHICS_SIZE_X = 900
SIMULATION_GRAPHICS_SIZE_Y = 900


SOCIAL_DISTANCE = 0  # initial minimal distance between agents
SOCIAL_DISTANCE_STEP = 0 # can move to a position x y +SOCIAL_DISTANCE_STEP and -SOCIAL_DISTANCE_STEP
CONTAGIOUS_DISTANCE = 2 # distance that triggers a possible contagious if one of the agents is infected


INFECTED_DAYS_THRESHOLD_FOR_INFECTED = 15 # after X days agents recover
INFECTED_DAYS_THRESHOLD_FOR_DEAD = 5 # people die after X days if immune system type IMR_DEADLY_INFECTED
INFECTED_DAYS_THRESHOLD_FOR_NOT_CONTAGIOUS = 10 # stop the virus propagation

NAMES_LIST_A = ["Abdelnour","Abdelrahman","Abdi","Abdo","Abdon","Abdoo","Abdou","Abdul","Abdulla","Abdullah","Abe","Abebe","Abed","Abee","Abegg","Abegglen","Abeita","Abel","Abela","Abele","Abeles","Abell","Abella","Abello","Abelman","Abeln","Abels","Abelson","Abend","Abendroth","Aber","Abercrombie","Aberg","Aberle","Aberman","Abernathey","Abernathy","Abernethy","Abert","Abeyta","Abid","Abila","Abitz","Abke","Able","Ableman","Abler","Ables","Abner","Abney","Jacot","Jacoway","Jacox","Jacquart","Jacque","Jacquemin","Jacques","Jacquet","Jacquez","Jacquin","Jacquot","Jadin","Jadwin","Jaeckel","Jaeckle","Jaecks","Jaeger","Jaegers","Jaekel","Jaenicke","Jaeschke","Jafari","Jaffa","Jaffe","Jaffee","Jaffer","Jafri","Jagels","Jager","Jagers","Jaggard","Jaggars","Jagger","Jaggers","Jaggi","Jagiello","Jagielski","Jagla","Jaglowski","Jagneaux","Jago","Jagoda","Jagodzinski","Jagoe","Jagow","Jagusch","Jahn","Jahner","Jahnke","Jahns","Taffet","Taflinger","Tafolla","Tafoya","Taft","Tafuri","Tag","Tagawa","Tager","Tagert","Tagg","Taggart","Tagge","Taggert","Tagle","Tagliaferri","Tagliaferro","Taglieri","Taguchi","Tague","Taha","Tahan","Tahara","Taheri","Tahir","Tahtinen","Tai","Taibi","Taillon","Tailor","Taing","Tainter","Taira","Tait","Taitano","Taite","Taitt","Tajima","Tak","Takach","Takacs","Takagi","Takahashi","Takai","Takaki","Takala","Takamoto","Takano","Takara","Takashima","Pacocha","Pacyna","Paczkowski","Padalino","Padberg","Paddack","Padden","Paddock","Paddy","Padelford","Paden","Paderewski","Padfield","Padget","Padgett","Padgham","Padgitt","Padilla","Padin","Padley","Padlo","Padmanabhan","Padmore","Pado","Padon","Padovani","Padovano","Padrick","Padro","Padron","Padua","Paduano","Paduch","Padula","Pae","Paek","Paepke","Paes","Paeth","Paetow","Paetz","Paetzold","Paez","Paff","Pafford","Paffrath","Pagac","Pagan","Paganelli","Pagani"]
NAMES_LIST_B = ["Ma","Maack","Maag","Maahs","Maalouf","Maas","Maaske","Maass","Maassen","Maat","Mabb","Mabbitt","Mabe","Mabee","Maben","Maberry","Mabery","Mabey","Mabie","Mabile","Mabin","Mable","Mabon","Mabray","Mabrey","Mabry","Mabus","Mac","MacAdam","MacAdams","MacAfee","Macak","MacAllister","MacAlpine","Macaluso","Macaraeg","Macari","Macario","MacArthur","MacArtney","MacAskill","MacAulay","MacAuley","MacBain","MacBeth","MacBride","MacCallum","Maccarone","MacCarthy","MacCartney","Macchi","Macchia","Macchio","Macchione","Maccini","MacConnell","MacCormack","MacCracken","MacCubbin","MacDermott","MacDiarmid","MacDonald","MacDonell","MacDonnell","MacDonough","MacDougal","MacDougall","MacDowell","MacDuff","Mace","MacEachern","Macedo","Macek","Macera","MacEwan","MacEwen","Macey","MacFadden","MacFadyen","MacFarland","MacFarlane","MacGeorge","MacGibbon","MacGill","MacGillivray","MacGowan","MacGregor","MacGuire","Mach","Macha","Machac","Machacek","Machado","Machak","Machala","Machamer","Machan","Machart","Machemer","Machen","Gaa","Gaal","Gaar","Gaarder","Gaba","Gabaldon","Gabay","Gabbard","Gabbay","Gabbert","Gabe","Gabehart","Gabel","Gabelman","Gaber","Gabert","Gabhart","Gable","Gabler","Gabor","Gaboriault","Gaboury","Gabrick","Gabriel","Gabriele","Gabrielle","Gabrielli","Gabrielse","Gabrielsen","Gabrielson","Gabris","Gabrys","Gaby","Gac","Gaccione","Gacek","Gach","Gacke","Gackle","Gad","Gadberry","Gadbois","Gadbury","Gadd","Gaddie","Gaddis","Gaddy","Gade","Gaden","Gadient","Gadomski","Gadoury","Gadow","Gadsby","Gadsden","Gadson","Gadway","Gadzinski","Gaebel","Gaebler","Gaede","Gaer","Gaertner","Gaeta","Gaetani","Gaetano","Gaeth","Gaetz","Gaff","Gaffaney","Gaffey","Gaffin","Gaffke","Gaffner","Gaffney","Gafford","Gafner","Gagan","Gagas","Gage","Gagel","Gagen","Gager","Gagliano","Gagliardi","Gagliardo","Gaglio","Gaglione","Gagnard","Gagne","Gagner","Gagnier","Gagnon","Gago","Gagon","Gahagan","Gahan","Gahm","Gahn","Gahr"]
NAMES_LIST_C = ["O’Banion","O’Bannon","O’Bar","O’Barr","O’Bear","O’Beirne","O’Berry","O’Boyle","O’Brian","O’Briant","O’Brien","O’Brion","O’Bryan","O’Bryant","O’Bryon","O’Byrne","O’Cain","O’Callaghan","O’Callahan","O’Carroll","O’Connell","O’Conner","O’Connor","O’Conor","O’Daniel","O’Day","O’Dea","O’Dean","O’Doherty","O’Donald","O’Donnel","O’Donnell","O’Donoghue","O’Donohue","O’Donovan","O’Dowd","O’Driscoll","O’Dwyer","O’Fallon","O’Farrell","O’Flaherty","O’Flanagan","O’Flynn","O’Gara","O’Gorman","O’Grady","O’Guin","O’Guinn","O’Hagan","O’Hair","O’Haire","O’Halloran","O’Hanlon","O’Hara","O’Hare","O’Harra","O’Harrow","O’Haver","O’Hearn","O’Hern","O’Herron","O’Higgins","O’Hora","O’Kane","O’Keefe","O’Keeffe","O’Kelley","O’Kelly","O’Laughlin","O’Lear","O’Leary","O’Loughlin","O’Mahoney","O’Mahony","O’Maley","O’Malley","O’Mara","O’Mary","O’Meara","O’Melia","O’Neal","O’Neall","O’Neel","O’Neil","O’Neill","O’Ney","O’Quin","O’Quinn","O’Rear","O’Regan","O’Reilly","O’Riley","O’Riordan","O’Roark","O’Rorke","O’Rourke","O’Ryan","O’Shaughnessy","O’Shea","Eachus","Eacker","Eacret","Eaddy","Eade","Eader","Eades","Eadie","Eads","Eady","Eagan","Eagar","Eagen","Eager","Eagerton","Eagle","Eagleburger","Eagles","Eagleson","Eagleston","Eagleton","Eaglin","Eagon","Eaken","Eaker","Eakes","Eakin","Eakins","Eakle","Eakman","Eales","Ealey","Ealy","Eames","Eanes","Eardley","Eargle","Earhart","Earl","Earle","Earles","Earley","Earll","Earls","Early","Earlywine","Earman","Earnest","Earney","Earnhardt","Earnhart","Earnheart","Earnshaw","Earnst","Earp","Earthman","Earwood","Eary","Eash","Easler","Easley","Easlick","Easom","Eason","East","Eastburn","Eastep","Easter","Easterbrook","Easterday","Easterlin","Easterling","Easterly","Easterwood","Eastes","Eastham","Eastin","Eastlack","Eastland","Eastlick","Eastling","Eastlund","Eastman","Eastmond","Easton","Eastridge","Eastwood","Eatherly","Eatherton","Eatman","Eatmon","Eaton","Eavenson","Eaves","Eavey","Ebach","Ebanks","Ebarb","Ebaugh","Ebben","Elsabichao"]