import ctypes
import sys
from math import trunc
import math

import sdl2
import sdl2.ext

STEP = 0.001
WIDTH = 500
HEIGHT = 500
SECTION = 30
INTERVAL = (-5, 5)


def draw(window, renderer, center):
    center_x, center_y = center
    width, _ = window_size(window)
    sdl2.SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255)
    sdl2.SDL_RenderClear(renderer)
    sdl2.SDL_SetRenderDrawColor(renderer, 0, 0, 0, 0)
    start, end = INTERVAL
    t = start
    current_section = 0
    a = width // 2 - (width // 3)
    while t < end:
        angle = abs(int(math.degrees(math.atan(t))))
        new_section = angle // SECTION
        if new_section != current_section:
            current_section = new_section
            color = SECTION * current_section * 4
            sdl2.SDL_SetRenderDrawColor(renderer, color, color, color, 1)
        x = a * t ** 2 / (1 + t ** 2) + center_x
        y = a * t ** 3 / (1 + t ** 2) + center_y
        draw_point(renderer, (trunc(x), trunc(y)))
        t += STEP
    sdl2.SDL_SetRenderDrawColor(renderer, 192, 57, 43, 1)
    sdl2.SDL_RenderDrawLine(renderer, center_x, 0, center_x, window_size(window)[1])
    sdl2.SDL_RenderPresent(renderer)


def draw_point(renderer, point):
    x, y = point
    sdl2.SDL_RenderDrawPoint(renderer, x, y)


def window_size(window):
    width = ctypes.c_int()
    height = ctypes.c_int()
    sdl2.SDL_GetWindowSize(window, ctypes.byref(width), ctypes.byref(height))
    return width.value, height.value


def window_center(window):
    return (x // 2 for x in window_size(window))


def main():
    sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
    window = sdl2.SDL_CreateWindow(
        b"Lab 1",
        sdl2.SDL_WINDOWPOS_CENTERED,
        sdl2.SDL_WINDOWPOS_CENTERED,
        HEIGHT,
        WIDTH,
        sdl2.SDL_WINDOW_RESIZABLE
    )
    renderer = sdl2.SDL_CreateRenderer(window, -1, sdl2.SDL_RENDERER_ACCELERATED)

    running = True
    event = sdl2.SDL_Event()
    center_x = WIDTH // 2
    center_y = HEIGHT // 2
    while running:
        while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == sdl2.SDL_WINDOWEVENT:
                if event.window.event == sdl2.SDL_WINDOWEVENT_RESIZED:
                    center_x, center_y = window_center(window)
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            draw(window, renderer, (center_x, center_y))
    sdl2.SDL_DestroyWindow(window)
    sdl2.SDL_Quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())
