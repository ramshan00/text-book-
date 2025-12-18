---
title: "Gazebo & Unity Integration"
description: "Using Gazebo for physics and Unity for high-quality rendering (static guidance)"
---

# Gazebo & Unity Integration

## Gazebo (conceptual)
- Use Gazebo for deterministic physics tests.
- Document physics parameters that affect control (gravity, friction, time step).

## Unity (conceptual)
- Use Unity for visual fidelity, user studies and human-in-the-loop experiments.
- Document rendering settings and export paths for synthetic dataset generation.

## Integration Pattern
- Keep physics engine and renderer decoupled.
- Use a messaging bridge (describe message topics and synchronization strategy).
- Produce a short checklist for syncing time steps and sensor timestamps between engines.
