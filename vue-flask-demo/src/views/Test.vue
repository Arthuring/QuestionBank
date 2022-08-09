<template>
  <div>
    <el-container style="flex-direction: column; padding: 10px 0">
      <el-header height="20px">
        <el-row type="flex">
          <el-col :span="12" style="color: #409eff;font-weight: bolder; font-size: large">
            Choose questions to begin self-test :)
          </el-col>

          <el-col :span="12">
            <search-bar/>
          </el-col>
        </el-row>
      </el-header>
      <el-main style="overflow: auto">
        <div>
          <el-table
              :data="tableData"
              max-height="550"
              stripe
              :table-layout="'auto'"
              @selection-change="handleSelectionChange"
          >
            <el-table-column type="selection" width="55"/>
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
              <template #default="scope">
                <el-button plain type="default" size="small" @click="handleDetail(scope.$index)" round>
                  <el-icon class="el-icon--left">
                    <CirclePlus/>
                  </el-icon>
                  Detail
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
        <div style="margin-top: 16px">
          <el-row justify="space-between" type="flex">
            <el-col :span="8">
              <router-link to="/testing" style="text-decoration: none">
                <el-button plain type="primary" size="default" @click="handleGoTest">
                  Test Selected
                  <el-icon>
                    <ArrowRight/>
                  </el-icon>
                </el-button>
              </router-link>
            </el-col>
            <el-col :span="8">
              <el-button type="primary" style="float: right;" size="default" @click="handleRandomTest">
                Random Test
                <el-icon>
                  <DArrowRight/>
                </el-icon>
              </el-button>
              <el-input-number
                  v-model="randomNum"
                  class="mx-4"
                  :min="1"
                  :max="this.totalPage < 10 ? this.totalPage : 10"
                  controls-position="right"
                  @change="handleChangeRandom"
                  style="float: right;"
                  size="default"
              />
            </el-col>
          </el-row>
        </div>
      </el-main>
      <el-footer style="position: absolute; bottom: 0">
        <el-pagination :currentPage="currentPage" :page-size="pageSize" :page-sizes="[5, 10, 15]"
                       layout="total, sizes, prev, pager, next, jumper" :total="totalPage"
                       @size-change="handleSizeChange"
                       @current-change="handleCurrentChange"/>
      </el-footer>
    </el-container>

    <el-dialog v-model="dialogVisibleDetail" title="Detail" width="70%" :before-close="handleCloseEdit">
      <!--      TODO: 绑定变量-->
      <el-descriptions
          class="margin-top"
          :title="this.formDetail.question"
          :column="1"
          size="default"
          border
      >
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">
              <el-icon :style="iconStyle">
                <Paperclip />
              </el-icon>
              ID
            </div>
          </template>

          {{ this.formDetail.ID }}

        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">
              <el-icon :style="iconStyle">
                <Filter/>
              </el-icon>
              Type
            </div>
          </template>
          <el-tag size="small">
            {{ this.formDetail.type }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">
              <el-icon :style="iconStyle">
                <user/>
              </el-icon>
              Uploader
            </div>
          </template>
          {{ this.formDetail.uploader }}
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">
              <el-icon :style="iconStyle">
                <ChatLineSquare />
              </el-icon>
              Description
            </div>
          </template>
          {{ this.formDetail.description }}
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script>
import SearchBar from "@/components/SearchBar";
import global from "@/components/Global";
import router from "@/router";
export default {
  components: {
    SearchBar
  },
  setup() {
    const formatter = (row, column) => {
      return row.address
    };
    const filterTag = (value, row) => {
      return row.type === value
    };
    const filterHandler = (
        value,
        row,
        column,
    ) => {
      const property = column['property']
      return row[property] === value
    };
    return {
      formatter,
      filterTag,
      filterHandler
    }

  },
  data() {
    return {
      randomNum: 1,
      dialogVisibleDetail: false,
      currentPage: 1,
      pageSize: 15,
      totalPage: 100,
      tableData: [],
      selected:[],
      formConfirmQuestion: {
        type: ' ',
        detail: '',
        question: ' ',
        ansFilling: '',
        ansMulti: '',
        ansSingle: '',
      },
      formDetail: {
        type: 'multiple choice',
        uploader: 'Arthuring',
        description: "下列正确的是 A：xxx B: xxx C: xxx D:xxx",
        question: '下列正确的是',
        ans: 'ABC',
        ID:0
      },
    }
  },
  name: "List",
  created() {
    this.getQuestion()
    this.getQuestionNum(-1, 'ready')
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
    handleChangeRandom(number) {
      this.randomNum = number
    },
    handleDetail(index) {
      this.dialogVisibleDetail = true
      this.formDetail.type = this.tableData[index].type
      this.formDetail.uploader = this.tableData[index].uploader
      this.formDetail.description = this.tableData[index].description
      this.formDetail.question = this.tableData[index].question
      this.formDetail.ans = this.tableData[index].ans
      this.formDetail.ID = this.tableData[index].ID
    },
    handleSelectionChange(val){
      this.selected = val
    },
    handleGoTest(){
      global.testTable = this.selected
    },
    handleRandomTest(){
      fetch("http://127.0.0.1:5001/api/getQuestionRandom", {
        method: "POST",
        body: JSON.stringify({
          "num": this.randomNum,
          "uuid": -1,
          "status": 'ready'
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
                global.testTable= responseJson['example_questions']
                router.push('testing')
              }
          )
    },
    getQuestion() {
      fetch("http://127.0.0.1:5001/api/getQuestionOrdered", {
        method: "POST",
        body: JSON.stringify({
          "num": this.pageSize,
          "offset": this.pageSize * (this.currentPage - 1),
          "uuid": -1,
          "status": 'ready'
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
    },
    getQuestionNum(user, option) {
      fetch("http://127.0.0.1:5001/api/getQuestionNum", {
        method: "POST",
        body: JSON.stringify({
          "num": this.pageSize,
          "uuid": user,
          "status": option
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
                this.totalPage = responseJson['num']
              }
          )
    },
  }
}
</script>

<style scoped>

</style>