#version 330
in float angle;
in float polarity;
out vec4 colour;

void main(void)
{
    colour = vec4(angle, polarity, 1.0, 1.0);
}
    
