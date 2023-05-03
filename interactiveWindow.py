import pygame
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

def draw_prism(height, length, width, num_height_subdivisions, num_length_subdivisions, num_width_subdivisions, mouse_position):
    # Calculate mouse ray origin and direction
    mouse_x, mouse_y = mouse_position
    viewport = glGetIntegerv(GL_VIEWPORT)
    mouse_pos_3d = gluUnProject(mouse_x, viewport[3] - mouse_y, 0.0, glGetDoublev(GL_MODELVIEW_MATRIX), glGetDoublev(GL_PROJECTION_MATRIX), viewport)
    mouse_pos_3d_end = gluUnProject(mouse_x, viewport[3] - mouse_y, 1.0, glGetDoublev(GL_MODELVIEW_MATRIX), glGetDoublev(GL_PROJECTION_MATRIX), viewport)
    mouse_ray = np.array(mouse_pos_3d_end) - np.array(mouse_pos_3d)
    mouse_ray /= np.linalg.norm(mouse_ray)

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
    
    # Calculate face normals and directions facing the screen
    face_normals = []
    for face in indices:
        v0, v1, v2, _ = [vertices[i] for i in face]
        normal = np.cross(np.array(v1) - np.array(v0), np.array(v2) - np.array(v0))
        face_normals.append(normal)

    face_directions = np.dot(face_normals, mouse_ray)

    def ray_triangle_intersection(ray_origin, ray_direction, v0, v1, v2):
    # Compute edge vectors
        e1 = np.array(v1) - np.array(v0)
        e2 = np.array(v2) - np.array(v0)

        # Compute determinant and check if ray is parallel to triangle
        p = np.cross(ray_direction, e2)
        det = np.dot(e1, p)
        if abs(det) < 1e-8:
            return None

        # Compute barycentric coordinates and check if intersection point is inside triangle
        t = np.array(ray_origin) - np.array(v0)
        u = np.dot(t, p) / det
        if u < 0 or u > 1:
            return None

        q = np.cross(t, e1)
        v = np.dot(ray_direction, q) / det
        if v < 0 or u + v > 1:
            return None

        # Compute intersection point and return it
        distance = np.dot(e2, q) / det
        intersection_point = np.array(ray_origin) + distance * np.array(ray_direction)
        return tuple(intersection_point)
    

    # Draw the faces, coloring yellow on click
    for ind, face in enumerate(indices):
        if face_directions[ind] < 0:
            continue
        if ray_triangle_intersection(mouse_pos_3d, mouse_ray, vertices[face[0]], vertices[face[1]], vertices[face[2]]) or ray_triangle_intersection(mouse_pos_3d, mouse_ray, vertices[face[2]], vertices[face[3]], vertices[face[0]]):
            glColor3f(1.0, 1.0, 0)
        else:
            glColor3f(0.5, 0.5, 0.5)
        glBegin(GL_QUADS)
        for vertex_ind in face:
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

def draw_text(text_dict, display, font):
    for text in text_dict:
        textSurface = font.render(f'{text["title"]}{text["text"]}', True, text['color']).convert_alpha()
        textData = pygame.image.tostring(textSurface, "RGBA", True)
        glWindowPos2d(text['x'], display[1] - text['y'] - textSurface.get_height())
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

def main():
    pygame.init()
    display = (1200, 800)
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
    pygame.display.set_caption('Geometry, Mesh, and Boundary Conditions')
    height = 5
    length = 1
    width = 10
    num_height_subdivisions = 10
    num_length_subdivisions = 5
    num_width_subdivisions = 20
    drag = False
    cube_dx, cube_dy = 0, 0
    axis_dx, axis_dy = 0, 0
    zoom = 5
    font = pygame.font.SysFont('arial', 20)
    text_dict = [{'title': 'Y Dimension: ', 'text': str(height), 'color': (0, 0, 0), 'x': 0, 'y': 0},
                {'title': 'X Dimension: ', 'text': str(length), 'color': (0, 0, 0), 'x': 0, 'y': 25},
                {'title': 'Z Dimension: ', 'text': str(width), 'color': (0, 0, 0), 'x': 0, 'y': 50},
                {'title': 'Y subdivisions: ', 'text': str(num_height_subdivisions), 'color': (0, 0, 0), 'x': 0, 'y': 75},
                {'title': 'X subdivisions: ', 'text': str(num_length_subdivisions), 'color': (0, 0, 0), 'x': 0, 'y': 100},
                {'title': 'Z subdivisions: ', 'text': str(num_width_subdivisions), 'color': (0, 0, 0), 'x': 0, 'y': 125}]
    selected_text = None
    mouse_position = (0, 0)

    glClearColor(1.0, 1.0, 1.0, 1.0)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    drag = True
                    mouse_position = pygame.mouse.get_pos()
                    for text in text_dict:
                        text_rect = font.render(f'{text["title"]}{text["text"]}', True, text['color']).get_rect(topleft=(text['x'], text['y']))
                        if text_rect.collidepoint(mouse_position):
                            selected_text = text
                            selected_text['color'] = (0, 255, 0)  # Change color to green
                        else:
                            text['color'] = (0, 0, 0)  # Change color to black
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drag = False
            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    zoom -= 0.1
                else:
                    zoom += 0.1
            elif event.type == pygame.KEYDOWN:
                if selected_text is not None and event.key == pygame.K_RETURN:
                    selected_text['text'] = f"{selected_text['text']}"
                    selected_text['color'] = (0, 0, 0)  # Reset color to black
                    if selected_text['title'] == 'Y Dimension: ':
                        height = float(selected_text['text'])
                    elif selected_text['title'] == 'X Dimension: ':
                        length = float(selected_text['text'])
                    elif selected_text['title'] == 'Z Dimension: ':
                        width = float(selected_text['text'])
                    elif selected_text['title'] == 'Y subdivisions: ':
                        num_height_subdivisions = int(selected_text['text'])
                    elif selected_text['title'] == 'X subdivisions: ':
                        num_length_subdivisions = int(selected_text['text'])
                    elif selected_text['title'] == 'Z subdivisions: ':
                        num_width_subdivisions = int(selected_text['text'])
                    selected_text = None
                elif event.key == pygame.K_BACKSPACE:
                    selected_text['text'] = selected_text['text'][:-1]  # Remove last character
                elif event.key == pygame.K_RETURN:
                    pass
                else:
                    selected_text['text'] += event.unicode  # Add typed character

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
        draw_prism(height, length, width, num_height_subdivisions, num_length_subdivisions, num_width_subdivisions, mouse_position)

        draw_text(text_dict, display, font)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()