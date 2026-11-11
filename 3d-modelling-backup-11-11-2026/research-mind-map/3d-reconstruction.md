# 3D Reconstruction

Nvidia glossary: https://www.nvidia.com/en-us/glossary/3d-reconstruction/

## Summary of the Nvidia glossary

- 3D reconstruction is the process of generating digital 3D representations of scenes and objects from inputs like images, video, or other sensor data.
- Traditional methods rely on geometry-based algorithms to estimate 3D structure from multi-view images or sensor data. Modern methods use neural networks that learn 3D geometry and appearance directly from images, videos, or other sensor inputs.
- Modern methods often learn to estimate camera poses from overlapping 2D images, a process called Structure from Motion (SfM):
    - https://www.mathworks.com/help/vision/ug/what-is-structure-from-motion.html
    - https://en.wikipedia.org/wiki/Structure_from_motion

Methods:
- NeRF: an MLP maps 3D coordinates and viewing directions to color and density. Quality degrades in a smooth, predictable way for views further from the captured data. Training and rendering are slow.
- 3D Gaussian Splatting (3DGS): models the scene as Gaussian ellipsoids. It enables faster training and real-time rendering. The Gaussians can be converted into dense point clouds. Views along the original trajectories are sharp, with potential quality degradation for novel views.
- 3D Gaussian Ray Tracing (3DGRT, Nvidia Research): adds ray tracing to 3DGS for reflections, refractions and shadows. Higher computational cost; suited where rendering quality outweighs performance. Link: https://gaussiantracer.github.io/
- 3D Gaussian Unscented Transform (3DGUT, Nvidia Research): handles nonlinear camera models such as fisheye lenses and rolling shutters while preserving real-time performance. A middle ground between 3DGS and 3DGRT. The code of 3DGRT and 3DGUT is open source. Link: https://research.nvidia.com/labs/toronto-ai/3DGUT/

Digital twin workflow:
1. Data collection: multi-view images or video, supplemented with lidar or depth. Sensor poses must be known or estimated with structure-from-motion (SfM) techniques like COLMAP. Ensure high-quality data for accurate reconstruction.
2. Neural reconstruction: a NeRF or 3D Gaussians are optimized to model scene geometry and appearance. Segmentation and inpainting remove dynamic elements (e.g., pedestrians) to create static environments. The output is a learned representation of the scene.
3. Rendering and simulation: the model generates sensor outputs from arbitrary viewpoints. Robots can be added as simulated agents.

Use cases:
- Industrial digital twins: highly accurate 3D models of facilities for simulation, layout optimization, predictive maintenance planning and personnel training.
- Robotics simulation: digital twins of warehouses, factory floors and homes for training and testing robots, e.g. in Nvidia Isaac Sim.
- Autonomous vehicle simulation: recorded drives become interactive environments for closed-loop testing.
