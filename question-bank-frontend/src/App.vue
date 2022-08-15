<template>
  <div>
    <!--    <router-link to="/">Home</router-link> |-->
    <!--    <router-link to="/about">About</router-link>-->
    <!--    头部-->
    <Headerup v-if="isRouterAlive"/>
    <!--    主体-->
    <div style="display: flex">
      <!--      侧边栏-->
      <Aside/>
      <!--      内容-->
      <router-view style="flex: 1" @login="handleLogin"/>
    </div>
  </div>
</template>

<script>
import Headerup from "@/components/Headerup";
import Aside from "@/components/Aside";
import global from "@/components/Global";
import {ElMessage} from "element-plus";

export default {
  name: "Layout",
  provide() {
    return {
      reload: this.reload
    }
  },
  components: {
    Headerup,
    Aside
  },
  data() {
    return {
      isRouterAlive: true
    }
  },
  methods: {
    handleLogin() {
      ElMessage.success('Login succeeded')
      this.reload()
    },
    reload() {
      this.isRouterAlive = false
      this.$nextTick(function() {this.isRouterAlive = true})
    }
  }
}
</script>

