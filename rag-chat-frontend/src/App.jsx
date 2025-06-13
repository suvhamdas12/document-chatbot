import React, { useState } from "react";
import axios from "axios";

function App() {
  const [pdfFile, setPdfFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [uploadStatus, setUploadStatus] = useState("");

  const handleFileChange = (e) => {
    setPdfFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!pdfFile) return alert("Please select a PDF first.");

    const formData = new FormData();
    formData.append("file", pdfFile);

    try {
      setUploadStatus("📤 Uploading...");
      const res = await axios.post("http://localhost:8000/upload_pdf/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setUploadStatus(res.data.message || "✅ Upload successful!");
    } catch (err) {
      console.error("Upload error:", err);
      setUploadStatus("❌ Upload failed.");
    }
  };

  const handleAsk = async () => {
    if (!question) return;
    try {
      const res = await axios.get("http://localhost:8000/ask/", {
        params: { question },
      });
      setAnswer(res.data.answer);
    } catch (err) {
      console.error(err);
      setAnswer("❌ Failed to get answer.");
    }
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        minWidth:"360vh",
        background: "linear-gradient(to right, #e0eafc, #cfdef3)",
        fontFamily: "Segoe UI, sans-serif",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        padding: "2rem",
      }}
    >
      <div
        style={{
          background: "#fff",
          padding: "2rem 3rem",
          borderRadius: "1rem",
          width: "100%",
          maxWidth: "700px",
          boxShadow: "0 8px 20px rgba(0, 0, 0, 0.1)",
        }}
      >
        <h1
          style={{
            fontSize: "2rem",
            fontWeight: "bold",
            marginBottom: "1.5rem",
            textAlign: "center",
            color: "#333",
          }}
        >
          📄 Document ChatBot
        </h1>

        {/* Upload PDF */}
        <div style={{ marginBottom: "1.5rem" }}>
          <label style={{ fontWeight: "600" }}>Upload PDF:</label>
          <div style={{ display: "flex", alignItems: "center", marginTop: "0.5rem" }}>
            <input
              type="file"
              accept="application/pdf"
              onChange={handleFileChange}
              style={{ flex: 1 }}
            />
            <button
              onClick={handleUpload}
              style={{
                marginLeft: "1rem",
                padding: "0.5rem 1rem",
                backgroundColor: "#28a745",
                color: "white",
                border: "none",
                borderRadius: "5px",
                cursor: "pointer",
                transition: "0.2s",
              }}
            >
              Upload
            </button>
          </div>
          <p style={{ marginTop: "0.5rem", color: uploadStatus.includes("❌") ? "red" : "green" }}>
            {uploadStatus}
          </p>
        </div>

        {/* Ask a Question */}
        <div style={{ marginBottom: "1.5rem" }}>
          <label style={{ fontWeight: "600" }}>Ask a Question:</label>
          <div style={{ display: "flex", marginTop: "0.5rem" }}>
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="e.g. What containerization tool did the user use?"
              style={{
                flex: 1,
                padding: "0.5rem",
                border: "1px solid #ccc",
                borderRadius: "5px 0 0 5px",
                fontSize: "1rem",
              }}
            />
            <button
              onClick={handleAsk}
              style={{
                padding: "0.5rem 1rem",
                backgroundColor: "#007bff",
                color: "white",
                border: "none",
                borderRadius: "0 5px 5px 0",
                cursor: "pointer",
                fontSize: "1rem",
              }}
            >
              Ask
            </button>
          </div>
        </div>

        {/* Answer Section */}
        {answer && (
          <div style={{ marginTop: "1rem" }}>
            <strong style={{ display: "block", marginBottom: "0.5rem" }}>Answer:</strong>
            <p style={{ background: "#e8f4fd", padding: "1rem", borderRadius: "8px", color: "#333" }}>
              {answer}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;