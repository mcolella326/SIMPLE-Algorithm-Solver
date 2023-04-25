import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

def draw_cube():
    # Set the color of all faces to red
    glColor3f(0.5, 0.5, 0.5)

    # Define vertices and indices
    vertices = [(-1, -1, -1),
                (1, -1, -1),
                (1, 1, -1),
                (-1, 1, -1),
                (-1, -1, 1),
                (1, -1, 1),
                (1, 1, 1),
                (-1, 1, 1)]
    
    indices = [(0, 1, 2, 3),
               (1, 5, 6, 2),
               (4, 0, 3, 7),
               (5, 4, 7, 6),
               (4, 5, 1, 0),
               (3, 2, 6, 7)]

    # draw the faces
    glBegin(GL_QUADS)
    for index_face in indices:
        for vertex_ind in index_face:
            glVertex3fv(vertices[vertex_ind])
    glEnd()

    # set the color of edges to black
    glColor3f(0, 0, 0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glLineWidth(2.0)  # set line width
    # draw the edges
    glBegin(GL_LINES)
    for index_face in indices:
        for i in range(len(index_face)):
            glVertex3fv(vertices[index_face[i]])
            glVertex3fv(vertices[index_face[(i+1)%4]])
    glEnd()

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
    pygame.display.set_caption('Geometry, Mesh, and Boundary Conditions')

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0, 0.0, -5)
    glRotatef(35.264, 1, 0, 0)
    glRotatef(-45, 0, 1, 0)

    glClearColor(1.0, 1.0, 1.0, 1.0)

    clock = pygame.time.Clock()

    drag = False
    mouse_position = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drag = True
                    mouse_position = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drag = False

        if drag:
            new_mouse_position = pygame.mouse.get_pos()
            dx = new_mouse_position[0] - mouse_position[0]
            dy = new_mouse_position[1] - mouse_position[1]

            glRotatef(dx, 0, 1, 0)
            glRotatef(dy, 1, 0, 0)

            mouse_position = new_mouse_position

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        draw_cube()
        pygame.display.flip()

        clock.tick(60)

if __name__ == "__main__":
    main()