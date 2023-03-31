export interface IPageOverviewData {
    profile?: {
        count_total: number
        count_onboard: number
        count_online: number
        count_online_recently: number
        count_offline: number
        count_unavailable: number
        count_gender: {
            male?: number
            female?: number
            other?: number
        }
    },
    activity?: {
        trend: {
            date: string
            count_request: number
            count_profile_total: number
            count_profile_new: number
        }[]
    }
}