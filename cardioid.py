#!/usr/bin/env python3

import numpy as np
import sys

class Stl:
    def __init__(self):
        self.faces = [ ]

    def add_face(self, a, b, c):
        self.faces.append((a, b, c))

    def save(self, out, name = "Heart"):
        out.write(f"solid {name}\n")
        for a, b, c in self.faces:
            n = np.cross(c - a, b - a)
            n /= np.sqrt(np.sum(np.square(n)))
            out.write(f"""\
  facet normal {n[0]} {n[1]} {n[2]}
    outer loop
      vertex {a[0]} {a[1]} {a[2]}
      vertex {b[0]} {b[1]} {b[2]}
      vertex {c[0]} {c[1]} {c[2]}
   endloop
  endfacet
""")
        out.write("endsolid\n")

def cardioid(points = 20, layers = 10, zscale = 2.0):
    def vertex(i, j):
        z = (1.0 * j) / layers
        phi = (np.pi * i * 2.0) / points - np.pi
        a = zscale * np.sqrt(1.0 - z * z)
        x = 2.0 * a * (1.0 - np.cos(phi)) * np.cos(phi)
        y = 2.0 * a * (1.0 - np.cos(phi)) * np.sin(phi)
        return np.array([x, y, z])

    res = Stl();

    for l in range(layers - 1):
        for i in range(points):
            ni = (i + 1) % points
            res.add_face(vertex(i, l), vertex(ni, l), vertex(i, l + 1))
            res.add_face(vertex(ni, l), vertex(ni, l + 1), vertex(i, l + 1))

            res.add_face(vertex(ni, -l), vertex(i, -l), vertex(i, -l - 1))
            res.add_face(vertex(ni, -l - 1), vertex(ni, -l), vertex(i, -l - 1))

    top = np.array([0.0, 0.0, 1.0])
    bottom = np.array([0.0, 0.0, -1.0])
    for i in range(points):
        ni = (i + 1) % points
        res.add_face(vertex(i, layers - 1), vertex(ni, layers - 1), top)
        res.add_face(vertex(ni, 1 - layers), vertex(i, 1 - layers), bottom)

    res.save(sys.stdout)

if __name__ == '__main__':
    cardioid()
