<template>

    <el-container style="padding: 0; margin: 0">
      <el-header style="padding: 0;height: 50px">
        <el-menu
            :default-active="activeIndex"
            class="el-menu-demo"
            mode="horizontal"
            @select="handleSelect"
            style="height: 50px"
        >
          <el-menu-item index="1" @click="handleSelect('wrong')">Wrong Questions List</el-menu-item>
          <el-menu-item index="2" @click="handleSelect('star')">Star Questions List</el-menu-item>
          <el-menu-item index="3" @click="handleSelect('history')">Score Analysis</el-menu-item>
        </el-menu>
      </el-header>
      <el-main style="padding: 0">
        <router-view  style="flex: 1"/>
      </el-main>
    </el-container>


<!--  <div style="float: left;">-->
<!--  ?-->
<!--  </div>-->

<!--  <div style="float: left;">-->
<!--    Hi-->
<!--  </div>-->
</template>

<script>
import router from "@/router";

export default {
  name: "Analysis",
  data(){
    return{
      activeIndex:"1",
    }
  },
  methods:{
    handleSelect(path){
      router.push('analysis')
      router.push(path)
    }
  }
}
</script>