'''Contains all adjustable parameters for Athena and its training
'''
class Parameters(object):


    def __init__(self):
        # Car physical properties
        self.car_mass = 320 # kg
        self.regen_efficiency = 0.8 # %
        self.battery_max_charge = 1.6e7 # joules
        self.Cd = 0.14 # Coefficient of drag 
        self.Crr = 0.022 # Coefficient of rolling resistance 

        self.frontal_area = 1 # m^2
        self.panel_area = 6 # m^2
        self.solarcell_base_efficiency = 0.16 
        self.battery_internal_resistance = 1.3 # ohlms
        self.power_inefficiency = 0.0001

        # Training Hyperparameters
        self.population_size = 40
        self.mutation_rate = 0.05
        self.selection_bias = 1
        self.inheritance_rate = 1.0
        self.generations = 10000

        # Training Indicators

        # Neural Network Parameters
        self.input_size = 4
        self.sizes = [self.input_size, 10, 1]

        # Map Generating Parameters

        # Simulation Parameters
        self.time_step = 600 # seconds
        self.max_race_time = 3600000 # seconds
        self.environment = [100000.] # TEMP
        self.velocity_noise = 0.000

        # Starting Race Conditions
        self.starting_position = 0 # meters, 0 by default
        self.race_time = 0 # seconds, 0 by default
        self.starting_solar_hour = 3 # hours after noon
        self.starting_battery_charge = 0.0 * self.battery_max_charge # joules

