import React, {useEffect, useState} from 'react';
import {Grid} from "@mui/material";
import ChartKeyPerformanceIndicator
    from "../../components/charts/chart_key_performance_indicator/ChartKeyPerformanceIndicator";
import {useTheme} from "@mui/material/styles";
import PeopleAltIcon from '@mui/icons-material/PeopleAlt';
import {IPageOverviewData} from "./PageOverview.types";
import Cookies from 'js-cookie';
import ChartBarColumn from "../../components/charts/chart_bar_column/ChartBarColumn";
import ChartDonut from "../../components/charts/chart_donut/ChartDonut";


const PageOverview: React.FunctionComponent = ({children}) => {
    const theme = useTheme()

    const [data, setData] = useState<IPageOverviewData>({})

    useEffect(() => {
        const identifierTimeout = setTimeout(() => fetchData(), 200)
        const identifierInterval = setInterval(() => fetchData(), 300000)

        return () => {
            clearTimeout(identifierTimeout)
            clearInterval(identifierInterval)
        }
    }, [])

    const fetchData = () => {
        fetch(
            '/dashboard/api/overview/',
            {
                method: 'GET',
                headers: {
                    "Content-Type": "application/json",
                    "csrftoken": Cookies.get('csrftoken'),
                    "X-CSRFToken": Cookies.get('X-CSRFToken')
                },
            }
        )
            .then(res => res.json())
            .then(
                (result: IPageOverviewData) => {
                    setData(result)

                    console.log('refresh')
                },
                (error) => console.log(error)
            )
    }

    return (
        <Grid
            container
            spacing={2}
        >
            <ChartKeyPerformanceIndicator
                label={'Total Users'}
                value={data.profile?.count_total}
                icon={PeopleAltIcon}
            />
            <ChartKeyPerformanceIndicator
                label={'Users Activated'}
                value={data.profile?.count_onboard}
                icon={PeopleAltIcon}
                color={theme.palette.primary.main}
            />
            <ChartKeyPerformanceIndicator
                label={'Online Users'}
                value={data.profile?.count_online}
                icon={PeopleAltIcon}
                color={theme.palette.success.light}
            />
            <ChartKeyPerformanceIndicator
                label={'Recently Online Users'}
                value={data.profile?.count_online_recently}
                icon={PeopleAltIcon}
                color={theme.palette.warning.light}
            />
            <ChartKeyPerformanceIndicator
                label={'Offline Users'}
                value={data.profile?.count_offline}
                icon={PeopleAltIcon}
                color={theme.palette.grey[800]}
            />
            <ChartKeyPerformanceIndicator
                label={'Unavailable Users'}
                value={data.profile?.count_unavailable}
                icon={PeopleAltIcon}
                color={theme.palette.grey[500]}
            />

            <ChartDonut
                title={'Onboarding'}
                subheader={'Distribution of all users'}
                data={[
                    {
                        label: 'Onboard',
                        value: data.profile?.count_onboard,
                        color: theme.palette.primary.light,
                    },
                    {
                        label: 'Unfinished',
                        value: data.profile?.count_total - data.profile?.count_onboard,
                        color: theme.palette.grey[500],
                    },
                ]}
            />
            <ChartDonut
                title={'Online status'}
                subheader={'Distribution of onboard users'}
                data={[
                    {
                        label: 'Online',
                        value: data.profile?.count_online,
                        color: theme.palette.success.light,
                    },
                    {
                        label: 'Recently Online',
                        value: data.profile?.count_online_recently,
                        color: theme.palette.warning.light,
                    },
                    {
                        label: 'Offline',
                        value: data.profile?.count_offline,
                        color: theme.palette.grey[800]
                    }
                ]}
            />
            <ChartDonut
                title={'Availability'}
                subheader={'Distribution of onboard users'}
                data={[
                    {
                        label: 'Available',
                        value: data.profile?.count_onboard - data.profile?.count_unavailable,
                        color: theme.palette.success.light,
                    },
                    {
                        label: 'Unavailable',
                        value: data.profile?.count_unavailable,
                        color: theme.palette.grey[500]
                    }
                ]}
            />
            <ChartDonut
                title={'Gender'}
                subheader={'Distribution of onboard users'}
                data={[
                    {
                        label: 'Male',
                        value: data.profile?.count_gender.male,
                        color: theme.palette.info.light,
                    },
                    {
                        label: 'Female',
                        value: data.profile?.count_gender.female,
                        color: theme.palette.success.light,
                    },
                    {
                        label: 'Other',
                        value: data.profile?.count_gender.other,
                        color: theme.palette.warning.light,
                    },
                ]}
            />

            <ChartBarColumn
                title={'Requests'}
                subheader={'Count of requests per day'}
                data={data.activity?.trend}
                fields={['count_request']}
                colors={[theme.palette.info.light]}
                keyLabel={'date'}
            />
            <ChartBarColumn
                title={'Users'}
                subheader={'Count of new and active users per day'}
                data={data.activity?.trend}
                fields={['count_profile_total', 'count_profile_new']}
                colors={[theme.palette.info.light, theme.palette.success.light]}
                keyLabel={'date'}
                stacked={true}
            />
        </Grid>
    )
}

export default PageOverview