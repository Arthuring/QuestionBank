<template>
  <div style="height: 50px; line-height: 50px; border-bottom: 1px solid #ccc; display: flex">
    <div style="width: 200px; padding-left: 30px; font-weight: bold; color: dodgerblue">Question Bank</div>
    <div style="flex: 1"></div>
    <div style="width: 150px">
      <el-avatar shape="circle" :size="30" :src="circleUrl" style="margin-right: 5px; margin-top: 7px"  />
      <el-dropdown>
    <span class="el-dropdown-link">
      <br>
      User name
      <el-icon class="el-icon--right">
        <arrow-down/>
      </el-icon>
    </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item><el-icon class="small"> <User /></el-icon>Information</el-dropdown-item>
            <el-dropdown-item> <el-icon class="small"> <Setting /></el-icon>Settings</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script>
export default {
  name: "Headerup"
}
</script>

<style scoped>

</style>