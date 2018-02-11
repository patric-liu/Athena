'''Contains all adjustable parameters for Athena and its training
'''
class Parameters(object):

    def __init__(self):
        # Car physical properties
        self.car_mass = 240 # kg
        self.regen_efficiency = 0.8 # %
        self.battery_max_charge = 1.6e7 # joules
        self.Cd = 0.11 # Coefficient of drag
        self.Crr = 0.0013 # Coefficient of rolling resistance

        self.frontal_Area = 1 # m^2
        self.panel_area = 4 # m^2
        self.solarcell_base_efficiency = 0.237 # %
        self.battery_internal_resistance = 1.3 # ohlms

        # Training Hyperparameters
        self.population_size = 20 
        self.mutation_rate = 0.1
        self.selection_bias = 1
        self.inheritance_rate = 1
        self.generations = 1000

        # Training Indicators

        # Neural Network Parameters
        self.input_size = 4
        self.sizes = [self.input_size, 10, 1]

        # Map Generating Parameters

        # Simulation Parameters
        self.time_step = 600 # seconds

        # Starting Race Conditions
        self.starting_position = 0 # meters
        self.race_time = 0 # seconds
        self.starting_solar_hour = -6 # hours after noon
        self.starting_battery_charge = 1.6e7 # joules

