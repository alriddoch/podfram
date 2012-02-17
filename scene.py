#  class Object:
#    def draw(): draw it

from OpenGL.GL import *
from OpenGL.GLU import *

import ode

class sphere:
  def __init__(self, game, pos):
    self.display_list = glGenLists(1)
    glNewList(self.display_list, GL_COMPILE)
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 100000, 16, 16)
    glEndList()

    self.body = ode.Body(game.world)
    self.body.setGravityMode(True)
    self.body.setPosition(pos)
    self.mass = ode.Mass()
    self.mass.setSphere(1000, 100000)
    self.geom = ode.GeomSphere(game.space,100000)
    self.geom.setBody(self.body)
  def draw(self):
    glColor3f(0,1,0)
    glPushMatrix()
    pos = self.body.getPosition()
    glTranslated(pos[0], pos[1], pos[2])
    glCallList(self.display_list)
    glPopMatrix()
  def obsolete(self):
    return False

class explosion:
  def __init__(self, game, pos):
    self.display_list = glGenLists(1)
    glNewList(self.display_list, GL_COMPILE)
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, 100000, 16, 16)
    glEndList()

    self.size = 0
    self.pos = pos

  def draw(self):
    factor = self.size / 100.0
    glColor3f(1,min(factor/10,0.5),0)
    self.size += 1
    glPushMatrix()
    pos = self.pos
    glTranslated(pos[0], pos[1], pos[2])
    glScalef(factor, factor, factor)
    glCallList(self.display_list)
    glPopMatrix()
  def obsolete(self):
    return self.size > 200
