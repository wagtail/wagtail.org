import React from "react";


export interface IPropTypesChartDonut {
    title: string
    subheader: string
    data: {
        label: string
        value: number | undefined
        color?: string
    }[]
}
