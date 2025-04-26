// File: src/pages/TestCockpit/TestCockpit.tsx
import { 
    CockpitContainer, 
    CockpitTitle, 
    ControlPanel, 
    ControlButton, 
    ButtonIcon
  } from './cockpit.style';
  
  const TestCockpit = () => {
    return (
      <CockpitContainer>
        <CockpitTitle>Test Cockpit</CockpitTitle>
        <ControlPanel>
          <ControlButton to="/data-input">
            <ButtonIcon>📊</ButtonIcon>
            Data Input
          </ControlButton>
          <ControlButton to="/model-selection">
            <ButtonIcon>🧠</ButtonIcon>
            Model Selection
          </ControlButton>
          <ControlButton to="/parameter-tuning">
            <ButtonIcon>🎛️</ButtonIcon>
            Parameter Tuning
          </ControlButton>
          <ControlButton to="/results-analysis">
            <ButtonIcon>📈</ButtonIcon>
            Results Analysis
          </ControlButton>
        </ControlPanel>
      </CockpitContainer>
    );
  };
  
  export default TestCockpit;