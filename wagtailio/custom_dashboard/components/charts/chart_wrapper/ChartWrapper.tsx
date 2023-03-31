import React from 'react';
import {styled} from '@mui/material/styles';
import {Card} from '@mui/material';
import CustomTypography from "../../custom/custom_typography/CustomTypography";
import {IPropTypesChartWrapper} from "./ChartWrapper.types";


const StyledCard = styled(Card)(({theme}) => ({
    color: theme.palette.text.primary,
    padding: theme.spacing(3, 3),
}))

const StyledTitle = styled(CustomTypography)(({theme}) => ({
    padding: theme.spacing(0, 2, 0)
}))

const StyledSubheader = styled(CustomTypography)(({theme}) => ({
    padding: theme.spacing(0, 2, 2)
}))


const ChartWrapper: React.FunctionComponent<IPropTypesChartWrapper> = (props) => {
    const {
        title,
        subheader,
        children
    } = props

    return (
        <StyledCard>
            <div>
                <StyledTitle variant={'h6'}>
                    {title}
                </StyledTitle>

                <StyledSubheader
                    variant={'subtitle2'}
                    color={'textSecondary'}
                >
                    {subheader}
                </StyledSubheader>
            </div>

            {children}
        </StyledCard>
    )
}

export default ChartWrapper