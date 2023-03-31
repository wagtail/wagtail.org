import React, {useEffect, useState} from 'react';
import {styled} from '@mui/material/styles';
import {Grid} from '@mui/material';
import {IPropTypesChartDonut} from "./ChartDonut.types";
import Chart from "react-apexcharts";
import ChartWrapper from "../chart_wrapper/ChartWrapper";
import {numberFormatter} from "../../../utils/utils_numbers";
import {useTheme} from "@mui/material/styles";


const StyledChart = styled(Chart)(({theme}) => ({
    backgroundColor: theme.palette.background.default,
    padding: theme.spacing(2, 0),
    borderRadius: theme.spacing(1)
}))


const ChartDonut: React.FunctionComponent<IPropTypesChartDonut> = (props) => {
    const {
        title,
        subheader,
        data,
    } = props

    const theme = useTheme()

    const [values, setValues] = useState<number[]>([])
    const [labels, setLabels] = useState<string[]>([])
    const [colors, setColors] = useState<string[]>([])

    useEffect(() => {
        if (!!data) {
            const dataLabels: string[] = []
            const dataValues: number[] = []
            const dataColors: string[] = []

            data.map(obj => {
                dataLabels.push(obj.label)
                dataValues.push(isNaN(obj.value) ? 0 : (obj.value ?? 0))

                !!obj.color && dataColors.push(obj.color)
            })

            setValues(dataValues)
            setLabels(dataLabels)
            setColors(dataColors)
        }
    }, [data])

    return (
        <Grid item xs={12} sm={12} md={6} lg={3}>
            <ChartWrapper
                title={title}
                subheader={subheader}
            >
                <StyledChart
                    options={{
                        plotOptions: {
                            pie: {
                                donut: {
                                    size: '85%',
                                    labels: {
                                        show: true,
                                        total: {
                                            show: !!values.length,
                                            formatter: (w) => {
                                                const sum = w.globals.seriesTotals.reduce((total: number, value: number) => total + value, 0)

                                                return numberFormatter(sum, 1)
                                            },
                                            color: theme.palette.text.primary
                                        },
                                        value: {
                                            formatter: (value) => numberFormatter(Number(value), 1)
                                        }
                                    }
                                }
                            }
                        },
                        dataLabels: {
                            enabled: false,
                        },
                        legend: {
                            position: 'bottom'
                        },
                        responsive: [
                            {
                                breakpoint: 1536,
                                options: {
                                    plotOptions: {
                                        pie: {
                                            donut: {
                                                size: '80%'
                                            }
                                        }
                                    }
                                }
                            }
                        ],
                        tooltip: {
                            y: {
                                formatter: function (val, opts) {
                                    const sum = opts.globals.seriesTotals.reduce((total: number, value: number) => total + value, 0)

                                    return `${val} (${Math.round((Number(val) / sum) * 1000) / 10}%)`
                                },
                            }
                        },
                        labels: labels,
                        ...(!!colors.length && {colors}),
                    }}
                    series={values}
                    type={"donut"}
                />
            </ChartWrapper>
        </Grid>
    )
}

export default ChartDonut