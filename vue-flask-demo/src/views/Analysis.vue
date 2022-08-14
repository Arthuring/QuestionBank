<template>
  <div style="">
    <el-menu
      :default-active="activeIndex"
      class="el-menu-demo"
      mode="horizontal"
      background-color="#545c64"
      text-color="#fff"
      active-text-color="#ffd04b"
      @select="handleSelect"
    > <!-- TODO: 更改颜色样式 -->
      <el-menu-item index="1">Wrong Questions List</el-menu-item>
      <el-menu-item index="2">Star Questions List</el-menu-item>
      <el-menu-item index="3">Score Analysis</el-menu-item>
    </el-menu>
  </div>
  <div style="float: left;">
  ?
  </div>

  <div style="float: left;">
    Hi
  </div>
</template>

<script>
export default {
  name: "Analysis"
}
</script>