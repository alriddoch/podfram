#!/usr/bin/env python

from OpenGL import GL

import game
import graphics
import io

def main():
  app = game.podflaps()
  app.add_renderer(graphics.renderer(app))
  app.run()

if __name__ == "__main__":
  main()

