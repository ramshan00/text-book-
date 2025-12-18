---
title: "Digital Twins"
description: "Designing, maintaining and using digital twins for sim-to-real"
---

# Digital Twins

A digital twin is a virtual replica of a robot and its environment. Use digital twins to:
- Simulate edge cases safely.
- Generate synthetic datasets.
- Validate deployment before flashing to edge devices.

## Digital Twin Workflow (static)
1. Model the robot geometry and mass properties (URDF/Xacro).
2. Validate dynamics in the simulator using a checklist.
3. Add virtual sensors and verify data formats and timing.
4. Create synthetic datasets with labels and metadata.
5. Plan sim-to-real transfer: domain randomization parameters and weight export process.

## Documentation Tips
- Keep a versioned record of the digital twin model.
- Store configuration parameters with clear comments for reproducibility.
