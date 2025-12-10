#!/usr/bin/env python3
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional


# -----------------------------
# ENUM TYPES
# -----------------------------

class DesireType(Enum):
    Eat = "Eat"
    Drink = "Drink"
    Rest = "Rest"
    CoolDown = "CoolDown"
    WarmUp = "WarmUp"
    Explore = "Explore"    # optional emotional action


class IntentionType(Enum):
    PerformPlan = "PerformPlan"   # a multi-step plan


# -----------------------------
# ATTITUDE
# -----------------------------

@dataclass
class Attitude:
    label: Enum
    representation: Dict[str, float]


# -----------------------------
# BASE BDI
# -----------------------------

class BDI:
    def __init__(self, beliefs):
        self.beliefs = beliefs
        self.desires: List[Attitude] = []
        self.intentions: List[Attitude] = []


# -----------------------------
# ANIMAT BDI AGENT (final version)
# -----------------------------

class AnimatBDI(BDI):

    def __init__(self, beliefs):
        super().__init__(beliefs)

        # persistent intention
        self.current_intention: Optional[Attitude] = None

        # hysteresis thresholds
        self.thirst_on = 60
        self.thirst_off = 40

        self.hunger_on = 40
        self.hunger_off = 30

        self.fatigue_on = 40
        self.fatigue_off = 20

        # desire priorities (Drink > Eat > Rest)
        self.priority = {
            "Drink": 3,
            "Eat": 2,
            "Rest": 1,
            "CoolDown": 5,
            "WarmUp": 5,
            "Explore": 0.5
        }

        # multi-step plans
        self.plans = {
            "Drink": ["GoToWater", "DrinkWater"],
            "Eat": ["GoToKitchen", "EatFood"],
            "Rest": ["GoToBed", "LieDown", "Sleep"],
            "CoolDown": ["MoveToShade", "CoolDownBody"],
            "WarmUp": ["FindHeatSource", "WarmBody"],
            "Explore": ["LookAround", "WalkRandomly"]
        }

        # homeostasis targets
        self.targets = {
            "hunger": 45,
            "thirst": 40,
            "fatigue": 30,
            "temperature": 37.0,
        }

    # -----------------------------------------
    # HOMEOSTATIC DRIVE
    # -----------------------------------------
    def drive(self, current, target):
        return max(0, current - target)

    # -----------------------------------------
    # STEP 1 — Generate desires (with hysteresis + homeostasis)
    # -----------------------------------------
    def generate_desires(self):
        m = self.beliefs[0]
        desires = []

        # --- THIRST ---
        thirst_drive = self.drive(m["thirst"], self.targets["thirst"])
        thirsty = (m["thirst"] > self.thirst_on)

        keep_drink = False
        if self.current_intention and self.current_intention.representation["action"] == "Drink":
            if m["thirst"] > self.thirst_off:
                keep_drink = True

        if thirsty or keep_drink:
            desires.append({
                "action": "Drink",
                "urgency": thirst_drive * self.priority["Drink"]
            })

        # --- HUNGER ---
        hunger_drive = self.drive(m["hunger"], self.targets["hunger"])
        hungry = (m["hunger"] > self.hunger_on)

        keep_eat = False
        if self.current_intention and self.current_intention.representation["action"] == "Eat":
            if m["hunger"] > self.hunger_off:
                keep_eat = True

        if hungry or keep_eat:
            desires.append({
                "action": "Eat",
                "urgency": hunger_drive * self.priority["Eat"]
            })

        # --- FATIGUE ---
        fatigue_drive = self.drive(m["fatigue"], self.targets["fatigue"])
        tired = (m["fatigue"] > self.fatigue_on)

        keep_rest = False
        if self.current_intention and self.current_intention.representation["action"] == "Rest":
            if m["fatigue"] > self.fatigue_off:
                keep_rest = True

        if tired or keep_rest:
            desires.append({
                "action": "Rest",
                "urgency": fatigue_drive * self.priority["Rest"]
            })

        # --- TEMPERATURE ---
        if m["temperature"] > 38:
            desires.append({
                "action": "CoolDown",
                "urgency": (m["temperature"] - self.targets["temperature"]) * self.priority["CoolDown"]
            })

        if m["temperature"] < 36:
            desires.append({
                "action": "WarmUp",
                "urgency": (self.targets["temperature"] - m["temperature"]) * self.priority["WarmUp"]
            })

        # --- OPTIONAL EMOTIONAL DESIRE: EXPLORE ---
        if m.get("boredom", 0) > 50:
            desires.append({
                "action": "Explore",
                "urgency": m["boredom"] * self.priority["Explore"]
            })

        return desires

    # -----------------------------------------
    # STEP 2 — Deliberation (with persistence)
    # -----------------------------------------
    def deliberate(self, desires):
        if not desires:
            self.current_intention = None
            return None

        # persistence: keep current intention if still valid
        if self.current_intention:
            cur_action = self.current_intention.representation["action"]
            for d in desires:
                if d["action"] == cur_action:
                    # update urgency
                    self.current_intention.representation["urgency"] = d["urgency"]
                    return self.current_intention

        # otherwise choose strongest desire
        strongest = max(desires, key=lambda d: d["urgency"])
        intention = Attitude(
            IntentionType.PerformPlan,
            {"action": strongest["action"], "urgency": strongest["urgency"]}
        )
        self.current_intention = intention
        return intention

    # -----------------------------------------
    # STEP 3 — Means–Ends Reasoning (multi-step plan)
    # -----------------------------------------
    def means_ends(self, intention):
        if intention is None:
            return None
        action = intention.representation["action"]
        return self.plans[action]

    # -----------------------------------------
    # STEP 4 — Execute Action: update metabolic state
    # -----------------------------------------
    def execute_action(self, plan):
        m = self.beliefs[0]

        # If plan exists, perform final step effect
        if plan:
            final_action = plan[-1]

            if final_action == "DrinkWater":
                m["thirst"] = max(0, m["thirst"] - 80)
                m["energy"] += 5

            elif final_action == "EatFood":
                m["hunger"] = max(0, m["hunger"] - 80)
                m["energy"] += 25

            elif final_action == "Sleep":
                m["fatigue"] = max(0, m["fatigue"] - 60)
                m["energy"] += 50

            elif final_action == "CoolDownBody":
                m["temperature"] -= 1.0

            elif final_action == "WarmBody":
                m["temperature"] += 1.0

        #  ALWAYS APPLY NATURAL DRIFT
        m["hunger"] += 2
        m["thirst"] += 2
        m["fatigue"] += 1
        m["temperature"] += 0.02
        m["boredom"] = max(0, m["boredom"] + 1)

        # clamp values
        m["hunger"] = min(m["hunger"], 200)
        m["thirst"] = min(m["thirst"], 200)
        m["fatigue"] = min(m["fatigue"], 200)
        m["temperature"] = min(max(30, m["temperature"]), 42)


# -----------------------------
# SIMULATION LOOP
# -----------------------------

def main():

    # metabolic + emotional beliefs
    beliefs = [{
        "hunger": 30,
        "thirst": 65,
        "fatigue": 10,
        "energy": 60,
        "temperature": 37,
        "boredom": 20,
    }]

    agent = AnimatBDI(beliefs)

    print("\n--- ANIMAT BDI SIMULATION ---\n")

    for minute in range(1, 21):
        print(f"MINUTE {minute}")

        desires = agent.generate_desires()
        intention = agent.deliberate(desires)
        plan = agent.means_ends(intention)
        agent.execute_action(plan)

        m = agent.beliefs[0]
        print(f"  Intention: {intention.representation['action'] if intention else 'None'}")
        print(f"  Plan: {plan}")
        print(f"  State: H={m['hunger']:.1f}, T={m['thirst']:.1f}, F={m['fatigue']:.1f}, E={m['energy']:.1f}, Temp={m['temperature']:.2f}, Bored={m['boredom']:.1f}\n")


if __name__ == "__main__":
    main()
