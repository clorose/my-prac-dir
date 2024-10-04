// src/components/ui/Card.tsx
import React from 'react';
import styled from 'styled-components';

const StyledCard = styled.div`
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  padding: 16px;
`;

type CardProps = {
  children: React.ReactNode;
};

const Card: React.FC<CardProps> = ({ children }) => {
  return <StyledCard>{children}</StyledCard>;
};

export default Card;