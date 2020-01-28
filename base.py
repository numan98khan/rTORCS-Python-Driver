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

class HeuristicDriver():

    def __init__(self):
        self.stage = None
        self.trackName = ""

        self.WARMUP = 0
        self.QUALIFYING = 1
        self.RACE = 2
        self.UNKNOWN = None

		        # /* Gear Changing Constants*/
        self.gearUp = [5000, 6000, 6000, 6500, 7000, 0]
        self.gearDown = [0, 2500, 3000, 3000, 3500, 3500]

        # /* Stuck constants*/
        self.stuckTime = 25
        self.stuckAngle = 0.523598775

        # /* Accel and Brake Constants*/
        self.maxSpeedDist = 70
        self.maxSpeed = 150
        self.sin5 = 0.08716
        self.cos5 = 0.99619

        # /* Steering constants*/
        self.steerLock = 0.366519
        self.steerSensitivityOffset = 80.0
        self.wheelSensitivityCoeff = 1

        # /* ABS Filter Constants */
        self.wheelRadius = [0.3306, 0.3306, 0.3276, 0.3276]
        self.absSlip = 2.0
        self.absRange = 3.0
        self.absMinSpeed = 3.0

        # clutching constant
        self.clutchMax = 0.5
        self.clutchDelta =  0.05
        self.clutchRange =  0.82
        self.clutchDeltaTime = 0.02
        self.clutchDeltaRaced = 10
        self.clutchDec =  0.01
        self.clutchMaxModifier = 1.3
        self.clutchMaxTime =  1.5

        self.stuck = 0

        # current clutch
        self.clutch = 0

	def getStage(self):
        return self.stage

    def setStage(self, stage):
        self.stage = stage

    def getTrackName(self):
        return self.trackName

    def setTrackName(self, trackName):
        self.trackName = trackName

    def reset(self):
        print("Restarting the race!")

    def shutdown(self):
        self.myPara.setDamage(damage)
        self.myPara.setTotalTime(totalTime)

	def initAngles(self):
        angles = [0.0] * 19

        # /* set angles as {-90,-75,-60,-45,-30,-20,-15,-10,-5,0,5,10,15,20,30,45,60,75,90} */

        for i in range(0, 5):
        # for (int i=0 i<5 i++)
            angles[i] = -90+i*15
            angles[18-i] = 90-i*15

        for i in range(5, 9):
        # for (int i=5 i<9 i++)
            angles[i] = -20+(i-5)*5
            angles[18-i] = 20-(i-5)*5

        angles[9] = 0
        return angles

	def getGear(self, sensors):
        gear = sensors.getGear()
        rpm = sensors.getRPM()

        #  if gear is 0 (N) or -1 (R) just return 1
        if (gear < 1):
            return 1
        #  check if the RPM value of car is greater than the one suggested
        #  to shift up the gear from the current one
        if (gear < 6 and rpm >= gearUp[gear-1]):
            return gear + 1
        else:
        	#  check if the RPM value of car is lower than the one suggested
        	#  to shift down the gear from the current one
            if (gear > 1 and rpm <= gearDown[gear-1]):
                return gear - 1
            else:  # otherwhise keep current gear
                return gear

	def getSteer(self, sensors):
        #  steering angle is compute by correcting the actual car angle w.r.t. to track
        #  axis [sensors.getAngle()] and to adjust car position w.r.t to middle of track [sensors.getTrackPos()*0.5]
        targetAngle = float(sensors.getAngleToTrackAxis() -
                            sensors.getTrackPosition()*0.5)
        #  at high speed reduce the steering command to avoid loosing the control
        if (sensors.getSpeed() > self.steerSensitivityOffset):
            return float(targetAngle/(self.steerLock*(sensors.getSpeed()-self.steerSensitivityOffset)*self.wheelSensitivityCoeff))
        else:
            return (targetAngle)/self.steerLock

	def getAccel(self, sensors):
        #  checks if car is out of track
        if (sensors.getTrackPosition() < 1 and sensors.getTrackPosition() > -1):
            #  reading of sensor at +5 degree w.r.t. car axis
            rxSensor = float(sensors.getTrackEdgeSensors()[10])
            #  reading of sensor parallel to car axis
            sensorsensor = float(sensors.getTrackEdgeSensors()[9])
            #  reading of sensor at -5 degree w.r.t. car axis
            sxSensor = float(sensors.getTrackEdgeSensors()[8])

            targetSpeed = 0.0

            #  track is straight and enough far from a turn so goes to max speed
            if (sensorsensor > self.maxSpeedDist or (sensorsensor >= rxSensor and sensorsensor >= sxSensor)):
                targetSpeed = self.maxSpeed
            else:
                #  approaching a turn on right
                if(rxSensor > sxSensor):
                    #  computing approximately the "angle" of turn
                    h = sensorsensor*self.sin5
                    b = rxSensor - sensorsensor*self.cos5
                    sinAngle = b*b/(h*h+b*b)
                    #  estimate the target speed depending on turn and on how close it is
                    targetSpeed = self.maxSpeed * \
                        (sensorsensor*self.sinAngle/self.maxSpeedDist)
                else:
                    #  computing approximately the "angle" of turn
                    h = sensorsensor*self.sin5
                    b = sxSensor - sensorsensor*self.cos5
                    sinAngle = b*b/(h*h+b*b)
                    #  estimate the target speed depending on turn and on how close it is
                    targetSpeed = self.maxSpeed * \
                        (sensorsensor*sinAngle/self.maxSpeedDist)

            #  accel/brake command is exponentially scaled w.r.t. the difference between target speed and current one
            return float(2/(1+math.exp(sensors.getSpeed() - targetSpeed)) - 1)
        else:
            #  when out of track returns a moderate acceleration command
            return float(0.3)	

	def filterABS(self, sensors, brake):
        #  convert speed to m/s
        speed = float(sensors.getSpeed() / 3.6)
        #  when spedd lower than min speed for abs do nothing
        if (speed < absMinSpeed):
            return brake

        #  compute the speed of wheels in m/s
        slip = 0.0
        for i in range(0, 4):
            wheelsSpeed = sensors.getWheelSpinVelocity()[i] * self.wheelRadius[i]
            slip += wheelsSpeed

        #  slip is the difference between actual speed of car and average speed of wheels
        slip = speed - slip/4.0
        #  when slip too high applu ABS
        if (slip > absSlip):
            brake = brake - (slip - absSlip)/absRange
  
        #  check brake is not negative, otherwise set it to zero
        if (brake < 0):
            return 0
        else:
            return brake

	def clutching(self, sensors, clutch): 
        maxClutch = self.clutchMax

    #    Check if the current situation is the race start
        if (sensors.getCurrentLapTime()<self.clutchDeltaTime  and self.getStage()==self.RACE and sensors.getDistanceRaced()<clutchDeltaRaced):
            clutch = maxClutch

        delta = 0.0
        #  Adjust the current value of the clutch
        if(clutch > 0):
            delta = clutchDelta
            if (sensors.getGear() < 2):
                #  Apply a stronger clutch output when the gear is one and the race is just started
                delta /= 2
                maxClutch *= clutchMaxModifier
            if (sensors.getCurrentLapTime() < clutchMaxTime):
                clutch = maxClutch
		

        #  check clutch is not bigger than maximum values
        clutch = min(maxClutch, clutch)

        #  if clutch is not at max value decrease it quite quickly
        if (clutch != maxClutch):
            clutch -= delta
            clutch = max(0.0, clutch)
		
        #  if clutch is at max value decrease it very slowly
        else:
            clutch -= clutchDec

        return clutch