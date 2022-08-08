<template>
  <el-input v-model="search" placeholder="Keywords" style="width: 67%"/>
  <el-button type="primary" style="margin-left: 5px" plain>
    <el-icon class="el-icon--left">
      <Search/>
    </el-icon>
    Search
  </el-button>
</template>

<script>
export default {
  name: "SearchBar",
}
</script>

<style scoped>

</style>