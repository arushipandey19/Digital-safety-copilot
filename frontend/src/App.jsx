import React, { useEffect, useState } from "react";

import InputTabs from "./components/InputTabs";
import RiskCard from "./components/RiskCard";
import IndicatorList from "./components/IndicatorList";
import EvidenceChain from "./components/EvidenceChain";
import SafeAction from "./components/SafeAction";
import WhyPanel from "./components/WhyPanel";

import { analyzeInput } from "./services/api";

/* =========================================================
   NAVBAR
========================================================= */

function Navbar({ darkMode, setDarkMode }) {
  return (
    <nav className="navbar">
      <div className="nav-logo">
        Digital Safety Copilot
      </div>

      <div className="nav-links">
        <a href="#features">Features</a>
        <a href="#overview">Overview</a>
        <a href="#workflow">Workflow</a>
        <a href="#about">About</a>
        <a href="#docs">Documentation</a>

        <button
          type="button"
          className="theme-toggle"
          onClick={() => setDarkMode((prev) => !prev)}
          aria-label="Toggle dark and light mode"
          title="Toggle theme"
        >
          {darkMode ? "☀" : "☾"}
        </button>
      </div>
    </nav>
  );
}

/* =========================================================
   HERO
========================================================= */

function Hero() {
  return (
    <section className="hero-section">
      <div className="hero-tag">
        AI • SECURITY • EXPLAINABILITY
      </div>

      <h1 className="hero-title">
        Digital Safety
        <span> Copilot</span>
      </h1>

      <p className="hero-description">
        From detection to decision.
      </p>

      <p className="hero-subtitle">
        Analyze suspicious messages, URLs and screenshots —
        then understand the evidence and choose a safer next step.
      </p>

      <a href="#analyzer" className="hero-button">
        Analyze Something
      </a>
    </section>
  );
}

/* =========================================================
   VIDEO / AWARENESS SECTION
========================================================= */

