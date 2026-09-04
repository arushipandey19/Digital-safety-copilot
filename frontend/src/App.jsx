import React, { useEffect, useRef, useState } from "react";
import { analyzeInput } from "./services/api";

const DEMO_TEXT =
  "URGENT! Your SBI account will be blocked. Verify your OTP immediately at https://sbi-secure-login.xyz";
const DEMO_URL = "https://sbi-secure-login.xyz";

const components = [
  {
    id: "input",
    number: "01",
    title: "Multimodal Input",
    short: "Message • URL • Screenshot",
    description:
      "Users can provide suspicious content in the format they already have. No direct WhatsApp access is required.",
    points: ["Paste a message", "Check a URL", "Upload a screenshot"],
  },
  {
    id: "extract",
    number: "02",
    title: "Evidence Extraction",
    short: "OCR • QR • Entities",
    description:
      "The system extracts visible text, URLs, claimed organizations and QR payloads before deeper analysis begins.",
    points: ["OCR text extraction", "QR decoding", "Organization detection"],
  },
  {
    id: "detect",
    number: "03",
    title: "Multi-Signal Detection",
    short: "Rules • ML • Vision",
    description:
      "Deterministic security rules, ML language signals and visual observations create a richer evidence set.",
    points: ["Domain checks", "Phishing-like language", "Visual cues"],
  },
  {
    id: "reason",
    number: "04",
    title: "Evidence Reasoning",
    short: "Cross-modal AI",
    description:
      "The reasoning layer connects independent signals instead of relying on one black-box prediction.",
    points: [
      "Claim vs evidence",
      "Cross-modal consistency",
      "Explainable reasoning",
    ],
  },
];

const workflow = [
  {
    number: "01",
    title: "Upload or Paste",
    text: "Share the suspicious message, URL or screenshot.",
  },
  {
    number: "02",
    title: "Extract",
    text: "OCR, URL parsing, QR decoding and entity extraction prepare the evidence.",
  },
  {
    number: "03",
    title: "Analyze",
    text: "Rules, ML, URL checks and visual analysis inspect independent signals.",
  },
  {
    number: "04",
    title: "Correlate",
    text: "Cross-modal reasoning checks whether the claim matches the evidence.",
  },
  {
    number: "05",
    title: "Explain",
    text: "The system turns technical findings into an understandable explanation.",
  },
  {
    number: "06",
    title: "Act Safely",
    text: "Users get a practical next step and an independent verification path.",
  },
];

function Icon({ type }) {
  const map = {
    shield: "◈",
    link: "↗",
    image: "▧",
    graph: "⌁",
    search: "⌕",
    eye: "◉",
    check: "✓",
    book: "▤",
    help: "?",
  };

  return <span className={`icon icon-${type}`}>{map[type] || "•"}</span>;
}

function Navbar({ onAnalyze, darkMode, setDarkMode }) {
  return (
    <header className="navbar">
      <a className="brand" href="#top" aria-label="Digital Safety Copilot home">
        <span className="brand-mark">
          <Icon type="shield" />
        </span>
        <span>
          <strong>Digital Safety</strong> <small>Copilot</small>
        </span>
      </a>

      <nav className="nav-links" aria-label="Main navigation">
        <a href="#features">Features</a>
        <a href="#architecture">Architecture</a>
        <a href="#workflow">How It Works</a>
        <a href="#about">About</a>
        <a href="#help">Help & Feedback</a>
        <a href="#docs">Documentation</a>
      </nav>

      <div className="nav-actions">
        <button
          className="theme-toggle"
          type="button"
          onClick={() => setDarkMode((current) => !current)}
          aria-label={
            darkMode ? "Switch to light mode" : "Switch to dark mode"
          }
          title={darkMode ? "Light mode" : "Dark mode"}
        >
          <span className={`theme-option ${!darkMode ? "active" : ""}`}>
            ☀️
          </span>
          <span className={`theme-option ${darkMode ? "active" : ""}`}>
            🌙
          </span>
        </button>

        <button className="login-button" type="button">
          Log in
        </button>

        <button className="nav-cta" type="button" onClick={onAnalyze}>
          Analyze Now
        </button>
      </div>
    </header>
  );
}

