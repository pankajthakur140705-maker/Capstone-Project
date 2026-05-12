function ExplanationBox({ text }) {
  return (
    <div className="explanation">
      <h3>Why you are eligible</h3>
      <p>{text}</p>
    </div>
  );
}

export default ExplanationBox;