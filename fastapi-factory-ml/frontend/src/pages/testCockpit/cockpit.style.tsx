import styled from 'styled-components';
import { Link } from 'react-router-dom';

export const CockpitContainer = styled.div`
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 3rem;
  border-radius: 20px;
  color: white;
  max-width: 1000px;
  margin: 3rem auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
`;

export const CockpitTitle = styled.h2`
  font-size: 2.5rem;
  margin-bottom: 2rem;
  text-align: center;
  font-weight: 700;
  color: #ffffff;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
`;

export const ControlPanel = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
`;

export const ControlButton = styled(Link)`
  background-color: rgba(255, 255, 255, 0.1);
  border: none;
  padding: 2rem 1.5rem;
  border-radius: 15px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  color: white;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);

  &:hover {
    background-color: rgba(255, 255, 255, 0.2);
  }
`;

export const ButtonIcon = styled.div`
  margin-bottom: 1rem;
  color: #ffffff;
`;

export const ButtonText = styled.span`
  font-size: 1.2rem;
  font-weight: 500;
  text-align: center;
`;