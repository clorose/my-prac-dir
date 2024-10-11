// File: C:\_YHJ\fast\frontend\src\components\ui\Button.tsx
// Component: Button
// TypeScript React Component

import styled from 'styled-components';

const StyledButton = styled.button`
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 8px 16px;
  cursor: pointer;
  &:hover {
    background: #0056b3;
  }
  &:disabled {
    background: #cccccc;
    cursor: not-allowed;
  }
`;

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  onClick?: () => void;
}

const Button = ({ onClick, children, ...props }: ButtonProps): JSX.Element => {
  return (
    <StyledButton onClick={onClick} {...props}>
      {children}
    </StyledButton>
  );
};

export default Button;