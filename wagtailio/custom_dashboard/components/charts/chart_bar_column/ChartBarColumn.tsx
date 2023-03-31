import React, {useEffect, useState} from 'react';
import {styled} from '@mui/material/styles';
import {Grid} from '@mui/material';
import {IChartSeries, IPropTypesChartBarColumn} from "./ChartBarColumn.types";
import Chart from "react-apexcharts";
import {IObject} from "../../../utils/utils_types";
import ChartWrapper from "../chart_wrapper/ChartWrapper";


const StyledChart = styled(Chart)(({theme}) => ({
    backgroundColor: theme.palette.background.default,
    padding: theme.spacing(2, 2, 0),
    borderRadius: theme.spacing(1)
}))


const ChartBarColumn: React.FunctionComponent<IPropTypesChartBarColumn> = (props) => {
    const {
        title,
        subheader,
        data,
        fields,
        colors,
        keyLabel,
        stacked,
    } = props

    const [values, setValues] = useState<IChartSeries[]>([])
    const [labels, setLabels] = useState<string[]>([''])

    useEffect(() => {
        if (!!data) {
            const dataLabels: string[] = []
            const dataValues = fields.reduce((dict: IObject<number[]>, field) => {
                dict[field] = []

                return dict
            }, {})

            data.forEach((obj) => {
                dataLabels.push(`${obj[keyLabel]}`)

                fields.forEach(field => {
                    dataValues[field].push(obj[field] as number)
                })
            })

            setLabels(!!dataLabels.length ? dataLabels : [''])
            setValues(
                Object.keys(dataValues).map(key => ({
                    name: key,
                    data: dataValues[key]
                }))
            )
        }
    }, [data])

    return (
        <Grid item xs={12} sm={12} md={12} lg={6}>
            <ChartWrapper
                title={title}
                subheader={subheader}
            >
                <StyledChart
                    options={{
                        plotOptions: {
                            bar: {
                                horizontal: false,
                                columnWidth: '55%',
                            },
                        },
                        dataLabels: {
                            enabled: false
                        },
                        stroke: {
                            show: true,
                            width: 2,
                            colors: ['transparent']
                        },
                        fill: {
                            opacity: 1
                        },
                        xaxis: {
                            categories: labels
                        },
                        chart: {
                            stacked: !!stacked,
                        },
                        ...(!!colors?.length && {colors}),
                    }}
                    series={values}
                    type={"bar"}
                    height={350}
                />
            </ChartWrapper>
        </Grid>
    )
}

export default ChartBarColumn