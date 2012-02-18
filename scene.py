#  class Object:
#    def draw(): draw it

from OpenGL.GL import *
from OpenGL.GLU import *

import ode

class floor:
  def __init__(self, game, width, height):
    self.display_list = glGenLists(1)
    glNewList(self.display_list, GL_COMPILE)
    glColor3f(1,.9,.5)
    glBegin(GL_QUADS)
    glNormal3d(0,0,1)
    glVertex3f(-width,-height,0)
    glVertex3f(-width,height,0)
    glVertex3f(width,height,0)
    glVertex3f(width,-height,0)
    glEnd()
    glEndList()

    self.body = ode.Body(game.world)
    self.body.setKinematic()
    self.body.setPosition((0,0,0))
    self.geom = ode.GeomBox(game.space, (width*2, height*2, 0.1))
    self.geom.setBody(self.body)
  def draw(self):
    glPushMatrix()
    pos = self.body.getPosition()
    glTranslated(pos[0], pos[1], pos[2])
    glCallList(self.display_list)
    glPopMatrix()
  def obsolete(self):
    return False

class cuboid:
  def __init__(self, game):
    self.display_list = glGenLists(1)
    glNewList(self.display_list, GL_COMPILE)
    glColor3f(.0,.0,.5)
    glBegin(GL_QUADS)
    glNormal3d(0,1,0)
    glVertex3f()
  def obsolete(self):
    return False

class sphere:
  def __init__(self, game, pos, radius):
    self.display_list = glGenLists(1)
    glNewList(self.display_list, GL_COMPILE)
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluQuadricDrawStyle(quadric, GLU_FILL)
    glColor3f(1,0,0)
    gluSphere(quadric, radius, 16, 16)
    glEndList()

    self.body = ode.Body(game.world)
    self.body.setGravityMode(True)
    self.body.setPosition(pos)
    self.body.kind = sphere
    self.mass = ode.Mass()
    self.mass.setSphere(0.0001, radius)
    self.body.setMass(self.mass)
    self.geom = ode.GeomSphere(game.space,radius)
    self.geom.setBody(self.body)
  def draw(self):
    glPushMatrix()
    pos = self.body.getPosition()
    glTranslated(pos[0], pos[1], pos[2])
    glCallList(self.display_list)
    glPopMatrix()
  def obsolete(self):
    return False

class avatar:
  def __init__(self, game, pos, radius):
    self.display_list = glGenLists(1)
    glNewList(self.display_list, GL_COMPILE)
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluQuadricDrawStyle(quadric, GLU_FILL)
    glColor3f(0,0,1)
    gluSphere(quadric, radius, 16, 16)
    glEndList()

    self.body = ode.Body(game.world)
    self.body.setGravityMode(True)
    self.body.setPosition(pos)
    self.body.kind = avatar
    self.mass = ode.Mass()
    self.mass.setSphere(100, radius)
    self.body.setMass(self.mass)
    self.geom = ode.GeomSphere(game.space,radius)
    self.geom.setBody(self.body)
  def draw(self):
    glPushMatrix()
    pos = self.body.getPosition()
    glTranslated(pos[0], pos[1], pos[2])
    glCallList(self.display_list)
    glPopMatrix()
  def obsolete(self):
    return False

class portal:
  def __init__(self, game, pos, radius):
    self.display_list = glGenLists(1)
    glNewList(self.display_list, GL_COMPILE)
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluQuadricDrawStyle(quadric, GLU_FILL)
    gluSphere(quadric, radius+1, 16, 16)
    glEndList()

    self.body = ode.Body(game.world)
    self.body.setKinematic()
    self.body.setPosition(pos)
    self.body.kind = portal
    self.geom = ode.GeomSphere(game.space,radius)
    self.geom.setBody(self.body)
    self.pos = pos
    self.age = 0
    self.game = game
  def draw(self):
    pos = self.pos
    glPushMatrix()
    glTranslated(pos[0], pos[1], pos[2])
    glCallList(self.display_list)
    glPopMatrix()
    self.age += 1
  def obsolete(self):
    if self.age > 300:
      print "suicide"
      self.game.space.remove(self.geom)
      return True
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
