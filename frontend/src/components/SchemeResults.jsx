import SchemeCard from "./SchemeCard";
import ExplanationBox from "./ExplanationBox";

function SchemeResults({ schemes, explanation }) {
  return (
    <div>
      <h2>Eligible Schemes</h2>

      {schemes.map((scheme, index) => (
        <SchemeCard key={index} scheme={scheme} />
      ))}

      <ExplanationBox text={explanation} />
    </div>
  );
}

export default SchemeResults;