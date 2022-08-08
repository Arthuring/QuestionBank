<template>
  <div>
    <el-container style="flex-direction: column; padding: 10px 0">
      <el-header height="20px">
        <el-row type="flex">
          <el-col :span="8" style="color: #409eff;font-weight: bolder; font-size: large">
            Choose questions to begin self-test :)
          </el-col>
          <el-col :span="4"/>
          <el-col :span="12">
            <search-bar/>
          </el-col>
        </el-row>
      </el-header>
      <el-main style="overflow: auto">
        <el-table :data="tableData" max-height="550" stripe :table-layout="'auto'">
          <el-table-column type="selection" width="55" />
          <el-table-column prop="ID" label="ID" sortable width="auto"/>
          <el-table-column prop="uploader" label="uploader"/>
          <el-table-column prop="question" label="Question"/>
          <el-table-column prop="type" label="Type" :filters="[
        { text: 'filling', value: 'filling' },
        { text: 'single choice', value: 'single choice' },
        { text: 'multiple choice', value: 'multiple choice' },
      ]" :filter-method="filterTag" filter-placement="bottom-end">
            <template #default="scope">
              <el-tag :type="scope.row.type === 'filling' ? '' :
          scope.row.type === 'single choice' ? 'warning' : 'success'" disable-transitions>{{ scope.row.type }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column fixed="right" label="Operations" width="fixed">
            <template #default>
              <el-button plain type="default" size="small" @click="handleEdit" round>
                <el-icon class="el-icon--left">
                  <CirclePlus/>
                </el-icon>
                Detail
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-main>
      <el-footer style="position: absolute; bottom: 0">
        <el-pagination :currentPage="currentPage" :page-size="pageSize" :page-sizes="[5, 10, 15]" :small="small"
                       layout="total, sizes, prev, pager, next, jumper" :total="totalPage"
                       @size-change="handleSizeChange"
                       @current-change="handleCurrentChange"/>
      </el-footer>
    </el-container>

    <el-dialog v-model="dialogVisibleEdit" title="Detail" width="70%" :before-close="handleCloseEdit">
      <template #default>
        <div
            class="demo-rich-conent"
            style="display: flex; gap: 16px; flex-direction: column"
        >
          <div>
            <p
                class="demo-rich-content__name"
                style="margin: 0; font-weight: 500"
            >
              Element Plus
            </p>
            <p
                class="demo-rich-content__mention"
                style="margin: 0; font-size: 14px; color: var(--el-color-info)"
            >
              @element-plus
            </p>
          </div>

          <p class="demo-rich-content__desc" style="margin: 0">
            Element Plus, a Vue 3 based component library for developers,
            designers and product managers
          </p>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import SearchBar from "@/components/SearchBar";

export default {
  components: {
    SearchBar
  },

  data() {
    return {
      dialogVisibleEdit: false,
      currentPage: 1,
      pageSize: 15,
      totalPage: 100,//TODO: 通过后端获取问题总数
      tableData: [],
      formConfirmQuestion: {
        type: ' ',
        detail: '',
        question: ' ',
        ansFilling: '',
        ansMulti: '',
        ansSingle: '',
      },
    }
  },
  name: "List",
  created() {
    this.getQuestion()
  },
  methods: {
    handleSizeChange(number) {
      this.pageSize = number
      this.getQuestion()
    },
    handleCurrentChange(number) {
      this.currentPage = number
      this.getQuestion()
    },
    handleEdit() {
      this.dialogVisibleEdit = true
    },
    getQuestion() {
      fetch("http://127.0.0.1:5001/api/getQuestionOrdered", {
        method: "POST",
        body: JSON.stringify({
          "num": this.pageSize,
          "offset": this.pageSize * (this.currentPage - 1)
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
                this.tableData = responseJson['example_questions']
              }
          )
    }
  }
}
</script>

<style scoped>

</style>