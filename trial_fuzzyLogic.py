import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as crtl

import msvcrt as m
def wait():
    m.getch()

# New Antecedent/Consecuent objects hold universe variables and membership
# functions
quality = crtl.Antecedent(np.arange(0, 11, 1), 'quality')
service = crtl.Antecedent(np.arange(0, 11, 1), 'service')
tip = crtl.Consequent(np.arange(0, 26, 1), 'tip')

# Auto-membership function population is possible with .automf(3, 5, or 7)
quality.automf(3)
service.automf(3)

# Custom membership functions can be built interactively with a familiar,
# Pythonic API
tip['low'] = fuzz.trimf(tip.universe, [0, 0, 13])
tip['medium'] = fuzz.trimf(tip.universe, [0, 13, 25])
tip['high'] = fuzz.trimf(tip.universe, [13, 25, 25])

quality['average'].view()
service.view()
tip.view()

rule1 = crtl.Rule(quality['poor'] | service['poor'], tip['low'])
rule2 = crtl.Rule(service['average'], tip['medium'])
rule3 = crtl.Rule(service['good'] | quality['good'], tip['high'])

rule1.view()

tipping_crtl = crtl.ControlSystem([rule1, rule2, rule3])
tipping = crtl.ControlSystemSimulation(tipping_crtl)

# Pass inputs to the ControlSystem using Antecedent labels with Pythonic API
# Note: if you like passinf many inputs all at once, use .inputs(dict_of_data)
tipping.input['quality'] = 6.5
tipping.input['service'] = 9.8

# Crunch the numbers
tipping.compute()

print(tipping.output['tip'])
tip.view(sim=tipping)

#wait()