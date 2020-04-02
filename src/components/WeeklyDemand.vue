<template>
<b-container fluid>
  <div class="row">
    <v-btn
      :loading="button_loading_update"
      :disable="button_loading_update"
      outlined color="#757575"
      style="margin-top:10px;margin-left:10px;float:left" 
      @click="update"
      >更新
      <span class="material-icons">
        cloud_upload
      </span>
    </v-btn>
  </div>

  <el-table
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
      prop="product_name"
      label="機種"
      width="150">
      <template slot-scope="scope">
        <a-input v-if="scope.$index === index && editable" v-model="scope.row.product_name"/>
        <div v-else>{{scope.row.product_name}}</div>
      </template>
    </el-table-column>
    <el-table-column
      align="center"
      prop="PN"
      label="料號"
      width="150">
      <template slot-scope="scope">
        <a-input v-if="scope.$index === index && editable" v-model="scope.row.PN"/>
        <div v-else>{{scope.row.PN}}</div>
      </template>
    </el-table-column>
    <el-table-column
      align="center"
      prop="name"
      label="品名"
      width="120">
      <template slot-scope="scope">
        <a-input v-if="scope.$index === index && editable" v-model="scope.row.name"/>
        <div v-else>{{scope.row.name}}</div>
      </template>
    </el-table-column>
    <el-table-column
      align="center"
      prop="demand"
      label="需求總量"
      width="120">
      <template slot-scope="scope">
        <a-input v-if="scope.$index === index && editable" v-model="scope.row.demand"/>
        <div v-else>{{scope.row.demand}}</div>
      </template>
    </el-table-column>
    <el-table-column
      align="center"
      prop="destination"
      label="出貨地"
      width="120">
      <template slot-scope="scope">
        <a-input v-if="scope.$index === index && editable" v-model="scope.row.destination"/>
        <div v-else>{{scope.row.destination}}</div>
      </template>
    </el-table-column>
    <el-table-column
      align="center"
      prop="use_ratio"
      label="用量比"
      width="80">
      <template slot-scope="scope">
        <a-input v-if="scope.$index === index && editable" v-model="scope.row.use_ratio"/>
        <div v-else>{{scope.row.use_ratio}}</div>
      </template>
    </el-table-column>
    <el-table-column
      align="center"
      prop="tons"
      label="噸位"
      width="120">
      <template slot-scope="scope">
        <a-input v-if="scope.$index === index && editable" v-model="scope.row.tons"/>
        <div v-else>{{scope.row.tons}}</div>
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
      prop="priority"
      label="優先級"
      width="80">
      <template slot-scope="scope">
        <a-input v-if="scope.$index === index && editable" v-model="scope.row.priority"/>
        <div v-else>{{scope.row.priority}}</div>
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
        </div>
      </template>
    </el-table-column>
  </el-table>
  <br>
  <el-pagination
      background      
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="currentPage"
      :page-size="pagesize"
      layout="total,jumper,prev, pager, next,sizes"
      :total="totalData"
    ></el-pagination>
  <hr>
</b-container>
</template>

<script>
import api from '../api'

export default {
  data() {
    return {
      tableData : [],
      loading: true,
      index: '',
      button_loading_update:false,
      editable: false,
      currentPage:1,
      pagesize:10,
      totalData:1,
    }
  },
  mounted() {
    const res = api.get_weeklydemand(this.currentPage, this.pagesize)
    res.then((value) => {
      this.tableData = value.data.data
      this.totalData = value.data.rows
      this.loading = false
    })
  },
  methods: {
    re_render_table() {
      this.loading= true
      const res = api.get_weeklydemand(this.currentPage, this.pagesize)
    res.then((value) => {
      this.tableData = value.data.data
      this.totalData = value.data.rows
      this.loading = false
    })
    },
    indexvalue(index) {
      index = (this.currentPage-1)*this.pagesize + index
      return index
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
        await api.update_weeklydemand(this.tableData)
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
    handleEdit(index, row) {
      this.index = index
      this.editable = true
    },
    editOK() {
      this.editable = false
    },
    handleSizeChange(size){
        this.pagesize = size
        this.re_render_table()
    },
    handleCurrentChange(currentPage) {
        this.currentPage = currentPage;
        this.re_render_table();
    },
  },
}
</script>

<style>

</style>