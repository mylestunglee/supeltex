import OpenGL.GL as gl
import OpenGL.GLUT as glut
import numpy as np

from PIL import Image
from PIL import ImageOps

def load_shader(shader_source, shader_type):
	shader_id = gl.glCreateShader(shader_type)
	gl.glShaderSource(shader_id, shader_source)
	gl.glCompileShader(shader_id)

	if gl.glGetShaderiv(shader_id, gl.GL_COMPILE_STATUS) != gl.GL_TRUE:
		info = gl.glGetShaderInfoLog(shader_id)
		gl.glDeleteShader(shader_id)
		raise RuntimeError('Shader compilation failed: {}'.format(info))

	return shader_id

def load_program(vertex_shader_filename, fragment_shader_filename):
	program_id = gl.glCreateProgram()

	with open(vertex_shader_filename) as vertex_shader_file:
		vertex_shader_id = load_shader(vertex_shader_file.read(), gl.GL_VERTEX_SHADER)

	with open(fragment_shader_filename) as fragment_shader_file:
		fragment_shader_id = load_shader(fragment_shader_file.read(), gl.GL_FRAGMENT_SHADER)

	gl.glAttachShader(program_id, vertex_shader_id)
	gl.glAttachShader(program_id, fragment_shader_id)

	gl.glLinkProgram(program_id)

	if gl.glGetProgramiv(program_id, gl.GL_LINK_STATUS) != gl.GL_TRUE:
		glDeleteProgram(program_id)
		glDeleteShader(vertex_shader_id)
		glDeleteShader(fragment_shader_id)
		info = glGetProgramInfoLog(program_id)
		raise RuntimeError('Error linking program: {}'.format(info))

	return program_id

def load_vbo(vertex_data):
	vbo_id = gl.glGenBuffers(1)
	gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo_id)
	gl.glBufferData(
		gl.GL_ARRAY_BUFFER,
		gl.ArrayDatatype.arrayByteCount(vertex_data),
		vertex_data,
		gl.GL_STATIC_DRAW)
	return vbo_id

def link_shaders(program_id):
	gl.glVertexAttribPointer(
		gl.glGetAttribLocation(program_id, 'vertex'),
		4,
		gl.GL_FLOAT,
		gl.GL_FALSE,
		0,
		None)
	gl.glEnableVertexAttribArray(gl.glGetAttribLocation(program_id, 'vertex'))
	gl.glUseProgram(program_id)

def opengl_render(vertex_data):
	program_id = load_program('vertex.glsl', 'fragment.glsl')
	vbo_id = load_vbo(vertex_data)
	link_shaders(program_id)
	gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, vertex_data.size // 4)

def render(width, height, vertex_data, filename):
	glut.glutInit()

	# 8x anti-aliasing
	glut.glutSetOption(glut.GLUT_MULTISAMPLE, 8);
	glut.glutInitDisplayMode(glut.GLUT_ALPHA | glut.GLUT_MULTISAMPLE)
	glut.glutInitWindowSize(width, height)
	glut.glutCreateWindow('')

	opengl_render(vertex_data)

	gl.glPixelStorei(gl.GL_PACK_ALIGNMENT, 1)
	data = gl.glReadPixels(0, 0, width, height, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE)
	image = Image.frombytes('RGBA', (width, height), data)
	image.save(filename)
