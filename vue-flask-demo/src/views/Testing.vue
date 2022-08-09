<template>
  <div>
    <el-container style="flex-direction: column; padding:10px 0">
      <el-header>
        <el-row type="flex">
          <el-col :span="8">
            <router-link to="/test" style="text-decoration: none">
              <el-button plain type="primary" size="default">
                <el-icon class="el-icon--left">
                  <DArrowLeft/>
                </el-icon>
                Back
              </el-button>
            </router-link>
          </el-col>
          <el-col :span="16" style="color: #409eff;font-weight: bolder; font-size: large">
            {{this.headerText}}
          </el-col>
        </el-row>
      </el-header>
      <el-main style="overflow: auto">
        <el-table :data="tableData" max-height="550" stripe :table-layout="'auto'">
          <el-table-column prop="ID" label="ID" sortable width="auto"/>
<!--表格-题目类型-->
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
<!--          表格-题目简写-->
          <el-table-column prop="question" label="Question"/>
<!--          表格-用户答案-->
          <el-table-column prop="userAns" label="Your answer"/>
<!--          表格-编辑答案-->
          <el-table-column fixed="right" label="Operations" width="120px">
            <template #default="scope">
              <el-button plain type="default" size="small" :disabled="!canExercise"
                         @click="handleExercise(scope.$index)" round>
                <el-icon class="el-icon--left">
                  <EditPen/>
                </el-icon>
                Write
              </el-button>
            </template>
          </el-table-column>
<!--          表格-提交后显示结果-->
          <el-table-column fixed="right" prop="result" label="Result" width="120px">
            <template #default="scope">
              <el-popover
                  placement="left-start"
                  title="Result"
                  :width="200"
                  trigger="hover"
              >
                <template #reference>
                  <el-button plain
                             :type="scope.row.result === 'wrong answer' ? 'danger' :
          scope.row.result === 'accepted' ? 'success' : 'info'"
                             :icon="scope.row.result === 'wrong answer' ? 'Close' :
          scope.row.result === 'accepted' ? 'Check' : 'Minus'"
                             :disabled="scope.row.result === 'wrong answer' ? false :
          scope.row.result!=='accepted'"
                             circle size="small"/>
                </template>
                <el-descriptions
                    class="margin-top"
                    :column="1"
                    size="default"

                >
                  <el-descriptions-item>
                    <template #label>
                      <div class="cell-item">
                        <el-icon :style="iconStyle">
                          <User/>
                        </el-icon>
                        Your answer
                      </div>
                    </template>

                    {{ scope.row.userAns }}

                  </el-descriptions-item>
                  <el-descriptions-item>
                    <template #label>
                      <div class="cell-item">
                        <el-icon :style="iconStyle">
                          <Check/>
                        </el-icon>
                        Correct answer
                      </div>
                    </template>

                    {{ scope.row.ans }}

                  </el-descriptions-item>
                </el-descriptions>
              </el-popover>
            </template>
          </el-table-column>
        </el-table>
      </el-main>
      <el-footer style="position: absolute; bottom: 0; width: 80%">
<!--        按钮-完成测试-->
        <el-popconfirm title="Are you sure to submit your answer?" @confirm="handleFinishTest">
          <template #reference>
            <el-button type="primary" size="default" style="float: right;padding: 10px" :disabled="!canExercise">
              I finished
              <el-icon class="el-icon--right">
                <Finished/>
              </el-icon>
            </el-button>
          </template>
        </el-popconfirm>
      </el-footer>
    </el-container>
<!--    弹窗--回答问题-->
    <el-dialog v-model="dialogVisibleExercise" title="Exercise" width="50%" :before-close="handleCloseEdit">
      <el-descriptions
          class="margin-top"
          :title="this.formExercise.question"
          :column="2"
          size="small"
      >
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
            {{ this.formExercise.type }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">
              <el-icon :style="iconStyle">
                <Document/>
              </el-icon>
              Description
            </div>
          </template>
          {{ this.formExercise.description }}
        </el-descriptions-item>
      </el-descriptions>
      <el-form :model="formExercise" label-width="120px">
        <el-form-item label="Your answer here">
          <el-input v-model="formExercise.userAns"/>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisibleExercise = false">Cancel</el-button>
          <el-button type="primary" @click="handleExerciseConfirm">
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
import global from "@/components/Global";
import {ElNotification} from "element-plus";
import {h} from "vue";
export default {
  name: "Testing",
  setup() {
    const filterTag = (value, row) => {
      return row.type === value
    };
    const filterResult = (value, row) => {
      return row.result === value
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
      filterResult,
      filterTag,
      filterHandler
    }

  },
  data() {
    return {
      formResult: {},
      headerText:'Test begin!',
      dialogVisibleExercise: false,
      canExercise: true,
      questionNum: global.testTable.length,
      correctNum:0,
      formExercise: {
        type: 'multiple choice',
        description: "下列正确的是 A：xxx B: xxx C: xxx D:xxx",
        question: '下列正确的是',
        ans: 'ABC',
        userAns: 'please input',
        index: -1,
      },
      formUserAns: {
        ans: ''
      },
      tableData: global.testTable,
    }
  },
  methods: {
    handleExercise(index) {
      this.dialogVisibleExercise = true
      this.formExercise.type = this.tableData[index].type
      this.formExercise.description = this.tableData[index].description
      this.formExercise.question = this.tableData[index].question
      this.formExercise.ans = this.tableData[index].ans
      this.formExercise.ID = this.tableData[index].ID
      this.formExercise.index = index
      this.formExercise.userAns = this.tableData[index].userAns
    },
    handleExerciseConfirm() {
      this.dialogVisibleExercise = false
      this.tableData[this.formExercise.index].userAns = this.formExercise.userAns
    },
    handleFinishTest() {
      this.canExercise = false
      for (var i=0; i<this.tableData.length; i+=1){
        if(this.tableData[i].userAns === this.tableData[i].ans){
          this.tableData[i].result = 'accepted'
          this.correctNum += 1
        }else {
          this.tableData[i].result = 'wrong answer'
        }
      }
      this.headerText = 'Test end, congratulation :)'
      ElNotification({
        title: 'Test result',
        message: h('i', { style: 'color: teal' }, 'you got ' + this.correctNum + '/' + this.questionNum + ' in this test. hover to see detail'),
      })
    }
  },


}
</script>

<style scoped>

</style>