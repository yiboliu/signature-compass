import React from 'react';
import { render, fireEvent, waitFor, screen } from '@testing-library/react';
import App from './App';
import fetchMock from 'jest-fetch-mock';

fetchMock.enableMocks();

beforeEach(() => {
  fetchMock.resetMocks();
});

global.WebSocket = jest.fn().mockImplementation(() => ({
  onopen: jest.fn(),
  onclose: jest.fn(),
  onmessage: jest.fn(),
  onerror: jest.fn(),
}));

test('loads and displays the fetch button', () => {
  render(<App />);
  expect(screen.getByText('Fetch Data')).toBeInTheDocument();
});

test('input value changes on user input', () => {
  render(<App />);
  const input = screen.getByPlaceholderText('Enter your query of a signature in hex format');
  fireEvent.change(input, { target: { value: '123' } });
  expect(input.value).toBe('123');
});

test('fetches data on button click and displays result', async () => {
  fetchMock.mockResponseOnce('Mocked response');

  render(<App />);
  const input = screen.getByPlaceholderText('Enter your query of a signature in hex format');
  fireEvent.change(input, { target: { value: '123' } });
  
  fireEvent.click(screen.getByText('Fetch Data'));

  const fetchedData = await screen.findByText(/Mocked response/i);
  expect(fetchedData).toBeInTheDocument();

  screen.debug();
});

test('displays an error message if the fetch fails', async () => {
  fetchMock.mockReject(new Error('Failed to fetch'));

  render(<App />);
  fireEvent.click(screen.getByText('Fetch Data'));

  await waitFor(() => screen.getByText(/failed to fetch/i));

  expect(screen.getByText(/failed to fetch/i)).toBeInTheDocument();
});
