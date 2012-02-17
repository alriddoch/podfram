from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *

class renderer:
  def __init__(self):
    self.clear_color = (1.,0.,1.,1.)
    self.size = (640, 360)
    self.perspective = (90, float(self.size[0])/self.size[1], .1,100)

    pygame.display.set_mode(self.size, OPENGL|DOUBLEBUF|HWSURFACE)
    glViewport(0,0,self.size[0], self.size[1])
    # self.move_camera()
    glClearColor(*self.clear_color)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    # glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_NORMALIZE)
    glMaterial(GL_FRONT, GL_AMBIENT, (.1,.1,.1,1))
    glMaterial(GL_FRONT, GL_DIFFUSE, (1,1,1,1))
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glEnable(GL_POLYGON_SMOOTH)
    glEnable(GL_BLEND)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(*self.perspective)
  def move_camera(self):
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslated(0, 0, -5)
  def update(self):
    glClear(GL_DEPTH_BUFFER_BIT|GL_COLOR_BUFFER_BIT)
    self.move_camera()
    glColor3f(.0,.1,.0)
    glBegin(GL_QUADS)
    glNormal3d(0,1,0)
    glVertex3f(0,0,0)
    glVertex3f(1,0,0)
    glVertex3f(1,1,0)
    glVertex3f(0,1,0)
    glEnd()
    pygame.display.flip()
    glFinish()
