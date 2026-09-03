export default function WhyPanel({ explanation }) {
  return (
    <section className="panel">
      <div className="section-title">Why?</div>
      <p className="explanation">{explanation}</p>
    </section>
  );
}
