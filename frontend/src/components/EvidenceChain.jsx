import React from "react";
export default function EvidenceChain({ chain = [] }) {
  return (
    <section className="panel">
      <div className="section-title">🔍 Evidence Chain</div>

      <div className="chain">
        {chain.map((item, index) => (
          <div className={`chain-item ${item.status}`} key={`${item.step}-${index}`}>
            <div className="chain-dot" />
            <div>
              <div className="chain-step">{item.step}</div>
              <div className="muted">{item.detail}</div>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
