class BDI:
    def __init__(self, beliefs):
        self.beliefs = beliefs  # a list of facts
        self.desires = []
        self.intentions = []

# Example: start with metabolic beliefs
beliefs = [{
    "hunger": 90.0,
    "thirst": 75.0,
    "fatigue": 10.0,
    "energy": 60.0,
    "temperature": 37.0
}]

# thresholds
thirst_on = 70
thirst_off = 40

hunger_on = 70
hunger_off = 40



agent = BDI(beliefs)
# agent remembers current intention
agent.current_intention = None
print(agent.beliefs)
"""
def generate_desires(agent):
    desires = []
    metabolic = agent.beliefs[0]  # assume first belief is metabolic

    if metabolic["thirst"] > 70:
        desires.append({"action": "Drink", "urgency": metabolic["thirst"]})
    if metabolic["hunger"] > 70:
        desires.append({"action": "Eat", "urgency": metabolic["hunger"]})
    if metabolic["fatigue"] > 60:
        desires.append({"action": "Rest", "urgency": metabolic["fatigue"]})

    return desires

desires = generate_desires(agent)
print(desires)

def deliberate(agent, desires):
    if not desires:
        return None

    # Choose strongest desire
    strongest = max(desires, key=lambda d: d["urgency"])
    agent.intentions = [strongest]  # commit
    return strongest

intention = deliberate(agent, desires)
print(intention)

def means_ends(intention):
    if intention:
        return intention["action"]
    return None

action = means_ends(intention)
print(action)

def execute_action(agent, action):
    metabolic = agent.beliefs[0]

    if action == "Drink":
        metabolic["thirst"] = max(0, metabolic["thirst"] - 80)
        metabolic["energy"] += 5
    elif action == "Eat":
        metabolic["hunger"] = max(0, metabolic["hunger"] - 80)
        metabolic["energy"] += 25
    elif action == "Rest":
        metabolic["fatigue"] = max(0, metabolic["fatigue"] - 60)
        metabolic["energy"] += 50

    # natural drift over time
    metabolic["hunger"] += 2
    metabolic["thirst"] += 2
    metabolic["fatigue"] += 1

execute_action(agent, action)
print(agent.beliefs)



def generate_desires_with_hysteresis(agent):
    desires = []
    metabolic = agent.beliefs[0]

    thirst = metabolic["thirst"]
    hunger = metabolic["hunger"]

    # --- THIRST with hysteresis ---
    keep_drinking = False

    if agent.current_intention and agent.current_intention["action"] == "Drink":
        if thirst > thirst_off:
            keep_drinking = True

    if thirst > thirst_on or keep_drinking:
        desires.append({"action": "Drink", "urgency": thirst})

    # --- HUNGER with hysteresis ---
    keep_eating = False

    if agent.current_intention and agent.current_intention["action"] == "Eat":
        if hunger > hunger_off:
            keep_eating = True

    if hunger > hunger_on or keep_eating:
        desires.append({"action": "Eat", "urgency": hunger})

    return desires


def deliberate_with_persistence(agent, desires):
    if not desires:
        agent.current_intention = None
        return None

    # persistence: keep current intention if still valid
    if agent.current_intention:
        for d in desires:
            if d["action"] == agent.current_intention["action"]:
                agent.current_intention["urgency"] = d["urgency"]
                return agent.current_intention

    # otherwise choose strongest desire
    strongest = max(desires, key=lambda d: d["urgency"])
    agent.current_intention = strongest
    return strongest


#for minute in range(1, 11):
#    desires = generate_desires(agent)
#    intention = deliberate(agent, desires)
#    action = means_ends(intention)
#    execute_action(agent, action)
#    print(f"Minute {minute}, Beliefs: {agent.beliefs}")

    
for minute in range(1, 11):

    desires = generate_desires_with_hysteresis(agent)
    intention = deliberate_with_persistence(agent, desires)
    action = means_ends(intention)
    execute_action(agent, action)

    print(f"Minute {minute}, Action: {action}, Beliefs: {agent.beliefs}")
"""