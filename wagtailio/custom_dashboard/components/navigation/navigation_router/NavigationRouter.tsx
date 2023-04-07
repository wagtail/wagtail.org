import React from 'react';
import {BrowserRouter as Router, Route, Routes} from "react-router-dom";
import NavigationLayout from "../navigation_layout/NavigationLayout";
import navigationStructure from "../navigation_structure/NavigationStructure";


const NavigationRouter: React.FunctionComponent = () => {
    return (
        <Router basename='/dashboard/'>
            <Routes>
                {
                    navigationStructure.map((route) => (
                        <Route
                            key={route.endpoint}
                            path={route.endpoint}
                            element={(
                                <NavigationLayout>
                                    <route.component />
                                </NavigationLayout>
                            )}
                        />
                    ))
                }
            </Routes>
        </Router>
    )
}

export default NavigationRouter
