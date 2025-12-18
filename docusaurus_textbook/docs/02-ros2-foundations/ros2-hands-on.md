---
title: "ROS 2 Core Concepts"
description: "Nodes, Topics, Services, Actions, DDS — Deep and Practical Understanding"
---

# ROS 2 Core Concepts

This chapter expands on the core concepts introduced in Module 1, with diagrams, patterns and guidelines.

## Nodes
- Single responsibility principle: each node handles one logical function.
- Lifecycle management: plan startup/shutdown and error recovery.

## Topics
- Use topics for streaming sensor data and state information.
- Define topic naming conventions and message rate expectations.

## Services
- Use services for calibration calls, configuration changes, or short one-off queries.

## Actions
- Use actions for missions or tasks that take time and need feedback (navigation, manipulation).

## QoS Guidelines
- Sensors (high-frequency) may use BEST_EFFORT for performance-sensitive streams.
- Critical control channels should use RELIABLE and appropriate deadlines.
- Document QoS choices in design docs for each topic.

## Executors & Scheduling
- Choose executor strategy (single-threaded, multi-threaded) based on concurrency needs.
- Plan for real-time requirements: isolate critical threads and prioritize them.

## Tools & Workflow
- Use topic/service/action naming conventions and a shared data dictionary for teams.
- Maintain testing procedures for message validation and replay.

## Diagrams & Patterns
- Include system-level diagrams to show flow between perception -> planner -> controller.
- Use sequence diagrams for action lifecycles and failure modes.

