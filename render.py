import OpenGL.GL as gl
import OpenGL.GLUT as glut

from PIL import Image

BUFFER_RESOLUTION = 512


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
        vertex_shader_id = load_shader(
            vertex_shader_file.read(), gl.GL_VERTEX_SHADER)

    with open(fragment_shader_filename) as fragment_shader_file:
        fragment_shader_id = load_shader(
            fragment_shader_file.read(), gl.GL_FRAGMENT_SHADER)

    gl.glAttachShader(program_id, vertex_shader_id)
    gl.glAttachShader(program_id, fragment_shader_id)

    gl.glLinkProgram(program_id)

    if gl.glGetProgramiv(program_id, gl.GL_LINK_STATUS) != gl.GL_TRUE:
        gl.glDeleteProgram(program_id)
        gl.glDeleteShader(vertex_shader_id)
        gl.glDeleteShader(fragment_shader_id)
        info = gl.glGetProgramInfoLog(program_id)
        raise RuntimeError('Error linking program: {}'.format(info))

    return (program_id, vertex_shader_id, fragment_shader_id)


def load_vbo(geometry):
    vbo_id = gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo_id)
    gl.glBufferData(
        gl.GL_ARRAY_BUFFER,
        gl.ArrayDatatype.arrayByteCount(geometry),
        geometry,
        gl.GL_STATIC_DRAW)
    return vbo_id


def unload_vbo(vbo_id):
    gl.glDeleteBuffers(vbo_id, 1)


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


def unlink_shaders(program_id, vertex_shader_id, fragment_shader_id):
    gl.glDisableVertexAttribArray(gl.glGetAttribLocation(program_id, 'vertex'))
    gl.glDeleteProgram(program_id)
    gl.glDeleteShader(vertex_shader_id)
    gl.glDeleteShader(fragment_shader_id)


def set_uniforms(program_id, patch):
    for key in patch:
        value = patch[key]
        loc = gl.glGetUniformLocation(program_id, key)

        if loc < 0:
            raise RuntimeError('Invalid uniform name: {}'.format(key))

        if isinstance(value, float):
            gl.glUniform1f(loc, value)
        elif isinstance(value, tuple):
            if len(value) == 2:
                gl.glUniform2f(loc, *value)
            elif len(value) == 3:
                gl.glUniform3f(loc, *value)
            elif len(value) == 4:
                gl.glUniform4f(loc, *value)
            else:
                raise RuntimeError(
                    'Tuple too many dimensions: {}'.format(value))
        else:
            raise RuntimeError('Invalid uniform {}: {}'.format(key, value))


def opengl_render(geometry, patch):
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    (program_id, vertex_shader_id, fragment_shader_id) = load_program(
        'vertex.glsl', 'fragment.glsl')
    vbo_id = load_vbo(geometry)
    link_shaders(program_id)
    set_uniforms(program_id, patch)
    gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, geometry.size // 4)
    unlink_shaders(program_id, vertex_shader_id, fragment_shader_id)
    unload_vbo(vbo_id)


def init():
    glut.glutInit()

    glut.glutInitDisplayMode(glut.GLUT_ALPHA)
    glut.glutInitWindowSize(BUFFER_RESOLUTION, BUFFER_RESOLUTION)

    glut.glutCreateWindow('')

    gl.glDepthMask(gl.GL_FALSE)
    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)


def render(geometry_patches, output_filename):
    for geometry, patch in geometry_patches:
        opengl_render(geometry, patch)

    gl.glPixelStorei(gl.GL_PACK_ALIGNMENT, 1)
    data = gl.glReadPixels(0, 0, BUFFER_RESOLUTION,
                           BUFFER_RESOLUTION, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE)

    image = Image.frombytes(
        'RGBA', (BUFFER_RESOLUTION, BUFFER_RESOLUTION), data)
    image.save(output_filename)
