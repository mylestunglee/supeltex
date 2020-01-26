#version 330
in float angle;
in float polarity;
out vec4 colour;

float power(float base, float exponent) {
	return base == 0.0 ? 0.0 : pow(base, exponent);
}

vec4 colourise(
	float angle_centre,
	float polarity_centre,
	float angle_size,
	float polarity_size,
	float sharpness,
	float steepness,
	vec3 shade) {

	float angle_offset = abs((angle - angle_centre) / angle_size);
	float polarity_offset = abs((polarity - polarity_centre) / polarity_size);
	float dist = power(power(angle_offset, sharpness) + power(polarity_offset, sharpness), 1.0 / sharpness);
	float clamped = clamp(dist, 0.0, 1.0);
	float alpha = power(1.0 - clamped * clamped, steepness);
	return vec4(shade, alpha);
}

void main(void) {
	colour = colourise(0.2, 0.5, 0.6, 0.3, 9.0, 2.0, vec3(1.0, 0.0, 0.0));
	return;
	float pi = radians(180.0);
	float theta = (angle + pi) / (2.0 * pi);
	colour = vec4(theta, 1.0, theta, polarity);
}
    
