/** Typed client for the Prompt Playground backend API. */

export interface ChatResponse {
  reply: string;
  latency_s: number;
  model: string;
  mock_mode: boolean;
}

export interface ModelInfo {
  id: string;
  name: string;
  description: string;
}

export interface HealthResponse {
  status: string;
  mock_mode: boolean;
  model: string;
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(path, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API error ${res.status}: ${text}`);
  }
  return (await res.json()) as T;
}

export function fetchHealth(): Promise<HealthResponse> {
  return request<HealthResponse>('/api/health');
}

export function fetchModels(): Promise<ModelInfo[]> {
  return request<ModelInfo[]>('/api/models');
}

export function sendChat(prompt: string, system?: string): Promise<ChatResponse> {
  return request<ChatResponse>('/api/chat', {
    method: 'POST',
    body: JSON.stringify({ prompt, system: system || undefined }),
  });
}
