#version 330
in float angle;
in float polarity;
out vec4 colour;

void main(void)
{
	float pi = radians(180.0);

    colour = vec4((angle + pi) / (2.0 * pi), polarity, 1.0, 1.0);
}
    
