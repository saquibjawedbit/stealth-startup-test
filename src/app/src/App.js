import { useState } from 'react';
import './App.css';
import useTodos from './hooks/useTodos';

export function App() {

  const { todos, loading, error, addTodo } = useTodos();
  const [submitting, setSubmitting] = useState(false);

  const handleTodoSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await addTodo({ title: e.target.todo.value });
      e.target.reset();
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="App">
      <div>
        <h1>List of TODOs</h1>
        {loading ? (
          <p>Loading...</p>
        ) : error ? (
          <p>Error: {error}</p>
        ) : (
          todos.map((todo) => (
            <div key={todo.id}>
              <p>{todo.title}</p>
            </div>
          ))
        )}
      </div>
      <div>
        <h1>Create a ToDo</h1>
        <form onSubmit={handleTodoSubmit}>
          <div>
            <label htmlFor="todo">ToDo: </label>
            <input
              id="todo"
              type="text"
              name="todo"
              required
              minLength={1}
              maxLength={300}
              placeholder="Enter todo description..."
            />
          </div>
          <div style={{ "marginTop": "5px" }}>
            <button disabled={submitting}>Add ToDo!</button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default App;
