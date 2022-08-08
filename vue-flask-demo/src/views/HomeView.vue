<template xmlns:el-col="http://www.w3.org/1999/html">
  <div style="padding: 10px 0;">
    <el-container style="flex-direction: column;">
      <el-header style="height: 70px">
        <div style="font-weight: bolder; color:#79bbff;font-size: large">
          Welcome to Question Bank :)
        </div>
        <el-row justify="space-between" style="padding: 10px 0">
          <el-col :span="8">
            <el-button type="primary" round size="large" @click="addQuestion">Upload Question
              <el-icon class="el-icon--right" size="large">
                <UploadFilled/>
              </el-icon>
            </el-button>
          </el-col>
          <el-col :span="8">
            <span style="text-align: right; margin-left: 5px; color: #6db1f8; font-weight: bold ">
              Your questions are following <el-icon size="large">
                <ArrowDownBold/>
              </el-icon>
            </span>
          </el-col>
        </el-row>
      </el-header>
      <el-main style="overflow: auto">
        <!--    upload-->
        <el-table :data="tableData" max-height="500" stripe :table-layout="'auto'">
          <el-table-column prop="ID" label="ID" sortable width="auto"/>
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
              <el-button-group class="ml-4">
                <el-button plain type="primary" size="small" :icon="'Edit'" @click="handleEdit(scope.$index)"/>
                <!--                <el-popconfirm title="Are you sure to delete this?" @confirm.prevent="handleDelete(scope.$index)">-->
                <!--                  <template #reference>-->
                <!--                    <el-button plain type="danger" size="small">-->
                <!--                      <el-icon>-->
                <!--                        <Delete />-->
                <!--                      </el-icon>-->
                <!--                    </el-button>-->

                <!--                  </template>-->
                <!--                </el-popconfirm>-->
                <el-button plain type="danger" size="small" @click="handleDelete(scope.$index)" >
                  <el-icon>
                    <Delete/>
                  </el-icon>
                </el-button>
              </el-button-group>
            </template>
          </el-table-column>
        </el-table>
      </el-main>
      <el-footer style="margin: 10px; position: absolute; bottom: 0">
        <el-row justify="space-between">
          <el-col :span="22">
            <el-pagination :currentPage="currentPage" :page-size="pageSize" :page-sizes="[5, 10, 15]" :small="small"
                           layout="total, sizes, prev, pager, next, jumper" :total="totalPage"
                           @size-change="handleSizeChange"
                           @current-change="handleCurrentChange"/>
          </el-col>
          <el-col :span="2">

            <el-button type="primary" size="default">
              submit
              <el-icon class="el-icon--right">
                <Check/>
              </el-icon>
            </el-button>
          </el-col>
        </el-row>
      </el-footer>
    </el-container>

    <!--    弹窗-上传问题-->
    <el-dialog v-model="dialogVisibleUpload" title="Upload question file" width="70%" :before-close="handleClose">
      <el-upload class="upload-demo" drag action="http://127.0.0.1:5001/api/uploadFile" multiple>
        <el-icon class="el-icon--upload">
          <upload-filled/>
        </el-icon>
        <div class="el-upload__text">
          Drop file here or <em>click to upload</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            jpg/png/pdf files with a size less than 500kb
          </div>
        </template>
      </el-upload>
    </el-dialog>
    <!--    弹窗-编辑问题-->
    <el-dialog v-model="dialogVisibleEdit" title="Confirm your question" width="70%" :before-close="handleCloseEdit">
      <el-form :model="formConfirmQuestion" :label-position="'left'" label-width="150px">
        <el-form-item label="Question">
          <el-input v-model="formConfirmQuestion.question"/>
        </el-form-item>
        <el-form-item label="detail">
          <el-input v-model="formConfirmQuestion.description" type="textarea"/>
        </el-form-item>
        <el-form-item label="type">
          <el-select v-model="formConfirmQuestion.type" placeholder="please select type">
            <el-option label="filling" value="filling"/>
            <el-option label="single choice" value="single choice"/>
            <el-option label="multiple choice" value="multiple choice"/>
          </el-select>
        </el-form-item>
        <el-form-item label="Answer">
          <el-input v-model="formConfirmQuestion.ansFilling" type="textarea"/>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisibleEdit = false">Cancel</el-button>
          <el-button type="primary" @click="dialogVisibleEdit = false">
            Confirm
            <el-icon class="el-icon--right">
              <Check/>
            </el-icon>
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'
import {TableColumnCtx} from 'element-plus/es/components/table/src/table-column/defaults'
import {UploadFilled} from '@element-plus/icons-vue'
import SearchBar from "@/components/SearchBar";

export default {

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
  name: 'HomeView',
  components: {
    // HelloWorld
    SearchBar,
  },
  data() {
    return {
      formUpload: {
        file: '',
      },
      formConfirmQuestion: {
        type: ' ',
        description: '',
        question: ' ',
        ansFilling: '请输入答案(不区分大小写，按字母顺序)',
      },
      search: "",
      currentPage: 1,
      pageSize: 10,
      totalPage: 100,//TODO: 通过后端获取问题总数
      dialogVisibleUpload: false,
      dialogVisibleEdit: false,
      tableData: [
        // {
        //   ID: '777',
        //   type: 'multiple choice',
        //   question: 'No. 189, Grove St, Los Angeles',
        //   ans:'',
        // }
      ]
    }
  },
  created() {
    this.getQuestion()
  },
  methods: {
    addQuestion() {
      this.dialogVisibleUpload = true
    },
    handleEdit(index) {
      this.dialogVisibleEdit = true
      this.formConfirmQuestion.question = this.tableData[index].question
      this.formConfirmQuestion.description = this.tableData[index].description
      this.formConfirmQuestion.type = this.tableData[index].type

    },
    handleDelete(index) {
      this.delQuestion(this.tableData[index].ID)
      this.getQuestion()
    },
    handleEditConfirm() {
      this.dialogVisibleEdit = false
    },
    handleSizeChange(number) {
      this.pageSize = number
      this.getQuestion()
    },
    handleCurrentChange(number) {
      this.currentPage = number
      this.getQuestion()
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
    },
    delQuestion(ID) {
      fetch("http://127.0.0.1:5001/api/getQuestionOrdered", {
        method: "POST",
        body: JSON.stringify({
          "ID": ID,
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
                //this.tableData = responseJson['example_questions']
              }
          )
    }
  }
}
</script>
