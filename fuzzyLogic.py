import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class FuzzyLogic():

    def __init__ (self):
        angleCenter = 26.0
        angleStep = 0.4
        angleSigma = 2.5
        forceCenter = 0.
        forceStep = 0.35
        forceSigma = 0.1

        # INPUT Variable Angle
        self.angle = ctrl.Antecedent(np.arange(0, 90, 0.5), 'angle')
        self.angle['too_tilted_left'] = fuzz.gaussmf(self.angle.universe, angleCenter * (1 + angleStep * 2), angleSigma)
        self.angle['slightly_tilted_left'] = fuzz.gaussmf(self.angle.universe, angleCenter * (1 + angleStep), angleSigma)
        self.angle['centered'] = fuzz.gaussmf(self.angle.universe, angleCenter, angleSigma)
        self.angle['slightly_tilted_right'] = fuzz.gaussmf(self.angle.universe, angleCenter * (1 - angleStep), angleSigma)
        self.angle['too_tilted_right'] = fuzz.gaussmf(self.angle.universe, angleCenter * (1 - angleStep * 2), angleSigma)

        # OUTPUT Variable Force
        self.force = ctrl.Consequent(np.arange(-1, 1, 0.05), 'force')
        self.force['turn_left'] = fuzz.gaussmf(self.force.universe, 0 - forceStep * 2, forceSigma)
        self.force['slightly_turn_left'] = fuzz.gaussmf(self.force.universe, 0 - forceStep, forceSigma)
        self.force['do_nothing'] = fuzz.gaussmf(self.force.universe, forceCenter, forceSigma)
        self.force['slightly_turn_right'] = fuzz.gaussmf(self.force.universe, 0 + forceStep, forceSigma)
        self.force['turn_right'] = fuzz.gaussmf(self.force.universe, 0 + forceStep * 2, forceSigma)

        # RULES
        rule1 = ctrl.Rule(self.angle['too_tilted_left'], self.force['turn_left'])
        rule2 = ctrl.Rule(self.angle['slightly_tilted_left'], self.force['slightly_turn_left'])
        rule3 = ctrl.Rule(self.angle['centered'], self.force['do_nothing'])
        rule4 = ctrl.Rule(self.angle['slightly_tilted_right'], self.force['slightly_turn_right'])
        rule5 = ctrl.Rule(self.angle['too_tilted_right'], self.force['turn_right'])

        turning_crtl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
        self.turning = ctrl.ControlSystemSimulation(turning_crtl)

    def getForce(self, angle, view=False):
        self.turning.input['angle'] = angle

        # Crunch the numbers
        self.turning.compute()

        if (view == True):
            self.angle.view(sim=self.turning)
            self.force.view(sim=self.turning)
        
        return round(self.turning.output['force'], 2)