<template>
<b-container>
  <div>
    <el-tabs type="border-card">
      <el-tab-pane label="排程中">
        <div class="row">
        <el-table
        :data="tableData"
        v-loading="loading"
        style="width: 100%"
        stripe>
          <el-table-column
            align="center"
            prop="tons"
            label="噸位"
            width="120"
            :filters="[{text: '100T', value: '100T'}, {text: '130T', value: '130T'}]"
            :filter-method="filterHandler">
          </el-table-column>
          <el-table-column
            align="center"
            prop="machine_number"
            label="機台號"
            width="120">
          </el-table-column>
          <el-table-column
            align="center"
            prop="start_time"
            label="起始時間"
            width="180">
          </el-table-column>
          <el-table-column
            align="center"
            prop="end_time"
            label="結束時間"
            width="180">
          </el-table-column>
          <el-table-column
            align="center"
            prop="PN"
            label="鴻海料號"
            width="200">
          </el-table-column>
          <el-table-column
            align="center"
            prop="name"
            label="品名"
            width="130">
          </el-table-column>
          <el-table-column
            align="center"
            prop="amount"
            label="數量"
            width="100">
          </el-table-column>
          <el-table-column
            align="center"
            prop="work_time"
            label="工時"
            width="100">
          </el-table-column>
        </el-table>
        </div>
      </el-tab-pane>
      <el-tab-pane label="未進排程">未進排程</el-tab-pane>
    </el-tabs>
  </div>
</b-container>
</template>

<script>
import api from '../api'

  export default {
    data() {
      return {
        time: '',
        tableData: [],
        loading: true
      }
    },
    mounted() {
      const res = api.get_result()
      res.then((value) => {
        this.tableData = value.data
        this.loading= false
      })
    },
    methods: {
      filterHandler(value, row, column) {
        const property = column['property'];
        return row[property] === value;
      },
    }
  }
</script>

<style>
  .el-table {
    margin-left: 10px;
  }
</style>