// File: src/components/LoadingFailure/loadingFailure.style.ts
import styled from 'styled-components';

export const ErrorContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #f8f9fa;
`;

export const ErrorMessage = styled.h2`
  font-size: 1.5rem;
  color: #dc3545;
  margin-bottom: 1rem;
`;

export const ErrorDescription = styled.p`
  font-size: 1rem;
  color: #6c757d;
  text-align: center;
  max-width: 80%;
  margin-bottom: 0.5rem;
`;

export const GameContainer = styled.div`
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin-top: 20px;
`;

export const Card = styled.div`
  width: 70px;
  height: 70px;
  perspective: 1000px;
  cursor: pointer;
`;

export const CardFront = styled.div`
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  background-color: #007bff;
  border-radius: 8px;
`;

export const CardBack = styled.div`
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  background-color: #ffffff;
  border: 2px solid #007bff;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.5rem;
  transform: rotateY(180deg);
`;