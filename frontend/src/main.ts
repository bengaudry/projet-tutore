import "./assets/main.css"
import "./assets/typography.css"
import "@flaticon/flaticon-uicons/css/regular/rounded.css";

import { createApp } from "vue"
import App from "./App.vue"
import router from "./router"
import VueApexCharts from "vue3-apexcharts"

const app = createApp(App)
app.use(router)
app.use(VueApexCharts)
app.component("apexchart", VueApexCharts)
app.mount("#app")
