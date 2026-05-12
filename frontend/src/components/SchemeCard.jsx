function SchemeCard({ scheme }) {
  return (
    <div className="card">
      <h3>{scheme.name}</h3>
      <p>✔ {scheme.benefit}</p>
      <p>{scheme.reason}</p>
    </div>
  );
}

export default SchemeCard;