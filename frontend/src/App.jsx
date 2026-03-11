import { useEffect, useRef, useState } from "react";

const starter = {
  role: "bot",
  text: "Hello, I am an Eliza-like chatbot. Tell me what is on your mind.",
};

export default function App() {
  const [messages, setMessages] = useState([starter]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const chatLogRef = useRef(null);

  useEffect(() => {
    if (!chatLogRef.current) return;
    chatLogRef.current.scrollTo({
      top: chatLogRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [messages, loading]);

  const sendMessage = async () => {
    const trimmed = input.trim();
    if (!trimmed || loading) return;

    const userMessage = { role: "user", text: trimmed };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: trimmed }),
      });

      if (!response.ok) {
        throw new Error("Network response failed");
      }

      const data = await response.json();
      setMessages((prev) => [...prev, { role: "bot", text: data.response }]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: "I could not reach the server. Please try again." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    sendMessage();
  };

  return (
    <div className="page">
      <div className="blob blob-one" aria-hidden="true" />
      <div className="blob blob-two" aria-hidden="true" />

      <main className="chat-shell">
        <header className="chat-header">
          <h1>Eliza Regex Chatbot</h1>
          <p>Python backend with 55 regex response rules</p>
        </header>

        <section ref={chatLogRef} className="chat-log" aria-live="polite">
          {messages.map((message, index) => (
            <article key={`${message.role}-${index}`} className={`bubble ${message.role}`}>
              {message.text}
            </article>
          ))}
          {loading && <article className="bubble bot">Thinking...</article>}
        </section>

        <form className="composer" onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Type your message..."
            value={input}
            onChange={(event) => setInput(event.target.value)}
          />
          <button type="submit" disabled={loading}>
            Send
          </button>
        </form>
      </main>
    </div>
  );
}
