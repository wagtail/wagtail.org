import React, {useEffect, useState} from 'react';
import {Grid} from "@mui/material";
import {useTheme} from "@mui/material/styles";
import {IPageOverviewData} from "./PageOverview.types";
import Cookies from 'js-cookie';
import CustomTypography from "../../components/custom/custom_typography/CustomTypography";


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
                (result: IPageOverviewData) => setData(result),
                (error) => console.log(error)
            )
    }

    return (
        <Grid
            container
            spacing={2}
        >
            <CustomTypography>
                {JSON.stringify(data)}
            </CustomTypography>
        </Grid>
    )
}

export default PageOverview
