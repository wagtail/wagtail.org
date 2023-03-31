import {SvgIcon} from "@mui/material";
import {ComponentType} from "react";


export interface IPropTypesLayoutNavigation {}

export interface IPropTypesLayoutNavigationItem extends ILayoutNavigationItem {
    isExternal: boolean
}

export interface ILayoutNavigationItem {
    icon: typeof SvgIcon
    label: string
    endpoint: string
    component: ComponentType
    badge?: number
}