function VideoSection() {
  return (
    <section className="video-section" id="about">
      <div className="section-heading">
        <span>STAY AWARE</span>
        <h2>Think before you trust.</h2>
      </div>

      <div className="video-card">
        <div className="video-placeholder">
          <div className="video-play">▶</div>

          <div>
            <h3>Digital Fraud Awareness</h3>
            <p>
              Suspicious messages often create urgency,
              ask for sensitive information, or redirect
              you to unexpected websites.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}

/* =========================================================
   OVERVIEW
========================================================= */

function OverviewSection() {
  return (
    <section className="overview-section" id="overview">
      <div className="overview-left">
        <div className="section-label">
          WHY DIGITAL SAFETY COPILOT
        </div>

        <h2>
          Detection is only
          <span> half the story.</span>
        </h2>

        <p>
          Most security tools tell you whether something looks
          suspicious. Digital Safety Copilot goes one step further:
          it explains the evidence and tells you what to do next.
        </p>
      </div>

      <div className="overview-right">
        <div className="overview-card">
          <span>01</span>
          <h3>Detect</h3>
          <p>
            Analyze language, URLs, screenshots and
            multiple security signals.
          </p>
        </div>

        <div className="overview-card">
          <span>02</span>
          <h3>Explain</h3>
          <p>
            Connect the evidence into a clear,
            human-readable reasoning chain.
          </p>
        </div>

        <div className="overview-card">
          <span>03</span>
          <h3>Guide</h3>
          <p>
            Give the user a safer next action instead
            of simply showing a risk score.
          </p>
        </div>
      </div>
    </section>
  );
}

/* =========================================================
   COMPONENT SHOWCASE
========================================================= */

function ComponentShowcase() {
  const [active, setActive] = useState(0);

  const components = [
    {
      number: "01",
      title: "Multimodal Input",
      description:
        "Accept suspicious messages, URLs and screenshots from one interface."
    },
    {
      number: "02",
      title: "Evidence Extraction",
      description:
        "Extract OCR text, URLs, QR payloads and important entities."
    },
    {
      number: "03",
      title: "Multi-Signal Detection",
      description:
        "Combine security rules, ML signals, URL analysis and vision."
    },
    {
      number: "04",
      title: "Evidence Reasoning",
      description:
        "Connect all available signals and explain why the content is risky."
    }
  ];

  const next = () => {
    setActive((prev) =>
      prev === components.length - 1 ? 0 : prev + 1
    );
  };

  const previous = () => {
    setActive((prev) =>
      prev === 0 ? components.length - 1 : prev - 1
    );
  };

  return (
    <section className="component-showcase" id="features">
      <div className="section-heading">
        <span>CORE CAPABILITIES</span>

        <h2>
          Signals become
          <span> evidence.</span>
        </h2>

        <p>
          Each stage contributes a meaningful signal to the final
          safety assessment.
        </p>
      </div>

      <div className="component-stage">
        <button
          type="button"
          className="carousel-arrow left-arrow"
          onClick={previous}
          aria-label="Previous component"
        >
          ←
        </button>

        <div className="component-cards">
          {components.map((item, index) => {
            const distance = Math.abs(index - active);

            let cardClass = "component-card";

            if (index === active) {
              cardClass += " active";
            } else if (distance === 1) {
              cardClass += " near";
            } else {
              cardClass += " far";
            }

            return (
              <div className={cardClass} key={item.number}>
                <div className="component-number">
                  {item.number}
                </div>

                <h3>{item.title}</h3>

                <p>{item.description}</p>
              </div>
            );
          })}
        </div>

        <button
          type="button"
          className="carousel-arrow right-arrow"
          onClick={next}
          aria-label="Next component"
        >
          →
        </button>
      </div>

      <div className="component-controls">
        <span>
          {String(active + 1).padStart(2, "0")} /{" "}
          {String(components.length).padStart(2, "0")}
        </span>

        <span>
          ↑ EXPLORE
        </span>

        <span>
          SCROLL ↓
        </span>
      </div>
    </section>
  );
}

/* =========================================================
   WORKFLOW
   NOTE: SYSTEM ARCHITECTURE SECTION INTENTIONALLY REMOVED
========================================================= */

function WorkflowSection() {
  const workflow = [
    {
      number: "01",
      title: "Receive",
      text: "User provides a suspicious message, URL or screenshot."
    },
    {
      number: "02",
      title: "Extract",
      text: "OCR, QR decoding, URL extraction and entity detection prepare the evidence."
    },
    {
      number: "03",
      title: "Detect",
      text: "Rules, ML, URL intelligence and visual analysis generate security signals."
    },
    {
      number: "04",
      title: "Reason",
      text: "The reasoning layer connects the available evidence."
    },
    {
      number: "05",
      title: "Act",
      text: "The user receives an understandable explanation and a safer next action."
    }
  ];

  return (
    <section className="workflow-section" id="workflow">
      <div className="section-heading">
        <span>WORKFLOW</span>

        <h2>
          From input to
          <span> safer action.</span>
        </h2>
      </div>

      <div className="workflow-list">
        {workflow.map((item) => (
          <div className="workflow-item" key={item.number}>
            <div className="workflow-number">
              {item.number}
            </div>

            <div className="workflow-content">
              <h3>{item.title}</h3>
              <p>{item.text}</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

/* =========================================================
   SIGNATURE FEATURES
========================================================= */

function SignatureFeatures() {
  return (
    <section className="signature-section">
      <div className="section-heading">
        <span>SIGNATURE FEATURES</span>

        <h2>
          More than a
          <span> fraud score.</span>
        </h2>
      </div>

      <div className="signature-grid">
        <div className="signature-card">
          <div className="signature-icon">◎</div>

          <h3>Evidence Chain</h3>

          <p>
            See exactly which signals contributed to the
            safety decision.
          </p>
        </div>

        <div className="signature-card">
          <div className="signature-icon">↔</div>

          <h3>Cross-Modal Reasoning</h3>

          <p>
            Compare text, URL, QR and visual evidence
            instead of examining them independently.
          </p>
        </div>

        <div className="signature-card">
          <div className="signature-icon">✓</div>

          <h3>Verify Independently</h3>

          <p>
            Get a safer path to verify the claim without
            trusting the suspicious message itself.
          </p>
        </div>
      </div>
    </section>
  );
}

/* =========================================================
   ANALYZER
========================================================= */

function Analyzer() {
  const [type, setType] = useState("text");
  const [text, setText] = useState("");
  const [url, setUrl] = useState("");
  const [file, setFile] = useState(null);

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleAnalyze() {
    setError("");
    setResult(null);
    setLoading(true);

    try {
      const response = await analyzeInput({
        type,
        text,
        url,
        file
      });

      setResult(response);
    } catch (err) {
      setError(
        err?.message || "Something went wrong while analyzing."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="analyzer-section" id="analyzer">
      <div className="section-heading">
        <span>TRY IT</span>

        <h2>
          Analyze something
          <span> suspicious.</span>
        </h2>

        <p>
          Paste a message, enter a URL or upload a screenshot.
        </p>
      </div>

      <div className="panel input-panel">
        <div className="section-title">
          What did you receive?
        </div>

        <InputTabs
          value={type}
          onChange={setType}
        />

        {type === "text" && (
          <textarea
            value={text}
            onChange={(event) => setText(event.target.value)}
            placeholder="Paste the suspicious message or email..."
          />
        )}

        {type === "url" && (
          <input
            className="text-input"
            type="text"
            value={url}
            onChange={(event) => setUrl(event.target.value)}
            placeholder="https://example.com/login"
          />
        )}

        {type === "screenshot" && (
          <div className="upload">
            <input
              type="file"
              accept="image/*"
              onChange={(event) =>
                setFile(
                  event.target.files?.[0] || null
                )
              }
            />

            <div className="muted">
              {file
                ? file.name
                : "Upload a screenshot of the message"}
            </div>
          </div>
        )}

        <button
          type="button"
          className="primary"
          onClick={handleAnalyze}
          disabled={loading}
        >
          {loading
            ? "Analyzing..."
            : "Analyze Safety"}
        </button>

        <div className="privacy-note">
          Your input is user-provided. No direct WhatsApp
          access is required.
        </div>

        {error && (
          <div className="error">
            {error}
          </div>
        )}
      </div>

      {result && (
        <section className="results">
          <RiskCard risk={result.risk} />

          <div className="two-col">
            <IndicatorList
              indicators={
                result.security_evidence?.indicators || []
              }
              mlPrediction={
                result.security_evidence?.ml_prediction
              }
            />

            <SafeAction
              actions={
                result.risk?.safe_actions || []
              }
            />
          </div>

          <WhyPanel
            explanation={
              result.risk?.explanation || ""
            }
          />

          {result.extracted?.qr_codes?.length > 0 && (
            <section className="panel">
              <div className="section-title">
                📱 QR Content Detected
              </div>

              {result.extracted.qr_codes.map((qr) => (
                <div
                  className="qr-row"
                  key={`${qr.index}-${qr.decoded_value}`}
                >
                  <div className="qr-title">
                    QR #{qr.index} ·{" "}
                    {String(
                      qr.content_type || ""
                    ).toUpperCase()}
                  </div>

                  <div className="muted qr-payload">
                    {qr.decoded_value}
                  </div>
                </div>
              ))}
            </section>
          )}

          {result.security_evidence?.visual_analysis
            ?.available && (
            <section className="panel">
              <div className="section-title">
                👁 Vision Evidence
              </div>

              {result.security_evidence.visual_analysis
                .visible_brand_or_organization && (
                <div className="visual-item">
                  <strong>
                    Visible organization/branding:
                  </strong>{" "}
                  {
                    result.security_evidence
                      .visual_analysis
                      .visible_brand_or_organization
                  }
                </div>
              )}

              <div className="visual-grid">
                <span>
                  Login / Verification:{" "}
                  {result.security_evidence.visual_analysis
                    .login_or_verification_ui
                    ? "Yes"
                    : "No"}
                </span>

                <span>
                  Payment Prompt:{" "}
                  {result.security_evidence.visual_analysis
                    .payment_prompt
                    ? "Yes"
                    : "No"}
                </span>

                <span>
                  QR Present:{" "}
                  {result.security_evidence.visual_analysis
                    .qr_present
                    ? "Yes"
                    : "No"}
                </span>

                <span>
                  Embedded Image:{" "}
                  {result.security_evidence.visual_analysis
                    .embedded_image_present
                    ? "Yes"
                    : "No"}
                </span>
              </div>
            </section>
          )}

          <EvidenceChain
            chain={result.evidence_chain || []}
          />
        </section>
      )}
    </section>
  );
}

/* =========================================================
   FOOTER
========================================================= */

function Footer() {
  return (
    <footer className="footer" id="docs">
      <div>
        <strong>
          Digital Safety Copilot
        </strong>

        <p>
          Detect. Explain. Guide.
        </p>
      </div>

      <div className="footer-right">
        <span>
          AI-assisted digital safety
        </span>
      </div>
    </footer>
  );
}

/* =========================================================
   APP
========================================================= */

export default function App() {
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    document.body.classList.toggle(
      "dark-mode",
      darkMode
    );

    return () => {
      document.body.classList.remove(
        "dark-mode"
      );
    };
  }, [darkMode]);

  return (
    <div
      className={
        darkMode
          ? "app dark-app"
          : "app"
      }
    >
      <Navbar
        darkMode={darkMode}
        setDarkMode={setDarkMode}
      />

      <Hero />

      <VideoSection />

      <OverviewSection />

      <ComponentShowcase />

      {/* System Architecture section removed */}

      <WorkflowSection />

      <SignatureFeatures />

      <Analyzer />

      <Footer />
    </div>
  );
}