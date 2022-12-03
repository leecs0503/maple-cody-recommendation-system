import { render, screen } from '@testing-library/react';
import Header from './component/Header';
import Result from './component/Result'


test('Head test', () => {
  render(<Header />);
  const linkElement = screen.getByText(/nexon.gg/i);
  expect(linkElement).toBeInTheDocument();
});


test('Result test', () => {
  render(<Result />);
  const linkElement = screen.getByText(/변환 된 아바타/i);
  expect(linkElement).toBeInTheDocument();
});
