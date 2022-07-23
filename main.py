import pyglet
import blockManager
import random
import time
random.seed(time.time())

window = pyglet.window.Window(128*4, 128*4, caption = "4. 2048 Pyglet - Press ESCAPE to restart")
pyglet.gl.glClearColor(0.05, 0.05, 0.05, 1.0)

gridBatch = pyglet.graphics.Batch()
grid1 = pyglet.shapes.Line(0,      128*3,  128*4,  128*3,  width = 2, color = (160, 160, 160), batch = gridBatch)
grid2 = pyglet.shapes.Line(0,      128*2,  128*4,  128*2,  width = 2, color = (160, 160, 160), batch = gridBatch)
grid3 = pyglet.shapes.Line(0,      128,    128*4,  128,    width = 2, color = (160, 160, 160), batch = gridBatch)
grid4 = pyglet.shapes.Line(128*3,  0,      128*3,  128*4,  width = 2, color = (160, 160, 160), batch = gridBatch)
grid5 = pyglet.shapes.Line(128*2,  0,      128*2,  128*4,  width = 2, color = (160, 160, 160), batch = gridBatch)
grid6 = pyglet.shapes.Line(128,    0,      128,    128*4,  width = 2, color = (160, 160, 160), batch = gridBatch)

manager = blockManager.BlockManager(lerpFactor = 20.0)

centerFocusBG = pyglet.shapes.Rectangle(x = 0, y = 0, width = 128*4, height = 128*4, color = (20, 20, 20))
centerText = pyglet.text.Label("", font_size = 60, x = 128*2, y = 128*2, anchor_x = "center", anchor_y = "center")

def update(deltaTime):
    if not manager.update(deltaTime):
        centerText.text = "YOU LOST!"
        centerFocusBG.opacity = 160
    elif manager.checkWin():
        centerText.text = "YOU WIN!"
        centerFocusBG.opacity = 160
    else:
        centerText.text = ""
        centerFocusBG.opacity = 0

pyglet.clock.schedule_interval(update, 1.0 / 120.0)

def on_key_press(k, mod):
    manager.on_key_press(k)
    if k == pyglet.window.key.ESCAPE:
        manager.reset()

window.on_key_press = on_key_press

def on_draw():
    window.clear()
    gridBatch.draw()
    manager.draw()

    centerFocusBG.draw()
    centerText.draw()
window.on_draw = on_draw

pyglet.app.run()