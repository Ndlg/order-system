const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? '/api/v1'

export type ApiRecord = Record<string, unknown>

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers ?? {}),
    },
    ...init,
  })

  if (!response.ok) {
    const message = await response.text()
    throw new Error(message || `Request failed with status ${response.status}`)
  }

  return (await response.json()) as T
}

export function getRecords(path: string): Promise<ApiRecord[]> {
  return request<ApiRecord[]>(path)
}

export function createRecord(path: string, payload: ApiRecord): Promise<ApiRecord> {
  return request<ApiRecord>(path, {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function login(username: string, password: string): Promise<{ access_token: string }> {
  return request<{ access_token: string }>('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  })
}
