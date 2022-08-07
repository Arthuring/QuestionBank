<template>
  <div>
<!--    <router-link to="/">Home</router-link> |-->
<!--    <router-link to="/about">About</router-link>-->
<!--    头部-->
    <Headerup/>
<!--    主体-->
    <div style="display: flex">
<!--      侧边栏-->
      <Aside />
<!--      内容-->
      <router-view style="flex: 1"/>
    </div>
  </div>
</template>

<!--<style>-->
<!--#app {-->
<!--  font-family: Avenir, Helvetica, Arial, sans-serif;-->
<!--  -webkit-font-smoothing: antialiased;-->
<!--  -moz-osx-font-smoothing: grayscale;-->
<!--  text-align: center;-->
<!--  color: #2c3e50;-->
<!--}-->

<!--nav {-->
<!--  padding: 30px;-->
<!--}-->

<!--nav a {-->
<!--  font-weight: bold;-->
<!--  color: #2c3e50;-->
<!--}-->

<!--nav a.router-link-exact-active {-->
<!--  color: #42b983;-->
<!--}-->
<!--</style>-->

<script>
import Headerup from "@/components/Headerup";
import Aside from "@/components/Aside";

export default {
  name: "Layout",
  components:{
    Headerup,
    Aside
  }
}
</script>

