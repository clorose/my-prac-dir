import { useEffect, useState } from 'react';
import axios from 'axios';
import { PageContainer, MainContent } from '../../styles/commonStyles';
import { FileList, FileItem, FileContent, CsvTable, CsvRow, CsvCell, StatusCell, ErrorMessage } from './model.style';

interface FileInfo {
  name: string;
  path: string;
  isDirectory: boolean;
}

const SERVER_URL = import.meta.env.VITE_SERVER_URL || 'http://localhost:8000';

const ModelViewer = () => {
  const [files, setFiles] = useState<FileInfo[]>([]);
  const [selectedFile, setSelectedFile] = useState<string | null>(null);
  const [csvFile, setCsvFile] = useState<File | null>(null);
  const [csvContent, setCsvContent] = useState<string[][] | null>(null);
  const [predictions, setPredictions] = useState<number[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    axios.get(`${SERVER_URL}/api/files`)
      .then(response => {
        setFiles(response.data);
      })
      .catch(error => {
        console.error('Error fetching files:', error);
        setError('Failed to load files');
      });
  }, []);

  const handleFileClick = (filePath: string) => {
    if (selectedFile === filePath) {
      setSelectedFile(null);
      setCsvFile(null);
      setCsvContent(null);
      setPredictions(null);
    } else {
      setSelectedFile(filePath);
      setCsvFile(null);
      setCsvContent(null);
      setPredictions(null);
    }
  };

  const handleCsvUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0] && selectedFile) {
      const file = event.target.files[0];
      setCsvFile(file);
  
      const formData = new FormData();
      formData.append('file', file);
      formData.append('selected_model', selectedFile);
  
      try {
        const response = await axios.post(`${SERVER_URL}/api/predict`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });
        const { predictions, csvData } = response.data;
  
        setCsvContent(csvData);
        setPredictions(predictions);
      } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
          console.error('Error during prediction:', error.response.data);
          setError(`Prediction failed: ${error.response.data.detail}`);
        } else {
          console.error('Unexpected error:', error);
          setError('An unexpected error occurred during prediction.');
        }
      }
    }
  };

  const renderCsvTable = () => {
    if (!csvContent || !predictions) return null;
    return (
      <CsvTable>
        <thead>
          <tr>
            {csvContent[0].map((header, index) => (
              <th key={index}>{header}</th>
            ))}
            <th>합/불 여부</th>
          </tr>
        </thead>
        <tbody>
          {csvContent.slice(1).map((row, rowIndex) => (
            <CsvRow key={rowIndex} isPass={predictions[rowIndex] === 1}>
              {row.map((cell, cellIndex) => (
                <CsvCell key={cellIndex}>{cell}</CsvCell>
              ))}
              <StatusCell isPass={predictions[rowIndex] === 1}>
                {predictions[rowIndex]}
              </StatusCell>
            </CsvRow>
          ))}
        </tbody>
      </CsvTable>
    );
  };

  if (error) {
    return <ErrorMessage>{error}</ErrorMessage>;
  }

  return (
    <PageContainer>
      <MainContent>
        <h2>Model Viewer</h2>
        <div>
          <FileList>
            {selectedFile ? (
              <>
                <FileItem onClick={() => handleFileClick(selectedFile)}>
                  📄 {files.find(file => file.path === selectedFile)?.name}
                </FileItem>
                <FileContent>
                  <input type="file" accept=".csv" onChange={handleCsvUpload} />
                  {csvFile && (
                    <>
                      <h4>{csvFile.name}</h4>
                      {renderCsvTable()}
                    </>
                  )}
                </FileContent>
              </>
            ) : (
              files.map((file) => (
                <FileItem key={file.path} onClick={() => handleFileClick(file.path)}>
                  📄 {file.name}
                </FileItem>
              ))
            )}
          </FileList>
        </div>
      </MainContent>
    </PageContainer>
  );
};

export default ModelViewer;
