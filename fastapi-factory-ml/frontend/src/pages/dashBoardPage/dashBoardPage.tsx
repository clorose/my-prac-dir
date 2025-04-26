// File: C:\_YHJ\fast\frontend\src\pages\DashboardPage\DashboardPage.tsx
// Component: DashboardPage
// TypeScript React Component

import { useState } from 'react';
import { PageContainer, Header, HeaderContent, Title, MainContent, ModelConfiguration, TabMenu, TabItem, TabContent, SaveButton } from './dashBoard.style';
import PerformanceTab from '../../components/tabs/PerformanceTab';
import DistributionTab from '../../components/tabs/DistributionTab';
import ImportanceTab from '../../components/tabs/ImportanceTab';
import RangesTab from '../../components/tabs/RangesTab';
import VisualsTab from '../../components/tabs/VisualsTab';

const DashboardPage = () => {
  const [activeTab, setActiveTab] = useState<string>('Performance');

  const renderActiveTabContent = () => {
    switch (activeTab) {
      case 'Performance':
        return <PerformanceTab />;
      case 'Distribution':
        return <DistributionTab />;
      case 'Importance':
        return <ImportanceTab />;
      case 'Ranges':
        return <RangesTab />;
      case 'Visualizations':
        return <VisualsTab />;
      default:
        return <PerformanceTab />;
    }
  };

  return (
    <PageContainer>
      <Header>
        <HeaderContent>
          <Title>QMS Dashboard</Title>
        </HeaderContent>
      </Header>
      <MainContent>
        <ModelConfiguration>
          {/* 모델 설정 부분 */}
          <input type="text" placeholder="Menu Label" />
          <input type="text" placeholder="Menu Label" />
          <button>Apply</button>
        </ModelConfiguration>
        <TabMenu>
          {['Performance', 'Distribution', 'Importance', 'Ranges', 'Visualizations'].map((tab) => (
            <TabItem
              key={tab}
              isActive={activeTab === tab}
              onClick={() => setActiveTab(tab)}
            >
              {tab}
            </TabItem>
          ))}
        </TabMenu>
        <TabContent>{renderActiveTabContent()}</TabContent>
        <SaveButton>Save Result</SaveButton>
      </MainContent>
    </PageContainer>
  );
};

export default DashboardPage;