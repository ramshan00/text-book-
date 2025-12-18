import React from "react";
import Layout from "@theme/Layout";
import Link from "@docusaurus/Link";

export default function Home() {
  return (
    <Layout
      title="Physical AI & Humanoid Robotics Textbook"
      description="Complete AI-Native textbook for mastering robotics, humanoids, ROS2, VLA systems, and digital twins."
    >
      <main className="tech-grid">
        {/* HERO SECTION */}
        <header className="hero">
          <div className="container" style={{ textAlign: "center", position: "relative", zIndex: 1 }}>
            <h1 className="hero__title">
              Physical AI & <br />Humanoid Robotics
            </h1>
            <p className="hero__subtitle" style={{ fontSize: "1.25rem", maxWidth: "800px", margin: "0 auto 2.5rem" }}>
              [ LOG_SYSTEM_RECOVERY: SUCCESS ]<br />
              A practical learning system for the future of intelligent machines.
            </p>

            <div style={{ marginTop: "40px" }}>
              <Link
                className="button-premium"
                to="/docs/introduction/intro"
              >
                Access Knowledge Base _
              </Link>
            </div>
          </div>
        </header>

        {/* ABOUT SECTION */}
        <section style={{ padding: "100px 20px", maxWidth: "1000px", margin: "0 auto" }}>
          <h2 className="section-title">
            Curriculum Overview
          </h2>
          <p style={{ fontSize: "1.1rem", lineHeight: "1.8", color: "var(--text-dim)", textAlign: "center" }}>
            This AI-native engineering curriculum covers physical AI, humanoid systems,
            embodied intelligence, and Vision-Language-Action (VLA) pipelines.
            Step by step, construct the future of physical embodiment.
          </p>
        </section>

        {/* MODULE CARDS */}
        <section style={{ padding: "80px 20px", background: "rgba(0,0,0,0.3)" }}>
          <div className="container">
            <h2 className="section-title">
              System Modules
            </h2>

            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))",
                gap: "30px",
                maxWidth: "1200px",
                margin: "0 auto",
              }}
            >
              <ModuleCard
                title="01 // ROS 2 Foundations"
                text="Master the nervous system of modern robots. Topics, services, actions, and real-time QoS orchestration."
                link="/docs/ros2-foundations/module-1-ros2"
              />
              <ModuleCard
                title="02 // Sim & Digital Twins"
                text="Gazebo, Unity Robotics, and Isaac Sim. Train robots safely in high-fidelity synthetic environments."
                link="/docs/simulation/module-2-simulation"
              />
              <ModuleCard
                title="03 // Hardware Foundations"
                text="Actuation, sensory perception, and embedded low-level control for humanoid physical embodiment."
                link="/docs/hardware-basics/module-3-hardware"
              />
              <ModuleCard
                title="04 // VLA Systems"
                text="Vision-Language-Action. LLM-driven command systems and embodied action planners."
                link="/docs/vla-systems/module-4-vla-foundations"
              />
              <ModuleCard
                title="05 // Advanced AI & Control"
                text="Reinforcement learning, motion planning, and trajectory optimization for complex task execution."
                link="/docs/advanced-ai-control/module-5-advanced-ai"
              />
              <ModuleCard
                title="06 // Humanoid Design"
                text="End-to-end humanoid creation: mechanics, kinematics, and AI-driven dynamic movement."
                link="/docs/humanoid-design/module-6-humanoid-design"
              />
            </div>
          </div>
        </section>

        {/* FEATURES SECTION */}
        <section style={{ padding: "120px 20px" }}>
          <div className="container">
            <div
              style={{
                maxWidth: "1100px",
                margin: "0 auto",
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))",
                gap: "40px",
              }}
            >
              <FeatureBox
                title="AI-NATIVE"
                text="Built for the modern robotics era where LLMs and Embodied AI are fundamental."
              />
              <FeatureBox
                title="HANDS-ON"
                text="Practical labs, code examples, and simulation workflows in every module."
              />
              <FeatureBox
                title="INDUSTRY-SCALE"
                text="Curriculum inspired by the tech behind Tesla Bot, Figure, and Unitree humanoids."
              />
            </div>
          </div>
        </section>

        {/* CTA SECTION */}
        <section
          style={{
            padding: "120px 20px",
            background: "linear-gradient(to bottom, transparent, var(--ifm-color-primary-darkest))",
            textAlign: "center",
          }}
        >
          <div className="container">
            <h2 style={{ fontSize: "3rem", fontWeight: "800", marginBottom: "2rem" }}>
              INITIATE NEURAL LINK
            </h2>
            <Link
              className="button-premium"
              to="/docs/introduction/intro"
              style={{ padding: "20px 50px" }}
            >
              Start Core Loading _
            </Link>
          </div>
        </section>
      </main>
    </Layout>
  );
}

function ModuleCard({ title, text, link }) {
  return (
    <div className="card-module">
      <h3 className="card-title">{title}</h3>
      <p className="card-text">{text}</p>
      <div style={{ marginTop: "auto" }}>
        <Link className="button-premium" to={link} style={{ display: "block", textAlign: "center", padding: "8px" }}>
          Examine →
        </Link>
      </div>
    </div>
  );
}

function FeatureBox({ title, text }) {
  return (
    <div className="feature-box">
      <h3>{title}</h3>
      <p style={{ color: "var(--text-dim)", lineHeight: "1.6", margin: 0 }}>{text}</p>
    </div>
  );
}
