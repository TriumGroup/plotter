import sys
from math import pi, sin, cos, trunc
import ctypes
import sdl2
import sdl2.ext


STEP = 0.01
A_COEFF = 100
WIDTH = 500
HEIGHT = 500


def draw(renderer, center):
    center_x, center_y = center
    sdl2.SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255)
    sdl2.SDL_RenderClear(renderer)

    points = []
    y_dots = []
    a = A_COEFF
    t = -100
    while t < 100:
        x = a * t**2 / (1 + t**2) + center_x
        y = a * t**3 / (1 + t**2) + center_y
        points.append((trunc(x), trunc(y)))
        y_dots.append((trunc(center_x), trunc(y)))
        t += STEP

    draw_points(renderer, from_points(points), (0, 0, 0, 0))
    draw_points(renderer, from_points(y_dots), (192, 57, 43, 1))
    sdl2.SDL_RenderPresent(renderer)


def draw_points(renderer, points, color):
    assert len(color) == 4
    sdl2.SDL_SetRenderDrawColor(renderer, color[0], color[1], color[2], color[3])
    sdl2.SDL_RenderDrawPoints(renderer, points, len(points))


def window_size(window):
    width = ctypes.c_long()
    height = ctypes.c_long()
    sdl2.SDL_GetWindowSize(window, ctypes.byref(width), ctypes.byref(height))
    return width.value, height.value

def window_center(window):
    return (x//2 for x in window_size(window))


def from_points(points):
    return (sdl2.SDL_Point*len(points))(*[sdl2.SDL_Point(p[0], p[1]) for p in points])


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
            if event.type ==  sdl2.SDL_WINDOWEVENT:
                if event.window.event == sdl2.SDL_WINDOWEVENT_RESIZED:
                    center_x, center_y = window_center(window)   
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
        draw(renderer, (center_x, center_y))
    sdl2.SDL_DestroyWindow(window)
    sdl2.SDL_Quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())
