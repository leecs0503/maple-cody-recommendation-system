const request = require('supertest');
const app = require('../server');

describe('Test /', () => {
  it('should return req status 200', async () => {
    await request(app).get('/').then((response) => {
      expect(response.status).toBe(200);
    });
  });
});


describe('Test /result', () => {
  it('should return req status 200', async () => {
    await request(app)
      .post('/result')
      .set('Accept', 'application/json')
      .type('application/json')
      .send({ name: '오지환' })
      .then((response) => {
        expect(response.status).toBe(200);
      });
  });
});
