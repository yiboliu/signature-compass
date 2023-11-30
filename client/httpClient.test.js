const { makeGetRequest } = require('./httpClient');

// Mocking the global fetch API
global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    text: () => Promise.resolve('Mocked response'),
  })
);

beforeEach(() => {
  fetch.mockClear();
});

test('makeGetRequest sends a request to the correct URL and returns text response', () => {
  const signature = '0x1a2b3c';

  makeGetRequest(signature).then(response => {
    expect(response).toBe('Mocked response');
    expect(fetch).toHaveBeenCalledTimes(1);
    expect(fetch).toHaveBeenCalledWith('https://signature-compass-63lof.ondigitalocean.app/get-text-signature?hex=0x1a2b3c');
  });
});

test('makeGetRequest adjusts the signature head correctly when not starting with 0x', () => {
  const signature = '1a2b3c4d5e';

  makeGetRequest(signature).then(() => {
    expect(fetch).toHaveBeenCalledWith('https://signature-compass-63lof.ondigitalocean.app/get-text-signature?hex=1a2b3c4d');
  });
});

test('makeGetRequest handles fetch errors', () => {
  fetch.mockImplementationOnce(() => Promise.reject(new Error('Fetch error')));

  expect(makeGetRequest('0x1a2b3c')).rejects.toThrow('Fetch error');
});
