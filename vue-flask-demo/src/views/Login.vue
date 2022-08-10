<template>
  <div :style="background">
    <el-container style="flex-direction: column;">
      <el-header style="height: 170px">
        <div style="font-weight: bolder; color:#f8ffff;font-size: xxx-large; text-align: center; padding: 130px 0">
          Welcome to Question Bank :)
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
                style="margin-top: 50px"
            >Sign in</el-button
            >
          </div>
        </div>

      </el-main>
      <el-footer style="text-align: center">

        <el-button size="large" plain type="primary" color="dodgerblue"> GO!<el-icon class="el-icon--right" size="large"><Promotion /></el-icon></el-button>

      </el-footer>
    </el-container>

  </div>
</template>

<!-- <script lang="ts" setup>
import { onMounted, ref } from 'vue'

interface RestaurantItem {
  value: string
  link: string
}

const state1 = ref('')
const state2 = ref('')

const restaurants = ref<RestaurantItem[]>([])
const querySearch = (queryString: string, cb: any) => {
  const results = queryString
    ? restaurants.value.filter(createFilter(queryString))
    : restaurants.value
  // call callback function to return suggestions
  cb(results)
}
const createFilter = (queryString: string) => {
  return (restaurant: RestaurantItem) => {
    return (
      restaurant.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0
    )
  }
}
const loadAll = () => {
  return [
    { value: 'vue', link: 'https://github.com/vuejs/vue' },
    { value: 'element', link: 'https://github.com/ElemeFE/element' },
    { value: 'cooking', link: 'https://github.com/ElemeFE/cooking' },
    { value: 'mint-ui', link: 'https://github.com/ElemeFE/mint-ui' },
    { value: 'vuex', link: 'https://github.com/vuejs/vuex' },
    { value: 'vue-router', link: 'https://github.com/vuejs/vue-router' },
    { value: 'babel', link: 'https://github.com/babel/babel' },
  ]
}

const handleSelect = (item: RestaurantItem) => {
  console.log(item)
}

onMounted(() => {
  restaurants.value = loadAll()
})
</script> -->
<script>
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
      inputPassword: ''
    }
  },
}
</script>

