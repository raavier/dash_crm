import { extendTheme, type ThemeConfig } from '@chakra-ui/react';

const config: ThemeConfig = {
  initialColorMode: 'light',
  useSystemColorMode: false,
};

const colors = {
  vale: {
    primary: '#007E7A',      // Verde Vale - cor principal
    secondary: '#ECB11F',    // Amarelo - atenção/warning
    tertiary: '#E37222',     // Laranja
    danger: '#BB133E',       // Vermelho - dados negativos/erro
    info: '#3D7EDB',         // Azul - informações neutras
    cyan: '#00B0CA',
    success: '#69BE28',      // Verde claro - dados positivos/sucesso
    warning: '#DFDF00',      // Amarelo limão - atenção
    gray: '#747678',         // Cinza - dados neutros
    background: '#FFFFFF',
    foreground: '#474747',
    tableAccent: '#007E7A',
  },
};

const fonts = {
  heading: `'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`,
  body: `'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`,
};

const styles = {
  global: {
    body: {
      bg: 'gray.50',
      color: 'vale.foreground',
    },
  },
};

const components = {
  Card: {
    baseStyle: {
      container: {
        borderRadius: 'lg',
        boxShadow: 'sm',
        bg: 'white',
        p: 6,
      },
    },
  },
  Button: {
    baseStyle: {
      fontWeight: 'medium',
      borderRadius: 'md',
    },
    variants: {
      primary: {
        bg: 'vale.primary',
        color: 'white',
        _hover: {
          bg: 'vale.primary',
          opacity: 0.9,
        },
      },
    },
  },
};

const theme = extendTheme({
  config,
  colors,
  fonts,
  styles,
  components,
});

export default theme;
