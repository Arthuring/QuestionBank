<template>
  <el-container style="flex-direction: column; padding: 10px 0">
    <el-header height="20px">
      <el-row type="flex">
        <el-col :span="8" style="color: #409eff;font-weight: bolder; font-size: large">
          History Score
        </el-col>
        <el-col :span="4"/>
        <el-col :span="12">
          <search-bar/>
        </el-col>
      </el-row>
    </el-header>
    <el-main style="overflow: auto">
      <el-table :data="tableData" max-height="500"  stripe :table-layout="'auto'">
        <template #empty>
          <div class="flex items-center justify-center h-100%">
            <el-empty/>
          </div>
        </template>
        <el-table-column type="index" width="50"/>
        <el-table-column sortable prop="time" label="Time"/>
        <el-table-column sortable prop="wrong" label="Number of wrong answer"/>
        <el-table-column prop="wrongID" label="Wrong ID"/>
        <el-table-column sortable prop="total" label="Total"/>
        <el-table-column sortable prop="accuracy" label="Accuracy"/>
      </el-table>
    </el-main>
    <el-footer style="position: absolute; bottom: 0">
      <el-pagination :currentPage="currentPage" :page-size="pageSize" :page-sizes="[5, 10, 15]" :small="small"
                     layout="total, sizes, prev, pager, next, jumper" :total="totalPage"
                     @size-change="handleSizeChange"
                     @current-change="handleCurrentChange"/>
    </el-footer>
  </el-container>
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
      fetch("http://127.0.0.1:5001/api/getUserRecord", {
        method: "POST",
        body: JSON.stringify({
          "uuid": global.uuid
        }),
        headers: {
          "Content-Type": "application/json"
        },
      }).then(res => res.json())
        .catch(error => {
          console.error('Error:', error)
        })
        .then((responseJson) => {
          console.log(responseJson)
          this.tableData = responseJson['data']
        }
        )
    },
  }

}
</script>

<style scoped>

</style>