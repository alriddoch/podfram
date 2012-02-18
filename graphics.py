from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
from pygame.locals import *

class renderer:
  def __init__(self, game):
    self.clear_color = (.1,.0,.1,.1)
    self.size = (640, 360)
    self.perspective = (50, float(self.size[0])/self.size[1], 1,100)

    self.clock = pygame.time.Clock()
    self.drops = []
    self.pre_objects = []
    self.objects = []
    self.huds = []

    pygame.display.set_mode(self.size, OPENGL|DOUBLEBUF|HWSURFACE)
    glViewport(0,0,self.size[0], self.size[1])
    # self.move_camera()
    glClearColor(*self.clear_color)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_NORMALIZE)
    glMaterial(GL_FRONT, GL_AMBIENT, (.1,.1,.1,1))
    glMaterial(GL_FRONT, GL_DIFFUSE, (1,1,1,1))
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glEnable(GL_POLYGON_SMOOTH)
    glEnable(GL_BLEND)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [10,10,10,1])
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0,0,0,1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.5,0.5,0.5,1])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.5,0.5,0.5,1])

  def world_projection(self, perspective):
    "Set up the project for 3D rendering, origin in the middle"
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(*perspective)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
  def hud_projection(self):
    "Set up the project for 2D rendering, origin at the bottom left"
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, self.size[0], 0, self.size[1], -800.0, 800.0)
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslated(0, 0, -200)
  def move_camera(self):
    "Set up the camera"
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslated(0, 0, -40)
    glRotate(-20, 1, 0, 0)
  def add_drop(self, o):
    "Add an object to the backdrop scene"
    self.drops.append(o)
  def add_object(self, o):
    self.objects.append(o)
  def update(self):
    glClear(GL_COLOR_BUFFER_BIT)

    # Draw the background
    self.hud_projection()
    for h in self.drops:
      h.draw(self)

    glClear(GL_DEPTH_BUFFER_BIT)
    # Draw the world
    self.world_projection(self.perspective)
    self.move_camera()
    for o in self.pre_objects:
      o.draw()
      if o.obsolete():
        self.objects.remove(o)
    for o in self.objects:
      o.draw()
      if o.obsolete():
        self.objects.remove(o)

    # Draw the heads up
    self.hud_projection()
    for h in self.huds:
      h.draw(self)

    # and finish
    pygame.display.flip()
    glFinish()
