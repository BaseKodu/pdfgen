import './assets/style.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { OhVueIcon, addIcons } from "oh-vue-icons";
import { FcGoogle } from "oh-vue-icons/icons";

addIcons(FcGoogle);

const app = createApp(App)

app.use(router)
app.component("v-icon", OhVueIcon);

app.mount('#app')

