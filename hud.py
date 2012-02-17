from OpenGL.GL import *
import Image

class backdrop:
  def __init__(self, filename):
    image = Image.open(filename)
    raw = image.tostring("raw", "RGBX", 0, -1)

    self.texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, self.texture)
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, image.size[0], image.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, raw)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

  def draw(self, r):
    
    glBindTexture(GL_TEXTURE_2D, self.texture)
    # glBlendFunc(GL_SRC_ALPHA,GL_ONE)
    glEnable(GL_TEXTURE_2D)
    glColor3f(1,1,1)
    glBegin(GL_QUADS)
    glTexCoord2d(0,0); glVertex3f(0,0,0)
    glTexCoord2d(0,1); glVertex3f(0,r.size[1],0)
    glTexCoord2d(1,1); glVertex3f(r.size[0],r.size[1],0)
    glTexCoord2d(1,0); glVertex3f(r.size[0],0,0)
    glEnd()
    glDisable(GL_TEXTURE_2D)
