import numpy as np 
import random
from math import pi as pi
from math import sin as sin
from math import cos as cos
from math import acos
import all_parameters
para = all_parameters.Parameters()


''' Contains functions modeling the physical behavior of the car

Purpose is to return the new car state (position/battery power) 
given a velocity, timestep, and environment

'''

class Argo(object):

	def __init__(self, 
		starting_position = para.starting_position, 
		starting_time = para.race_time, 
		starting_charge = para.starting_battery_charge, 
		battery_temperature = 25, 
		panel_temperature = 25, 
		time_step = para.time_step, 
		starting_solar_hour = para.starting_solar_hour, 
		cell_voltage = 3.5):
		
		# states
		self.position = starting_position # distance from start of race (meters)
		self.race_time = starting_time # time since start of race (seconds)
		self.solar_hour = starting_solar_hour  # time to solar hour
		self.battery_charge = starting_charge # charge at start of race
		self.time_step = time_step # time spent at a velocity
		self.pack_voltage = 28 * cell_voltage # TEMP voltage of battery pack
		self.irradiance = 0
		self.aero_loss = 0
		self.rolling_loss = 0
		self.set_constants()

	'''
	initializes the car's constants
	'''
	def set_constants(self):
		#Car Constants
		self.mass = para.car_mass

		#Battery Constants
		self.E_regen = para.regen_efficiency
		self.power_inefficiency = para.power_inefficiency
		self.max_charge = para.battery_max_charge

		#Motion Constants
		self.Cd = para.Cd
		self.Crr = para.Crr
		self.Frontal_Area = para.frontal_area
		
		#Panel Constants
		self.panel_area = para.panel_area
		self.basecell_efficiency = para.solarcell_base_efficiency

		#TODO: are these things correct?
		self.panel_tilt = para.panel_tilt
		self.azimuth_angle = para.azimuth_angle

		#Location Constants
		self.Latitude = para.Latitude
		self.avg_acceleration = para.avg_acceleration
		self.day_of_year = para.day_of_year
		self.solar_hour = para.solar_hour
	

	'''
	some other version of initialize car's the constants
	'''

	'''
	def set_constants(self, mass, E_battery2, E_regen, E_HV2motor, 
					E_2battery, max_charge, Cd, Crr, Frontal_Area, 
					Latitude, day_of_year, solar_hour, avg_acceleration, 
					panel_area, panel_tilt, azimuth_angle, t_loss, 
					ideal_temp, basecell_efficiency, ancillary_loss):
		#Car Constants
		self.mass = mass
		#Battery Constants
		self.E_battery2 = E_battery2
		self.E_regen = E_regen
		self.E_HV2motor = E_HV2motor
		self.E_2battery = E_2battery
		self.max_charge = max_charge
		#Motion Constants
		self.Cd = Cd
		self.Crr = Crr
		self.Frontal_Area = Frontal_Area
		#Location Constants
		self.Latitude = Latitude
		self.avg_acceleration = avg_acceleration
		self.day_of_year = day_of_year
		self.solar_hour = solar_hour
		#Panel Constants
		self.panel_area = panel_area
		self.t_loss = t_loss
		self.ideal_temp = ideal_temp
		self.panel_tilt = panel_tilt
		self.azimuth_angle = azimuth_angle
		self.basecell_efficiency = basecell_efficiency
		self.irradiance()
		#
		self.ancillary_loss = ancillary_loss

	'''

	'''
	Updates positiion, clock, time of race, and battery charge
	'''
	def update_state(self, velocity):
		self.position += self.time_step * velocity # update position (meters)
		self.race_time += self.time_step # update time since start of race (seconds)
		self.solar_hour += self.time_step/3600  # update clock time (hours)
		if self.solar_hour > 4: # change time to 8 AM at 5 PM
			self.solar_hour = -5

		self.update_battery_charge(velocity) # update battery charge
		#print(self.position, 'meters' , self.race_time, 'seconds')
		return 

	'''
	Changes the charge of the battery based on solar irradiance and powerlosses from motion and ineficiencies
	'''
	def update_battery_charge(self, velocity):
		# net_power is solar power into panels
		self.irradiance = self.get_irradiance()
		net_power = self.irradiance * self.basecell_efficiency * float(self.panel_area)
		self.sensor_solar_p = net_power

		# net_power is the net power TO batteries (not in batteries)
		net_power -= self.motion_loss(velocity)

		# heat loss due to current
		self.sensor_batteryheatlosspower = net_power
		self.sensor_battery_heat_loss = (self.power_inefficiency) * net_power**2
		
		# if net power is positive, battery takes in less power than net_power
		if net_power > 0.:
			self.sensor_battery_dCharge = net_power - self.sensor_battery_heat_loss
			self.battery_charge += self.sensor_battery_dCharge * self.time_step

		# if net power is negative, battery drains more power than net_power
		else:
			self.sensor_battery_dCharge = net_power - self.sensor_battery_heat_loss
			self.battery_charge += self.sensor_battery_dCharge * self.time_step

		self.sensor_avg_battery_current = -self.sensor_battery_dCharge/ self.pack_voltage

	'''
	returns the amount of energy incident on the solar array
	'''
	def get_irradiance(self):

		# get current state of the sun
		panel_tilt = self.panel_tilt
		panel_azimuth_angle = self.azimuth_angle
		day_of_year = self.day_of_year
		Latitude = self.Latitude
		solar_hour = self.solar_hour
		panel_area = self.panel_area

		Solar_Hour_Angle = solar_hour * pi / 12
		Solar_Declination = 0.41 * sin((day_of_year-81)*2*pi/365)
		Apparent_Solar_Irradiance = 1160 + 75 * sin((day_of_year-275)*2*pi/365)
		
		Optical_Depth = 0.174 + 0.035 * sin((day_of_year-100)*2*pi/365)
		Solar_Altitude_Angle = np.arcsin( cos(Latitude) * cos(Solar_Declination) * cos(Solar_Hour_Angle) + sin(Latitude) * sin(Solar_Declination))
		Solar_Azimuth_Angle = np.arcsin( cos(Solar_Declination) * sin(Solar_Hour_Angle)/cos(Solar_Altitude_Angle) )
		Air_Mass_Ratio = np.sqrt((708*sin(Solar_Altitude_Angle))**2 + 1417) - 708 * sin(Solar_Altitude_Angle)
		Clear_Sky_Direct_Beam_Radiation = Apparent_Solar_Irradiance * np.exp( - Optical_Depth * Air_Mass_Ratio)
		Beam_Panel_Incidence_Angle = np.arccos( cos(Solar_Altitude_Angle) * cos(Solar_Azimuth_Angle - panel_azimuth_angle) * sin(panel_tilt) + sin(Solar_Altitude_Angle)*cos(panel_tilt))
		Panel_Irradiation = Clear_Sky_Direct_Beam_Radiation * cos(Beam_Panel_Incidence_Angle)
		
		Incident_Solar_Power = Panel_Irradiation * panel_area
		return Incident_Solar_Power

	'''
	returns the total loss of power from motion, includes aerodynamic drag and motion drag
	'''
	def motion_loss(self, velocity):

		# power loss due to aerodynamics
		self.aero_loss = velocity**3 * 0.5 * 1.225 * self.Frontal_Area * self.Cd

		# power loss due to rolling resistance
		self.rolling_loss = self.mass * 9.81 * self.Crr * velocity
		
		self.sensor_motion_p_loss = self.aero_loss + self.rolling_loss
		return self.sensor_motion_p_loss