function EvidenceMockup() {
  return (
    <div className="evidence-mockup" aria-label="Evidence chain preview">
      <div className="mock-header">
        <div>
          <span className="mock-kicker">LIVE ANALYSIS</span>
          <strong>Evidence Chain</strong>
        </div>
        <span className="mock-status">● analyzing</span>
      </div>

      <div className="mock-message">
        <span className="message-tag">MESSAGE</span>
        <p>“Your account will be blocked. Verify now.”</p>
      </div>

      <div className="mock-chain">
        <div className="chain-node good">
          <span>CLAIM</span>
          <strong>SBI Bank</strong>
        </div>

        <div className="connector" />

        <div className="chain-node warn">
          <span>URL</span>
          <strong>sbi-secure-login.xyz</strong>
        </div>

        <div className="connector danger-line" />

        <div className="chain-node danger">
          <span>MISMATCH</span>
          <strong>Domain not verified</strong>
        </div>
      </div>

      <div className="mock-signals">
        <div>
          <span className="signal-dot danger-dot" /> Urgency
        </div>
        <div>
          <span className="signal-dot danger-dot" /> OTP request
        </div>
        <div>
          <span className="signal-dot warn-dot" /> ML phishing signal
        </div>
      </div>

      <div className="mock-result">
        <div>
          <small>RISK ASSESSMENT</small>
          <strong>HIGH RISK</strong>
        </div>
        <span>
          91<span>/100</span>
        </span>
      </div>
    </div>
  );
}

function Hero({ onAnalyze }) {
  return (
    <section className="hero" id="top">
      <div className="hero-copy">
        <div className="eyebrow">AI • SECURITY • EXPLAINABILITY</div>

        <h1>
          Make safer digital decisions <span>before you click.</span>
        </h1>

        <p>
          Digital Safety Copilot analyzes suspicious messages, links and
          screenshots, connects the evidence, explains the risk and guides you
          toward a safer next step.
        </p>

        <div className="hero-actions">
          <button className="primary-button" onClick={onAnalyze} type="button">
            Analyze Something <span>→</span>
          </button>

          <a className="secondary-link" href="#workflow">
            Explore how it works ↓
          </a>
        </div>

        <div className="hero-proof">
          <div>
            <strong>Text</strong>
            <span>message analysis</span>
          </div>

          <div>
            <strong>URL</strong>
            <span>domain evidence</span>
          </div>

          <div>
            <strong>Image</strong>
            <span>OCR + QR</span>
          </div>

          <div>
            <strong>AI</strong>
            <span>explainable reasoning</span>
          </div>
        </div>
      </div>

      <div className="hero-visual">
        <div className="visual-glow" />
        <EvidenceMockup />
      </div>
    </section>
  );
}

function VideoSection() {
  return (
    <section className="video-section">
      <div className="video-copy">
        <div className="eyebrow">CYBER FRAUD AWARENESS</div>

        <h2>
          Fraud can look convincing. <span>Learn the warning signs.</span>
        </h2>

        <p>
          Phishing and online fraud often use urgent messages, fake branding,
          suspicious links and OTP requests. Watch how simple warning signs can
          help users pause and verify before taking action.
        </p>

        <div className="video-meta">
          <span>Cyber Fraud Awareness</span>
          <span>•</span>
          <span>Safety First</span>
        </div>
      </div>

      <div className="video-card">
        <video
          className="security-video"
          autoPlay
          muted
          loop
          playsInline
          preload="auto"
        >
          <source src="/cyber-fraud-awareness.mp4" type="video/mp4" />
          Your browser does not support HTML5 video.
        </video>

        <div className="video-overlay" />

        <div className="video-live">
          <span className="live-dot" /> FRAUD AWARENESS
        </div>

        <div className="video-caption">
          <strong>Think Before You Click</strong>
          <span>Suspicious links • OTP scams • Fake messages</span>
        </div>
      </div>
    </section>
  );
}

