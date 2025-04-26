// File: src/pages/MainPage/MainPageStyles.ts
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

export const PageContainer = styled.div`
  min-height: 100vh;
  background-color: #f0f4f8;
  font-family: 'Roboto', sans-serif;
`;

export const MainContent = styled.main`
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
`;

export const FeatureSection = styled.div`
  display: flex;
  justify-content: space-between;
  gap: 2rem;
  margin-bottom: 3rem;
`;

export const FeatureCard = styled(motion.div)`
  background-color: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  flex: 1;
  text-align: center;
`;

export const IconWrapper = styled.div`
  margin-bottom: 1rem;
  color: #3498db;
`;

export const FeatureTitle = styled.h3`
  font-size: 1.25rem;
  color: #2c3e50;
  margin-bottom: 0.5rem;
`;

export const FeatureDescription = styled.p`
  font-size: 1rem;
  color: #34495e;
`;

export const ActionSection = styled.div`
  text-align: center;
`;

export const ActionButton = styled(motion(Link))`
  display: inline-block;
  background-color: #3498db;
  color: white;
  padding: 1rem 2rem;
  border-radius: 30px;
  text-decoration: none;
  font-weight: bold;
  font-size: 1.1rem;
  transition: background-color 0.3s ease;

  &:hover {
    background-color: #2980b9;
  }
`;