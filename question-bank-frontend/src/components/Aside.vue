<template>
  <div>
    <el-menu
        style="width: 200px; min-height: calc(100vh - 50px)"
        default-active="2"
        class="el-menu-vertical-demo"
    >
      <!--      <el-sub-menu index="1">-->
      <!--        <template #title>-->
      <!--          <el-icon>-->
      <!--            <location/>-->
      <!--          </el-icon>-->
      <!--          <span>Upload Question</span>-->
      <!--        </template>-->
      <!--&lt;!&ndash;        <el-menu-item index="1-1">item one</el-menu-item>&ndash;&gt;-->
      <!--&lt;!&ndash;        <el-menu-item index="1-2">item Two</el-menu-item>&ndash;&gt;-->
      <!--        &lt;!&ndash;        <el-menu-item-group title="Group Two">&ndash;&gt;-->
      <!--        &lt;!&ndash;          <el-menu-item index="1-3">item three</el-menu-item>&ndash;&gt;-->
      <!--        &lt;!&ndash;        </el-menu-item-group>&ndash;&gt;-->
      <!--        &lt;!&ndash;        <el-sub-menu index="1-4">&ndash;&gt;-->
      <!--        &lt;!&ndash;          <template #title>item four</template>&ndash;&gt;-->
      <!--        &lt;!&ndash;          <el-menu-item index="1-4-1">item one</el-menu-item>&ndash;&gt;-->
      <!--        &lt;!&ndash;        </el-sub-menu>&ndash;&gt;-->
      <!--      </el-sub-menu>-->

      <el-menu-item index="1" @click="handleAside('/upload')">
        <el-icon>
          <el-icon>
            <Upload/>
          </el-icon>
        </el-icon>
        <span>Upload Question</span>
      </el-menu-item>


      <el-menu-item index="2" @click="handleAside('/list')">
        <el-icon>
          <Document/>
        </el-icon>
        <span>Question List</span>
      </el-menu-item>


      <el-menu-item index="3" @click="handleAside('/test')">
        <el-icon>
          <DocumentChecked/>
        </el-icon>
        <span>Test</span>
      </el-menu-item>


      <el-menu-item index="4" @click="handleAside('/analysis')">
        <el-icon>
          <el-icon>
            <DataLine/>
          </el-icon>
        </el-icon>
        <span>Analysis</span>
      </el-menu-item>

    </el-menu>

  </div>
</template>

<script>
import global from "@/components/Global";
import router from "@/router";
import {ElMessage} from "element-plus";

export default {
  name: "Aside",
  data() {
    return {
      logged: global.uuid,
      visibleLogged: this.logged
    }
  },
  methods: {
    handleAside(rout) {
      if (!(global.uuid === -1)) {
        router.push(rout)
      } else {
        ElMessage({
          showClose: true,
          message: 'Please login first ',
        })
      }
    }
  }
}
</script>

<style scoped>

</style>