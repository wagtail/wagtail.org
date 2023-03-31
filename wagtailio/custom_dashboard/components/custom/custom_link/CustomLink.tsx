import React from "react";
import {IPropTypesCustomLink} from "./CustomLink.types";
import {Link} from "react-router-dom";
import CustomConditionalWrapper from "../custom_conditional_wrapper/CustomConditionalWrapper";


const CustomLink: React.FunctionComponent<IPropTypesCustomLink> = (props) => {
    const {
        url,
        isExternal,
        children
    } = props;

    return (
        <CustomConditionalWrapper
            condition={!isExternal}
            wrapper={(children) => (
                <Link
                    to={url}
                    style={{
                        textDecoration: 'none',
                        color: 'inherit',
                    }}
                >
                    {children}
                </Link>
            )}
            wrapperFalse={(children) => (
                <a
                    href={url}
                    target={"_blank"}
                    style={{
                        textDecoration: 'none',
                        color: 'inherit'
                    }}
                >
                    {children}
                </a>
            )}
        >
            {children}
        </CustomConditionalWrapper>
    )
}


export default CustomLink