function OverviewSection() {
  return (
    <section className="overview-section" id="about">
      <div className="section-label">OVERVIEW</div>

      <div className="overview-grid">
        <div className="overview-copy">
          <h2>
            A safety assistant built around <span>evidence.</span>
          </h2>

          <p>
            Instead of asking users to trust a single prediction, Digital Safety
            Copilot combines extraction, security checks, machine learning and
            multimodal AI. The result is a simple story: what was claimed, what
            was found, why the signals matter, and what to do next.
          </p>

          <div className="overview-quote">
            <span>“</span>
            <strong>
              We don't just detect what looks suspicious. We show why.
            </strong>
          </div>
        </div>

        <div className="overview-art">
          <div className="art-grid" />

          <div className="art-card art-card-main">
            <span className="art-chip">CLAIM</span>
            <strong>Organization identity</strong>
            <span>ABC Bank</span>
          </div>

          <div className="art-line line-a" />

          <div className="art-card art-card-url">
            <span className="art-chip">EVIDENCE</span>
            <strong>Detected destination</strong>
            <span>abc-secure-login.xyz</span>
          </div>

          <div className="art-line line-b" />

          <div className="art-card art-card-risk">
            <span className="art-chip red-chip">RESULT</span>
            <strong>Evidence mismatch</strong>
            <span>HIGH RISK</span>
          </div>
        </div>
      </div>
    </section>
  );
}

function ComponentShowcase() {
  const [active, setActive] = useState(0);
  const sectionRef = useRef(null);

  useEffect(() => {
    const section = sectionRef.current;
    if (!section) return undefined;

    const onWheel = (event) => {
      const rect = section.getBoundingClientRect();

      const inZone =
        rect.top < window.innerHeight * 0.35 &&
        rect.bottom > window.innerHeight * 0.65;

      if (!inZone) return;
      if (Math.abs(event.deltaY) < 10) return;

      event.preventDefault();

      setActive((current) => {
        if (event.deltaY > 0) {
          return Math.min(components.length - 1, current + 1);
        }

        return Math.max(0, current - 1);
      });
    };

    window.addEventListener("wheel", onWheel, { passive: false });

    return () => {
      window.removeEventListener("wheel", onWheel);
    };
  }, []);

  const selected = components[active];

  return (
    <section className="components-section" id="features" ref={sectionRef}>
      <div className="section-heading centered">
        <div className="eyebrow">KEY COMPONENTS</div>

        <h2>
          Everything works as one <span>safety system.</span>
        </h2>

        <p>
          Explore the core layers. Scroll or select a card to move through the
          intelligence pipeline.
        </p>
      </div>

      <div className="component-stage">
        <button
          className="carousel-arrow left-arrow"
          type="button"
          onClick={() => setActive((current) => Math.max(0, current - 1))}
          aria-label="Previous component"
        >
          ←
        </button>

        <div className="component-cards">
          {components.map((item, index) => {
            const distance = Math.abs(index - active);

            const className =
              index === active
                ? "component-card active-card"
                : distance === 1
                  ? "component-card near-card"
                  : "component-card far-card";

            return (
              <button
                key={item.id}
                className={className}
                onClick={() => setActive(index)}
                type="button"
                aria-pressed={index === active}
              >
                <div className="component-number">{item.number}</div>

                <div className="component-icon">
                  <Icon
                    type={
                      index === 0
                        ? "image"
                        : index === 3
                          ? "graph"
                          : index === 2
                            ? "search"
                            : "shield"
                    }
                  />
                </div>

                <strong>{item.title}</strong>
                <span>{item.short}</span>
              </button>
            );
          })}
        </div>

        <button
          className="carousel-arrow right-arrow"
          type="button"
          onClick={() =>
            setActive((current) =>
              Math.min(components.length - 1, current + 1)
            )
          }
          aria-label="Next component"
        >
          →
        </button>
      </div>

      <div className="component-detail">
        <div className="detail-number">{selected.number}</div>

        <div>
          <h3>{selected.title}</h3>
          <p>{selected.description}</p>

          <div className="detail-points">
            {selected.points.map((point) => (
              <span key={point}>• {point}</span>
            ))}
          </div>
        </div>
      </div>

      <div className="carousel-dots" aria-label="Component position">
        {components.map((item, index) => (
          <button
            key={item.id}
            className={index === active ? "dot active" : "dot"}
            onClick={() => setActive(index)}
            type="button"
            aria-label={`Go to ${item.title}`}
          />
        ))}
      </div>
    </section>
  );
}

