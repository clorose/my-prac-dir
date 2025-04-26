// File: C:\_YHJ\fast\frontend\src\components\FileUpload\FileUpload.tsx
// Component: FileUpload
// TypeScript React Component

import { useState, ChangeEvent, FormEvent } from 'react';
import styled from 'styled-components';
import { UploadCloud } from 'lucide-react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Button from '../ui/Button';
import Card from '../ui/Card';
import { CardHeader, CardTitle, CardContent } from '../../styles/commonStyles';

const SERVER_URL = import.meta.env.VITE_SERVER_URL || 'http://localhost:8000';

const FileUpload = (): JSX.Element => {
  const [file, setFile] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState<string>('');
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const [statusCode, setStatusCode] = useState<number | null>(null);
  const navigate = useNavigate();

  const isCSVFile = (file: File): boolean => {
    return file.type === 'text/csv' || file.name.toLowerCase().endsWith('.csv');
  };

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      const selectedFile = event.target.files[0];
      if (isCSVFile(selectedFile)) {
        setFile(selectedFile);
        setUploadStatus('');
        setStatusCode(null);
      } else {
        event.target.value = ''; // Clear the file input
        setFile(null);
        setUploadStatus('Error: Only CSV files are allowed. Please select a CSV file.');
        setStatusCode(400);
      }
    }
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!file) return;

    setIsUploading(true);
    setUploadStatus('Uploading...');
    setStatusCode(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${SERVER_URL}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 300000, // 5 minutes timeout
      });

      setStatusCode(response.status);
      setUploadStatus(`${response.data.status} File: ${response.data.filename}`);

      // Navigate to TestPage with analysisResult as state
      navigate('/test', { state: response.data });
    } catch (error) {
      console.error('Error uploading file:', error);
      if (axios.isAxiosError(error)) {
        setStatusCode(error.response?.status || 500);
        if (error.code === 'ECONNABORTED') {
          setUploadStatus('Upload timed out. The file might be too large or the connection is slow.');
        } else {
          const errorMessage = error.response?.data?.detail || error.message || 'An error occurred while uploading the file.';
          setUploadStatus(`Error: ${errorMessage}`);
        }
      } else {
        setStatusCode(500);
        setUploadStatus('An unexpected error occurred.');
      }
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <StyledCard>
      <CardHeader>
        <CardTitle>Upload CSV File</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit}>
          <UploadContainer>
            <UploadCloud size={48} />
            <UploadText>Select a CSV file for analysis</UploadText>
            <HiddenInput
              type="file"
              onChange={handleFileChange}
              id="fileInput"
              accept=".csv"
            />
            <Button onClick={() => document.getElementById('fileInput')?.click()}>
              Choose File
            </Button>
            {file && <SelectedFile>Selected file: {file.name}</SelectedFile>}
            <Button type="submit" disabled={!file || isUploading}>
              {isUploading ? 'Uploading...' : 'Upload File'}
            </Button>
            {uploadStatus && (
              <StatusMessage $isError={uploadStatus.includes('Error')}>
                {uploadStatus}
                {statusCode && ` (Status Code: ${statusCode})`}
              </StatusMessage>
            )}
          </UploadContainer>
        </form>
      </CardContent>
    </StyledCard>
  );
};

export default FileUpload;

const StyledCard = styled(Card)`
  width: 100%;
`;

const UploadContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1.5rem;
  background-color: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
`;

const UploadText = styled.p`
  font-size: 0.875rem;
  color: #4b5563;
  margin-bottom: 1rem;
  text-align: center;
`;

const HiddenInput = styled.input`
  display: none;
`;

const SelectedFile = styled.p`
  margin-top: 1rem;
  font-size: 0.875rem;
  color: #4b5563;
`;

const StatusMessage = styled.p<{ $isError: boolean }>`
  margin-top: 1rem;
  font-size: 0.875rem;
  color: ${props => props.$isError ? 'red' : 'green'};
  font-weight: bold;
`;