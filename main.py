import render
import numpy as np

vertex_data = np.array([0.75, 0.75, 0.0, 0.0,
	0.75, -0.75, 1.0, 0.0,
	-0.75, -0.75, 0.0, 1.0], dtype=np.float32)

render.render(400, 300, vertex_data, 'output.png')
