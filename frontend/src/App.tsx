import './App.css';
import ApiTest from './components/api_test';

const App = (): JSX.Element => {
  return (
    <div className="App">
      <h1>FastAPI + React Integration Test</h1>
      <ApiTest />
    </div>
  );
};

export default App;