function ArchitectureSection() {
  const steps = [
    ["01", "User Input", "Message • URL • Screenshot"],
    ["02", "Extraction", "OCR • URL • QR • Entities"],
    ["03", "Detection", "Rules • ML • Vision"],
    ["04", "Reasoning", "Cross-modal AI"],
    ["05", "Risk Engine", "Evidence-weighted score"],
    ["06", "Safety Action", "Why? • Verify independently"],
  ];

  return (
    <section className="architecture-section" id="architecture">
      <div className="architecture-copy">
        <div className="eyebrow">SYSTEM ARCHITECTURE</div>

        <h2>
          Connect the signals. <span>Explain the decision.</span>
        </h2>

        <p>
          Every stage has a clear responsibility: prepare the evidence, detect
          signals, correlate them and then present a human-readable safety
          decision.
        </p>

        <div className="architecture-note">
          <Icon type="graph" />

          <div>
            <strong>Evidence-first design</strong>

            <span>
              Rules and models provide signals. The reasoning layer connects
              them.
            </span>
          </div>
        </div>
      </div>

      <div className="architecture-flow">
        {steps.map(([number, title, text], index) => (
          <div className="architecture-step" key={number}>
            <div className="step-index">{number}</div>

            <div className="step-content">
              <strong>{title}</strong>
              <span>{text}</span>
            </div>

            {index < steps.length - 1 && (
              <div className="step-arrow">↓</div>
            )}
          </div>
        ))}
      </div>
    </section>
  );
}

