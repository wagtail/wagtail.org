import {ReactNode} from "react";


export interface IPropTypesCustomConditionalWrapper {
    condition: boolean
    wrapper: (children: ReactNode) => any
    wrapperFalse?: (children: ReactNode) => any
}
