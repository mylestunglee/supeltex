import OpenGL.GL as gl
import OpenGL.GLUT as glut
from OpenGL.GL import *
import numpy as np

from PIL import Image
from PIL import ImageOps

import sys

width, height = 300, 300

def init():
	gl.glClearColor(0.5, 0.5, 0.5, 1.0)
	gl.glColor(0.0, 1.0, 0.0)
	gl.glViewport(0, 0, width, height)

vertex = '''
#version 330
in vec3 vin_position;
in vec3 vin_color;
out vec3 vout_color;

void main(void)
{
	vout_color = vin_color;
	gl_Position = vec4(vin_position, 1.0);
}
'''


fragment = '''
#version 330
in vec3 vout_color;
out vec4 fout_color;

void main(void)
{
	fout_color = vec4(vout_color, 1.0);
}
'''

vertex_data = np.array([0.75, 0.75, 0.0,
						0.75, -0.75, 0.0,
						-0.75, -0.75, 0.0], dtype=np.float32)

color_data = np.array([1, 0, 0,
						0, 1, 0,
						0, 0, 1], dtype=np.float32)

def load_shader(shader_source, shader_type):
	shader_id = gl.glCreateShader(shader_type)
	gl.glShaderSource(shader_id, shader_source)
	gl.glCompileShader(shader_id)

	if gl.glGetShaderiv(shader_id, GL_COMPILE_STATUS) != GL_TRUE:
		info = gl.glGetShaderInfoLog(shader_id)
		gl.glDeleteShader(shader_id)
		raise RuntimeError('Shader compilation failed: {}'.format(info))

	return shader_id

def load_program(vertex_shader_source, fragment_shader_source):
	program_id = gl.glCreateProgram()

	vertex_shader_id = load_shader(vertex_shader_source, gl.GL_VERTEX_SHADER)
	fragment_shader_id = load_shader(fragment_shader_source, gl.GL_FRAGMENT_SHADER)

	gl.glAttachShader(program_id, vertex_shader_id)
	gl.glAttachShader(program_id, fragment_shader_id)

	gl.glLinkProgram(program_id)

	if glGetProgramiv(program_id, GL_LINK_STATUS) != GL_TRUE:
		glDeleteProgram(program_id)
		glDeleteShader(vertex_shader_id)
		glDeleteShader(fragment_shader_id)
		info = glGetProgramInfoLog(program_id)
		raise RuntimeError('Error linking program: {}'.format(info))

	return program_id

def render():
	glClear(GL_COLOR_BUFFER_BIT)

	program_id = load_program(vertex, fragment)

	# Lets create our Vertex Buffer objects - these are the buffers
	# that will contain our per vertex data
	vbo_id = glGenBuffers(2)

	# Bind a buffer before we can use it
	glBindBuffer(GL_ARRAY_BUFFER, vbo_id[0])

	# Now go ahead and fill this bound buffer with some data
	glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(vertex_data), vertex_data, GL_STATIC_DRAW)

	# Now specify how the shader program will be receiving this data
	# In this case the data from this buffer will be available in the shader as the vin_position vertex attribute
	glVertexAttribPointer(gl.glGetAttribLocation(program_id, 'vin_position'), 3, GL_FLOAT, GL_FALSE, 0, None)

	# Turn on this vertex attribute in the shader
	glEnableVertexAttribArray(0)

	# Now do the same for the other vertex buffer
	glBindBuffer(GL_ARRAY_BUFFER, vbo_id[1])
	glBufferData(GL_ARRAY_BUFFER, ArrayDatatype.arrayByteCount(color_data), color_data, GL_STATIC_DRAW)
	glVertexAttribPointer(gl.glGetAttribLocation(program_id, 'vin_color'), 3, GL_FLOAT, GL_FALSE, 0, None)
	glEnableVertexAttribArray(1)

	# Specify shader to be used
	glUseProgram(program_id)

	# Modern GL makes the draw call really simple
	# All the complexity has been pushed elsewhere
	glDrawArrays(GL_TRIANGLES, 0, 3)


def main():
	glut.glutInit(sys.argv)

	glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGB)
	glut.glutInitWindowSize(300, 300)
	glut.glutCreateWindow(b'Opengl.gl Offscreen')
	glut.glutHideWindow()

	init()
	render()

	gl.glPixelStorei(gl.GL_PACK_ALIGNMENT, 1)
	data = gl.glReadPixels(0, 0, width, height, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE)
	image = Image.frombytes('RGBA', (width, height), data)
	image.save('output.png')

	#gl.glutDisplayFunc(draw)
	#gl.glutMainLoop()

main()
