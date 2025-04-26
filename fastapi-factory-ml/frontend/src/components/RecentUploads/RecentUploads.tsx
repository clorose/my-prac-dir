// File: C:\_YHJ\fast\frontend\src\components\RecentUploads\RecentUploads.tsx
// Component: RecentUploads
// TypeScript React Component

import styled from 'styled-components';
import { File, CheckCircle, AlertCircle } from 'lucide-react';
import Card from '../ui/Card';
import { CardHeader, CardTitle, CardContent } from '../../styles/commonStyles';
import { UploadItem } from "../../types"

// Mock data for recent uploads
const recentUploads: UploadItem[] = [
  { id: 1, name: 'data_analysis_2023.csv', date: '2023-09-30', status: 'completed' },
  { id: 2, name: 'quality_metrics_q3.csv', date: '2023-09-29', status: 'processing' },
  { id: 3, name: 'production_log.csv', date: '2023-09-28', status: 'completed' },
];

// 타입: () => JSX.Element
const RecentUploads = () => {
  return (
    <StyledCard>
      <CardHeader>
        <CardTitle>Recent Uploads</CardTitle>
      </CardHeader>
      <CardContent>
        <UploadList>
          {recentUploads.map((upload) => (
            <UploadListItem key={upload.id}>
              <UploadInfo>
                <StyledFile />
                <div>
                  <FileName>{upload.name}</FileName>
                  <UploadDate>{upload.date}</UploadDate>
                </div>
              </UploadInfo>
              <StatusIcon>
                {upload.status === 'completed' ? (
                  <CheckCircle className="text-green-500" />
                ) : (
                  <AlertCircle className="text-yellow-500" />
                )}
              </StatusIcon>
            </UploadListItem>
          ))}
        </UploadList>
      </CardContent>
    </StyledCard>
  );
};

export default RecentUploads;

const StyledCard = styled(Card)`
  width: 100%;
`;

const UploadList = styled.ul`
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const UploadListItem = styled.li`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0;
  border-bottom: 1px solid #e5e7eb;

  &:last-child {
    border-bottom: none;
  }
`;

const UploadInfo = styled.div`
  display: flex;
  align-items: center;
`;

const StyledFile = styled(File)`
  width: 1.25rem;
  height: 1.25rem;
  color: #9ca3af;
  margin-right: 0.75rem;
`;

const FileName = styled.p`
  font-size: 0.875rem;
  font-weight: 500;
  color: #111827;
`;

const UploadDate = styled.p`
  font-size: 0.75rem;
  color: #6b7280;
`;

const StatusIcon = styled.div`
  width: 1.25rem;
  height: 1.25rem;
`;