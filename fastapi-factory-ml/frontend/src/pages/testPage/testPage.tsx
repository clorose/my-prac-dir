import React from 'react';
import { useLocation } from 'react-router-dom';
import {
  PageContainer,
  Header,
  HeaderContent,
  Title,
  MainContent
} from '../../styles/commonStyles';
import styled from 'styled-components';
import { Table, TableBody, TableCell, TableHead, TableRow } from '@mui/material';

// 업로드 결과 인터페이스
interface UploadResult {
  filename: string;
  status: string;
}

// ML 결과 인터페이스
interface MLResult {
  error?: string;
  accuracy?: number;
  f1_score?: number;
  auc?: number;
  classification_report?: Record<string, any>;
}

// 전체 분석 결과 인터페이스
interface AnalysisResult {
  upload_result: UploadResult;
  ml_result: MLResult;
}

const TestPage: React.FC = () => {
  const location = useLocation();
  const analysisResult = location.state as AnalysisResult | undefined;

  // 콘솔에 현재 상태 로깅 (디버깅용)
  console.log("Location state:", location.state);
  console.log("Analysis result:", analysisResult);

  // 분석 결과가 없는 경우
  if (!analysisResult) {
    console.log("No analysis result available");
    return (
      <PageContainer>
        <Header>
          <HeaderContent>
            <Title>No Analysis Data Available</Title>
          </HeaderContent>
        </Header>
        <MainContent>
          <p>No data available. Please upload a file first.</p>
          {/* 디버그 정보 표시 */}
          <p>Debug info:</p>
          <pre>{JSON.stringify(location.state, null, 2)}</pre>
        </MainContent>
      </PageContainer>
    );
  }

  const { upload_result, ml_result } = analysisResult;

  // ML 처리 중 에러가 발생한 경우
  if (ml_result.error) {
    return (
      <PageContainer>
        <Header>
          <HeaderContent>
            <Title>Analysis Error</Title>
          </HeaderContent>
        </Header>
        <MainContent>
          <h2>File: {upload_result.filename}</h2>
          <p>Status: {upload_result.status}</p>
          <ErrorMessage>Error: {ml_result.error}</ErrorMessage>
          <p>The analysis could not be completed due to an error. Please check your data and try again.</p>
        </MainContent>
      </PageContainer>
    );
  }

  // 분류 보고서 렌더링 함수
  const renderClassificationReport = () => {
    if (!ml_result.classification_report) return null;

    const headers = ["Label", "Precision", "Recall", "F1-Score", "Support"];
    const rows = Object.entries(ml_result.classification_report).filter(([key]) => !["accuracy", "macro avg", "weighted avg"].includes(key));
    const summary = Object.entries(ml_result.classification_report).filter(([key]) => ["accuracy", "macro avg", "weighted avg"].includes(key));

    return (
      <div>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                {headers.map((header) => (
                  <TableCell key={header}><strong>{header}</strong></TableCell>
                ))}
              </TableRow>
            </TableHead>
            <TableBody>
              {rows.map(([label, metrics]: [string, any]) => (
                <TableRow key={label}>
                  <TableCell>{label}</TableCell>
                  <TableCell>{metrics.precision ? metrics.precision.toFixed(4) : 'N/A'}</TableCell>
                  <TableCell>{metrics.recall ? metrics.recall.toFixed(4) : 'N/A'}</TableCell>
                  <TableCell>{metrics["f1-score"] ? metrics["f1-score"].toFixed(4) : 'N/A'}</TableCell>
                  <TableCell>{metrics.support ?? 'N/A'}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
        <SummaryContainer>
          {summary.map(([key, value]: [string, any]) => (
            <div key={key} style={{ marginBottom: '1rem' }}>
              <strong>{key.toUpperCase()}:</strong>
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      {Object.keys(value).map((subKey) => (
                        <TableCell key={subKey}><strong>{subKey}</strong></TableCell>
                      ))}
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    <TableRow>
                      {Object.values(value).map((subValue: any, index: number) => (
                        <TableCell key={index}>{typeof subValue === 'number' ? subValue.toFixed(4) : String(subValue)}</TableCell>
                      ))}
                    </TableRow>
                  </TableBody>
                </Table>
              </TableContainer>
            </div>
          ))}
        </SummaryContainer>
      </div>
    );
  };

  // 메인 렌더링
  return (
    <PageContainer>
      <Header>
        <HeaderContent>
          <Title>Analysis Results</Title>
        </HeaderContent>
      </Header>
      <MainContent>
        <h2>File: {upload_result.filename}</h2>
        <p>Status: {upload_result.status}</p>
        <h3>Model Performance Metrics</h3>
        {ml_result.accuracy && <p>Accuracy: {(ml_result.accuracy * 100).toFixed(2)}%</p>}
        {ml_result.f1_score && <p>F1 Score: {ml_result.f1_score.toFixed(4)}</p>}
        {ml_result.auc && <p>AUC: {ml_result.auc.toFixed(4)}</p>}
        <h3>Classification Report</h3>
        {renderClassificationReport()}
      </MainContent>
    </PageContainer>
  );
};

export default TestPage;

// 스타일 컴포넌트
const TableContainer = styled.div`
  margin-top: 2rem;
  overflow-x: auto;
`;

const SummaryContainer = styled.div`
  margin-top: 2rem;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 8px;
`;

const ErrorMessage = styled.p`
  color: red;
  font-weight: bold;
`;