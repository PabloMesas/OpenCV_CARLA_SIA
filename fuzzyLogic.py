import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class FuzzyLogic():

    def __init__ (self):
        angleCenter = -28
        angleEdgeDistance = 60
        angleSigma = 6
        distanceCenter = 215
        distanceEdgeDistance = 2500
        distanceSigma = 300
        forceCenter = 0
        forceEdgeDistance = .6
        forceSigma = 0.1

        # INPUT Variable Angle
        self.angle = ctrl.Antecedent(np.arange(-90, 90, 0.5), 'angle')
        self.angle['too_off-center_right'] = fuzz.gaussmf(self.angle.universe, angleCenter - angleEdgeDistance, angleSigma / 1.5)
        self.angle['slightly_off-center_right'] = fuzz.gaussmf(self.angle.universe, angleCenter - angleEdgeDistance/2, angleSigma)
        self.angle['centered'] = fuzz.gaussmf(self.angle.universe, angleCenter, angleSigma * 1.5)
        self.angle['slightly_off-center_left'] = fuzz.gaussmf(self.angle.universe, angleCenter + angleEdgeDistance/2, angleSigma)
        self.angle['too_off-center_left'] = fuzz.gaussmf(self.angle.universe, angleCenter + angleEdgeDistance, angleSigma / 1.5)

        # INPUT Variable Distance
        self.distance = ctrl.Antecedent(np.arange(-3500, 3500, 1), 'distance')
        self.distance['too_far_right'] = fuzz.gaussmf(self.distance.universe, distanceCenter - distanceEdgeDistance, distanceSigma / 1.5)
        self.distance['far_right'] = fuzz.gaussmf(self.distance.universe, distanceCenter - distanceEdgeDistance/2, distanceSigma)
        self.distance['centered'] = fuzz.gaussmf(self.distance.universe, distanceCenter, distanceSigma * 1.5)
        self.distance['far_left'] = fuzz.gaussmf(self.distance.universe, distanceCenter + distanceEdgeDistance/2, distanceSigma)
        self.distance['too_far_left'] = fuzz.gaussmf(self.distance.universe, distanceCenter + distanceEdgeDistance, distanceSigma / 1.5)

        # OUTPUT Variable Force
        self.force = ctrl.Consequent(np.arange(-1, 1, 0.05), 'force')
        self.force['turn_left'] = fuzz.gaussmf(self.force.universe, forceCenter - forceEdgeDistance, forceSigma / 1.5)
        self.force['slightly_turn_left'] = fuzz.gaussmf(self.force.universe, forceCenter - forceEdgeDistance/2, forceSigma)
        self.force['do_nothing'] = fuzz.gaussmf(self.force.universe, forceCenter, forceSigma * 1.5)
        self.force['slightly_turn_right'] = fuzz.gaussmf(self.force.universe, forceCenter + forceEdgeDistance/2, forceSigma)
        self.force['turn_right'] = fuzz.gaussmf(self.force.universe, forceCenter + forceEdgeDistance, forceSigma / 1.5)

        # RULES
        rule1  = ctrl.Rule(self.angle['too_off-center_left'] & self.distance['too_far_right'], self.force['turn_left'])
        rule2  = ctrl.Rule(self.angle['too_off-center_left'] & self.distance['far_right'], self.force['turn_left'])
        rule3  = ctrl.Rule(self.angle['too_off-center_left'] & self.distance['centered'], self.force['turn_left'])
        rule4  = ctrl.Rule(self.angle['too_off-center_left'] & self.distance['far_left'], self.force['slightly_turn_left'])
        rule5  = ctrl.Rule(self.angle['too_off-center_left'] & self.distance['too_far_left'], self.force['do_nothing'])
        rule6  = ctrl.Rule(self.angle['slightly_off-center_left'] & self.distance['too_far_right'], self.force['turn_left'])
        rule7  = ctrl.Rule(self.angle['slightly_off-center_left'] & self.distance['far_right'], self.force['turn_left'])
        rule8  = ctrl.Rule(self.angle['slightly_off-center_left'] & self.distance['centered'], self.force['slightly_turn_left'])
        rule9  = ctrl.Rule(self.angle['slightly_off-center_left'] & self.distance['far_left'], self.force['slightly_turn_left'])
        rule10 = ctrl.Rule(self.angle['slightly_off-center_left'] & self.distance['too_far_left'], self.force['do_nothing'])
        rule11 = ctrl.Rule(self.angle['centered'] & self.distance['too_far_right'], self.force['turn_left'])
        rule12 = ctrl.Rule(self.angle['centered'] & self.distance['far_right'], self.force['slightly_turn_left'])
        rule13 = ctrl.Rule(self.angle['centered'] & self.distance['centered'], self.force['do_nothing'])
        rule14 = ctrl.Rule(self.angle['centered'] & self.distance['far_left'], self.force['slightly_turn_right'])
        rule15 = ctrl.Rule(self.angle['centered'] & self.distance['too_far_left'], self.force['turn_right'])
        rule16 = ctrl.Rule(self.angle['slightly_off-center_right'] & self.distance['too_far_right'], self.force['turn_left'])
        rule17 = ctrl.Rule(self.angle['slightly_off-center_right'] & self.distance['far_right'], self.force['do_nothing'])
        rule18 = ctrl.Rule(self.angle['slightly_off-center_right'] & self.distance['centered'], self.force['slightly_turn_right'])
        rule19 = ctrl.Rule(self.angle['slightly_off-center_right'] & self.distance['far_left'], self.force['turn_right'])
        rule20 = ctrl.Rule(self.angle['slightly_off-center_right'] & self.distance['too_far_left'], self.force['turn_right'])
        rule21 = ctrl.Rule(self.angle['too_off-center_right'] & self.distance['too_far_right'], self.force['do_nothing'])
        rule22 = ctrl.Rule(self.angle['too_off-center_right'] & self.distance['far_right'], self.force['slightly_turn_right'])
        rule23 = ctrl.Rule(self.angle['too_off-center_right'] & self.distance['centered'], self.force['turn_right'])
        rule24 = ctrl.Rule(self.angle['too_off-center_right'] & self.distance['far_left'], self.force['turn_left'])
        rule25 = ctrl.Rule(self.angle['too_off-center_right'] & self.distance['too_far_left'], self.force['turn_left'])

        turning_crtl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5,
                                            rule6, rule7, rule8, rule9, rule10,
                                            rule11, rule12, rule13, rule14, rule15,
                                            rule16, rule17, rule18, rule19, rule20,
                                            rule21, rule22, rule23, rule24, rule25,])
        self.turning = ctrl.ControlSystemSimulation(turning_crtl)

    def getForce(self, angle, distance, view=False):
        self.turning.input['angle'] = angle
        self.turning.input['distance'] = distance

        # Crunch the numbers
        self.turning.compute()

        if (view == True):
            self.angle.view(sim=self.turning)
            self.distance.view(sim=self.turning)
            self.force.view(sim=self.turning)
        
        return round(self.turning.output['force'], 2)
