export default function SafeAction({ actions = [] }) {
  return (
    <section className="panel safe-panel">
      <div className="section-title">🛡 Safe Next Action</div>

      {actions.map((action, index) => (
        <div className="action" key={index}>
          <span className="action-mark">✓</span>
          {action}
        </div>
      ))}
    </section>
  );
}
