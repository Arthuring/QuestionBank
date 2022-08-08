<template>
  <div style="padding: 10px 0;">
    <el-container style="flex-direction: column;">
      <el-header style="height: 70px">
        <div style="font-weight: bolder; color:#79bbff;font-size: large; text-align:center;">
          Login
        </div>
      </el-header>
      <el-main style="overflow: auto">
        <div style="width:100%; float:left">
          <div style="height:30px;width:300px;float:left;"></div>
          <div class="mt-4" style="width:50%; text-alinn:center; float:left">
            <el-input v-model="input1" placeholder="请输入用户名">
              <template #prepend>用户名</template>
            </el-input>
          </div>
        </div>

        <div class="mt-4" style="width:50%; text-align:center;">
        </div>

        <div style="height:30px;width:300px;float:left;">
        </div>

        <div style="width:100%; float:left">
          <div style="height:30px;width:300px;float:left;"></div>
          <div class="mt-4" style="width:50%; text-alinn:center; float:left">
              <el-input v-model="input" type="password" placeholder="请输入密码" show-password>
                <template #prepend>密码</template>
              </el-input>
          </div>
        </div>
      </el-main>
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
  name: "Login"
}
</script>
