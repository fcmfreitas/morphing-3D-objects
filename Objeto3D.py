from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from Ponto import *

class Objeto3D:

    def __init__(self):
        self.vertices = []
        self.faces = []
        self.position = Ponto(0,0,0)
        self.rotation = [0,0,0,1]
        self.morphed_object = self
        pass

    def LoadFile(self, file:str):
        f = open(file, "r")

        # leitor de .obj baseado na descrição em https://en.wikipedia.org/wiki/Wavefront_.obj_file    
        for line in f:
            values = line.split(' ')
            # dividimos a linha por ' ' e usamos o primeiro elemento para saber que tipo de item temos

            if values[0] == 'v': 
                # item é um vértice, os outros elementos da linha são a posição dele
                self.vertices.append(Ponto(float(values[1]),
                                           float(values[2]),
                                           float(values[3])))

            if values[0] == 'f':
                # item é uma face, os outros elementos da linha são dados sobre os vértices dela
                self.faces.append([])
                for fVertex in values[1:]:
                    fInfo = fVertex.split('/')
                    # dividimos cada elemento por '/'
                    self.faces[-1].append(int(fInfo[0]) - 1) # primeiro elemento é índice do vértice da face
                    # ignoramos textura e normal
                
            # ignoramos outros tipos de items, no exercício não é necessário e vai só complicar mais
        pass

    def Scale(self, scale_factor):
        for v in self.vertices:
            v.x *= scale_factor
            v.y *= scale_factor
            v.z *= scale_factor

    def DesenhaVertices(self):
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glRotatef(self.rotation[3], self.rotation[0], self.rotation[1], self.rotation[2])
        glColor3f(.1, .1, .8)
        glPointSize(8)

        glBegin(GL_POINTS)
        for v in self.vertices:
            glVertex(v.x, v.y, v.z)
        glEnd()
        
        glPopMatrix()
        pass

    def DesenhaWireframe(self):
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glRotatef(self.rotation[3], self.rotation[0], self.rotation[1], self.rotation[2])
        glColor3f(0, 0, 0)
        glLineWidth(2)        
        
        for f in self.faces:            
            glBegin(GL_LINE_LOOP)
            for iv in f:
                v = self.vertices[iv]
                glVertex(v.x, v.y, v.z)
            glEnd()
        
        glPopMatrix()
        pass

    def Desenha(self):
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, self.position.z)
        glRotatef(self.rotation[3], self.rotation[0], self.rotation[1], self.rotation[2])
        glColor3f(0.34, .34, .34)
        glLineWidth(2)        
        
        for f in self.faces:            
            glBegin(GL_TRIANGLE_FAN)
            for iv in f:
                v = self.vertices[iv]
                glVertex(v.x, v.y, v.z)
            glEnd()
        
        glPopMatrix()
        pass
    
    def MorphTo(self, other, t):
        morph_vertices = []
        morph_faces = []

        # Número de vértices a considerar no morphing
        max_vertices = max(len(self.vertices), len(other.vertices))
        max_faces = max(len(self.faces), len(other.faces))

        for i in range(max_vertices):
            v1 = self.vertices[i % len(self.vertices)] #resto para voltar pro inicio
            v2 = other.vertices[i % len(other.vertices)]

            # Interpolação dos vértices
            x = (1 - t) * v1.x + t * v2.x
            y = (1 - t) * v1.y + t * v2.y
            z = (1 - t) * v1.z + t * v2.z
            morph_vertices.append(Ponto(x, y, z))

        for i in range(max_faces):
            f1 = self.faces[i % len(self.faces)]
            f2 = other.faces[i % len(other.faces)]

            # Interpolação das faces
            interpolated_face = []
            for j in range(len(f2)):
                v1_index = f1[j % len(f1)]
                v2_index = f2[j % len(f2)]
                interpolated_index = int((1 - t) * v1_index + t * v2_index)
                interpolated_face.append(interpolated_index)

            morph_faces.append(interpolated_face)

        # Retorna um novo objeto 3D com os vértices interpolados
        self.morphed_object = Objeto3D()
        self.morphed_object.vertices = morph_vertices
        self.morphed_object.faces = morph_faces

