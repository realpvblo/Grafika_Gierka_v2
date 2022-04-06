TITLE = "The Return of Quazzy Osborne"
SCREENWIDTH = 930
SCREENHEIGHT = 480
FPS = 60
STAGEWIDTH = 2600
STAGEHEIGHT = 600

# Define Colours
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
CYAN = (0,255,255)
MAGENTA  = (255,0,255)

# Player Settings
PLAYER_ACCELERATION = 0.5
PLAYER_FRICTION = -0.12
GRAVITY = 0.8
JUMP_HEIGHT = 12

JSONLEVELS = '{"Levels": ['
JSONLEVELS +=    '{"Level":"01", "Map":"Map01","Eniemes":['
JSONLEVELS +=       '{"Type":"Rocks","Entities":['
JSONLEVELS +=           '{"Height":180,"DelayStart":3,"FreqSecs":8,"Direction":"Right","Speed":5,"Size":30,"Set":"0"},'
JSONLEVELS +=           '{"Height":260,"DelayStart":3,"FreqSecs":5,"Direction":"Left","Speed":5,"Size":30,"Set":"0"},'
JSONLEVELS +=           '{"Height":160,"DelayStart":10,"FreqSecs":10,"Direction":"Left","Speed":10,"Size":70,"Set":"0"}'
JSONLEVELS +=       ']}'
JSONLEVELS +=   ']}'
JSONLEVELS += ']}'

STATUS_RUNNING = "Running"
STATUS_DYING = "Dying"
STATUS_DEAD = "Dead"
STATUS_OUTOFLIVES = "OutOfLives"
STATUS_GOALGOT = "GoalGot"

TEXT_FONT = "tahoma"


