import { ChakraProvider } from '@chakra-ui/react';
import theme from './theme';
import { DashboardProvider } from './context/DashboardContext';
import MainLayout from './components/Layout/MainLayout';
import DashboardPage from './pages/DashboardPage';

function App() {
  return (
    <ChakraProvider theme={theme}>
      <DashboardProvider>
        <MainLayout>
          <DashboardPage />
        </MainLayout>
      </DashboardProvider>
    </ChakraProvider>
  );
}

export default App;
