// File: C:\gaon\2024\fast\frontend\src\pages\TimeSeriesPage\time.style.ts
import styled from 'styled-components';
import { motion } from 'framer-motion';

export const PageContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
`;

export const Title = styled.h1`
  font-size: 2.5rem;
  text-align: center;
  margin-bottom: 2rem;
  color: #333;
`;

export const CategoryGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
`;

export const CategoryCard = styled(motion.div)`
  background-color: #ffffff;
  border-radius: 15px;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;

  &:hover {
    box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
  }
`;

export const CardIcon = styled.div`
  margin-bottom: 1rem;
  color: #3498db;
`;

export const CardTitle = styled.h2`
  font-size: 1.5rem;
  text-align: center;
  color: #2c3e50;
`;