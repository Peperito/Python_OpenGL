from Engine2.glapp.Mesh import *
import numpy as np
from Engine2.glapp.Utils import *


class MovingCube(Mesh):
    def __init__(self, program_id,
                 location=pygame.Vector3(0, 0, 0),
                 move_rotation=pygame.Vector3(0, 1, 0)):
        coordinates = [(0.5, -0.5, 0.5),
                       (-0.5, -0.5, 0.5),
                       (0.5, 0.5, 0.5),
                       (-0.5, 0.5, 0.5),
                       (0.5, 0.5, -0.5),
                       (-0.5, 0.5, -0.5),
                       (0.5, -0.5, -0.5),
                       (-0.5, -0.5, -0.5),
                       (0.5, 0.5, 0.5),
                       (-0.5, 0.5, 0.5),
                       (0.5, 0.5, -0.5),
                       (-0.5, 0.5, -0.5),
                       (0.5, -0.5, -0.5),
                       (0.5, -0.5, 0.5),
                       (-0.5, -0.5, 0.5),
                       (-0.5, -0.5, -0.5),
                       (-0.5, -0.5, 0.5),
                       (-0.5, 0.5, 0.5),
                       (-0.5, 0.5, -0.5),
                       (-0.5, -0.5, -0.5),
                       (0.5, -0.5, -0.5),
                       (0.5, 0.5, -0.5),
                       (0.5, 0.5, 0.5),
                       (0.5, -0.5, 0.5)
                       ]
        triangles = [0, 2, 3, 0, 3, 1, 8, 4, 5, 8, 5, 9, 10, 6, 7, 10, 7, 11, 12,
                     13, 14, 12, 14, 15, 16, 17, 18, 16, 18, 19, 20, 21, 22, 20, 22, 23]

        vertices = format_vertices(coordinates, triangles)

        colors = np.random.uniform(low=0.0, high=1.0, size=(36, 3))
        super().__init__(program_id, vertices, colors, GL_TRIANGLES, location,
                         move_rotation=move_rotation)
