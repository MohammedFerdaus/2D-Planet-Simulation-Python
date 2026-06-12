import pygame
import numpy as np
import config

def world_to_screen(position, scale, offset):
    screen_x = int(position[0] * scale + offset[0])
    screen_y = int(position[1] * -scale + offset[1])    
    return (screen_x, screen_y)

def draw_background(surface):
    surface.fill((0, 0, 0))

def draw_trails(surface, bodies, scale, offset):
    for body in bodies:
        if len(body.trail) < 2:
            continue

        points = [world_to_screen(pos, scale, offset) for pos in body.trail]        
        pygame.draw.lines(surface, body.color, False, points, 1)

def draw_bodies(surface, bodies, scale, offset):
    for body in bodies:
        screen_pos = world_to_screen(body.pos, scale, offset)        
        pygame.draw.circle(surface, body.color, screen_pos, body.radius)


def draw_labels(surface, bodies, scale, offset, font):
    for body in bodies:
        screen_pos = world_to_screen(body.pos, scale, offset)        
        
        text_surface = font.render(body.name, True, (255, 255, 255))
        text_offset = (screen_pos[0] + body.radius + 5, screen_pos[1] + 5)
        
        surface.blit(text_surface, text_offset)


def draw_hud(surface, sim_time, speed_index, font):
    years = int(sim_time)
    days = int((sim_time - years) * 365.25)
    date_str = f"Time: {years}y {days}d"
    
    date_surface = font.render(date_str, True, (255, 255, 255))
    surface.blit(date_surface, (20, 20))

    multiplier = config.speed_steps[speed_index]
    speed_str = f"Speed: {multiplier}x"
    speed_surface = font.render(speed_str, True, (255, 255, 255))
    surface.blit(speed_surface, (20, 50))

def draw_scale_bar(surface, scale, font):
    bar_pixels = 100    
    au_value = bar_pixels / scale
    
    window_height = surface.get_height()
    start_pos = (20, window_height - 40)
    end_pos = (20 + bar_pixels, window_height - 40)
    
    pygame.draw.line(surface, (255, 255, 255), start_pos, end_pos, 2)
    
    label_text = f"{au_value:.1f} AU"
    label_surface = font.render(label_text, True, (255, 255, 255))
    
    label_pos = (start_pos[0], start_pos[1] + 10)
    surface.blit(label_surface, label_pos)