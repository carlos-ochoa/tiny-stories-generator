"""Setups for synthetic data generation
"""

resource = ""
skill_a, skill_b = "", ""
resource_a, resource_b = "", ""

resource_sharing = f"""
Setup: A has resource {resource} that B needs
Conflict: B doesn't have {resource}, might not achieve their goal
Decision: A voluntarily shares {resource} with B
Action: Both use {resource} (together or taking turns)
Consequence: Both achieve their objectives
Learning: Sharing enables mutual success
"""

turn_taking = f"""
Setup: A and B both want to use resource {resource} at the same time
Conflict: Only one can use {resource} at a time
Decision: They agree to take turns
Action: "You first, then me" (or vice versa)
Consequence: Both enjoy {resource} without fighting
Learning: Taking turns prevents conflict and allows everyone to enjoy
"""

complementary_skills = f"""
Setup: Problem/goal that requires multiple skills
Context: A has skill {skill_a}, B has skill {skill_b}
Realization: Neither can succeed alone, but together they can
Decision: Work together, each contributes their skill
Consequence: They solve the problem/achieve the goal
Learning: Different skills together > working alone
"""

tradeoffs_and_exchange = f"""
Setup: A has {resource_a} and wants {resource_b}, B has {resource_b} and wants {resource_a}
Recognition: Each has what the other needs
Decision: They propose an exchange
Action: They trade {resource_a} for {resource_b}
Consequence: Both get what they wanted
Learning: Trading creates mutual value
"""

joint_problem_solving = f"""
Setup: Problem that neither can solve alone
Attempt: A tries alone → fails, B tries alone → fails
Realization: "We need to work together"
Decision: They join forces, plan together
Action: They implement collaborative solution
Consequence: They solve the problem
Learning: Difficult problems require collaboration
"""

communication_coordination = f"""
Setup: Activity requiring coordination between A and B
Challenge: They must communicate to synchronize
Action: A communicates intention/need, B responds/adapts
Result: They achieve successful coordination
Consequence: They complete the activity
Learning: Clear communication enables coordination
"""

altruism = f"""
Setup: B has a problem or need
Context: A can help without significant cost
Decision: A helps without being asked (or after being asked)
Action: A helps B
Consequence: B solves problem, both feel good
Learning: Helping others is valuable in itself
"""

conflict_resolution = f"""
Setup: A and B have a disagreement or initial conflict
Escalation: Tension briefly increases
De-escalation: One proposes cooperative solution
Decision: Both accept compromise or alternative
Consequence: Conflict resolved, relationship preserved
Learning: Conflicts can be resolved cooperatively
"""

failed_cooperation_adjustment = f"""
Setup: A and B attempt to cooperate
Complication: Miscommunication or incorrect timing
Consequence: Initial failure
Resolution: They adjust their approach, second attempt succeeds
Learning: Cooperation requires clear communication
"""

non_cooperative_agent = f"""
Setup: A and B cooperate, C acts selfishly
Action: A and B achieve goal by cooperating, C fails alone
Consequence: A and B successful, C is not
Learning: Cooperation > selfishness (but recognizes it exists)
"""

win_lose_inevitable = f"""
Setup: Limited resource, no perfect win-win solution
Decision: One sacrifices something for greater good or relationship
Consequence: Asymmetric outcome but accepted
Learning: Sometimes cooperation involves sacrifice
"""

fair_competition = f"""
Setup: A and B compete
Action: They compete while respecting rules
Consequence: One wins, one loses, but both accept the result
Learning: Competition can coexist with respect
"""

basic_setup = """
The story
should have the following features: {features}.
"""

all_setups = {
    "resource_sharing" : resource_sharing,
    "turn_taking" : turn_taking,
    "complementary_skills" : complementary_skills,
    "tradeoffs_and_exchange" : tradeoffs_and_exchange,
    "joint_problem_solving" : joint_problem_solving,
    "communication_coordination" : communication_coordination,
    "altruism" : altruism,
    "conflict_resolution" : conflict_resolution,
    "failed_cooperation_adjustment" : failed_cooperation_adjustment,
    "non_cooperative_agent" : non_cooperative_agent,
    "win_lose_inevitable" : win_lose_inevitable,
    "fair_competition" : fair_competition,
    "basic_setup" : basic_setup,
}