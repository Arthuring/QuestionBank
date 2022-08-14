<template>
  <el-table :data="tableData" max-height="500"  stripe :table-layout="'auto'">
    <template #empty>
      <div class="flex items-center justify-center h-100%">
        <el-empty/>
      </div>
    </template>
    <el-table-column type="index" width="50"/>
    <el-table-column sortable prop="time" label="Time"/>
    <el-table-column sortable prop="wrong" label="Wrong answer"/>
    <el-table-column prop="wrongID" label="Wrong ID"/>
    <el-table-column sortable prop="total" label="Total"/>
    <el-table-column sortable prop="accuracy" label="Accuracy"/>
  </el-table>

</template>

<script>
import global from "@/components/Global";
export default {
  name: "HistoryScore",
  created() {
    this.getUserHistory()
  },
  data(){
    return{
      tableData:[
        // {
        //   wrong:5,
        //   total:10,
        //   accuracy:0.5,
        //   wrongID:[1, 2,3,4,5],
        // }
      ]
    }
  },
  methods:{
    getUserHistory(){


    },
  }

}
</script>

<style scoped>

</style>