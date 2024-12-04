// File: C:\_YHJ\fast\frontend\src\router\router.tsx

import { createBrowserRouter } from 'react-router-dom';
import MainPage from '../pages/mainPage/mainPage';
import DashboardPage from '../pages/dashBoardPage/dashBoardPage';
import NotFoundPage from '../pages/notFoundPage/notFoundPage';
import TestPage from '../pages/testPage/testPage';
import ModelViewer from '../pages/modelPage/modelPage';
import Layout from '../components/Layout/layout';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,  // 공통 레이아웃 적용
    children: [
      { path: '', element: <MainPage /> },
      { path: 'dashboard', element: <DashboardPage /> },
      { path: 'test', element: <TestPage /> },
      { path: 'model', element: <ModelViewer /> },
      { path: '*', element: <NotFoundPage /> },
    ],
  },
]);
