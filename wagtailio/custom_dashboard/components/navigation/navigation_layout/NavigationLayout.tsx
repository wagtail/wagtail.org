import * as React from 'react';
import {useEffect, useState} from 'react';
import {useTheme} from '@mui/material/styles';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import StorageIcon from '@mui/icons-material/Storage';
import MenuIcon from '@mui/icons-material/Menu';
import ExitToAppIcon from '@mui/icons-material/ExitToApp';
import LogoSVG from '../../../assets/icons/logo/logo_full.svg';
import navbarList from '../navigation_structure/NavigationStructure';
import CustomAvatarUser from '../../custom/custom_avatar_user/CustomAvatarUser';
import {IPropTypesLayoutNavigation} from "./NavigationLayout.types";
import NavigationLayoutItem from "./NavigationLayoutItem";
import CustomLink from "../../custom/custom_link/CustomLink";


const NavigationLayout: React.FunctionComponent<IPropTypesLayoutNavigation> = (props) => {
    const {
        children
    } = props

    const theme = useTheme();

    console.log(theme)

    const user = {
        // name: JSON.parse(document.getElementById('user_name').textContent),
        // function: JSON.parse(document.getElementById('user_function').textContent),
    }

    const drawerWidthOpen = 240
    const paddingIconButton = 10
    const marginIconButton = 14
    const iconFontSize = 20

    const drawerWidthClosed = (paddingIconButton + marginIconButton) * 2 + iconFontSize

    const [drawerIsOpen, setDrawerIsOpen] = useState(false)
    const [drawerWidth, setDrawerWidth] = useState<number>(drawerWidthClosed)

    useEffect(() => {
        setDrawerWidth(drawerIsOpen ? drawerWidthOpen : drawerWidthClosed)
    }, [drawerIsOpen])

    return (
        <Box
            sx={{
                display: 'flex',
            }}
        >
            <Drawer
                variant="permanent"
                sx={{
                    position: 'absolute',
                    width: drawerWidth,
                    transition: theme.transitions.create('width', {
                        easing: theme.transitions.easing.sharp,
                        duration: drawerIsOpen
                            ? theme.transitions.duration.leavingScreen
                            : theme.transitions.duration.enteringScreen,
                    }),
                    '& ::-webkit-scrollbar': {
                        width: 0,
                    },
                    '& .MuiDrawer-paper': {
                        marginLeft: '0',
                        overflowX: 'hidden',
                        width: drawerWidth,
                        borderRight: '0px',
                        borderRadius: '0px 0px 0px 0px',
                        boxShadow: theme.shadows[8],
                        backgroundColor: theme.navigation.colors.background,
                        transition: theme.transitions.create(
                            'width',
                            {
                                easing: theme.transitions.easing.sharp,
                                duration: drawerIsOpen
                                    ? theme.transitions.duration.leavingScreen
                                    : theme.transitions.duration.enteringScreen,
                            }
                        ),
                    },
                }}
            >
                <Box
                    sx={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        height: '42px',
                        width: 'auto',
                        backgroundColor: 'transparent',
                        margin: '2px 14px 14px 14px',
                        padding: '12px 0px',
                        borderBottom: `1px solid ${theme.navigation.colors.content}`,
                        alignItems: 'flex-end',
                    }}
                >
                    <Box
                        sx={{
                            flexShrink: 0,
                            display: drawerIsOpen ? 'flex' : 'none',
                            margin: '10px 5px',
                            justifyContent: 'center',
                            alignItems: 'center'
                        }}
                    >
                        <LogoSVG
                            width={100}
                            height={25}
                            fill={theme.navigation.colors.content}
                        />
                    </Box>

                    <Button
                        onClick={() => setDrawerIsOpen(prevState => !prevState)}
                        sx={{
                            minWidth: 'initial',
                            padding: '10px',
                            color: 'gray',
                            borderRadius: '8px',
                            backgroundColor: 'transparent',
                            '&:hover': {
                                backgroundColor: '#26284687',
                            },
                        }}
                    >
                        <MenuIcon
                            sx={{
                                fontSize: '20px',
                                color: theme.navigation.colors.content
                            }}
                        />
                    </Button>
                </Box>

                <List dense={true} disablePadding={true}>
                    {
                        navbarList.map((item) => (
                            <NavigationLayoutItem
                                key={item.label}
                                isExternal={false}
                                {...item}
                            />
                        ))
                    }
                </List>

                <Box
                    sx={{
                        flexGrow: 1,
                    }}
                />

                <List dense={true} disablePadding={true}>
                    <NavigationLayoutItem
                        label={'Admin Panel'}
                        component={React.Fragment}
                        icon={StorageIcon}
                        endpoint={'/admin'}
                        isExternal={true}
                    />
                </List>

                <Box
                    sx={{
                        display: 'flex',
                        justifyContent: 'flex-start',
                        alignItems: 'center',
                        alignContents: 'center',
                        margin: '14px 14px 2px 14px',
                        padding: '12px 4px',
                        borderTop: `1px solid ${theme.navigation.colors.content}`,
                    }}
                >
                    <Box
                        sx={{
                            display: 'flex',
                            marginRight: '18px',
                            paddingLeft: '0px',
                            alignItems: 'center',
                            alignContent: 'center',
                        }}
                    >
                        {/*<CustomAvatarUser*/}
                        {/*    name={user.name}*/}
                        {/*    status={'online'}*/}
                        {/*/>*/}
                    </Box>

                    <Box
                        sx={{
                            display: 'flex',
                            flexDirection: 'column',
                            flexGrow: 1,
                        }}
                    >
                        <Typography
                            component="span"
                            variant="body2"
                            noWrap={true}
                            sx={{
                                width: 110,
                                display: 'block',
                                whiteSpace: 'nowrap',
                                lineHeight: 'inherit',
                                color: theme.navigation.colors.content,
                                marginTop: '5px',
                                marginBottom: '3px'
                            }}
                        >
                            {/*{user.name}*/}
                        </Typography>

                        <Typography
                            component="span"
                            variant="caption"
                            noWrap={true}
                            sx={{
                                width: 110,
                                display: 'block',
                                color: theme.navigation.colors.content,
                                margin: 0,
                                fontStyle: 'italic'
                            }}
                        >
                            {/*{!!user.name && user.function}*/}
                        </Typography>
                    </Box>

                    <CustomLink url={'/admin/logout/'} isExternal={true}>
                        <IconButton
                            sx={{color: theme.navigation.colors.content}}
                        >
                            <ExitToAppIcon/>
                        </IconButton>
                    </CustomLink>

                </Box>
            </Drawer>

            <Box
                component="main"
                sx={{
                    marginLeft: {
                        xs: `${drawerWidthClosed}px`,
                        // sm: `${drawerWidth}px`
                    },
                    padding: theme.spacing(2),
                    flexGrow: 1,
                }}
            >
                {children}
            </Box>
        </Box>
    )
}

export default NavigationLayout
