import FileUpload from '../../components/FileUpload/FileUpload';
import RecentUploads from '../../components/RecentUploads/RecentUploads';
import { PageContainer, Header, HeaderContent, Title, MainContent } from '../../styles/commonStyles';

// 타입: () => JSX.Element
const MainPage = () => {
  return (
    <PageContainer>
      <Header>
        <HeaderContent>
          <Title>AI Model Simulation</Title>
        </HeaderContent>
      </Header>
      <MainContent>
        <FileUpload />
        <RecentUploads />
      </MainContent>
    </PageContainer>
  );
};

export default MainPage;