import React from "react";
export default function InputTabs({ value, onChange }) {
  return (
    <div className="tabs">
      {[
        ["text", "Message"],
        ["url", "URL"],
        ["screenshot", "Screenshot"]
      ].map(([key, label]) => (
        <button
          key={key}
          className={value === key ? "tab active" : "tab"}
          onClick={() => onChange(key)}
        >
          {label}
        </button>
      ))}
    </div>
  );
}
