import { ChakraProvider } from '@chakra-ui/react';
import theme from './theme';
import { DashboardProvider } from './context/DashboardContext';
import { ChatProvider } from './context/ChatContext';
import MainLayout from './components/Layout/MainLayout';
import DashboardPage from './pages/DashboardPage';
import ChatWidget from './components/Chat/ChatWidget';

function App() {
  return (
    <ChakraProvider theme={theme}>
      <DashboardProvider>
        <ChatProvider>
          <MainLayout>
            <DashboardPage />
            <ChatWidget />
          </MainLayout>
        </ChatProvider>
      </DashboardProvider>
    </ChakraProvider>
  );
}

export default App;
