import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

def draw_cube(height, length, width, num_height_subdivisions=1, num_length_subdivisions=1, num_width_subdivisions=1):
    # Set the color of all faces to gray
    glColor3f(0.5, 0.5, 0.5)

    # Define vertices and indices

    # Vertices defined in (length, height, width) order
    vertices = [(-length / 2, -height / 2, -width / 2),
                (length / 2, -height / 2, -width / 2),
                (length / 2, height / 2, -width / 2),
                (-length / 2, height / 2, -width / 2),
                (-length / 2, -height / 2, width / 2),
                (length / 2, -height / 2, width / 2),
                (length / 2, height / 2, width / 2),
                (-length / 2, height / 2, width / 2)]
    
    indices = [(0, 1, 2, 3),
               (1, 5, 6, 2),
               (4, 0, 3, 7),
               (5, 4, 7, 6),
               (4, 5, 1, 0),
               (3, 2, 6, 7)]

    # Draw the faces
    glBegin(GL_QUADS)
    for index_face in indices:
        for vertex_ind in index_face:
            glVertex3fv(vertices[vertex_ind])
    glEnd()

    # Set the color of edges to black and adjust polygon mode to get desired projection mode
    glColor3f(0, 0, 0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glLineWidth(2.0)

    # Calculate subdivision sizes
    height_subdivision_size = height / (num_height_subdivisions)
    length_subdivision_size = length / (num_length_subdivisions)
    width_subdivision_size = width / (num_width_subdivisions)

    # Draw subdivided edges along height dimension
    glBegin(GL_LINES)
    for i in range(num_width_subdivisions):
        z = (-width / 2) + i*width_subdivision_size
        for j in range(num_length_subdivisions):
            x1 = (-length / 2) + j*length_subdivision_size
            x2 = x1 + length_subdivision_size
            y1 = -height / 2
            y2 = height / 2
            glVertex3f(x1, y1, z)
            glVertex3f(x2, y1, z)
            glVertex3f(x2, y1, z)
            glVertex3f(x2, y2, z)
            glVertex3f(x2, y2, z)
            glVertex3f(x1, y2, z)
            glVertex3f(x1, y2, z)
            glVertex3f(x1, y1, z)
    glEnd()

    # Draw subdivided edges along length dimension
    glBegin(GL_LINES)
    for i in range(num_length_subdivisions):
        x = (-length / 2) + i*length_subdivision_size
        for j in range(num_height_subdivisions):
            y1 = (-height / 2) + j*height_subdivision_size
            y2 = y1 + height_subdivision_size
            z1 = -width / 2
            z2 = width / 2
            glVertex3f(x, y1, z1)
            glVertex3f(x, y1, z2)
            glVertex3f(x, y1, z2)
            glVertex3f(x, y2, z2)
            glVertex3f(x, y2, z2)
            glVertex3f(x, y2, z1)
            glVertex3f(x, y2, z1)
            glVertex3f(x, y1, z1)
    glEnd()

    # Draw subdivided edges along width dimension
    glBegin(GL_LINES)
    for i in range(num_height_subdivisions):
        y = (-height / 2) + i*height_subdivision_size
        for j in range(num_width_subdivisions):
            z1 = (-width / 2) + j*width_subdivision_size
            z2 = z1 + width_subdivision_size
            x1 = -length / 2
            x2 = length / 2
            glVertex3f(x1, y, z1)
            glVertex3f(x1, y, z2)
            glVertex3f(x1, y, z2)
            glVertex3f(x2, y, z2)
            glVertex3f(x2, y, z2)
            glVertex3f(x2, y, z1)
            glVertex3f(x2, y, z1)
            glVertex3f(x1, y, z1)
    glEnd()

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

def draw_axes():
        # Draw the x-axis
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(2.5, 0.0, 0.0)
    glEnd()

    # Draw the y-axis
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 2.5, 0.0)
    glEnd()

    # Draw the z-axis
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_LINES)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 2.5)
    glEnd()

def main():
    pygame.init()
    display = (1200, 800)
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
    pygame.display.set_caption('Geometry, Mesh, and Boundary Conditions')
    length = 1
    height = 5
    width = 10

    gluPerspective(45, (display[0]/display[1]), 0.1, 50000.0)

    glClearColor(1.0, 1.0, 1.0, 1.0)

    clock = pygame.time.Clock()

    drag = False
    mouse_position = None
    cube_dx, cube_dy = 0, 0
    axis_dx, axis_dy = 0, 0
    zoom = 5

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
            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    zoom -= 0.1
                else:
                    zoom += 0.1

        if drag:
            new_mouse_position = pygame.mouse.get_pos()
            dx = new_mouse_position[0] - mouse_position[0]
            dy = new_mouse_position[1] - mouse_position[1]

            cube_dx += dx
            cube_dy += dy

            axis_dx += dx
            axis_dy += dy

            mouse_position = new_mouse_position

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glViewport(0, 0, display[0]//4, display[1]//4)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(-10, 10, -10, 10)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glRotatef(axis_dy+35.264, 1, 0, 0)
        glRotatef(axis_dx-45, 0, 1, 0)
        draw_axes()

        glViewport(0, 0, display[0], display[1])
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (display[0]/display[1]), 0.1, 50000.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -max(length, height, width)-zoom)
        glRotatef(cube_dy+35.264, 1, 0, 0)
        glRotatef(cube_dx-45, 0, 1, 0)
        draw_cube(height, length, width, 10, 10, 10)

        pygame.display.flip()

        clock.tick(60)

if __name__ == "__main__":
    main()