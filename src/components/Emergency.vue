<template>
<b-container fluid>
<div style="margin-left:70px">
  <v-btn
    @click="addRow"
    outlined color="#757575" 
    style="margin-top:10px;float:left;margin-right:10px"
    >新增
    <span class="material-icons">
      add
    </span>
  </v-btn>
  <v-btn
    :loading="button_loading_update"
    :disable="button_loading_update"
    outlined color="#757575"
    style="margin-top:10px;float:left" 
    @click="update"
    >更新
    <span class="material-icons">
      cloud_upload
    </span>
  </v-btn>
  
  <el-table-draggable>
  <el-table
    highlight-current-row
    :data="tableData"
    v-loading="loading"
    style="width: 100%"
    stripe>
    <el-table-column
      align="center"
      type="index"
      width="70"
      :index="indexvalue">
    </el-table-column>
    <el-table-column
      align="center"
      prop="PN"
      label="鴻海料號"
      width="150">
      <template slot-scope="scope">
        <a-input v-if="scope.$index === index && editable" v-model="scope.row.PN"/>
        <div v-else>{{scope.row.PN}}</div>
      </template>
    </el-table-column>
    <el-table-column
      align="center"
      prop="tons"
      label="噸位"
      width="60">
      <template slot-scope="scope">
        <a-input v-if="scope.$index === index && editable" v-model="scope.row.tons"/>
        <div v-else>{{scope.row.tons}}</div>
      </template>
    </el-table-column>
    <el-table-column
      align="center"
      prop="name"
      label="品名"
      width="140">
      <template slot-scope="scope">
        <a-input v-if="scope.$index === index && editable" v-model="scope.row.name"/>
        <div v-else>{{scope.row.name}}</div>
      </template>
    </el-table-column>
    <el-table-column
      align="center"
      prop="UPH"
      label="產能"
      width="80">
      <template slot-scope="scope">
        <a-input v-if="scope.$index === index && editable" v-model="scope.row.UPH"/>
        <div v-else>{{scope.row.UPH}}</div>
      </template>
    </el-table-column>
    <el-table-column
      align="center"
      prop="demand"
      label="需求"
      width="100">
      <template slot-scope="scope">
        <a-input v-if="scope.$index === index && editable" v-model="scope.row.demand"/>
        <div v-else>{{scope.row.demand}}</div>
      </template>
    </el-table-column>
    <el-table-column
      align="center"
      prop="work_time"
      label="工時"
      width="80">
      <template slot-scope="scope">
        <a-input v-if="scope.$index === index && editable" v-model="scope.row.work_time"/>
        <div v-else>{{scope.row.work_time}}</div>
      </template>
    </el-table-column>
    <el-table-column
      align="center"
      prop="color"
      label="顏色"
      width="80">
      <template slot-scope="scope">
        <a-input v-if="scope.$index === index && editable" v-model="scope.row.color"/>
        <div v-else>{{scope.row.color}}</div>
      </template>
    </el-table-column>
    <el-table-column
      align="center"
      prop="mold_number"
      label="模具數"
      width="80">
      <template slot-scope="scope">
        <a-input v-if="scope.$index === index && editable" v-model="scope.row.mold_number"/>
        <div v-else>{{scope.row.mold_number}}</div>
      </template>
    </el-table-column>
    <el-table-column
      align="center"
      prop="delivery"
      label="交期"
      width="80">
      <template slot-scope="scope">
        <a-input v-if="scope.$index === index && editable" v-model="scope.row.delivery"/>
        <div v-else>{{scope.row.delivery}}</div>
      </template>
    </el-table-column>
    <el-table-column
      align="center"
      prop="notes"
      label="備註"
      width="180">
      <template slot-scope="scope">
        <a-input v-if="scope.$index === index && editable" v-model="scope.row.notes"/>
        <div v-else>{{scope.row.notes}}</div>
      </template>
    </el-table-column>
    <el-table-column width="180">
      <template slot-scope="scope">
        <div v-if="scope.$index === index && editable">
          <el-button
            size="mini"
            @click="editOK">確認</el-button>
          <el-button
            size="mini"
            @click="editable=false">取消</el-button>
        </div>
        <div v-else>
          <el-button
            size="mini"
            @click="handleEdit(scope.$index, scope.row)">修改</el-button>
          <el-button
            size="mini"
            type="danger"
            @click="deleteRow(scope.$index)">刪除</el-button>
        </div>
      </template>
    </el-table-column>
  </el-table>
  </el-table-draggable>
</div>
</b-container>
</template>

<script>
import api from '../api'
import ElTableDraggable from 'element-ui-el-table-draggable'

  export default {
    components: {
      ElTableDraggable
    },
    data() {
      return {
        tableData: [],
        editable: false,
        index: '',
        loading: true,
        button_loading_update: false,
        button_loading_delete: false,
        dragging: false,
      }
    },
    mounted() {
      const res = api.get_emergency()
      res.then((value) => {
        this.tableData = value.data
        this.loading= false
      })
    },
    methods: {
      re_render_table() {
        this.loading= true
        const res = api.get_emergency()
        res.then((value) => {
          this.tableData = value.data
          this.loading= false
        })
      },
      async update() {
        this.button_loading_update = true
        if (this.check_NULL()) {
          this.button_loading_update = false
          alert('表格不可為空!')
        }
        else {
          await api.delete_all(this.tableData)
          console.log(this.tableData)
          await api.update_emergency(this.tableData)
          this.button_loading_update = false
          alert('更新成功!')
          this.re_render_table()
        }
      },
      check_NULL() {
        for (var i=0; i<this.tableData.length; i++) {
          if ( this.tableData[i].PN.length === 0 || this.tableData[i].tons.length === 0 || this.tableData[i].name.length === 0 ||
               this.tableData[i].UPH.length === 0 || this.tableData[i].demand.length === 0 || this.tableData[i].color.length === 0 || 
               this.tableData[i].mold_number.length === 0 || this.tableData[i].delivery.length === 0 ) {
            return true
          }
        }
        return false
      },
      indexvalue(index) {
        return index
      },
      handleEdit(index, row) {
        this.index = index
        this.editable = true
      },
      editOK() {
        this.editable = false
      },
      addRow() {
        this.tableData.push({
          id: 'null',
          PN: '',
          tons: '',
          name: '',
          UPH: '',
          demand: '',
          work_time: '',
          color: '',
          mold_number: '',
          delivery: '',
          notes: ''
        })
      },
      deleteRow(index) {
        this.tableData.splice(index, 1)
      },
    },
    computed: {
      calculate_worktime() {
        if (this.formData.UPH === '') {
          return ''
        }
        else {
          this.formData.work_time = this.formData.demand/this.formData.UPH
          return this.formData.work_time
        }
      },
    }
  }
</script>

<style scoped>
  span {
    font-size: 20px;
  }
  .el-input, .el-select {
    margin-bottom: 10px;
  }
</style>