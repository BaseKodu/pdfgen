import './assets/style.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { OhVueIcon, addIcons } from "oh-vue-icons";
import { FcGoogle, BiPlus, BiDash, BiX, BiCheck, BiArrowLeft, BiArrowRight,
  BiArrowUp, BiArrowDown, BiClipboard, BiPencil, BiTrash,
  BiDownload, BiUpload, BiCheckCircle, BiXCircle,
  BiExclamationTriangle, BiInfoCircle, BiList, BiSearch,
  BiFunnel, BiGear, BiPerson, BiLock, BiUnlock, BiKey,
  BiFileText, BiCode, BiTerminal, BiArrowClockwise,
  BiQuestionCircle  } from "oh-vue-icons/icons";

addIcons(
  FcGoogle,
  BiPlus, BiDash, BiX, BiCheck, BiArrowLeft, BiArrowRight,
  BiArrowUp, BiArrowDown, BiClipboard, BiPencil, BiTrash,
  BiDownload, BiUpload, BiCheckCircle, BiXCircle,
  BiExclamationTriangle, BiInfoCircle, BiList, BiSearch,
  BiFunnel, BiGear, BiPerson, BiLock, BiUnlock, BiKey,
  BiFileText, BiCode, BiTerminal, BiArrowClockwise,
  BiQuestionCircle
);

const app = createApp(App)

app.use(router)
app.component("v-icon", OhVueIcon);

app.mount('#app')

