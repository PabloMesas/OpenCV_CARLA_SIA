import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class fuzzyLogic():

    def __init__ (self, data):
        # INPUT Variable Angle
        self.angle = ctrl.Antecedent(np.arange(-90, 90, 0.5), 'angle')
        self.angle['too_tilted_left'] = fuzz.gaussmf(self.angle.universe, 
                                                    data['angle']['too_tilted_left'].mean,
                                                    data['angle']['too_tilted_left'].sigma)
        self.angle['slightly_tilted_left'] = fuzz.gaussmf(self.angle.universe, 
                                                    data['angle']['slightly_tilted_left'].mean,
                                                    data['angle']['slightly_tilted_left'].sigma)
        self.angle['centered'] = fuzz.gaussmf(self.angle.universe, 
                                                    data['angle']['centered'].mean,
                                                    data['angle']['centered'].sigma)
        self.angle['slightly_tilted_right'] = fuzz.gaussmf(self.angle.universe, 
                                                    data['angle']['slightly_tilted_right'].mean,
                                                    data['angle']['slightly_tilted_right'].sigma)
        self.angle['too_tilted_right'] = fuzz.gaussmf(self.angle.universe, 
                                                    data['angle']['too_tilted_right'].mean,
                                                    data['angle']['too_tilted_right'].sigma)

        # OUTPUT Variable Force
        self.force = ctrl.Consequent(np.arange(-10, 10, 0.1), 'force')
        self.force['turn_left'] = fuzz.gaussmf(self.force.universe, 
                                                    data['force']['turn_left'].mean,
                                                    data['force']['turn_left'].sigma)
        self.force['slightly_turn_left'] = fuzz.gaussmf(self.force.universe, 
                                                    data['force']['slightly_turn_left'].mean,
                                                    data['force']['slightly_turn_left'].sigma)
        self.force['do_nothing'] = fuzz.gaussmf(self.force.universe, 
                                                    data['force']['do_nothing'].mean,
                                                    data['force']['do_nothing'].sigma)
        self.force['slightly_turn_right'] = fuzz.gaussmf(self.force.universe, 
                                                    data['force']['slightly_turn_right'].mean,
                                                    data['force']['slightly_turn_right'].sigma)
        self.force['turn_right'] = fuzz.gaussmf(self.force.universe, 
                                                    data['force']['turn_right'].mean,
                                                    data['force']['turn_right'].sigma)
        # RULES
        rule1 = ctrl.Rule(self.angle['too_tilted_left'], self.force['turn_right'])
        rule2 = ctrl.Rule(self.angle['slightly_tilted_left'], self.force['slightly_turn_right'])
        rule3 = ctrl.Rule(self.angle['centered'], self.force['do_nothing'])
        rule4 = ctrl.Rule(self.angle['slightly_tilted_right'], self.force['slightly_turn_left'])
        rule5 = ctrl.Rule(self.angle['too_tilted_right'], self.force['turn_left'])

        turning_crtl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
        self.turning = ctrl.ControlSystemSimulation(turning_crtl)

    def getForce(self, angle):
        self.turning.input['angle'] = angle

        self.turning.compute()
        
        return self.turning.output['force']