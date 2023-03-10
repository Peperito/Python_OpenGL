import time

import pygame

from glapp.PyOGLApp import *
from glapp.GraphicsData import *
import numpy as np
from glapp.Utils import *
from glapp.Square import *
from glapp.WorldAxes import *
from glapp.ChristmasTriangle import *
from glapp.Cube import *
from glapp.LoadMesh import *
from glapp.MovingCube import *
from glapp.Light import *

vertex_shader = r'''
#version 330 core
in vec3 position;
in vec3 vertex_color;
in vec3 vertex_normal;
uniform mat4 projection_mat;
uniform mat4 model_mat;
uniform mat4 view_mat;
out vec3 color;
out vec3 normal;
out vec3 frag_pos;
out vec3 view_pos;
void main() 
{
    view_pos = vec3(inverse(model_mat) * 
                vec4(view_mat[3][0], view_mat[3][1], view_mat[3][2], 1));
    gl_Position = projection_mat * inverse(view_mat) * model_mat * vec4(position, 1);
    normal = mat3(transpose(inverse(model_mat))) * vertex_normal;
    frag_pos = vec3(model_mat * vec4(position, 1));
    color = vertex_color;
}
'''

fragment_shader = r'''
#version 330 core
in vec3 color;
in vec3 normal;
in vec3 frag_pos;
in vec3 view_pos;
out vec4 frag_color;

struct light {
    vec3 position;
    vec3 color;
};

#define NUM_LIGHTS 3
uniform light light_data[NUM_LIGHTS];

vec4 Create_Light(vec3 light_pos, vec3 light_color, vec3 normal, vec3 frag_pos, vec3 view_dir) 
{

    //ambient
    float a_strength = 0.2;
    vec3 ambient = a_strength * light_color;
    
    //diffuse
    vec3 norm = normalize(normal);
    vec3 light_dir = normalize(light_pos - frag_pos);
    float diff = max(dot(norm, light_dir), 0);
    vec3 diffuse = diff * light_color;

    //specular 
    float s_strength = 0.8;
    vec3 reflect_dir = normalize(-light_dir - norm);
    float spec = pow(max(dot(view_dir, reflect_dir), 0), 32);
    vec3 specular = s_strength * spec * light_color; 
    
    return vec4(color * (ambient + diffuse + specular), 1);
}

void main()
{
    vec3 view_dir = normalize(view_pos - frag_pos);
    for(int i = 0; i < NUM_LIGHTS; i++){
        frag_color += Create_Light(light_data[i].position, light_data[i].color, normal, frag_pos, view_dir); 
    }
}
'''


class ShadedObject(PyOGLApp):

    def __init__(self):
        super().__init__(850, 200, 1000, 800)
        #self.world_axes = None
        self.teapot = None
        self.light = None
        self.light_2 = None
        self.light_3 = None

    def initialise(self):
        self.program_id = create_program(vertex_shader, fragment_shader)
        #self.world_axes = WorldAxes(self.program_id, location=pygame.Vector3(0, 0, 0))
        self.teapot = LoadMesh("./objs/teapot.obj", self.program_id,
                               location=pygame.Vector3(0, 0, 0),
                               scale=pygame.Vector3(0.5, 0.5, 0.5),
                               move_rotation=Rotation(1, pygame.Vector3(0, 1, 0)))
        self.light = Light(self.program_id, pygame.Vector3(3, 3, 3), pygame.Vector3(1, 0, 1), 0)
        self.light_2 = Light(self.program_id, pygame.Vector3(-3, 3, 3), pygame.Vector3(0, 1, 0), 1)
        self.light_3 = Light(self.program_id, pygame.Vector3(0, 4, 4), pygame.Vector3(1, 0, 1), 2)
        self.camera = Camera(self.program_id, self.screen_width, self.screen_height)
        glEnable(GL_DEPTH_TEST)

    def camera_init(self):
        pass

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.program_id)
        self.camera.update()
        self.light.update()
        self.light_2.update()
        self.light_3.update()
        #self.world_axes.draw()
        self.teapot.draw()


ShadedObject().mainloop()
