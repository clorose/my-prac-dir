// File: C:\gaon\2024\fast\frontend\src\components\Header\header.style.ts

import styled from 'styled-components';

export const HeaderContainer = styled.header`
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

export const Subtitle = styled.h2`
  font-size: 1.2rem;
  color: #4a5568;
  margin-top: 0.5rem;
`;

export const NavBar = styled.nav`
  width: 100%;
  background-color: #1f2937;
  padding: 1rem;
  display: flex;
  justify-content: center;
  gap: 2rem;
`;

export const NavLink = styled.a`
  color: white;
  text-decoration: none;
  font-weight: bold;
  &:hover {
    text-decoration: underline;
  }
`;