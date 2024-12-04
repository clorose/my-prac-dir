// File: C:\_YHJ\fast\frontend\src\pages\modelPage\model.style.ts
// Module: model.style
// Description: Styled components for Model Viewer page.

import styled from 'styled-components';

export const FileList = styled.ul`
  list-style: none;
  padding: 0;
  margin: 1rem 0;
`;

export const FileItem = styled.li`
  cursor: pointer;
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid #ccc;
  border-radius: 5px;
  transition: background-color 0.2s;
  
  &:hover {
    background-color: #f0f0f0;
  }

  & > div {
    margin-top: 1rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
`;

export const FileContent = styled.div`
  margin-top: 2rem;
  padding: 1rem;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 5px;
`;

export const CsvTable = styled.table`
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;

  th, td {
    border: 1px solid #ddd;
    padding: 0.5rem;
    text-align: left;
  }

  th {
    background-color: #f0f0f0;
    font-weight: bold;
  }
`;

export const CsvRow = styled.tr<{ isPass: boolean }>`
  background-color: ${({ isPass }) => (isPass ? '#e0ffe0' : '#ffe0e0')};
`;

export const CsvCell = styled.td`
  padding: 0.5rem;
  border: 1px solid #ddd;
`;

export const StatusCell = styled.td<{ isPass: boolean }>`
  font-weight: bold;
  color: ${({ isPass }) => (isPass ? 'green' : 'red')};
  text-align: center;
`;

export const ErrorMessage = styled.p`
  color: red;
  font-weight: bold;
`;
