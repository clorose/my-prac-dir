// File: C:\_YHJ\fast\frontend\src\pages\notFoundPage\notFound.style.ts
// Module: notFound.style
// TypeScript Module

import styled, { keyframes, createGlobalStyle } from 'styled-components';

export const GlobalStyle = createGlobalStyle`
  body {
    margin: 0;
    padding: 0;
    font-family: 'RixXladywatermelonR', sans-serif;
  }
`;

const fadeIn = keyframes`
  from { opacity: 0; }
  to { opacity: 1; }
`;

const bounce = keyframes`
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-30px); }
  60% { transform: translateY(-15px); }
`;

const float = keyframes`
  0% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
  100% { transform: translateY(0px); }
`;

const typeWriter = keyframes`
  from { width: 0; }
  to { width: 100%; }
`;

const rotateIcon = keyframes`
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
`;

export const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #6e8efb, #a777e3);
  padding: 1rem;
  color: white;
  overflow: hidden;
  position: relative;
`;

export const Bubble = styled.div`
  position: absolute;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  animation: ${float} 4s infinite ease-in-out;

  &:nth-child(1) {
    width: 60px;
    height: 60px;
    left: 10%;
    top: 20%;
  }

  &:nth-child(2) {
    width: 80px;
    height: 80px;
    right: 15%;
    top: 40%;
    animation-delay: 1s;
  }

  &:nth-child(3) {
    width: 40px;
    height: 40px;
    left: 20%;
    bottom: 30%;
    animation-delay: 2s;
  }
`;

export const ErrorCode = styled.div`
  font-size: 8rem;
  border-radius: 0.5rem;
  font-family: 'TTSamlipCreamyWhiteR', sans-serif;
  font-weight: 600;
  color: white;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
  animation: ${bounce} 2s ease infinite;
`;

export const Message = styled.div`
  background-color: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(5px);
  border-radius: 0.375rem;
  padding: 1rem;
  margin-bottom: 1.5rem;
  animation: ${fadeIn} 1s ease-out;
  max-width: 80%;
  text-align: center;
`;

export const Title = styled.h2`
  font-size: 1.25rem;
  color: white;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
`;

export const Description = styled.p`
  color: rgba(255, 255, 255, 0.8);
`;

export const SubMessage = styled.p`
  font-size: 1.25rem;
  margin-bottom: 1rem;
  color: white;
`;

export const Button = styled.button`
  background-color: white;
  color: #6e8efb;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.25rem;
  font-size: 1rem;
  font-family: 'RixXladywatermelonR', sans-serif;
  cursor: pointer;
  display: flex;
  align-items: center;
  transition: all 0.3s;
  
  &:hover {
    background-color: #f0f0f0;
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  svg {
    margin-right: 0.5rem;
    transition: transform 0.3s;
  }

  &:hover svg {
    animation: ${rotateIcon} 1s linear infinite;
  }
`;

export const TypewriterText = styled.span`
  display: inline-block;
  overflow: hidden;
  border-right: 0.15em solid white;
  white-space: nowrap;
  margin: 0 auto;
  letter-spacing: 0.15em;
  animation:
    ${typeWriter} 3.5s steps(40, end),
    blink-caret 0.75s step-end infinite;

  @keyframes blink-caret {
    from, to { border-color: transparent; }
    50% { border-color: white; }
  }
`; 