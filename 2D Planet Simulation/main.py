import pygame
import numpy as np
import config
import physics
import renderer
 
def init():
    pygame.init()
    
    surface = pygame.display.set_mode((config.window_width, config.window_height))
    pygame.display.set_caption("N-Body Orbital Simulation")

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 14)
    
    bodies = []
    for b in config.bodies:
        body_obj = physics.Body(
            name=b["name"],
            mass=b["mass"],
            radius=b["radius"],
            color=b["color"],
            position=b["position"],
            velocity=b["velocity"])
        bodies.append(body_obj) 

    return surface, clock, font, bodies

def handle_events(paused, speed_index):
    quit_sim = False
    reset = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_sim = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit_sim = True
            if event.key == pygame.K_SPACE:
                paused = not paused
            if event.key == pygame.K_UP:
                speed_index = min(speed_index + 1, len(config.speed_steps) - 1)
            if event.key == pygame.K_DOWN:
                speed_index = max(speed_index - 1, 0)
            if event.key == pygame.K_r:
                reset = True

    return quit_sim, reset, paused, speed_index


def run():
    surface, clock, font, bodies = init()

    sim_time    = 0.0
    paused      = False
    speed_index = 2
    step_count  = 0

    running = True
    while running:
        quit_sim, reset, paused, speed_index = handle_events(paused, speed_index)

        if quit_sim:
            break

        if reset:
            for body in bodies:
                body.reset()
            sim_time   = 0.0
            step_count = 0

        if not paused:
            multiplier      = config.speed_steps[speed_index]
            steps_per_frame = max(1, int(multiplier / (config.dt * config.fps)))

            for _ in range(steps_per_frame):
                physics.integrate(bodies, config.dt)
                sim_time   += config.dt
                step_count += 1
                if step_count % 5 == 0:
                    for body in bodies:
                        body.update_trail()

        renderer.draw_background(surface)
        renderer.draw_trails(surface, bodies, config.scale, config.offset)
        renderer.draw_bodies(surface, bodies, config.scale, config.offset)
        renderer.draw_labels(surface, bodies, config.scale, config.offset, font)
        renderer.draw_scale_bar(surface, config.scale, font)
        renderer.draw_hud(surface, sim_time, speed_index, font)

        pygame.display.flip()
        clock.tick(config.fps)

    pygame.quit()


if __name__ == "__main__":
    run()
