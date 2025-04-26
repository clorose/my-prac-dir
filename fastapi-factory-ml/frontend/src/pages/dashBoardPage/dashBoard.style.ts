// File: C:\_YHJ\fast\frontend\src\pages\DashboardPage\DashboardPage.styles.ts
// Styled components for DashboardPage

import styled from 'styled-components';

export const PageContainer = styled.div`
  min-height: 100vh;
  background-color: #f9fafb;
`;

export const Header = styled.header`
  width: 100%;
  background-color: white;
  border-bottom: 1px solid #e5e7eb;
`;

export const HeaderContent = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
`;

export const Title = styled.h1`
  font-size: 1.5rem;
  font-weight: bold;
  color: #1f2937;
`;

export const MainContent = styled.main`
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
`;

export const ModelConfiguration = styled.div`
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
`;

export const TabMenu = styled.div`
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #ccc;
`;

export const TabItem = styled.button<{ isActive: boolean }>`
  padding: 0.5rem 1rem;
  font-weight: ${({ isActive }) => (isActive ? 'bold' : 'normal')};
  background: ${({ isActive }) => (isActive ? '#e5e7eb' : 'transparent')};
  border: none;
  cursor: pointer;

  &:hover {
    background: #f0f0f0;
  }
`;

export const TabContent = styled.div`
  margin-top: 1rem;
`;

export const SaveButton = styled.button`
  margin-top: 2rem;
  padding: 0.75rem 1.5rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;

  &:hover {
    background-color: #0056b3;
  }
`;