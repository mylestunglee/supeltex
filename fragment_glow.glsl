#version 330
in float angle;
in float polarity;
out vec4 colour;

void main(void)
{
	float pi = radians(180.0);
	float theta = (angle + pi) / (2.0 * pi);
    colour = vec4(1.0, theta, theta, polarity);
}
    
