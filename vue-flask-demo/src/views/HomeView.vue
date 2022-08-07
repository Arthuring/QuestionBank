<template>
  <div style="padding: 10px">
    <!--    <img alt="Vue logo" src="../assets/logo.png">-->
    <!--    <HelloWorld msg="Welcome to Your Vue.js App"/>-->
    <div style="margin: 10px 0;font-weight: bold; color:#79bbff;font-size: large">
      Welcome to Question Bank :)
    </div>
    <!--    upload-->
    <div style="margin: 10px 0">
      <el-button type="primary" round size="large" @click="addQuestion">Upload Question
        <el-icon class="el-icon--right">
          <Upload />
        </el-icon>
      </el-button>
    </div>
    <!--    search-->
    <div style="margin: 10px 0">
      <el-input v-model="search" placeholder="Keywords" style="width: 25%" />
      <el-button type="primary" style="margin-left: 5px" plain>
        <el-icon class="el-icon--left">
          <Search />
        </el-icon>
        Search
      </el-button>
      <span style="margin-left: 5px; color: #409eff">
        Here are questions we already have!
      </span>
    </div>
    <!--    table-->
    <el-table :data="tableData" max-height="auto" stripe style="max-width: calc(100vw - 20px)">
      <el-table-column prop="ID" label="ID" sortable />
      <el-table-column prop="question" label="Question" />
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
          <el-button plain type="primary" size="small" @click="handleDetail">Detail</el-button>
          <el-button plain size="small">Edit</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div style="margin:10px 0">
      <el-pagination :currentPage="currentPage" :page-size="pageSize" :page-sizes="[5, 10, 15]" :small="small"
        layout="total, sizes, prev, pager, next, jumper" :total="totalPage" @size-change="handleSizeChange"
        @current-change="handleCurrentChange" />
    </div>
    <!--    弹窗-上传问题-->
    <el-dialog v-model="dialogVisibleUpload" title="Upload question file" width="70%" :before-close="handleClose">
      <el-upload class="upload-demo" drag action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
        multiple>
        <el-icon class="el-icon--upload">
          <upload-filled />
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
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisibleUpload = false">Cancel</el-button>
          <el-button type="primary" @click="dialogVisibleUpload = false; dialogVisibleConfirm = true">
            Upload
            <el-icon class="el-icon--right">
              <Upload />
            </el-icon>
          </el-button>
        </span>
      </template>
    </el-dialog>
    <!--    弹窗-确认问题-->
    <el-dialog v-model="dialogVisibleConfirm" title="Confirm your question" width="70%" :before-close="handleClose">
      <el-form :model="formConfirmQuestion" label-width="150px">
        <el-form-item label="Question description">
          <el-input v-model="formConfirmQuestion.question" />
        </el-form-item>
        <el-form-item label="Question type">
          <el-select v-model="formConfirmQuestion.type" placeholder="please select type">
            <el-option label="filling" value="filling" />
            <el-option label="single choice" value="single choice" />
            <el-option label="multiple choice" value="multiple choice" />
          </el-select>
        </el-form-item>
        <el-form-item label="Activity type">
          <el-checkbox-group v-model="formConfirmQuestion.type">
            <el-checkbox label="Online activities" name="type" />
            <el-checkbox label="Promotion activities" name="type" />
            <el-checkbox label="Offline activities" name="type" />
            <el-checkbox label="Simple brand exposure" name="type" />
          </el-checkbox-group>
        </el-form-item>
        <el-form-item label="Resources">
          <el-radio-group v-model="formConfirmQuestion.resource">
            <el-radio label="Sponsor" />
            <el-radio label="Venue" />
          </el-radio-group>
        </el-form-item>
        <el-form-item label="Activity form">
          <el-input v-model="formConfirmQuestion.desc" type="textarea" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit">Create</el-button>
          <el-button>Cancel</el-button>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisibleConfirm = false">Cancel</el-button>
          <el-button type="primary" @click="dialogVisibleConfirm = false">
            Confirm
            <el-icon class="el-icon--right">
              <Check />
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
import { TableColumnCtx } from 'element-plus/es/components/table/src/table-column/defaults'
import { UploadFilled } from '@element-plus/icons-vue'
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
  },
  data() {
    return {
      formUpload: {
        file: '',
      },
      formConfirmQuestion: {
        type: ' ',
        question: ' ',
        choice: {
          A: ' ',
          B: ' ',
          C: ' ',
          D: ' ',
        },
        ans: '',
      },
      search: "",
      currentPage: 1,
      pageSize: 10,
      totalPage: 10,
      dialogVisibleUpload: false,
      dialogVisibleConfirm: false,
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
    handleDetail() {

    },
    handleSizeChange() {

    },
    handleCurrentChange() {

    },
    getQuestion() {
      fetch("http://127.0.0.1:5001/api/getQuestionOrdered", {
        method: "POST",
        body: JSON.stringify({
          "num": 100,
          "offset": 0
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
