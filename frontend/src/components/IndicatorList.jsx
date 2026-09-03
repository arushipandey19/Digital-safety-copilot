export default function IndicatorList({ indicators = [], mlPrediction }) {
  return (
    <section className="panel">
      <div className="section-title">Detected Indicators</div>

      {indicators.length === 0 && !mlPrediction?.available ? (
        <div className="muted">No strong indicators detected.</div>
      ) : (
        <div className="indicator-list">
          {indicators.map((item) => (
            <div className={`indicator ${item.severity}`} key={item.code}>
              <div className="indicator-head">
                <span>{item.label}</span>
                <span className="badge">{item.severity}</span>
              </div>
              <div className="muted">{item.evidence}</div>
            </div>
          ))}

          {mlPrediction?.available && (
            <div className={`indicator ml ${mlPrediction.label}`}>
              <div className="indicator-head">
                <span>ML language classification</span>
                <span className="badge">
                  {Math.round(mlPrediction.confidence * 100)}%
                </span>
              </div>
              <div className="muted">
                Model signal: <strong>{mlPrediction.label}</strong>
              </div>
            </div>
          )}
        </div>
      )}
    </section>
  );
}
