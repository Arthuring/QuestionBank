<template>
  <div :style="background">
    <el-container style="flex-direction: column;">
      <el-header style="height: 170px">
        <div style="font-weight: bolder; color:#f8ffff;font-size: xxx-large; text-align: center; padding: 130px 0">
          Welcome to Question Bank :-)
        </div>
      </el-header>
      <el-main style="overflow: auto">
        <div style="font-weight: bolder; color:#f7f8ff; text-align:center; padding-top: 50px; padding-bottom: 30px;
         font-size: x-large">
          Login
        </div>

        <div style="width:100%; float:left; text-align: center" >

          <div class="mt-4" style="width:100%; text-align:center; float:left; ">
            <el-input v-model="inputUsername" placeholder="Please input username" style="width: 500px">
              <template #prepend>username</template>
            </el-input>
          </div>
        </div>

        <div class="mt-4" style="width:50%; text-align:center;">
        </div>

        <div style="height:30px;width:300px;float:left;">
        </div>

        <div style="width:100%; float:left">
<!--          <div style="height:30px;width:300px;float:left;"></div>-->
          <div class="mt-4" style="width:100%; text-align:center; ">
            <el-input v-model="inputPassword" style="width: 500px" type="password" placeholder="please input password" show-password>
              <template #prepend>password</template>
            </el-input>

          </div>
          <div class="mt-4" style="width:100%; text-align:center; ">
            <el-button
                :type="'primary'"
                plain
                style="margin-top: 50px; width: 100px"
                size="default"
                @click="dialogVisibleSign=true"
            >Sign up
              <el-icon class="el-icon--right" size="large"><Pointer /></el-icon>
            </el-button
            >
          </div>
        </div>

      </el-main>
      <el-footer style="text-align: center">

        <el-button size="large" plain type="primary" color="dodgerblue" @click="handleLogin" style="width: 100px">
          GO!
          <el-icon class="el-icon--right" size="large"><Promotion /></el-icon></el-button>

      </el-footer>
    </el-container>
<!--    注册弹窗-->
    <el-dialog v-model="dialogVisibleSign" title="Sign Up" width="70%" :before-close="handleCloseEdit">
      <el-form
          ref="ruleFormRef"
          :model="formSignIn"
          status-icon
          label-width="120px"
          class="demo-ruleForm"
      >
        <el-form-item label="Username" prop="username">
          <el-input v-model.number="formSignIn.userName" />
        </el-form-item>
        <el-form-item label="Password" prop="pass">
          <el-input v-model="formSignIn.password" type="password" autocomplete="off" />
        </el-form-item>
        <el-form-item label="Confirm" prop="checkPassword">
          <el-input
              v-model="formSignIn.checkPassword"
              type="password"
              autocomplete="off"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm()"
          >Submit <el-icon class="el-icon--right" size="large"><Promotion /></el-icon></el-button
          >
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import {ElMessage} from "element-plus";
import global from "@/components/Global";
import router from "@/router";
import aside from "@/components/Aside";
import app from "@/App";
export default {
  name: "Login",
  data() {
    return {
      background: {
        // 背景图片地址
        backgroundImage: 'url(' + require('@/assets/cool-background.svg') + ')',
        // 背景图片是否重复
        backgroundRepeat: 'no-repeat',
        // 背景图片大小
        backgroundSize: 'cover',
        // 背景颜色
        backgroundColor: '#ffffff',
        // 背景图片位置
        backgroundPosition: 'center top'
      },
      inputUsername: '',
      inputPassword: '',
      dialogVisibleSign:false,
      formSignIn:{
        userName: '',
        password:'',
        checkPassword:'',
      }
    }
  },

  methods:{
    submitForm(){
      let valid = true
      if(this.formSignIn.userName === ''){
        valid = false;
        ElMessage.error('Username can not be empty')
      }
      if(this.formSignIn.password === ''){
        valid = false;
        ElMessage.error('Password can not be empty')
      }
      if(this.formSignIn.userName === ''){
        valid = false;
        ElMessage.error('Please check your password')
      }
      if(!(this.formSignIn.password === this.formSignIn.checkPassword)){
        valid = false;
        ElMessage.error('Please input check same with password')
      }
      if(valid){
        ElMessage.success('Signed In succeeded')
        this.dialogVisibleSign = false
        // TODO:上传用户信息到后端
      }
    },
    handleLogin(){
      if(this.inputUsername === 'admin' && this.inputPassword === '123456'){

        global.uuid = 0
        global.userName = 'admin'
        // app.components.Aside.data().logged = true
        // app.components.Aside.data().visibleLogged = true
        this.$emit('login')
        router.push('upload')
      }else{
        this.inputUsername = ''
        this.inputPassword = ''
        ElMessage.error('Username or password wrong')
      }
    }
  }
}
</script>

