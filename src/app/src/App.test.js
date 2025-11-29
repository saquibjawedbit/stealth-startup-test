import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from './App';

// Mock the fetch API
global.fetch = jest.fn();

describe('App Component', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    jest.clearAllMocks();
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  test('renders TODO list heading', () => {
    // Mock successful fetch with empty todos
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ todos: [] }),
    });

    render(<App />);
    expect(screen.getByText(/List of TODOs/i)).toBeInTheDocument();
  });

  test('renders create TODO form', () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ todos: [] }),
    });

    render(<App />);
    expect(screen.getByText(/Create a ToDo/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/ToDo:/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Add ToDo!/i })).toBeInTheDocument();
  });

  test('displays loading state initially', () => {
    fetch.mockImplementationOnce(() => new Promise(() => { })); // Never resolves

    render(<App />);
    expect(screen.getByText(/Loading.../i)).toBeInTheDocument();
  });

  test('fetches and displays todos from API', async () => {
    const mockTodos = [
      { id: '1', title: 'Buy groceries' },
      { id: '2', title: 'Walk the dog' },
      { id: '3', title: 'Finish homework' },
    ];

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ todos: mockTodos }),
    });

    render(<App />);

    // Wait for todos to be displayed
    await waitFor(() => {
      expect(screen.getByText('Buy groceries')).toBeInTheDocument();
      expect(screen.getByText('Walk the dog')).toBeInTheDocument();
      expect(screen.getByText('Finish homework')).toBeInTheDocument();
    });

    // Verify fetch was called with correct URL
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining('/todos/')
    );
  });

  test('displays error message when fetch fails', async () => {
    fetch.mockResolvedValueOnce({
      ok: false,
      status: 500,
    });

    render(<App />);

    await waitFor(() => {
      expect(screen.getByText(/Error:/i)).toBeInTheDocument();
    });
  });

  test('form input has proper validation attributes', () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ todos: [] }),
    });

    render(<App />);

    const input = screen.getByLabelText(/ToDo:/i);

    expect(input).toHaveAttribute('required');
    expect(input).toHaveAttribute('minLength', '1');
    expect(input).toHaveAttribute('maxLength', '300');
    expect(input).toHaveAttribute('placeholder', 'Enter todo description...');
  });

  test('handles POST error gracefully', async () => {
    // Mock initial fetch
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ todos: [] }),
    });

    render(<App />);

    await waitFor(() => {
      expect(screen.queryByText(/Loading.../i)).not.toBeInTheDocument();
    });

    // Mock failed POST request that throws
    fetch.mockRejectedValueOnce(new Error('POST failed: 400'));

    const input = screen.getByLabelText(/ToDo:/i);
    const submitButton = screen.getByRole('button', { name: /Add ToDo!/i });

    await userEvent.type(input, 'Test todo');
    await userEvent.click(submitButton);

    // Wait a bit for the async operation to complete
    await new Promise(resolve => setTimeout(resolve, 100));

    // The error is caught and logged, but doesn't crash the app
    // This test verifies graceful error handling
    expect(screen.getByText(/Create a ToDo/i)).toBeInTheDocument();
  });

  test('displays empty state when no todos exist', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ todos: [] }),
    });

    render(<App />);

    await waitFor(() => {
      expect(screen.queryByText(/Loading.../i)).not.toBeInTheDocument();
    });

    // Should not display any todo items
    const todoElements = screen.queryAllByText(/Buy|Walk|Finish/i);
    expect(todoElements).toHaveLength(0);
  });

  test('handles network error', async () => {
    fetch.mockRejectedValueOnce(new Error('Network error'));

    render(<App />);

    await waitFor(() => {
      expect(screen.getByText(/Error:/i)).toBeInTheDocument();
    });
  });
});