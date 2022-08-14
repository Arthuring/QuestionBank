<template>
  <div>
    <el-container style="flex-direction: column; padding: 10px 0">
      <el-header height="20px">
        <el-row type="flex">
          <el-col :span="8" style="color: #409eff;font-weight: bolder; font-size: large">
            Wrong Questions List :(
          </el-col>
          <el-col :span="4"/>
          <el-col :span="12">
            <search-bar/>
          </el-col>
        </el-row>
      </el-header>
      <el-main style="overflow: auto">
        <el-table :data="tableData" max-height="550" stripe :table-layout="'auto'">
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
          <el-table-column fixed="right" label="Detail" width="fixed">
            <template #default="scope">
              <el-button plain type="default" size="small" @click="handleDetail(scope.$index)" circle>
                <el-icon>
                  <MoreFilled/>
                </el-icon>
              </el-button>
            </template>
          </el-table-column>
          <el-table-column prop="wrongRate" label="wrongRate" sortable width="auto"/>
        </el-table>
      </el-main>
      <el-footer style="position: absolute; bottom: 0">
        <el-pagination :currentPage="currentPage" :page-size="pageSize" :page-sizes="[5, 10, 15]" :small="small"
                       layout="total, sizes, prev, pager, next, jumper" :total="totalPage"
                       @size-change="handleSizeChange"
                       @current-change="handleCurrentChange"/>
      </el-footer>
    </el-container>
    <!--弹窗-详情-->
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
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">
              <el-icon :style="iconStyle">
                <MagicStick />
              </el-icon>
              Answer
            </div>
          </template>
          {{ this.formDetail.ans }}
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">
              <el-icon :style="iconStyle">
                <Warning />
              </el-icon>
              Wrong Rate
            </div>
          </template>
          {{ this.formDetail.wrongRate }}
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script>
import SearchBar from "@/components/SearchBar";

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
      dialogVisibleDetail: false,
      currentPage: 1,
      pageSize: 15,
      totalPage: 100,//TODO: 通过后端获取问题总数
      tableData: [
        {
          ID: '123',
          type: 'multiple choice',
          uploader: 'Arthuring',
          description: "下列正确的是 A：xxx B: xxx C: xxx D:xxx",
          question: '下列正确的是',
          ans: 'ABC',
          stared: true,
          wrongRate: 0.4,
        },
        {
          ID: '456',
          type: 'multiple choice',
          uploader: 'Arthuring',
          description: "下列正确的是 A：xxx B: xxx C: xxx D:xxx",
          question: '下列正确的是',
          ans: 'ABC',
          stared: false,
          wrongRate: 0.2,
        },

      ],
      formConfirmQuestion: {
        ID: '',
        type: ' ',
        detail: '',
        question: ' ',
        ansFilling: '',
        ansMulti: '',
        ansSingle: '',
      },
      formDetail: {
        ID: '',
        type: 'multiple choice',
        uploader: 'Arthuring',
        description: "下列正确的是 A：xxx B: xxx C: xxx D:xxx",
        question: '下列正确的是',
        ans: 'ABC',
        wrongRate: 0.333,
      }
    }
  },
  name: "WrongList",
  created() {
    this.getQuestion()
    this.getQuestionNum(-1,'ready')
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
    handleDetail(index) {
      this.dialogVisibleDetail = true
      this.formDetail.type = this.tableData[index].type
      this.formDetail.uploader = this.tableData[index].uploader
      this.formDetail.description = this.tableData[index].description
      this.formDetail.question = this.tableData[index].question
      this.formDetail.ans = this.tableData[index].ans
      this.formDetail.ID = this.tableData[index].ID
      this.formDetail.wrongRate = this.tableData[index].wrongRate
    },
    handleStared(index){
      this.tableData[index].stared = !this.tableData[index].stared;
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