from OpenGL.GL import *
import pygame
from pygame.locals import *

class renderer:
  def __init__(self):
    pygame.display.set_mode((640,480), OPENGL|DOUBLEBUF|HWSURFACE)
    glViewport(0,0,640,480)
    # self.move_camera()
    glClearColor(*self.clear_color)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_NORMALIZE)
    glMaterial(GL_FRONT, GL_AMBIENT, (.1,.1,.1,1))
    glMaterial(GL_FRONT, GL_DIFFUSE, (1,1,1,1))
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glEnable(GL_POLYGON_SMOOTH)
    glEnable(GL_BLEND)
  def update(self):
    # clear screen
    # lists?
    # update_screen
    glFinish()
