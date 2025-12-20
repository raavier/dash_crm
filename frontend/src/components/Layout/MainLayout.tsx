import { Box } from '@chakra-ui/react';
import Header from './Header';

interface MainLayoutProps {
  children: React.ReactNode;
}

const MainLayout = ({ children }: MainLayoutProps) => {
  return (
    <Box minH="100vh" bg="gray.50">
      <Header />
      <Box maxW="1920px" mx="auto" p={6}>
        {children}
      </Box>
    </Box>
  );
};

export default MainLayout;
