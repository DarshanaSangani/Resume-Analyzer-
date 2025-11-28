import React, { useState } from "react";

const ResumeAnalyzer = () => {
  const [files, setFiles] = useState([]);
  const [jobKeywords, setJobKeywords] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!files.length || !jobKeywords.trim()) {
      alert("Please upload one PDF and enter job keywords.");
      return;
    }

    const formData = new FormData();
    formData.append("resumes", files[0]); // Single file
    formData.append("job_keywords", jobKeywords);

    setLoading(true);
    try {
      const res = await fetch("http://localhost:5000/analyze-pdf", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setResults(data.results || []);
    } catch (error) {
      console.error("❌ Error:", error);
      alert("Something went wrong.");
    }
    setLoading(false);
  };

  const handleDownload = () => {
    window.open("http://localhost:5000/download-report", "_blank");
  };

  return (
    <div
      style={{
        padding: "30px 20px",
        maxWidth: "700px",
        margin: "0 auto",
        fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
      }}
    >
      <h2 style={{ textAlign: "center", marginBottom: "20px", color: "#2c3e50" }}>
        📄 Resume Analyzer
      </h2>

      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: "12px",
          marginBottom: "20px",
        }}
      >
        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setFiles(Array.from(e.target.files))}
          style={{
            padding: "10px",
            borderRadius: "6px",
            border: "1px solid #ccc",
          }}
        />

        <input
          type="text"
          placeholder="Enter job keywords (comma-separated)"
          value={jobKeywords}
          onChange={(e) => setJobKeywords(e.target.value)}
          style={{
            padding: "10px",
            borderRadius: "6px",
            border: "1px solid #ccc",
            fontSize: "15px",
          }}
        />

        <button
          onClick={handleAnalyze}
          disabled={loading}
          style={{
            backgroundColor: loading ? "#aaa" : "#28a745",
            color: "#fff",
            padding: "12px",
            border: "none",
            fontSize: "16px",
            borderRadius: "6px",
            cursor: "pointer",
          }}
        >
          {loading ? "🔍 Analyzing..." : "🚀 Analyze Resume"}
        </button>
      </div>

      {results.length > 0 && (
        <div>
          <h3 style={{ color: "#34495e", marginBottom: "10px" }}>📊 Analysis Results:</h3>
          {results.map((res, idx) => (
            <div
              key={idx}
              style={{
                backgroundColor: "#f9f9f9",
                border: "1px solid #ddd",
                borderRadius: "8px",
                padding: "15px",
                marginBottom: "20px",
                boxShadow: "0 2px 4px rgba(0,0,0,0.05)",
              }}
            >
              <h4 style={{ marginBottom: "10px", color: "#2c3e50" }}>{res.filename}</h4>
              <p><strong>✅ Match Score:</strong> {res.match_score}%</p>
              <p><strong>✅ Matched Keywords:</strong> {res.matched_keywords.join(", ") || "None"}</p>
              <p><strong>❌ Missing Keywords:</strong> {res.missing_keywords.join(", ") || "None"}</p>
              <p><strong>💡 Suggestions:</strong> {res.suggestions.join(" ") || "None"}</p>
            </div>
          ))}

          <button
            onClick={handleDownload}
            style={{
              width: "100%",
              padding: "12px",
              backgroundColor: "#007bff",
              color: "#fff",
              fontSize: "16px",
              border: "none",
              borderRadius: "6px",
              cursor: "pointer",
            }}
          >
            ⬇️ Download TXT Report
          </button>
        </div>
      )}
    </div>
  );
};

export default ResumeAnalyzer;
