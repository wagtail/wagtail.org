import * as React from 'react';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import Badge from '@mui/material/Badge';
import Tooltip from '@mui/material/Tooltip';
import Chip from '@mui/material/Chip';
import {IPropTypesLayoutNavigationItem} from "./NavigationLayout.types";
import CustomConditionalWrapper from "../../custom/custom_conditional_wrapper/CustomConditionalWrapper";
import CustomLink from "../../custom/custom_link/CustomLink";


const NavigationLayoutItem: React.FunctionComponent<IPropTypesLayoutNavigationItem> = (props) => {
    const {
        label,
        badge,
        endpoint,
        isExternal,
    } = props

    return (
        <Tooltip
            title={label}
            placement={'right'}
            componentsProps={{
                tooltip: {
                    sx: {
                        backgroundColor: 'gray',
                        color: 'white',
                        marginLeft: '22px !important',
                        boxShadow: '0px 0px 22px -2px rgba(0,0,0,0.20)',
                    },
                },
            }}
        >
            <div>
                <CustomLink url={endpoint} isExternal={isExternal}>
                    <ListItemButton
                        sx={{
                            margin: '6px 14px',
                            padding: '10px',
                            borderRadius: '8px',
                            '&:hover': {
                                backgroundColor: '#26284687',
                            },
                        }}
                    >
                        <ListItemIcon sx={{minWidth: '46px'}}>
                            <CustomConditionalWrapper
                                condition={!!badge}
                                wrapper={(children) => (
                                    <Badge
                                        badgeContent={badge}
                                        color="secondary"
                                        variant="dot"
                                    >
                                        {children}
                                    </Badge>
                                )}
                            >
                                <props.icon
                                    sx={{
                                        fontSize: '20px',
                                        color: 'lightgray'
                                    }}
                                />
                            </CustomConditionalWrapper>
                        </ListItemIcon>

                        <ListItemText
                            primary={label}
                            primaryTypographyProps={{
                                variant: 'body2',
                            }}
                            sx={{
                                display: 'inline',
                                margin: '0px',
                                overflowX: 'hidden',
                                color: 'lightgray',
                                whiteSpace: 'nowrap',
                                minWidth: '126px',
                            }}
                        />

                        {
                            !!badge && (
                                <Chip
                                    label={badge}
                                    color={'secondary'}
                                    size="small"
                                    sx={{height: 'auto'}}
                                />
                            )
                        }
                    </ListItemButton>
                </CustomLink>
            </div>
        </Tooltip>
    )
}

export default NavigationLayoutItem