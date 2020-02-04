#version 330
in vec4 vertex;
out float angle;
out float polarity;
out vec2 position;

void main(void)
{
    gl_Position = vec4(vertex.xy, 0.0, 1.0);
    angle = vertex.z;
    polarity = vertex.w;
    position = vertex.xy;
}

