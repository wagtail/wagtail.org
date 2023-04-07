import React from "react";
import {IPropTypesCustomConditionalWrapper} from "./CustomConditionalWrapper.types";


// https://blog.hackages.io/conditionally-wrap-an-element-in-react-a8b9a47fab2
const CustomConditionalWrapper: React.FunctionComponent<IPropTypesCustomConditionalWrapper> = (props) => {
    const {condition, wrapper, wrapperFalse, children} = props;

    return (
        <React.Fragment>
            {
                condition
                    ? wrapper(children)
                    : !!wrapperFalse
                        ? wrapperFalse(children)
                        : children
            }
        </React.Fragment>
    )
}


export default CustomConditionalWrapper