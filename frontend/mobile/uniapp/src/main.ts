// @ts-nocheck
import { createSSRApp } from "vue";
import App from "./App.vue";
import { onLoad } from "@dcloudio/uni-app";

export function createApp() {
  const app = createSSRApp(App);
  return {
    app,
  };
}