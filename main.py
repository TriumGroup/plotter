import sys
from math import pi, sin, cos, trunc
import ctypes
import sdl2
import sdl2.ext


STEP = 0.01
A_COEFF = 100
CENTER_X = 250
CENTER_Y = 250


def draw(renderer):
    sdl2.SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255)
    sdl2.SDL_RenderClear(renderer)
    sdl2.SDL_SetRenderDrawColor(renderer, 0, 0, 0, 0)

    points_set = []

    a = A_COEFF
    t = -100
    while t < 100:
        x = a * t**2 / (1 + t**2) + CENTER_X
        y = a * t**3 / (1 + t**2) + CENTER_Y
        points_set.append((trunc(x), trunc(y)))
        points_set.append((trunc(CENTER_X), trunc(y)))
        t += STEP

    points_count = len(points_set)
    points_array = (sdl2.SDL_Point*points_count)(*[sdl2.SDL_Point(p[0], p[1]) for p in points_set])

    sdl2.SDL_RenderDrawPoints(renderer, points_array, points_count)
    sdl2.SDL_RenderPresent(renderer)


def main():
    sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
    window = sdl2.SDL_CreateWindow(b"Lab 1",
                                   sdl2.SDL_WINDOWPOS_CENTERED, sdl2.SDL_WINDOWPOS_CENTERED,
                                   500, 500, sdl2.SDL_WINDOW_RESIZABLE)
    renderer = sdl2.SDL_CreateRenderer(
        window, -1, sdl2.SDL_RENDERER_ACCELERATED)

    running = True
    event = sdl2.SDL_Event()
    while running:
        while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type ==  sdl2.SDL_WINDOWEVENT:
                if event.window.event == sdl2.SDL_WINDOWEVENT_RESIZED:
                    a = ctypes.c_long()
                    b = ctypes.c_long()
                    sdl2.SDL_GetWindowSize(window, ctypes.byref(a), ctypes.byref(b))
                    global CENTER_X
                    CENTER_X = a.value // 2
                    global CENTER_Y 
                    CENTER_Y = b.value // 2   
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
        draw(renderer)
    sdl2.SDL_DestroyWindow(window)
    sdl2.SDL_Quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())