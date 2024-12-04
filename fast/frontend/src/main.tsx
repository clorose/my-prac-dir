// File: C:\_YHJ\fast\frontend\src\main.tsx
// Component: main
// TypeScript React Component

import React from 'react';
import ReactDOM from 'react-dom/client';
import { RouterProvider } from 'react-router-dom';
import { router } from './router/router'; // Router.tsx에서 export한 router를 import
import './reset.css';
import './globalStyle.css';

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);