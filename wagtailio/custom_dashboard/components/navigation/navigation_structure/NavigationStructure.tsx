import DashboardOutlined from '@mui/icons-material/DashboardOutlined';
import Person from '@mui/icons-material/Person';
import Analytics from '@mui/icons-material/Analytics';
import {ILayoutNavigationItem} from "../navigation_layout/NavigationLayout.types";
import PageOverview from "../../../pages/page_overview/PageOverview";
import PageAnalytics from "../../../pages/page_analytics/PageAnalytics";
import PageProfile from "../../../pages/page_profile/PageProfile";


const navigationStructure: ILayoutNavigationItem[] = [
    {
        icon: DashboardOutlined,
        label: 'Dashboard',
        component: PageOverview,
        endpoint: '/',
        badge: 0,
    },
    {
        icon: Person,
        label: 'Profiles',
        component: PageProfile,
        endpoint: '/profiles',
        badge: 0,
    },
    {
        icon: Analytics,
        label: 'Analytics',
        component: PageAnalytics,
        endpoint: '/analytics',
        badge: 0,
    },
]

export default navigationStructure
