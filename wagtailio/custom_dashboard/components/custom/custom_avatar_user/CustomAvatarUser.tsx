import * as React from 'react';
import {styled, useTheme} from '@mui/material/styles';
import Avatar from '@mui/material/Avatar';
import Badge from '@mui/material/Badge';
import Box from '@mui/material/Box';
import {IPropTypesCustomAvatarUser} from "./CustomAvatarUser.types";


const StyledBadge = styled(Badge, {
    shouldForwardProp: (prop) => prop !== "statusColor",
})<{ statusColor: string}>(({theme, statusColor}) => ({
    '& .MuiBadge-badge': {
        backgroundColor: statusColor,
        color: statusColor,
        boxShadow: `0 0 0 2px ${theme.palette.background.paper}`,
        '&::after': {
            position: 'absolute',
            top: -1,
            left: -1,
            width: '100%',
            height: '100%',
            borderRadius: '50%',
            animation: 'ripple 1.2s infinite ease-in-out',
            border: '1px solid currentColor',
            content: '""',
        },
    },
    '@keyframes ripple': {
        '0%': {
            transform: 'scale(.8)',
            opacity: 1,
        },
        '100%': {
            transform: 'scale(2)',
            opacity: 0,
        },
    },
}))

const CustomAvatarUser: React.FunctionComponent<IPropTypesCustomAvatarUser> = (props) => {
    const {
        name,
        status
    } = props

    const theme = useTheme()

    return (
        <Box>
            <StyledBadge
                overlap="circular"
                anchorOrigin={{
                    vertical: 'bottom',
                    horizontal: 'right'
                }}
                variant="dot"
                statusColor={
                    status === 'online'
                        ? theme.palette.success.light
                        : status === 'unavailable'
                            ? theme.palette.warning.light
                            : theme.palette.error.light
                }
            >
                <Avatar
                    alt={name}
                    sx={{
                        width: '32px',
                        height: '32px'
                    }}
                >
                    {name.charAt(0).toUpperCase()}
                </Avatar>
            </StyledBadge>
        </Box>
    )
}

export default CustomAvatarUser