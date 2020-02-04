#version 330
in vec2 position;
in float angle;
in float polarity;
out vec4 colour;

uniform float angle_centre;
uniform float polarity_centre;
uniform float angle_size;
uniform float polarity_size;
uniform float sharpness;
uniform vec3 shade;

float power(float base, float exponent) {
	return base == 0.0 ? 0.0 : pow(base, exponent);
}

void main(void) {
	float angle_offset = abs((angle - angle_centre) / angle_size);
	float polarity_offset = abs((polarity - polarity_centre) / polarity_size);
	float dist = power(power(angle_offset, sharpness) + power(polarity_offset, sharpness), 1.0 / sharpness);
	colour = dist < 0.0 || dist > 1.0 ? vec4(0.0, 0.0, 0.0, 0.0) : vec4(shade, 1.0);
}
    
