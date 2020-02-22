#version 330
in vec4 vertex;
uniform float scale;
uniform vec2 offset;
out float angle;
out float polarity;
out vec2 position;

void main(void)
{
    vec2 projected = vertex.xy * scale + offset;
    gl_Position = vec4(projected, 0.0, 1.0);
    angle = vertex.z;
    polarity = vertex.w;
    position = vertex.xy;
}

