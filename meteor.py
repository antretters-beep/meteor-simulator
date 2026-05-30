import math
import random

G = 6.674e-11
M_earth = 5.972e24
KM_TO_M = 1000

class Meteor:
    def __init__(self, x, y, vx, vy, mass):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass
        self.time = 0.0

    def distance_to_point(self, x, y):
        return math.sqrt((x - self.x)**2 + (y - self.y)**2)
    
    def update(self, earth_x, earth_y, sun_x, sun_y, dt=0.1):
        distance_earth = self.distance_to_point(earth_x, earth_y)
        distance_earth_m = distance_earth * KM_TO_M
        acceleration_magnitude_earth = (G * M_earth) / (distance_earth_m ** 2)
    
        dx_earth = earth_x - self.x
        dy_earth = earth_y - self.y
        direction_x_earth = dx_earth / distance_earth
        direction_y_earth = dy_earth / distance_earth
    
        acceleration_x_earth = direction_x_earth * acceleration_magnitude_earth
        acceleration_y_earth = direction_y_earth * acceleration_magnitude_earth

        distance_sun = self.distance_to_point(sun_x, sun_y)
        distance_sun_m = distance_sun * KM_TO_M
        M_sun = 1.989e30
        acceleration_magnitude_sun = (G * M_sun) / (distance_sun_m ** 2)
    
        dx_sun = sun_x - self.x
        dy_sun = sun_y - self.y
        direction_x_sun = dx_sun / distance_sun
        direction_y_sun = dy_sun / distance_sun
    
        acceleration_x_sun = direction_x_sun * acceleration_magnitude_sun
        acceleration_y_sun = direction_y_sun * acceleration_magnitude_sun

        total_acceleration_x = acceleration_x_earth + acceleration_x_sun
        total_acceleration_y = acceleration_y_earth + acceleration_y_sun
        
        self.vx = self.vx + total_acceleration_x * dt
        self.vy = self.vy + total_acceleration_y * dt
        
        self.x = self.x + self.vx * dt
        self.y = self.y + self.vy * dt
        
        self.time = self.time + dt

class Earth:
    def __init__(self, x, y, radius, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = mass

class Sun:
    def __init__(self):
        self.x = 149600000
        self.y = 0
        self.radius = 696000
        self.mass = 1.989e30

def generate_placeholder_meteors(count=100):
    meteors = []
    for i in range(count):
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(8000, 400000)
        x = distance * math.cos(angle)
        y = distance * math.sin(angle)
        
        velocity_magnitude = random.uniform(5, 50)
        direction_x = -x / distance
        direction_y = -y / distance
        vx = direction_x * velocity_magnitude
        vy = direction_y * velocity_magnitude
        
        mass = random.uniform(100, 10000)
        
        meteor = Meteor(x, y, vx, vy, mass)
        meteors.append(meteor)
    
    return meteors

sun1 = Sun()

earth1 = Earth(0, 0, 6371, 5.972e24)

meteor1 = Meteor(149_600_000, 100_000, 0, -30, 1000)

all_meteors = generate_placeholder_meteors(100)

for i in range(5):
    meteor = all_meteors[i]
    print(f"\nMeteor {i+1}: Start pos ({meteor.x:.0f}, {meteor.y:.0f}), velocity ({meteor.vx:.2f}, {meteor.vy:.2f})")
    
    for step in range(100000):
        meteor.update(earth1.x, earth1.y, sun1.x, sun1.y, 0.1)
        
        distance = meteor.distance_to_point(earth1.x, earth1.y)
        
        if distance < earth1.radius:
            print(f"  → IMPACT at time {meteor.time:.1f}s")
            break
        
        if step == 99999:
            print(f"  → ESCAPED (time {meteor.time:.1f}s)")