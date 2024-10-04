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

export const CardHeader = styled.div`
  padding: 1.5rem 1.5rem 0;
`;

export const CardTitle = styled.h2`
  font-size: 1.25rem;
  font-weight: 600;
  color: #111827;
`;

export const CardContent = styled.div`
  padding: 1.5rem;
`;