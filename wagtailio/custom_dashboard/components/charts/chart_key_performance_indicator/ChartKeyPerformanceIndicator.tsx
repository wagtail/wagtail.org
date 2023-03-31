import React from 'react';
import {alpha, styled} from '@mui/material/styles';
import {Card, Grid} from '@mui/material';
import {numberFormatter} from "../../../utils/utils_numbers";
import {IPropTypesChartKeyPerformanceIndicator, IStyledIconWrapper} from "./ChartKeyPerformanceIndicator.types";
import CustomTypography from "../../custom/custom_typography/CustomTypography";


const StyledCard = styled(Card)(({theme}) => ({
    textAlign: 'center',
    color: theme.palette.text.primary,
    padding: theme.spacing(5, 0),
}))

const StyledIconWrapper = styled('div')<IStyledIconWrapper>(({theme, color}) => {
    const colorIcon = color ?? theme.palette.grey[600]

    return {
        margin: 'auto',
        display: 'flex',
        borderRadius: '50%',
        alignItems: 'center',
        width: theme.spacing(8),
        height: theme.spacing(8),
        justifyContent: 'center',
        marginBottom: theme.spacing(3),
        color: colorIcon,
        backgroundImage: `linear-gradient(135deg, ${alpha(colorIcon, 0)} 0%, ${alpha(
            colorIcon,
            0.24
        )} 100%)`
    }
})


const ChartKeyPerformanceIndicator: React.FunctionComponent<IPropTypesChartKeyPerformanceIndicator> = (props) => {
    const {
        label,
        value,
        color,
    } = props

    return (
        <Grid item xs={12} sm={6} md={3} lg={2}>
            <StyledCard>
                <StyledIconWrapper color={color}>
                    <props.icon width={24} height={24}/>
                </StyledIconWrapper>

                <CustomTypography variant="h4">
                    {
                        value !== undefined
                            ? numberFormatter(value, 2)
                            : '\u00a0'
                    }
                </CustomTypography>

                <CustomTypography variant="subtitle2" color={'textSecondary'}>
                    {label}
                </CustomTypography>
            </StyledCard>
        </Grid>
    )
}

export default ChartKeyPerformanceIndicator