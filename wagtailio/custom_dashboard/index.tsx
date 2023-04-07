import React from 'react';
import ReactDOM from 'react-dom';
import {theme} from "./src/theme";
import {ThemeProvider} from '@mui/material/styles';
import NavigationRouter from "./components/navigation/navigation_router/NavigationRouter";


ReactDOM.render(
    <React.StrictMode>
        <ThemeProvider theme={theme}>
            <NavigationRouter />
        </ThemeProvider>
    </React.StrictMode>,
    document.getElementById('root')
)
