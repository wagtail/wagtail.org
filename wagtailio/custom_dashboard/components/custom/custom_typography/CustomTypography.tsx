import React from 'react';
import {IPropTypesCustomTypography} from "./CustomTypography.types";
import Typography from "@mui/material/Typography";
import CustomConditionalWrapper from "../custom_conditional_wrapper/CustomConditionalWrapper";


const CustomTypography: React.FunctionComponent<IPropTypesCustomTypography> = (props) => {
    const {children} = props;

    return (
        <Typography
            {...props}
            title={typeof children === 'string' ? children : ''}
        >
            <React.Fragment>
                <CustomConditionalWrapper
                    condition={!!props.noWrap}
                    wrapper={(children) => (
                        <div
                            style={{
                                whiteSpace: 'nowrap',
                                textOverflow: 'ellipsis',
                                overflow: 'hidden',
                            }}
                            {...(typeof children === "string" && {title: children.trim()})}
                        >
                            {children}
                        </div>
                    )}
                >
                    {children}
                </CustomConditionalWrapper>
            </React.Fragment>
        </Typography>
    )
};

export default CustomTypography;