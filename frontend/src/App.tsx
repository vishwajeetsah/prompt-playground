import { useEffect, useState } from 'react';
import { fetchHealth, fetchModels, sendChat, type ChatResponse, type ModelInfo } from './api';
import './styles.css';

interface Message {
  role: 'user' | 'assistant';
  text: string;
  latency_s?: number;
}

export default function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [system, setSystem] = useState('');
  const [models, setModels] = useState<ModelInfo[]>([]);
  const [mockMode, setMockMode] = useState<boolean | null>(null);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchHealth()
      .then((h) => setMockMode(h.mock_mode))
      .catch(() => setMockMode(null));
    fetchModels()
      .then(setModels)
      .catch(() => setModels([]));
  }, []);

  async function onSend() {
    const prompt = input.trim();
    if (!prompt || sending) return;
    setSending(true);
    setError(null);
    setMessages((m) => [...m, { role: 'user', text: prompt }]);
    setInput('');
    try {
      const res: ChatResponse = await sendChat(prompt, system.trim() || undefined);
      setMessages((m) => [...m, { role: 'assistant', text: res.reply, latency_s: res.latency_s }]);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Request failed. Is the backend running?');
    } finally {
      setSending(false);
    }
  }

  return (
    <div className="app">
      <header>
        <h1>Prompt Playground</h1>
        <p className="subtitle">Experiment with prompts against any OpenAI-compatible backend.</p>
        {mockMode === true && <span className="badge mock">mock mode — no API key needed</span>}
        {mockMode === false && <span className="badge live">live model</span>}
      </header>

      <section className="models">
        <strong>Models:</strong>{' '}
        {models.length === 0 ? (
          <em>backend unreachable?</em>
        ) : (
          models.map((m) => (
            <span key={m.id} className="model" title={m.description}>
              {m.name}
            </span>
          ))
        )}
      </section>

      <section className="system">
        <input
          value={system}
          onChange={(e) => setSystem(e.target.value)}
          placeholder="Optional system instruction, e.g. 'Explain like I'm five'…"
        />
      </section>

      <main className="messages">
        {messages.length === 0 && (
          <p className="empty">Send your first prompt below to start experimenting.</p>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`message ${m.role}`}>
            <div className="bubble">
              <pre>{m.text}</pre>
              {m.latency_s !== undefined && (
                <span className="latency">{m.latency_s.toFixed(2)}s</span>
              )}
            </div>
          </div>
        ))}
        {sending && <p className="empty">Thinking…</p>}
        {error && <p className="error">{error}</p>}
      </main>

      <footer className="composer">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && onSend()}
          placeholder="Type a prompt and hit Enter…"
          disabled={sending}
        />
        <button onClick={onSend} disabled={sending || !input.trim()}>
          Send
        </button>
      </footer>
    </div>
  );
}
