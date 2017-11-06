#!/usr/bin/python
import json
import math

from shapely.geometry import Polygon, Point
from flask import Flask, render_template, abort, request
from functools import lru_cache
from collections import defaultdict

app = Flask(__name__)

def generate_vertices(x, y):
    result = None
    x_offset = math.floor(x / 2)
    #I don't actually need to have an if statement here
    #it seems better than cluttering up the math though
    if x % 2 == 1:
        result = {'v1' : {'x' : (x - 1 - x_offset) * 10,
                          'y' : y * 10},
                  'v2' : {'x' : (x - 1 - x_offset) * 10,
                          'y' : (y + 1) * 10},
                  'v3' : {'x' : (x - x_offset) * 10,
                          'y' : (y + 1) * 10}}
    else:
        result = {'v1' : {'x' : (x - 1 - x_offset) * 10,
                          'y' : y * 10},
                  'v2' : {'x' : (x - x_offset) * 10,
                          'y' : y  * 10},
                  'v3' : {'x' : (x - x_offset) * 10,
                          'y' : (y + 1) * 10}}
    return result

def make_render_string(vertices):
    #This can work for any polygon
    #this format for rendering should work with
    #the svg>polygon html tag
    result = ''
    for ndx, vert in enumerate(vertices.keys()):
        result += str(vertices[vert]['x']) + ',' + str(vertices[vert]['y'])
        if ndx < len(vertices):
            result += ','
    return result

def get_centroid(vertices):
    centroid = None
    if isinstance(vertices,dict):
        x, y = 0, 0
        for key in vertices.keys():
            x += vertices[key]['x']
            y += vertices[key]['y']
        x = x / len(vertices)
        y = y / len(vertices)
        centroid = (x, y)
    elif isinstance(vertices, list):
        x, y = 0, 0
        for vert in vertices:
            x += vert[0]
            y += vert[1]
        x = x / len(vertices)
        y = y / len(vertices)
        centroid = (x, y)
    return centroid

def get_name(x, y):
    return str(chr(65 + y)) + str(x)

#lru_cache memoizes input
#this is just a really simple performance gain
@lru_cache(maxsize=100)
def generate_triangles(rows, columns):
    triangles = []
    for x in range(1, columns + 1):
        for y in range(rows):
            verts = generate_vertices(x, y)
            render_string = make_render_string(verts)
            name = get_name(x, y)
            centroid = get_centroid(verts)
            triangles.append({'vertices' : verts,
                              'render_string' : render_string,
                              'x' : x,
                              'y' : y,
                              'id' : name,
                              'centroid' : centroid
                              })
    return triangles

def determine_comparison(vertices, comparator, rows=6, columns=12):
    #Unoptimized but this could be done a few different ways
    #This is a higher order function the comparator is a lambda
    #due to pythons duck typing we can just pass a function that
    #makes the polygon comparisons
    result = []
    triangles = generate_triangles(rows, columns)
    polygon_to_check = Polygon(vertices)
    try:
        for triangle in triangles:
            verts = [(triangle['vertices']['v1']['x'], triangle['vertices']['v1']['y']),
                    (triangle['vertices']['v2']['x'], triangle['vertices']['v2']['y']),
                    (triangle['vertices']['v3']['x'], triangle['vertices']['v3']['y'])]
            new_poly = Polygon(verts)
            if comparator(polygon_to_check, new_poly):
               result.append(triangle['id'])
    except:
        #Polygon was non convex
        result = []
    return result

def determine_strict(vertices):
    return []

def generate_verts_for_comparison(vertices):
    vertices = [ int(x) for x in vertices.split(',')]
    if len(vertices) % 2 != 0:
        return None
    verts = []
    for x in range(1,len(vertices), 2):
        verts.append((vertices[x - 1], vertices[x]))
    return verts

@app.route('/intersect/<vertices>')
def intersect(vertices):
    verts = generate_verts_for_intersect(vertices)
    comp = lambda x,y: x.crosses(y) or x.within(y) or x.contains(y)
    if not verts:
        abort(400)
    return json.dumps(determine_comparison(verts))

@app.route('/triangles/<rows>/<columns>', methods=['GET'])
def vertices(rows, columns):
    try:
        rows = int(rows)
        columns = int(columns)
        return json.dumps(generate_triangles(rows, columns))
    except ValueError:
        #If we fail to parse rows and columns into ints
        #that's a 400
        abort(400)
    except:
        #If we fail because we've messed up for any other reason
        #that's a 500
        abort(500)

def get_view_port(rows, columns):
    view_port = {}
    view_port['x_extent'] = (math.floor((columns + 1) / 2) * 10)
    view_port['y_extent'] = rows * 10
    return view_port

def get_matches(mode, polygon, rows, columns):
    matches = defaultdict(None)
    verts = generate_verts_for_comparison(polygon)
    comp = lambda x, y: False
    comp = lambda x,y : x.centroid().within(y)
    if mode == 'Strict':
        comp = lambda x,y: x.equals(y)
    elif mode == 'Intersect':
        comp = lambda x,y: x.intersects(y)

    for item in determine_comparison(verts, comp, rows, columns):
        matches[item] = True

    return matches

@app.route('/')
def index():
    rows = int(request.args.get('rows',6))
    columns = int(request.args.get('columns',12))
    polygon = request.args.get('vertices', None)
    mode = request.args.get('mode', None)

    mode = None if mode == '' else mode
    polygon = None if polygon == '' else polygon
    view_port = get_view_port(rows, columns)
    triangles = generate_triangles(rows, columns)
    matches = get_matches(mode, polygon, rows, columns)

    return render_template('index.html', triangles=triangles, view_port=view_port, rows=rows, columns=columns, polygon=polygon, mode=mode, matches=matches)

if __name__ == '__main__':
    app.run(debug=False)
