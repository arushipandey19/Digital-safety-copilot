import React from "react";

export default function IndicatorList({
  indicators = [],
  mlPrediction,
  evidenceChain = [],
}) {
  const derivedIndicators =
    indicators.length > 0
      ? indicators
      : evidenceChain
          .filter(
            (entry) =>
              entry.status === "danger" ||
              entry.status === "warning"
          )
          .map((entry, index) => ({
            code: `evidence-${index}`,
            label: entry.step,
            severity:
              entry.status === "danger"
                ? "high"
                : "medium",
            evidence: entry.detail,
          }));

  return (
    <section className="panel">
      <div className="section-title">
        Detected Indicators
      </div>

      {derivedIndicators.length === 0 &&
      !mlPrediction?.available ? (
        <div className="muted">
          No strong indicators detected.
        </div>
      ) : (
        <div className="indicator-list">
          {derivedIndicators.map((item) => (
            <div
              className={`indicator ${item.severity || ""}`}
              key={item.code}
            >
              <div className="indicator-head">
                <span>
                  {item.label}
                </span>

                <span className="badge">
                  {item.severity || "signal"}
                </span>
              </div>

              <div className="muted">
                {item.evidence}
              </div>
            </div>
          ))}

          {mlPrediction?.available && (
            <div
              className={`indicator ml ${mlPrediction.label}`}
            >
              <div className="indicator-head">
                <span>
                  ML language classification
                </span>

                <span className="badge">
                  {Math.round(
                    mlPrediction.confidence * 100
                  )}
                  %
                </span>
              </div>

              <div className="muted">
                Model signal:{" "}
                <strong>
                  {mlPrediction.label}
                </strong>
              </div>
            </div>
          )}
        </div>
      )}
    </section>
  );
}