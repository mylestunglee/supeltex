#version 330
in vec3 vin_position;

void main(void)
{
    gl_Position = vec4(vin_position, 1.0);
}

