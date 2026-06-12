import numpy as np
 
# Display
window_width  = 750
window_height = 600
trail_length  = 300
offset        = np.array([window_width / 2, window_height / 2])
scale         = min(window_width, window_height) / 2 / 32
fps           = 60

# Physics
gravity   = 4 * np.pi**2
softening = 1e-6

# Time
dt          = 0.0001
time_scale  = 1.0
speed_steps = [0.1, 0.5, 1, 2, 5, 10, 50, 100]

def circular_velocity(r):
    # Exact circular orbit speed in AU/year for a body at distance r from Sun
    return 2 * np.pi / np.sqrt(r)

# Body data — Sun first, then planets Mercury → Neptune
_planet_data = [
    {"name": "Sun",     "mass": 1.0,      "radius": 20, "color": (255, 255,   0), "position": [0.0,    0.0]},
    {"name": "Jupiter", "mass": 9.55e-4,  "radius": 11, "color": (255, 165,  80), "position": [5.203,  0.0]},
    {"name": "Saturn",  "mass": 2.86e-4,  "radius": 9,  "color": (210, 180, 140), "position": [9.537,  0.0]},
    {"name": "Uranus",  "mass": 4.37e-5,  "radius": 6,  "color": (173, 216, 230), "position": [19.19,  0.0]},
    {"name": "Neptune", "mass": 5.15e-5,  "radius": 6,  "color": ( 63,  84, 186), "position": [30.07,  0.0]},
]

bodies = []
for p in _planet_data:
    r = p["position"][0]
    v = 0.0 if r == 0.0 else circular_velocity(r)
    bodies.append({**p, "velocity": [0.0, -v]})
