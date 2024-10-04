import { createBrowserRouter } from "react-router-dom";
import MainPage from "../pages/mainPage/mainPage";
import PerformancePage from "../pages/performancePage/PerformancePage";
import RangesPage from "../pages/rangesPage/RangesPage";
import VisualsPage from "../pages/visualPage/VisualsPage";
import NotFoundPage from "../pages/notFoundPage/notFoundPage";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <MainPage />,
    errorElement: <NotFoundPage />,
    children: [
      {
        path: "performance",
        element: <PerformancePage />,
      },
      {
        path: "ranges",
        element: <RangesPage />,
      },
      {
        path: "visuals",
        element: <VisualsPage />,
      },
    ],
  },
]);

// Router 컴포넌트는 더 이상 필요하지 않으므로 제거할 수 있습니다.
// const Router = () => {
//   return <RouterProvider router={router} />;
// };
// 
// export default Router;