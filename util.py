class MySensorModel():
	## basic information about your car and the track (you probably should take care of these somehow)
	def __init__(self):
		self.speed = None
		self.trackPosition = None
		self.angleToTrackAxis = None
		self.lateralSpeed = None
		self.currentLapTime = None
		self.damage = None
		self.distanceFromStartLine = None
		self.distanceRaced = None
		self.fuelLevel = None
		self.lastLapTime = None
		self.RPM = None
		self.ZSpeed = None
		self.Z = None
		self.trackEdgeSensors = None
		self.focusSensors = None
		self.opponentSensors = None
		self.gear = None
		self.racePosition = None
		self.wheelSpinVelocity = None
		self.message = None

    def setCarState(self, carstate):
		self.speed = carstate.speed_x
		self.trackPosition = carstate.distance_from_center
		self.angleToTrackAxis = carstate.angle
		self.lateralSpeed = carstate.speed_y
		self.currentLapTime = carstate.current_lap_time
		self.damage = carstate.damage
		self.distanceFromStartLine = carstate.distance_from_start
		self.distanceRaced = carstate.distance_raced
		self.fuelLevel = carstate.fuel
		self.lastLapTime = carstate.last_lap_time
		self.RPM = carstate.rpm
		self.ZSpeed = carstate.speed_z
		self.Z = carstate.z
		self.trackEdgeSensors = carstate.distances_from_edge
		self.focusSensors = carstate.focused_distances_from_edge
		self.opponentSensors = carstate.opponents
		self.gear = carstate.gear
		self.racePosition = carstate.race_position
		self.wheelSpinVelocity = carstate.wheel_velocities
		self.message = ""