import React from "react";
import {createTheme} from "@mui/material/styles"
import createCache from "@emotion/cache";


declare module '@mui/material/styles' {
    interface Theme {
        navigation: {
            colors: {
                background: React.CSSProperties['color']
                content: React.CSSProperties['color']
            }
        }
    }

    interface ThemeOptions {
        navigation: {
            colors: {
                background: React.CSSProperties['color']
                content: React.CSSProperties['color']
            }
        }
    }
}

export const muiCache = createCache({
    'key': 'mui',
    'prepend': true,
})

export const theme = createTheme({
    navigation: {
        colors: {
            background: "#11101D",
            content: "lightgray",
        }
    },
    palette: {
        common: {
            black: "#000",
            white: "#fff"
        },
        primary: {
            light: "#9a126c",
            main: "#9a126c",
            dark: "#9a126c",
            contrastText: "#fafafa"
        },
        secondary: {
            light: "#384a57",
            main: "#29363f",
            dark: "#1c2932",
            contrastText: "#fafafa"
        },
        background: {
            paper: '#fff',
            default: "#f5f5f5"
        },
    }
})


