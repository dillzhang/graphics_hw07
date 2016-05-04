import mdl
from display import *
from matrix import *
from draw import *
from math import *

def run(filename):
    """
    This function runs an mdl script
    """
    color = [255, 255, 255]
    tmp = new_matrix()
    ident(tmp)

    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print "Parsing failed."
        return

    stack = [tmp]
    screen = new_screen()
    points = []
    
    for command in commands:
        print command
        if command[0] == "push":
            temp = new_matrix()
            for i in range(4):
                for j in range(4):
                    temp[i][j] = stack[-1][i][j]
            stack.append(temp)
        elif command[0] == "pop":
            stack.pop()
        elif command[0] == "move":
            t = make_translate(command[1], command[2], command[3])
            matrix_mult(stack[-1], t)
            stack[-1] = t
        elif command[0] == "rotate":
            print command[1], command[2]
            if command[1] == 'x':
                print "x rot"
                r = make_rotX(radians(command[2]))
            elif command[1] == 'y':
                print "y rot"
                r = make_rotY(radians(command[2]))
            elif command[1] == 'z':
                print "z rot"
                r = make_rotZ(radians(command[2]))
            matrix_mult(stack[-1], r)
            stack[-1] = r
        elif command[0] == "scale":
            s = make_scale(command[1], command[2], command[3])
            matrix_mult(stack[-1], s)
            stack[-1] = s
        elif command[0] in ['sphere', 'torus', 'box']:
            if command[0] == "box":
                add_box(points, command[1], command[2], command[3], command[4], command[5], command[6])
            elif command[0] == "sphere":
                add_sphere(points, command[1], command[2], command[3], command[4], 5)
            elif command[0] == "torus":
                add_torus(points, command[1], command[2], 0, command[3], command[4], 5)
            matrix_mult(stack[-1], points)
            draw_polygons(points, screen, color)
            points = []
        elif command[0] == "line":
            add_edge(points, command[1], command[2], command[3], command[4], command[5], command[6])
            matrix_mult(stack[-1], points)
            draw_lines(points)
            points = []
        elif command[0] == "display":
            display(screen)
        elif command[0] == "save":
            save_extension(screen, str(command[1]).strip())
        elif command[0] == "quit":
            return
        else:
            print "Invalid Command: " + command
