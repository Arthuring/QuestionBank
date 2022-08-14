<template>
  <div style="height: 50px; line-height: 50px; border-bottom: 1px solid #ccc; display: flex">
    <div style="width: 200px; padding-left: 30px; font-weight: bold; color: dodgerblue">Question Bank</div>
    <div style="flex: 1"></div>
    <div style="width: 150px">
      <el-avatar shape="circle" :size="30" :src="circleUrl" style="margin-right: 5px; margin-top: 7px"  />
      <el-dropdown>
    <span v-if="isReloadData" class="el-dropdown-link">
      <br>
      {{ this.userName }}
      <el-icon class="el-icon--right">
        <arrow-down/>
      </el-icon>
    </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="handleItemOne"><el-icon class="small"> <User /></el-icon>
              {{ this.itemText }}</el-dropdown-item>
            <el-dropdown-item @click="handleLogout"> <el-icon class="small"> <SwitchButton /></el-icon>logout</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script>
import global from "@/components/Global";
import router from "@/router";
import login from "@/views/Login";
export default {
  name: "Headerup",
  inject:['reload'],
  created() {
    this.userName = global.userName
  },
  data(){
    return{
      isReloadData:true,
      userName: global.userName,
      itemText:global.uuid === -1 ? 'Login' : 'My space',
    }
  },
  methods:{
    handleItemOne(){
      if(global.uuid === -1){
        router.push('/login')
      }
    },
    reloadPart(){
      this.isReloadData = false;
      this.$nextTick(() => {
        this.isReloadData = true
      })
    },
    handleLogout(){
      //TODO:将uuid发给后端
      global.uuid = -1
      global.userName = 'not logged'
      this.userName = global.userName
      this.itemText = global.uuid === -1 ? 'Login' : 'My space'
      router.push('/login')
    }
  },
}
</script>

<style scoped>

</style>