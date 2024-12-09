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
        self.face_associations_self = []
        self.face_associations_other = []
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

        # Verifica qual objeto tem mais faces e faz o balanceamento
        max_faces = max(len(self.faces), len(other.faces))

        # Cria listas de faces associadas para ambos os objetos
        face_associations_self = []
        face_associations_other = []

        for i in range(max_faces):
            face_self = self.faces[i % len(self.faces)]  # Repete faces se necessário
            face_other = other.faces[i % len(other.faces)]  # Repete faces se necessário
            face_associations_self.append(face_self)
            face_associations_other.append(face_other)

        # Interpola vértices e faces
        for i in range(len(face_associations_self)):
            face_self = face_associations_self[i]
            face_other = face_associations_other[i]

            # Ajusta o número de vértices das faces para corresponder
            max_vertices = max(len(face_self), len(face_other))

            # Expande ou repete vértices de face_self e face_other
            adjusted_face_self = [face_self[j % len(face_self)] for j in range(max_vertices)]
            adjusted_face_other = [face_other[j % len(face_other)] for j in range(max_vertices)]

            # Cria uma nova face morfada com vértices interpolados
            morph_face = []
            for j in range(max_vertices):
                # Obtém os vértices correspondentes
                v_self = self.vertices[adjusted_face_self[j]]
                v_other = other.vertices[adjusted_face_other[j]]

                # Interpola os vértices
                x = v_self.x * (1 - t) + v_other.x * t
                y = v_self.y * (1 - t) + v_other.y * t
                z = v_self.z * (1 - t) + v_other.z * t
                morph_vertex = Ponto(x, y, z)

                # Adiciona o vértice morfado na lista de vértices
                morph_vertices.append(morph_vertex)
                morph_face.append(len(morph_vertices) - 1)

            # Adiciona a nova face morfada
            morph_faces.append(morph_face)

        # Atualiza o objeto morfado
        self.morphed_object = Objeto3D()
        self.morphed_object.vertices = morph_vertices
        self.morphed_object.faces = morph_faces