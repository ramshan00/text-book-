---
title: "Module 1: The Robotic Nervous System - ROS 2"
description: "Mastering the middleware that makes modern humanoid robots think and move"
module: 1
duration: "6-8 hours"
prerequisites: "Python basics, Linux command line"
objectives:
  - Understand why ROS 2 is the de-facto robotic operating system
  - Master nodes, topics, services, and actions conceptually
  - Learn how AI agents map to ROS 2 concepts
  - Model any humanoid robot using URDF/Xacro (conceptual guidance)
---

# Module 1: The Robotic Nervous System - ROS 2

## Decoding the Future of Humanoid Robotics

Welcome, future architects of physical intelligence! In this module we learn the **concepts and architecture** of ROS 2 and how it serves as the central framework for humanoid robotics.

---

## Learning Outcomes

Upon completing this module, you will be able to:

* Explain the architectural differences and advantages of ROS 2 over ROS 1.
* Describe nodes, topics, services, and actions and when to use each.
* Map AI agent components (perception, planning, control) onto ROS 2 architecture.
* Outline URDF/Xacro modeling workflow and visualization with RViz2.
* Apply debugging and best-practice approaches conceptually in a development process.

---

## Why ROS 2 Matters

Key points:
- Distributed, reliable communication via DDS.
- Improved real-time support and QoS control.
- Language-agnostic ecosystem allowing Python/C++ interop.
- Strong community and industry adoption.

---

## Core Concepts (High Level)

### Nodes, Topics, Publishers/Subscribers
Nodes are independent processes. Topics are named channels for asynchronous streaming data. Publishers send, subscribers receive.

### Services vs Actions
Services: synchronous request/response for short operations.  
Actions: long-running goals with feedback and cancellation.

### DDS and QoS
DDS provides discovery and QoS (reliability, durability, deadline) that determine communication behavior.

### Real-time & Safety
ROS 2 supports real-time patterns but real hard-real-time requires OS/kernel configuration and careful system design.

---

## Hands-on (Non-executable, Conceptual Steps)

1. **Workspace planning**: create a workspace layout with one package per functional area (perception, planning, control).
2. **Node design**: list required nodes, their responsibilities, and the topics/services/actions they use.
3. **Message design**: define the high-level messages and expected fields (names and semantics).
4. **Simulation test plan**: design test cases to validate message flows and failure scenarios.
5. **Debug checklist**: common checks (QoS mismatch, message size, stalled executors).

> Note: This page intentionally contains conceptual steps only. Implementation code lives in example repos (link in Appendix → Resources) if you decide to add runnable examples later.
