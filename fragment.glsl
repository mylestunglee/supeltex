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
uniform float scale;
uniform vec2 offset;
uniform vec3 shade;

float power(float base, float exponent) {
	return base == 0.0 ? 0.0 : pow(base, exponent);
}

void main(void) {

	bool inside = pow(2.0 * position.x, 2.0) + pow(position.y, 2.0) < 1.0;
	// compute patch geometry
	float angle_offset = abs((angle - angle_centre) / angle_size);
	float polarity_offset = abs((polarity - polarity_centre) / polarity_size);
	float dist = power(power(angle_offset, sharpness) + power(polarity_offset, sharpness), 1.0 / sharpness);

	vec4 patch_colour = dist < 0.0 || dist > 1.0 ? vec4(0.0, 0.0, 0.0, 0.0) : vec4(shade, 1.0);

	colour = inside ? patch_colour : vec4(1.0, 1.0, 1.0, 1.0);
}
