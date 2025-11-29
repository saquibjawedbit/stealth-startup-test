import './App.css';
import useTodos from './hooks/useTodos';

export function App() {

  const { todos, loading, error, addTodo } = useTodos();

  const handleTodoSubmit = (e) => {
    e.preventDefault();
    try {
      addTodo({ title: e.target.todo.value });
    } catch (err) {
      console.error(err);
    }
    e.target.todo.value = "";
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
            <input type="text" name="todo" />
          </div>
          <div style={{ "marginTop": "5px" }}>
            <button>Add ToDo!</button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default App;
