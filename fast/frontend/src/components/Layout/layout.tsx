// File: C:\_YHJ\fast\frontend\src\components\Layout\Layout.tsx

import { Outlet } from 'react-router-dom';
import Header from '../Header/Header';
import { PageContainer } from '../../styles/commonStyles';

const Layout = () => {
  return (
    <PageContainer>
      <Header />
      <Outlet /> {/* 각 페이지의 내용이 여기 렌더링됩니다 */}
    </PageContainer>
  );
};

export default Layout;
