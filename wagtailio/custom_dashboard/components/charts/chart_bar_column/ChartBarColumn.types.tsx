import React from "react";
import {IObject} from "../../../utils/utils_types";


export interface IPropTypesChartBarColumn {
    title: string
    subheader: string
    data: IObject<string | number>[]
    fields: string[]
    colors?: string[]
    keyLabel: string
    stacked?: boolean
}

export interface IChartSeries {
    name: string
    data: number[]
}