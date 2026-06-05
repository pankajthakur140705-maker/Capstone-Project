<<<<<<< HEAD
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

=======
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

>>>>>>> 6ce4515f3c6bb5527f994a20db585a667279390c
export default SchemeResults;