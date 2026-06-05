<<<<<<< HEAD
import { useState } from "react";

function UserForm({ onSubmit }) {
  const [age, setAge] = useState("");
  const [income, setIncome] = useState("");
  const [category, setCategory] = useState("student");

  const handleSubmit = (e) => {
    e.preventDefault();

    onSubmit({
      age: Number(age),
      income: Number(income),
      category
    });
  };

  return (
    <form onSubmit={handleSubmit} className="form-box">
      <input
        placeholder="Age"
        value={age}
        onChange={(e) => setAge(e.target.value)}
      />

      <input
        placeholder="Income"
        value={income}
        onChange={(e) => setIncome(e.target.value)}
      />

      <select value={category} onChange={(e) => setCategory(e.target.value)}>
        <option value="student">Student</option>
        <option value="farmer">Farmer</option>
        <option value="women">Women</option>
      </select>

      <button type="submit">Check Schemes</button>
    </form>
  );
}

=======
import { useState } from "react";

function UserForm({ onSubmit }) {
  const [age, setAge] = useState("");
  const [income, setIncome] = useState("");
  const [category, setCategory] = useState("student");

  const handleSubmit = (e) => {
    e.preventDefault();

    onSubmit({
      age: Number(age),
      income: Number(income),
      category
    });
  };

  return (
    <form onSubmit={handleSubmit} className="form-box">
      <input
        placeholder="Age"
        value={age}
        onChange={(e) => setAge(e.target.value)}
      />

      <input
        placeholder="Income"
        value={income}
        onChange={(e) => setIncome(e.target.value)}
      />

      <select value={category} onChange={(e) => setCategory(e.target.value)}>
        <option value="student">Student</option>
        <option value="farmer">Farmer</option>
        <option value="women">Women</option>
      </select>

      <button type="submit">Check Schemes</button>
    </form>
  );
}

>>>>>>> 6ce4515f3c6bb5527f994a20db585a667279390c
export default UserForm;