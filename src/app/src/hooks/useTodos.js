import { useState, useCallback, useEffect } from "react";
import { API_BASE } from "../configs/config";

export default function useTodos() {
    const [todos, setTodos] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const fetchTodos = useCallback(async () => {
        setLoading(true);
        setError(null);
        try {
            const res = await fetch(`${API_BASE}/todos/`);
            if (!res.ok) throw new Error(`Fetch failed: ${res.status}`);
            const payload = await res.json();
            setTodos(payload.todos || []);
        } catch (err) {
            setError(err.message || "Unknown error");
        } finally {
            setLoading(false);
        }
    }, []);

    const addTodo = useCallback(async (todoInput) => {
        // todoInput : { title: "Buy milk" }
        setError(null);
        try {
            const res = await fetch(`${API_BASE}/todos/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(todoInput),
            });
            if (!res.ok) {
                const body = await res.json().catch(() => ({}));
                throw new Error(body.error || `POST failed: ${res.status}`);
            }
            const created = await res.json();
            // re-fetch authoritative list
            await fetchTodos();
            return created;
        } catch (err) {
            setError(err.message || "Failed to add todo");
            throw err;
        }
    }, [fetchTodos]);

    useEffect(() => {
        fetchTodos();
    }, [fetchTodos]);

    return { todos, loading, error, refresh: fetchTodos, addTodo };
}