function WorkflowSection() {
  const [active, setActive] = useState(0);

  return (
    <section className="workflow-section" id="workflow">
      <div className="section-heading centered">
        <div className="eyebrow">HOW IT WORKS</div>

        <h2>
          A six-step path from <span>content to clarity.</span>
        </h2>

        <p>
          Select a step to see how suspicious content moves through the safety
          pipeline.
        </p>
      </div>

      <div className="workflow-layout">
        <div className="workflow-list">
          {workflow.map((item, index) => (
            <button
              key={item.number}
              type="button"
              className={
                index === active ? "workflow-item active" : "workflow-item"
              }
              onClick={() => setActive(index)}
            >
              <span className="workflow-number">{item.number}</span>
              <span className="workflow-title">{item.title}</span>
              <span className="workflow-chevron">→</span>
            </button>
          ))}
        </div>

        <div className="workflow-feature">
          <div className="feature-step">{workflow[active].number}</div>

          <div className="feature-icon">
            <Icon
              type={
                active === 1 ? "search" : active === 5 ? "check" : "shield"
              }
            />
          </div>

          <h3>{workflow[active].title}</h3>
          <p>{workflow[active].text}</p>

          <div className="feature-progress">
            {workflow.map((item, index) => (
              <span
                key={item.number}
                className={index <= active ? "filled" : ""}
              />
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

function SignatureFeatures() {
  const cards = [
    {
      icon: "eye",
      title: "Evidence Chain",
      body: "See the exact relationship between a claim, the detected evidence and the resulting risk.",
    },
    {
      icon: "graph",
      title: "What Changed?",
      body: "Compare a normal-looking message with a suspicious version and surface the signals that changed.",
    },
    {
      icon: "shield",
      title: "Verify Independently",
      body: "Move beyond “don't click” with a clear alternative verification path through official channels.",
    },
  ];

  return (
    <section className="signature-section">
      <div className="section-heading">
        <div className="eyebrow">SIGNATURE FEATURES</div>

        <h2>
          Built to make the <span>“why?”</span> visible.
        </h2>
      </div>

      <div className="signature-grid">
        {cards.map((card) => (
          <article className="signature-card" key={card.title}>
            <div className="signature-icon">
              <Icon type={card.icon} />
            </div>

            <div className="signature-arrow">↗</div>

            <h3>{card.title}</h3>
            <p>{card.body}</p>
          </article>
        ))}
      </div>
    </section>
  );
}

function Analyzer({ onClose }) {
  const [type, setType] = useState("text");
  const [text, setText] = useState("");
  const [url, setUrl] = useState("");
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const runDemo = () => {
    setResult(null);
    setError("");

    if (type === "text") {
      setText(DEMO_TEXT);
    }

    if (type === "url") {
      setUrl(DEMO_URL);
    }
  };

  const onFile = (event) => {
    const selected = event.target.files?.[0] || null;

    setFile(selected);
    setResult(null);
    setError("");

    if (selected) {
      setPreview(URL.createObjectURL(selected));
    } else {
      setPreview("");
    }
  };

  const analyze = async () => {
    if (type === "text" && !text.trim()) {
      return setError("Paste a message first.");
    }

    if (type === "url" && !url.trim()) {
      return setError("Enter a URL first.");
    }

    if (type === "screenshot" && !file) {
      return setError("Upload a screenshot first.");
    }

    setLoading(true);
    setError("");

    try {
      const data = await analyzeInput({ type, text, url, file });
      setResult(data);
    } catch (err) {
      setError(err?.message || "Unable to analyze this input.");
    } finally {
      setLoading(false);
    }
  };

  const indicators = result?.security_evidence?.indicators || [];
  const qrCodes = result?.extracted?.qr_codes || [];
  const vision = result?.security_evidence?.visual_analysis;
  const ml = result?.security_evidence?.ml_prediction;
  const riskLevel = (result?.risk_level || "unknown").toLowerCase();

  return (
    <div className="analyzer-overlay">
      <div className="analyzer-shell">
        <div className="analyzer-topbar">
          <div className="brand compact">
            <span className="brand-mark">
              <Icon type="shield" />
            </span>

            <span>
              <strong>Digital Safety</strong> <small>Copilot</small>
            </span>
          </div>

          <button className="close-button" onClick={onClose} type="button">
            ×
          </button>
        </div>

        <div className="analyzer-body">
          {!result ? (
            <>
              <div className="analyzer-heading">
                <div className="eyebrow">SAFETY ANALYZER</div>

                <h2>What did you receive?</h2>

                <p>
                  Provide the content. We'll turn it into an evidence trail.
                </p>
              </div>

              <div className="analyzer-tabs">
                {["text", "url", "screenshot"].map((item) => (
                  <button
                    key={item}
                    className={
                      type === item
                        ? "analyzer-tab active"
                        : "analyzer-tab"
                    }
                    onClick={() => {
                      setType(item);
                      setError("");
                    }}
                    type="button"
                  >
                    {item === "text"
                      ? "Message"
                      : item === "url"
                        ? "URL"
                        : "Screenshot"}
                  </button>
                ))}
              </div>

              {type === "text" && (
                <textarea
                  className="analyzer-input"
                  placeholder="Paste a suspicious message or email..."
                  value={text}
                  onChange={(event) => setText(event.target.value)}
                />
              )}

              {type === "url" && (
                <input
                  className="analyzer-input single"
                  placeholder="https://example.com/login"
                  value={url}
                  onChange={(event) => setUrl(event.target.value)}
                />
              )}

              {type === "screenshot" && (
                <label className="analyzer-dropzone">
                  {preview ? (
                    <img src={preview} alt="Selected screenshot" />
                  ) : (
                    <>
                      <div className="upload-symbol">↥</div>
                      <strong>Drop or choose a screenshot</strong>
                      <span>OCR + QR decoding supported</span>
                    </>
                  )}

                  <input
                    type="file"
                    accept="image/*"
                    onChange={onFile}
                  />
                </label>
              )}

              <div className="analyzer-actions">
                {(type === "text" || type === "url") && (
                  <button
                    className="ghost-button"
                    onClick={runDemo}
                    type="button"
                  >
                    Try demo
                  </button>
                )}

                <button
                  className="primary-button"
                  onClick={analyze}
                  disabled={loading}
                  type="button"
                >
                  {loading ? "Analyzing..." : "Analyze Safety →"}
                </button>
              </div>

              {error && <div className="analyzer-error">⚠ {error}</div>}
            </>
          ) : (
            <div className="analysis-result">
              <div className="result-heading-row">
                <div>
                  <div className="eyebrow">ASSESSMENT COMPLETE</div>
                  <h2>Safety Report</h2>
                </div>

                <button
                  className="ghost-button"
                  onClick={() => {
                    setResult(null);
                    setError("");
                  }}
                  type="button"
                >
                  New analysis
                </button>
              </div>

              <div className={`result-hero ${riskLevel}`}>
                <div>
                  <small>AI-ASSISTED RISK ASSESSMENT</small>

                  <strong>
                    {(result.risk_level || "UNKNOWN").toUpperCase()} RISK
                  </strong>
                </div>

                {result.risk_score !== undefined &&
                  result.risk_score !== null && (
                    <div className="risk-score">
                      <strong>{result.risk_score}</strong>
                      <span>/100</span>
                    </div>
                  )}
              </div>

              <div className="result-columns">
                <section className="result-panel">
                  <div className="result-panel-title">
                    Detected Indicators
                  </div>

                  {indicators.length ? (
                    <div className="indicator-list">
                      {indicators.map((item) => (
                        <div
                          className={`result-indicator ${item.severity || ""}`}
                          key={item.code}
                        >
                          <div>
                            <span className="indicator-dot" />

                            <strong>{item.label}</strong>

                            {item.severity && (
                              <span className="indicator-severity">
                                {item.severity}
                              </span>
                            )}
                          </div>

                          <small>{item.evidence}</small>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="result-muted">
                      No strong deterministic indicators were detected.
                    </p>
                  )}

                  {ml?.available && (
                    <div className="ml-signal">
                      <div>
                        <span>ML language classification</span>
                        <strong>{ml.label}</strong>
                      </div>

                      <em>{Math.round(ml.confidence * 100)}%</em>
                    </div>
                  )}
                </section>

                <section className="result-panel safe-result">
                  <div className="result-panel-title">
                    <span>🛡</span> Safe Next Action
                  </div>

                  {(result.safe_actions || []).length > 0 ? (
                    (result.safe_actions || []).map((action, index) => (
                      <div className="safe-action" key={index}>
                        <span>✓</span>
                        <p>{action}</p>
                      </div>
                    ))
                  ) : (
                    <p className="result-muted">
                      No specific action was returned.
                    </p>
                  )}
                </section>
              </div>

              <section className="result-panel why-result">
                <div className="result-panel-title">Why?</div>

                <p className="why-text">
                  {result.explanation || "No explanation was returned."}
                </p>
              </section>

              {(qrCodes.length > 0 || vision?.available) && (
                <div className="result-columns">
                  {qrCodes.length > 0 && (
                    <section className="result-panel">
                      <div className="result-panel-title">
                        QR Content
                      </div>

                      {qrCodes.map((qr) => (
                        <div
                          className="qr-result"
                          key={`${qr.index}-${qr.decoded_value}`}
                        >
                          <span>QR #{qr.index}</span>

                          <strong>
                            {(qr.content_type || "unknown").toUpperCase()}
                          </strong>

                          <small>{qr.decoded_value}</small>
                        </div>
                      ))}
                    </section>
                  )}

                  {vision?.available && (
                    <section className="result-panel">
                      <div className="result-panel-title">
                        Vision Evidence
                      </div>

                      <div className="vision-grid">
                        <span>
                          Branding:{" "}
                          <strong>
                            {vision.visible_brand_or_organization ||
                              "Not detected"}
                          </strong>
                        </span>

                        <span>
                          Login / Verify:{" "}
                          <strong>
                            {vision.login_or_verification_ui ? "Yes" : "No"}
                          </strong>
                        </span>

                        <span>
                          Payment prompt:{" "}
                          <strong>
                            {vision.payment_prompt ? "Yes" : "No"}
                          </strong>
                        </span>

                        <span>
                          Embedded image:{" "}
                          <strong>
                            {vision.embedded_image_present ? "Yes" : "No"}
                          </strong>
                        </span>
                      </div>
                    </section>
                  )}
                </div>
              )}

              <section className="result-panel evidence-result">
                <div className="result-panel-title">
                  🔍 Evidence Chain
                </div>

                {result.evidence_chain?.length ? (
                  <div className="result-chain">
                    {result.evidence_chain.map((entry, index) => (
                      <div
                        className={`result-chain-row ${entry.status || ""}`}
                        key={`${entry.step}-${index}`}
                      >
                        <span className="chain-index">
                          {String(index + 1).padStart(2, "0")}
                        </span>

                        <div>
                          <strong>{entry.step}</strong>
                          <small>{entry.detail}</small>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="result-muted">
                    No evidence chain was returned.
                  </p>
                )}
              </section>

              <div className="result-footer-note">
                <span>◈</span>
                This assessment is decision support. When in doubt, verify
                through an official channel.
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function Footer() {
  return (
    <footer className="footer" id="help">
      <div>
        <div className="brand compact">
          <span className="brand-mark">
            <Icon type="shield" />
          </span>

          <span>
            <strong>Digital Safety</strong> <small>Copilot</small>
          </span>
        </div>

        <p>Detect. Explain. Guide.</p>
      </div>

      <div className="footer-links" id="docs">
        <a href="#features">Features</a>
        <a href="#architecture">Architecture</a>
        <a href="#workflow">How It Works</a>
        <a href="#about">About</a>
        <a href="#help">Help & Feedback</a>
        <a href="#top">Back to top ↑</a>
      </div>
    </footer>
  );
}

export default function App() {
  const [analyzerOpen, setAnalyzerOpen] = useState(false);
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    document.body.classList.toggle("dark-mode", darkMode);

    return () => {
      document.body.classList.remove("dark-mode");
    };
  }, [darkMode]);

  useEffect(() => {
    document.body.style.overflow = analyzerOpen ? "hidden" : "";

    return () => {
      document.body.style.overflow = "";
    };
  }, [analyzerOpen]);

  return (
    <div className={`site-shell ${darkMode ? "dark-theme" : ""}`}>
      <Navbar
        onAnalyze={() => setAnalyzerOpen(true)}
        darkMode={darkMode}
        setDarkMode={setDarkMode}
      />

      <main>
        <Hero onAnalyze={() => setAnalyzerOpen(true)} />
        <VideoSection />
        <OverviewSection />
        <ComponentShowcase />
        <ArchitectureSection />
        <WorkflowSection />
        <SignatureFeatures />
      </main>

      <Footer />

      {analyzerOpen && (
        <Analyzer onClose={() => setAnalyzerOpen(false)} />
      )}
    </div>
  );
}
