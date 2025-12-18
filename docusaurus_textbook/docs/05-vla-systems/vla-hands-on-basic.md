---
title: "Hands-On: Basic VLA Agent (Design Only)"
description: "A static, copy-paste friendly lab plan for a basic VLA interaction using simulated perception and text commands"
---

# Hands-On: Basic VLA Agent (Design & Lab Plan)

This is a **lab plan** (no code). Use it as a handout to run a supervised demo or to implement later in a separate repo.

## Goal
Robot receives a high-level text command (e.g., "move to the red block"), identifies the target via perception, generates a plan and issues motion commands. All steps are described below conceptually.

## Lab Steps (textual)
1. **Define inputs & outputs**:  
   - Input: natural language command text.  
   - Perception: list of detected objects and positions.  
   - Output: motion intent / velocity commands.

2. **Language stage (design)**:  
   - Outline how to parse commands into (action, object) pairs.  
   - Specify ambiguity-handling rules and confirmation policy.

3. **Perception stage (design)**:  
   - List sensors used and the expected data formats.  
   - Describe an object table format: `name`, `position_x`, `position_y`, `confidence`.

4. **Planner stage (design)**:  
   - Define logic: select target object → compute relative offset → generate simple motion primitive.

5. **Execution & Safety (design)**:  
   - State checks before executing: path clear, joint limits, timeouts.
   - Define safe-stop behavior.

6. **Evaluation**:  
   - Success criteria (arrive within 0.2 m), timeouts, number of re-plans.

## Deliverable (for students)
- A one-page design spec describing each stage, message schemas, and test cases.
