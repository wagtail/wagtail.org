import React from "react";
import {SvgIcon} from "@mui/material";

export interface IStyledIconWrapper {
    color?: React.CSSProperties['color']
}

export interface IPropTypesChartKeyPerformanceIndicator extends IStyledIconWrapper {
    label: string
    value?: number
    icon: typeof SvgIcon
}