from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from Objeto3D import *

o1:Objeto3D

# Variáveis globais para ângulos de rotação
angulo_x = 0.0
angulo_y = 0.0
velocidade_rotacao = 5.0  # Aumente esse valor para ajustar a velocidade
morph_t = 0.0
morphing = False
morphed_object = None

def init():
    global o1, o2
    glClearColor(0.5, 0.5, 0.9, 1.0)
    glClearDepth(1.0)

    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    o1 = Objeto3D()
    o1.LoadFile('AK_47.obj')

    o2 = Objeto3D()
    o2.LoadFile('kar98.obj')

    DefineLuz()
    PosicUser()


def DefineLuz():
    # Define cores para um objeto dourado
    luz_ambiente = [0.4, 0.4, 0.4]
    luz_difusa = [0.7, 0.7, 0.7]
    luz_especular = [0.9, 0.9, 0.9]
    posicao_luz = [2.0, 3.0, 0.0]  # PosiÃ§Ã£o da Luz
    especularidade = [1.0, 1.0, 1.0]

    # ****************  Fonte de Luz 0

    glEnable(GL_COLOR_MATERIAL)

    #Habilita o uso de iluminaÃ§Ã£o
    glEnable(GL_LIGHTING)

    #Ativa o uso da luz ambiente
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, luz_ambiente)
    # Define os parametros da luz nÃºmero Zero
    glLightfv(GL_LIGHT0, GL_AMBIENT, luz_ambiente)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, luz_difusa)
    glLightfv(GL_LIGHT0, GL_SPECULAR, luz_especular)
    glLightfv(GL_LIGHT0, GL_POSITION, posicao_luz)
    glEnable(GL_LIGHT0)

    # Ativa o "Color Tracking"
    glEnable(GL_COLOR_MATERIAL)

    # Define a reflectancia do material
    glMaterialfv(GL_FRONT, GL_SPECULAR, especularidade)

    # Define a concentraÃ§Ã£oo do brilho.
    # Quanto maior o valor do Segundo parametro, mais
    # concentrado serÃ¡ o brilho. (Valores vÃ¡lidos: de 0 a 128)
    glMateriali(GL_FRONT, GL_SHININESS, 51)

def PosicUser():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Configura a matriz da projeção perspectiva (FOV, proporção da tela, distância do mínimo antes do clipping, distância máxima antes do clipping
    # https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/gluPerspective.xml
    gluPerspective(100, 16/9, 0.01, 50)  # Projecao perspectiva
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    #Especifica a matriz de transformação da visualização
    # As três primeiras variáveis especificam a posição do observador nos eixos x, y e z
    # As três próximas especificam o ponto de foco nos eixos x, y e z
    # As três últimas especificam o vetor up
    # https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/gluLookAt.xml
    gluLookAt(-23, 6, -10, 0, 0, 0, 0, 1.0, 0)

def DesenhaLadrilho():
    glColor3f(0.5, 0.5, 0.5)  # desenha QUAD preenchido
    glBegin(GL_QUADS)
    glNormal3f(0, 1, 0)
    glVertex3f(-0.5, 0.0, -0.5)
    glVertex3f(-0.5, 0.0, 0.5)
    glVertex3f(0.5, 0.0, 0.5)
    glVertex3f(0.5, 0.0, -0.5)
    glEnd()

    glColor3f(1, 1, 1)  # desenha a borda da QUAD
    glBegin(GL_LINE_STRIP)
    glNormal3f(0, 1, 0)
    glVertex3f(-0.5, 0.0, -0.5)
    glVertex3f(-0.5, 0.0, 0.5)
    glVertex3f(0.5, 0.0, 0.5)
    glVertex3f(0.5, 0.0, -0.5)
    glEnd()

def DesenhaPiso():
    glPushMatrix()
    glTranslated(-20, -1, -10)
    for x in range(-20, 20):
        glPushMatrix()
        for z in range(-20, 20):
            DesenhaLadrilho()
            glTranslated(0, 0, 1)
        glPopMatrix()
        glTranslated(1, 0, 0)
    glPopMatrix()

def DesenhaCubo():
    glPushMatrix()
    glColor3f(1, 0, 0)
    glTranslated(0, 0.5, 0)
    glutSolidCube(1)

    glColor3f(0.5, 0.5, 0)
    glTranslated(0, 0.5, 0)
    glRotatef(90, -1, 0, 0)
    glRotatef(45, 0, 0, 1)
    glutSolidCone(1, 1, 4, 4)
    glPopMatrix()

def desenha():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glTranslatef(0.0, 0.0, -35.0)

    # Aplica as rotações nos ângulos X e Y acumulados
    glRotatef(angulo_x, 1.0, 0.0, 0.0)
    glRotatef(angulo_y, 0.0, 1.0, 0.0)

    if morphing:
        if morphed_object:  # Desenha o objeto morfando
            morphed_object.Desenha()
            #morphed_object.DesenhaWireframe()
    else:
        # Quando o morphing terminar, desenhe apenas o `o2`
        if not morphed_object: # Desenha o objeto original inicialmente
            o1.Desenha()
            o1.DesenhaWireframe()  
        else: # Após o morphing, desenhe o objeto final (o2)
            o2.Desenha()
            o2.DesenhaWireframe()  

    #o.DesenhaVertices()

    glutSwapBuffers()
    pass

def teclado(key, x, y):
    global angulo_x, angulo_y, morphing
    
    if key == b'w' or key == b'W':
        angulo_x += velocidade_rotacao  #eixo X
    elif key == b's' or key == b'S':
        angulo_x -= velocidade_rotacao  #eixo X
    elif key == b'a' or key == b'A':
        angulo_y -= velocidade_rotacao  #eixo Y
    elif key == b'd' or key == b'D':
        angulo_y += velocidade_rotacao  #eixo Y
    elif key == b'm' or key == b'M':
        if not morphing:    # M para morfar
            morphing = True
            morph_t = 0.0
            morphed_object = o1 
            glutTimerFunc(30, atualiza_morph, 0)

    glutPostRedisplay()
    pass

def atualiza_morph(value):
    global morph_t, morphing, morphed_object, o1, o2

    if morphing:
        morph_t += 0.05  # Incrementa o estado do morph
        if morph_t > 1.0:
            morph_t = 1.0
            morphing = False  # Finaliza o morphing
            morphed_object = None

        # Gera o objeto intermediário
        morphed_object = o1.MorphTo(o2, morph_t)
        glutPostRedisplay()

        if morphing:
            glutTimerFunc(30, atualiza_morph, 0)


def main():

    glutInit(sys.argv)

    # Define o modelo de operacao da GLUT
    glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)

    # Especifica o tamnho inicial em pixels da janela GLUT
    glutInitWindowSize(640, 480)

    # Especifica a posição de início da janela
    glutInitWindowPosition(100, 100)

    # Cria a janela passando o título da mesma como argumento
    glutCreateWindow('Computacao Grafica - 3D')

    # Função responsável por fazer as inicializações
    init()

    # Registra a funcao callback de redesenho da janela de visualizacao
    glutDisplayFunc(desenha)

    # Registra a funcao callback para tratamento das teclas ASCII
    glutKeyboardFunc(teclado)

    try:
        # Inicia o processamento e aguarda interacoes do usuario
        glutMainLoop()
    except SystemExit:
        pass

if __name__ == '__main__':
    main()