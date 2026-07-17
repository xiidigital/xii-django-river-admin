import { createApp } from 'vue'
import App from '@/App.vue'
import vuetify from '@/vuetify'
import store from '@/store'
import router from '@/routers'

const app = createApp(App)

app.use(store)
app.use(router)
app.use(vuetify)

app.mount('#app')
