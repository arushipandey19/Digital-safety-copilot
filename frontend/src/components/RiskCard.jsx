export default function RiskCard({ risk }) {
  const className = risk.level.toLowerCase();

  return (
    <div className={`risk-card ${className}`}>
      <div>
        <div className="eyebrow">AI-Assisted Risk Assessment</div>
        <div className="risk-title">{risk.level} RISK</div>
      </div>

      <div className="score">
        {risk.score}
        <span>/100</span>
      </div>
    </div>
  );
}
